from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.users.models import UserRole


class UserUpdate(BaseModel):
    department: str
    experience_years: int
    location: str
    active_task_count: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: UserRole
    department: str
    experience_years: int
    location: str
    active_task_count: int
    created_at: datetime
    updated_at: datetime
