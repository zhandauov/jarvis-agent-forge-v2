from datetime import datetime

from pydantic import BaseModel


class KBDocumentOut(BaseModel):
    id: int
    report_id: int
    filename: str
    file_type: str
    status: str
    chunk_count: int
    error_msg: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
