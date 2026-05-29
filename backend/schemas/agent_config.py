from datetime import datetime

from pydantic import BaseModel, field_validator
import json


class AgentConfigUpsert(BaseModel):
    supervisor_prompt: str
    worker_prompt: str
    worker_roles: list[str]
    worker_count: int = 3
    max_rounds: int = 4
    model: str = "claude-sonnet-4-6"
    internet_access: bool = False
    aggregate_prompt: str | None = None
    pptx_aggregate_prompt: str | None = None

    @field_validator("worker_roles")
    @classmethod
    def validate_roles(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("At least one worker role is required")
        return v


class AgentConfigOut(BaseModel):
    id: int
    chapter_id: int
    supervisor_prompt: str
    worker_prompt: str
    worker_roles: list[str]
    worker_count: int
    max_rounds: int
    model: str
    internet_access: bool
    aggregate_prompt: str | None
    pptx_aggregate_prompt: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("worker_roles", mode="before")
    @classmethod
    def parse_roles(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
