from datetime import datetime

from pydantic import BaseModel


class ReportCreate(BaseModel):
    title: str
    description: str | None = None


class ReportUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class ReportOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
