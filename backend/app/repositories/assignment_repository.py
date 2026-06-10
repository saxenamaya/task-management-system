from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.assignments.models import TaskAssignment
from app.tasks.models import Task
from app.users.models import User


class AssignmentRepository:
    """Data access layer for TaskAssignment entities."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create_assignment(self, assignment: TaskAssignment) -> TaskAssignment:
        self._db.add(assignment)
        self._db.flush()
        self._db.refresh(assignment)
        return assignment

    def upsert_assignment(self, assignment: TaskAssignment) -> TaskAssignment:
        existing = self.get_by_task_and_user(assignment.task_id, assignment.user_id)
        if existing is None:
            return self.create_assignment(assignment)

        existing.is_eligible = assignment.is_eligible
        self._db.flush()
        self._db.refresh(existing)
        return existing

    def get_by_task_and_user(
        self,
        task_id: int,
        user_id: int,
    ) -> TaskAssignment | None:
        stmt = select(TaskAssignment).where(
            TaskAssignment.task_id == task_id,
            TaskAssignment.user_id == user_id,
        )
        return self._db.scalars(stmt).first()

    def get_eligible_users(self, task_id: int) -> list[User]:
        stmt = (
            select(User)
            .join(TaskAssignment, TaskAssignment.user_id == User.id)
            .where(
                TaskAssignment.task_id == task_id,
                TaskAssignment.is_eligible.is_(True),
            )
        )
        return list(self._db.scalars(stmt).all())

    def get_eligible_tasks(self, user_id: int) -> list[Task]:
        stmt = (
            select(Task)
            .join(TaskAssignment, TaskAssignment.task_id == Task.id)
            .where(
                TaskAssignment.user_id == user_id,
                TaskAssignment.is_eligible.is_(True),
            )
        )
        return list(self._db.scalars(stmt).all())

    def delete_task_assignments(self, task_id: int) -> int:
        stmt = delete(TaskAssignment).where(TaskAssignment.task_id == task_id)
        result = self._db.execute(stmt)
        self._db.flush()
        return result.rowcount

    def list_assignments(self, task_id: int) -> list[TaskAssignment]:
        stmt = select(TaskAssignment).where(TaskAssignment.task_id == task_id)
        return list(self._db.scalars(stmt).all())
