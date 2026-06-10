from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskRuleCreate(BaseModel):
    task_id: int = Field(..., gt=0)
    department: str | None = Field(None, max_length=100)
    min_experience: int | None = Field(None, ge=0)
    max_active_tasks: int | None = Field(None, ge=0)
    location: str | None = Field(None, max_length=255)


class TaskRuleUpdate(BaseModel):
    department: str | None = None
    min_experience: int | None = None
    max_active_tasks: int | None = None
    location: str | None = None


class TaskRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    department: str | None
    min_experience: int | None
    max_active_tasks: int | None
    location: str | None
    created_at: datetime
    updated_at: datetime
