from sqlalchemy import select
from sqlalchemy.orm import Session

from app.tasks.models import Task


class TaskRepository:
    """Data access layer for Task entities."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create_task(self, task: Task) -> Task:
        self._db.add(task)
        self._db.flush()
        self._db.refresh(task)
        return task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self._db.get(Task, task_id)

    def list_tasks(self, *, skip: int = 0, limit: int = 100) -> list[Task]:
        stmt = select(Task).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())

    def update_task(self, task: Task) -> Task:
        self._db.flush()
        self._db.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self._db.delete(task)
        self._db.flush()
