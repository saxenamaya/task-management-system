from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.tasks.models import TaskPriority, TaskStatus
from app.users.models import UserRole


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


class TaskSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: date | None
    created_by: int
    created_at: datetime
    updated_at: datetime


class EligibleUsersResponse(BaseModel):
    task_id: int
    count: int
    eligible_users: list[UserResponse]


class EligibleTasksResponse(BaseModel):
    user_id: int
    count: int
    eligible_tasks: list[TaskSummaryResponse]
