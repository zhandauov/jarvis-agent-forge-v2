import asyncio
import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.dependencies import get_db
from knowledge_base.extractor import extract_and_chunk
from knowledge_base.store import KBStore
from models.knowledge_base import KBDocument
from models.report import Report
from schemas.knowledge_base import KBDocumentOut

router = APIRouter(prefix="/api/reports/{report_id}/kb", tags=["knowledge-base"])

ALLOWED_TYPES = {"pdf": "pdf", "docx": "docx", "doc": "docx"}


async def _get_report_or_404(report_id: int, db: AsyncSession) -> Report:
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    return report


@router.get("", response_model=list[KBDocumentOut])
async def list_kb_documents(report_id: int, db: AsyncSession = Depends(get_db)):
    await _get_report_or_404(report_id, db)
    result = await db.execute(select(KBDocument).where(KBDocument.report_id == report_id))
    return result.scalars().all()


@router.post("/upload", response_model=KBDocumentOut, status_code=201)
async def upload_kb_document(report_id: int, file: UploadFile, db: AsyncSession = Depends(get_db)):
    await _get_report_or_404(report_id, db)

    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: .{ext}. Allowed: pdf, docx")

    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(413, f"File too large (max {settings.MAX_UPLOAD_MB} MB)")

    upload_dir = Path(settings.UPLOAD_DIR) / str(report_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = str(upload_dir / unique_name)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    doc = KBDocument(
        report_id=report_id,
        filename=file.filename,
        file_path=file_path,
        file_type=ALLOWED_TYPES[ext],
        status="processing",
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    asyncio.create_task(_index_document(doc.id, file_path, ALLOWED_TYPES[ext], report_id, doc.filename))
    return doc


async def _index_document(doc_id: int, file_path: str, file_type: str, report_id: int, filename: str) -> None:
    from core.database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        doc = await session.get(KBDocument, doc_id)
        if not doc:
            return
        try:
            chunks = await extract_and_chunk(file_path, file_type)
            KBStore.instance().add_document(report_id, doc_id, filename, chunks)
            doc.status = "ready"
            doc.chunk_count = len(chunks)
        except Exception as exc:
            doc.status = "error"
            doc.error_msg = str(exc)
        await session.commit()


@router.delete("/{doc_id}", status_code=204)
async def delete_kb_document(report_id: int, doc_id: int, db: AsyncSession = Depends(get_db)):
    doc = await db.get(KBDocument, doc_id)
    if not doc or doc.report_id != report_id:
        raise HTTPException(404, "Document not found")
    KBStore.instance().remove_document(report_id, doc_id)
    try:
        os.remove(doc.file_path)
        sidecar = doc.file_path + ".chunks.json"
        if os.path.exists(sidecar):
            os.remove(sidecar)
    except OSError:
        pass
    await db.delete(doc)
    await db.commit()
