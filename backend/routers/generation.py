from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user, get_db
from models.chapter import Chapter
from models.generation_run import AgentMessage, GenerationRun
from schemas.generation import AgentMessageOut, GenerationRunOut, GenerationTriggerResponse

router = APIRouter(tags=["generation"], dependencies=[Depends(get_current_user)])


@router.post("/api/chapters/{chapter_id}/generate", response_model=GenerationTriggerResponse, status_code=201)
async def trigger_generation(chapter_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapter not found")

    existing = await db.execute(
        select(GenerationRun).where(GenerationRun.chapter_id == chapter_id, GenerationRun.status == "running")
    )
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Generation already running for this chapter")

    run = GenerationRun(chapter_id=chapter_id, status="pending")
    db.add(run)
    await db.commit()
    await db.refresh(run)

    from agents.orchestrator import run_generation
    background_tasks.add_task(run_generation, run.id)

    return GenerationTriggerResponse(run_id=run.id)


@router.get("/api/chapters/{chapter_id}/runs", response_model=list[GenerationRunOut])
async def list_runs(chapter_id: int, db: AsyncSession = Depends(get_db)):
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapter not found")
    result = await db.execute(
        select(GenerationRun).where(GenerationRun.chapter_id == chapter_id).order_by(GenerationRun.created_at.desc())
    )
    return result.scalars().all()


@router.get("/api/runs/{run_id}", response_model=GenerationRunOut)
async def get_run(run_id: int, db: AsyncSession = Depends(get_db)):
    run = await db.get(GenerationRun, run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    return run


@router.post("/api/runs/{run_id}/stop", status_code=200)
async def stop_run(run_id: int, db: AsyncSession = Depends(get_db)):
    run = await db.get(GenerationRun, run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    if run.status not in ("running", "pending"):
        raise HTTPException(409, "Run is not active")

    from agents.orchestrator import cancel_run
    cancel_run(run_id)

    return {"ok": True}


@router.get("/api/runs/{run_id}/messages", response_model=list[AgentMessageOut])
async def get_run_messages(run_id: int, db: AsyncSession = Depends(get_db)):
    run = await db.get(GenerationRun, run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    result = await db.execute(
        select(AgentMessage).where(AgentMessage.run_id == run_id).order_by(AgentMessage.sequence)
    )
    return result.scalars().all()
