from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db
from models.chapter import Chapter
from models.report import Report
from schemas.chapter import ChapterCreate, ChapterOut, ChapterReorder, ChapterUpdate

router = APIRouter(prefix="/api/reports/{report_id}/chapters", tags=["chapters"])


async def _get_report_or_404(report_id: int, db: AsyncSession) -> Report:
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    return report


@router.get("", response_model=list[ChapterOut])
async def list_chapters(report_id: int, db: AsyncSession = Depends(get_db)):
    await _get_report_or_404(report_id, db)
    result = await db.execute(
        select(Chapter).where(Chapter.report_id == report_id).order_by(Chapter.order_index)
    )
    return result.scalars().all()


@router.post("", response_model=ChapterOut, status_code=201)
async def create_chapter(report_id: int, body: ChapterCreate, db: AsyncSession = Depends(get_db)):
    await _get_report_or_404(report_id, db)
    chapter = Chapter(report_id=report_id, **body.model_dump())
    db.add(chapter)
    await db.commit()
    await db.refresh(chapter)
    return chapter


@router.get("/{chapter_id}", response_model=ChapterOut)
async def get_chapter(report_id: int, chapter_id: int, db: AsyncSession = Depends(get_db)):
    chapter = await db.get(Chapter, chapter_id)
    if not chapter or chapter.report_id != report_id:
        raise HTTPException(404, "Chapter not found")
    return chapter


@router.put("/{chapter_id}", response_model=ChapterOut)
async def update_chapter(report_id: int, chapter_id: int, body: ChapterUpdate, db: AsyncSession = Depends(get_db)):
    chapter = await db.get(Chapter, chapter_id)
    if not chapter or chapter.report_id != report_id:
        raise HTTPException(404, "Chapter not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(chapter, field, value)
    await db.commit()
    await db.refresh(chapter)
    return chapter


@router.delete("/{chapter_id}", status_code=204)
async def delete_chapter(report_id: int, chapter_id: int, db: AsyncSession = Depends(get_db)):
    chapter = await db.get(Chapter, chapter_id)
    if not chapter or chapter.report_id != report_id:
        raise HTTPException(404, "Chapter not found")
    await db.delete(chapter)
    await db.commit()


@router.patch("/reorder", response_model=list[ChapterOut])
async def reorder_chapters(report_id: int, body: ChapterReorder, db: AsyncSession = Depends(get_db)):
    await _get_report_or_404(report_id, db)
    result = await db.execute(select(Chapter).where(Chapter.report_id == report_id))
    chapters = {c.id: c for c in result.scalars().all()}
    for idx, chapter_id in enumerate(body.ordered_ids):
        if chapter_id in chapters:
            chapters[chapter_id].order_index = idx
    await db.commit()
    result = await db.execute(
        select(Chapter).where(Chapter.report_id == report_id).order_by(Chapter.order_index)
    )
    return result.scalars().all()
