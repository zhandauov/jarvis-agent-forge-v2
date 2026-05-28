from datetime import datetime

from pydantic import BaseModel


class PromptTemplateOut(BaseModel):
    id: int
    key: str
    name: str
    description: str
    body: str
    updated_at: datetime

    model_config = {"from_attributes": True}


class PromptTemplateUpdate(BaseModel):
    body: str
