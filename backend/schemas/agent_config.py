from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator
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
    mode: str = "team"
    single_agent_instructions: str | None = None

    @model_validator(mode="after")
    def validate_for_mode(self) -> "AgentConfigUpsert":
        if self.mode == "single":
            if not (self.single_agent_instructions and self.single_agent_instructions.strip()):
                raise ValueError("Instructions are required in single-agent mode")
        else:
            if not self.worker_roles:
                raise ValueError("At least one worker role is required")
        return self


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
    mode: str
    single_agent_instructions: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("worker_roles", mode="before")
    @classmethod
    def parse_roles(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
