from datetime import datetime

from pydantic import BaseModel


class GenerationRunOut(BaseModel):
    id: int
    chapter_id: int
    status: str
    final_output: str | None
    error_msg: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AgentMessageOut(BaseModel):
    id: int
    run_id: int
    sequence: int
    role: str
    content: str
    message_type: str
    created_at: datetime

    model_config = {"from_attributes": True}


class GenerationTriggerResponse(BaseModel):
    run_id: int
