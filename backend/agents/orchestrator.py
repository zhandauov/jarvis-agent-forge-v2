import asyncio
import json
from datetime import datetime, timezone

import anthropic

from agents.message_bus import MessageBus

_cancel_flags: set[int] = set()


def cancel_run(run_id: int) -> None:
    _cancel_flags.add(run_id)


def _check_cancelled(run_id: int) -> None:
    if run_id in _cancel_flags:
        _cancel_flags.discard(run_id)
        raise asyncio.CancelledError(f"Run {run_id} cancelled by user")
    
from agents.models import WorkerResult
from agents.prompts import SUPERVISOR_SYSTEM_DEFAULT, WORKER_SYSTEM_DEFAULT
from agents.supervisor import SupervisorAgent
from agents.worker import WorkerAgent
from core.config import settings
from knowledge_base.store import KBStore


async def run_generation(run_id: int) -> None:
    from core.database import AsyncSessionLocal
    from models.chapter import Chapter
    from models.agent_config import AgentTeamConfig
    from models.generation_run import AgentMessage, GenerationRun

    bus = MessageBus.instance()

    async with AsyncSessionLocal() as db:
        run = await db.get(GenerationRun, run_id)
        if not run:
            return

        chapter = await db.get(Chapter, run.chapter_id)
        if not chapter:
            return

        from sqlalchemy import select
        result = await db.execute(select(AgentTeamConfig).where(AgentTeamConfig.chapter_id == chapter.id))
        config = result.scalar_one_or_none()

        if not config:
            run.status = "error"
            run.error_msg = "No agent team config found for this chapter"
            await db.commit()
            await bus.publish(run_id, {"type": "error", "data": {"message": run.error_msg}})
            return

        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        await db.commit()

        await bus.publish(run_id, {"type": "status_update", "data": {"status": "running"}})

        try:
            worker_roles: list[str] = json.loads(config.worker_roles)
            kb_chunks = KBStore.instance().search(chapter.report_id, f"{chapter.title} {chapter.description or ''}", top_k=10)

            client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            supervisor_prompt = config.supervisor_prompt or SUPERVISOR_SYSTEM_DEFAULT
            worker_base_prompt = config.worker_prompt or WORKER_SYSTEM_DEFAULT

            agent_model = config.model or "claude-opus-4-7"
            internet_access = bool(config.internet_access)
            supervisor = SupervisorAgent(supervisor_prompt, client, run_id, bus, model=agent_model)
            workers = {
                role: WorkerAgent(role, worker_base_prompt, client, model=agent_model, internet_access=internet_access)
                for role in worker_roles
            }

            sequence = 0

            # Step 1: Supervisor creates plan
            await bus.publish(run_id, {"type": "agent_message", "data": {"role": "supervisor", "content": "Creating research plan...", "message_type": "system", "sequence": sequence}})
            plan = await supervisor.create_plan(chapter.title, chapter.description or "", worker_roles, kb_chunks)
            sequence += 1

            plan_content = f"**Research Plan**\n\n{plan.plan_summary}\n\n" + "\n".join(f"- **{t.worker_role}**: {t.task}" for t in plan.tasks)
            msg = AgentMessage(run_id=run_id, sequence=sequence, role="supervisor", content=plan_content, message_type="plan")
            db.add(msg)
            await db.commit()
            await bus.publish(run_id, {"type": "agent_message", "data": {"role": "supervisor", "content": plan_content, "message_type": "plan", "sequence": sequence}})

            # Step 2: Workers execute initial tasks
            task_map = {t.worker_role: t.task for t in plan.tasks}
            all_results: list[WorkerResult] = []

            async def run_worker(role: str, task: str) -> WorkerResult:
                nonlocal sequence
                worker = workers.get(role) or WorkerAgent(role, worker_base_prompt, client, model=agent_model, internet_access=internet_access)
                sequence += 1
                await bus.publish(run_id, {"type": "agent_message", "data": {"role": role, "content": f"Working on: {task}", "message_type": "task", "sequence": sequence}})
                result = await worker.execute_task(task, kb_chunks)
                sequence += 1
                result_content = f"**{role} Report**\n\n{result.findings}" + (("\n\n**Key data points:**\n" + "\n".join(f"- {p}" for p in result.data_points)) if result.data_points else "")
                msg = AgentMessage(run_id=run_id, sequence=sequence, role=role, content=result_content, message_type="result")
                db.add(msg)
                await db.commit()
                await bus.publish(run_id, {"type": "agent_message", "data": {"role": role, "content": result_content, "message_type": "result", "sequence": sequence}})
                return result

            results = await asyncio.gather(*[run_worker(role, task_map.get(role, f"Research {chapter.title}")) for role in worker_roles])
            all_results.extend(results)

            _check_cancelled(run_id)

            # Step 3: Discussion rounds
            for round_num in range(config.max_rounds):
                decision = await supervisor.review_and_decide(chapter.title, all_results)
                if decision.ready_to_aggregate or not decision.follow_up_tasks:
                    break

                follow_up_content = "**Follow-up requests:**\n" + "\n".join(f"- **{t.worker_role}**: {t.task}" for t in decision.follow_up_tasks)
                sequence += 1
                msg = AgentMessage(run_id=run_id, sequence=sequence, role="supervisor", content=follow_up_content, message_type="discussion")
                db.add(msg)
                await db.commit()
                await bus.publish(run_id, {"type": "agent_message", "data": {"role": "supervisor", "content": follow_up_content, "message_type": "discussion", "sequence": sequence}})

                follow_up_results = await asyncio.gather(*[run_worker(t.worker_role, t.task) for t in decision.follow_up_tasks])
                all_results.extend(follow_up_results)
                _check_cancelled(run_id)

            # Step 4: Aggregate final output
            sequence += 1
            await bus.publish(run_id, {"type": "agent_message", "data": {"role": "supervisor", "content": "Writing final report section...", "message_type": "system", "sequence": sequence}})
            final_markdown = await supervisor.aggregate(chapter.title, chapter.description or "", all_results, kb_chunks)

            sequence += 1
            msg = AgentMessage(run_id=run_id, sequence=sequence, role="supervisor", content=final_markdown, message_type="final")
            db.add(msg)

            run.status = "complete"
            run.final_output = final_markdown
            run.completed_at = datetime.now(timezone.utc)
            chapter.status = "complete"
            chapter.final_output = final_markdown
            await db.commit()

            await bus.publish(run_id, {"type": "final_output", "data": {"markdown": final_markdown}})

        except asyncio.CancelledError:
            run.status = "cancelled"
            run.error_msg = "Stopped by user"
            run.completed_at = datetime.now(timezone.utc)
            chapter.status = "pending"
            await db.commit()
            await bus.publish(run_id, {"type": "error", "data": {"message": "Stopped by user"}})
        except Exception as exc:
            run.status = "error"
            run.error_msg = str(exc)
            run.completed_at = datetime.now(timezone.utc)
            chapter.status = "error"
            await db.commit()
            await bus.publish(run_id, {"type": "error", "data": {"message": str(exc)}})
