from datetime import datetime, timezone
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user, get_db
from models.chapter import Chapter
from models.slide_config import SlideConfig
from pptx_builder import build_slide
from schemas.slide_config import SlideConfigOut, SlideConfigUpsert

router = APIRouter(prefix="/api/chapters/{chapter_id}", tags=["slides"], dependencies=[Depends(get_current_user)])


async def _get_chapter_or_404(chapter_id: int, db: AsyncSession) -> Chapter:
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(404, "Chapter not found")
    return chapter


async def _get_or_default(chapter_id: int, db: AsyncSession) -> SlideConfig:
    result = await db.execute(select(SlideConfig).where(SlideConfig.chapter_id == chapter_id))
    config = result.scalar_one_or_none()
    if config:
        return config
    # Return an unsaved default object (not persisted) so GET always succeeds
    return SlideConfig(chapter_id=chapter_id)


@router.get("/slide-config", response_model=SlideConfigOut)
async def get_slide_config(chapter_id: int, db: AsyncSession = Depends(get_db)):
    await _get_chapter_or_404(chapter_id, db)
    config = await _get_or_default(chapter_id, db)
    # If not yet persisted, fill in defaults manually for the response
    if not config.id:
        return SlideConfigOut(
            id=0,
            chapter_id=chapter_id,
            output_mode=config.output_mode,
            slide_ratio=config.slide_ratio,
            title_font=config.title_font,
            title_font_size=config.title_font_size,
            title_bold=config.title_bold,
            title_color=config.title_color,
            body_font=config.body_font,
            body_font_size=config.body_font_size,
            body_bold=config.body_bold,
            body_color=config.body_color,
            bg_color=config.bg_color,
            margin_top=config.margin_top,
            margin_left=config.margin_left,
            margin_right=config.margin_right,
            margin_bottom=config.margin_bottom,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    return config


@router.put("/slide-config", response_model=SlideConfigOut)
async def upsert_slide_config(chapter_id: int, body: SlideConfigUpsert, db: AsyncSession = Depends(get_db)):
    await _get_chapter_or_404(chapter_id, db)
    result = await db.execute(select(SlideConfig).where(SlideConfig.chapter_id == chapter_id))
    config = result.scalar_one_or_none()

    data = body.model_dump()
    if config:
        for field, value in data.items():
            setattr(config, field, value)
    else:
        config = SlideConfig(chapter_id=chapter_id, **data)
        db.add(config)

    await db.commit()
    await db.refresh(config)
    return config


@router.get("/export/pptx")
async def export_pptx(chapter_id: int, db: AsyncSession = Depends(get_db)):
    chapter = await _get_chapter_or_404(chapter_id, db)
    if not chapter.final_output:
        raise HTTPException(400, "No generated content available for this chapter")

    config = await _get_or_default(chapter_id, db)
    if config.output_mode != "pptx":
        raise HTTPException(400, "Chapter is not in PPTX output mode")

    pptx_bytes = build_slide(chapter.final_output, config, chapter.title)
    filename = chapter.title.replace(" ", "_") + ".pptx"
    encoded = quote(filename, safe="")
    disposition = f"attachment; filename=\"slide.pptx\"; filename*=UTF-8''{encoded}"
    return Response(
        content=pptx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": disposition},
    )
