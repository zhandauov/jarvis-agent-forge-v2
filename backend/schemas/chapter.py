from datetime import datetime

from pydantic import BaseModel


class ChapterCreate(BaseModel):
    title: str
    description: str | None = None
    order_index: int = 0


class ChapterUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    order_index: int | None = None
    status: str | None = None


class ChapterReorder(BaseModel):
    ordered_ids: list[int]


class ChapterOut(BaseModel):
    id: int
    report_id: int
    title: str
    description: str | None
    order_index: int
    status: str
    final_output: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
