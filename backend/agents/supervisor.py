import json
import re

import anthropic

from agents.message_bus import MessageBus
from agents.models import PlanResult, SupervisorDecision, WorkerResult, WorkerTask


class SupervisorAgent:
    def __init__(
        self,
        supervisor_prompt: str,
        client: anthropic.AsyncAnthropic,
        run_id: int,
        bus: MessageBus,
        model: str = "claude-sonnet-4-6",
        plan_template: str = "",
        review_template: str = "",
        aggregate_template: str = "",
        kb_section_template: str = "",
    ) -> None:
        self.system_prompt = supervisor_prompt
        self.client = client
        self.run_id = run_id
        self.bus = bus
        self.model = model
        self.plan_template = plan_template
        self.review_template = review_template
        self.aggregate_template = aggregate_template
        self.kb_section_template = kb_section_template

    async def create_plan(
        self,
        chapter_title: str,
        chapter_description: str,
        worker_roles: list[str],
        kb_chunks: list[dict],
    ) -> PlanResult:
        kb_section = _format_kb(kb_chunks, self.kb_section_template)
        roles_list = "\n".join(f"- {r}" for r in worker_roles)

        user_msg = self.plan_template.format(
            chapter_title=chapter_title,
            chapter_description=chapter_description or "",
            kb_section=kb_section,
            worker_roles_list=roles_list,
        )

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_msg}],
        )

        content = message.content[0].text
        try:
            data = json.loads(_extract_json(content))
            tasks = [WorkerTask(worker_role=t["worker_role"], task=t["task"]) for t in data.get("tasks", [])]
            return PlanResult(plan_summary=data.get("plan_summary", ""), tasks=tasks)
        except (json.JSONDecodeError, KeyError):
            tasks = [WorkerTask(worker_role=r, task=f"Research {chapter_title}") for r in worker_roles]
            return PlanResult(plan_summary=content, tasks=tasks)

    async def review_and_decide(
        self,
        chapter_title: str,
        worker_results: list[WorkerResult],
    ) -> SupervisorDecision:
        outputs = _format_worker_results(worker_results)
        user_msg = self.review_template.format(
            chapter_title=chapter_title,
            worker_outputs=outputs,
        )

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_msg}],
        )

        content = message.content[0].text
        try:
            data = json.loads(_extract_json(content))
            follow_ups = [
                WorkerTask(worker_role=t["worker_role"], task=t["task"])
                for t in data.get("follow_up_tasks", [])
            ]
            return SupervisorDecision(
                ready_to_aggregate=data.get("ready_to_aggregate", True),
                follow_up_tasks=follow_ups,
            )
        except (json.JSONDecodeError, KeyError):
            return SupervisorDecision(ready_to_aggregate=True)

    async def aggregate(
        self,
        chapter_title: str,
        chapter_description: str,
        all_results: list[WorkerResult],
        kb_chunks: list[dict],
    ) -> str:
        kb_section = _format_kb(kb_chunks, self.kb_section_template)
        findings = _format_worker_results(all_results)

        user_msg = self.aggregate_template.format(
            chapter_title=chapter_title,
            chapter_description=chapter_description or "",
            all_findings=findings,
            kb_section=kb_section,
        )

        full_text = ""
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_msg}],
        ) as stream:
            async for delta in stream.text_stream:
                full_text += delta
                await self.bus.publish(self.run_id, {"type": "streaming_chunk", "data": {"delta": delta}})

        return _extract_markdown_from_aggregate(full_text)


def _format_kb(chunks: list[dict], kb_section_template: str) -> str:
    if not chunks:
        return ""
    formatted = "\n\n---\n\n".join(f"[{c['filename']}]\n{c['text']}" for c in chunks)
    return kb_section_template.format(chunks=formatted)


def _format_worker_results(results: list[WorkerResult]) -> str:
    parts = []
    for r in results:
        points = "\n".join(f"  - {p}" for p in r.data_points)
        parts.append(f"**{r.role}**:\n{r.findings}" + (f"\n\nKey data points:\n{points}" if points else ""))
    return "\n\n---\n\n".join(parts)


def _extract_markdown_from_aggregate(text: str) -> str:
    """If Claude still returns JSON for the aggregate step, pull the markdown out of it."""
    stripped = text.strip()
    if not stripped.startswith('{'):
        return text
    try:
        data = json.loads(stripped)
        for key in ('report_section', 'markdown', 'content', 'chapter_content', 'output', 'report'):
            if key in data and isinstance(data[key], str):
                return data[key]
    except json.JSONDecodeError:
        pass
    return text


def _extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text
