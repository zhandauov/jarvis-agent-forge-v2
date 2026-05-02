from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db
from models.report import Report
from schemas.report import ReportCreate, ReportOut, ReportUpdate

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("", response_model=list[ReportOut])
async def list_reports(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).order_by(Report.created_at.desc()))
    return result.scalars().all()


@router.post("", response_model=ReportOut, status_code=201)
async def create_report(body: ReportCreate, db: AsyncSession = Depends(get_db)):
    report = Report(**body.model_dump())
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/{report_id}", response_model=ReportOut)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db)):
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    return report


@router.put("/{report_id}", response_model=ReportOut)
async def update_report(report_id: int, body: ReportUpdate, db: AsyncSession = Depends(get_db)):
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(report, field, value)
    await db.commit()
    await db.refresh(report)
    return report


@router.delete("/{report_id}", status_code=204)
async def delete_report(report_id: int, db: AsyncSession = Depends(get_db)):
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    await db.delete(report)
    await db.commit()
