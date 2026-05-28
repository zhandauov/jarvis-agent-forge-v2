from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agents.prompt_seeder import PROMPT_DEFAULTS
from core.dependencies import get_current_user, get_db
from models.prompt_template import PromptTemplate
from schemas.prompt_template import PromptTemplateOut, PromptTemplateUpdate

router = APIRouter(prefix="/api/prompts", tags=["prompts"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[PromptTemplateOut])
async def list_prompts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PromptTemplate).order_by(PromptTemplate.id))
    return result.scalars().all()


@router.get("/{key}", response_model=PromptTemplateOut)
async def get_prompt(key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PromptTemplate).where(PromptTemplate.key == key))
    pt = result.scalar_one_or_none()
    if not pt:
        raise HTTPException(404, "Prompt template not found")
    return pt


@router.put("/{key}", response_model=PromptTemplateOut)
async def update_prompt(key: str, body: PromptTemplateUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PromptTemplate).where(PromptTemplate.key == key))
    pt = result.scalar_one_or_none()
    if not pt:
        raise HTTPException(404, "Prompt template not found")
    pt.body = body.body
    await db.commit()
    await db.refresh(pt)
    return pt


@router.post("/{key}/reset", response_model=PromptTemplateOut)
async def reset_prompt(key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PromptTemplate).where(PromptTemplate.key == key))
    pt = result.scalar_one_or_none()
    if not pt:
        raise HTTPException(404, "Prompt template not found")

    default = next((d for d in PROMPT_DEFAULTS if d["key"] == key), None)
    if not default:
        raise HTTPException(500, "No default found for this key")

    pt.body = default["body"]
    await db.commit()
    await db.refresh(pt)
    return pt
