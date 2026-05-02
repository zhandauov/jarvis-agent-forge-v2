import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db
from models.agent_config import AgentTeamConfig
from models.chapter import Chapter
from schemas.agent_config import AgentConfigOut, AgentConfigUpsert

router = APIRouter(prefix="/api/chapters/{chapter_id}/agent-config", tags=["agent-config"])


async def _get_chapter_or_404(chapter_id: int, db: AsyncSession) -> Chapter:
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapter not found")
    return chapter


@router.get("", response_model=AgentConfigOut)
async def get_agent_config(chapter_id: int, db: AsyncSession = Depends(get_db)):
    await _get_chapter_or_404(chapter_id, db)
    result = await db.execute(select(AgentTeamConfig).where(AgentTeamConfig.chapter_id == chapter_id))
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(404, "Agent config not found")
    return config


@router.put("", response_model=AgentConfigOut)
async def upsert_agent_config(chapter_id: int, body: AgentConfigUpsert, db: AsyncSession = Depends(get_db)):
    await _get_chapter_or_404(chapter_id, db)
    result = await db.execute(select(AgentTeamConfig).where(AgentTeamConfig.chapter_id == chapter_id))
    config = result.scalar_one_or_none()

    data = body.model_dump()
    data["worker_roles"] = json.dumps(data["worker_roles"])

    if config:
        for field, value in data.items():
            setattr(config, field, value)
    else:
        config = AgentTeamConfig(chapter_id=chapter_id, **data)
        db.add(config)

    await db.commit()
    await db.refresh(config)
    return config
