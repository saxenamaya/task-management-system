from sqlalchemy import select
from sqlalchemy.orm import Session

from app.rule_engine.models import TaskRule


class TaskRuleRepository:
    """Data access layer for TaskRule entities."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create_rule(self, rule: TaskRule) -> TaskRule:
        self._db.add(rule)
        self._db.flush()
        self._db.refresh(rule)
        return rule

    def get_rule_by_id(self, rule_id: int) -> TaskRule | None:
        return self._db.get(TaskRule, rule_id)

    def get_rule_by_task_id(self, task_id: int) -> TaskRule | None:
        """Return the single eligibility rule for a task, if one exists."""
        return self._db.scalars(
            select(TaskRule).where(TaskRule.task_id == task_id)
        ).first()

    def list_rules(self, *, skip: int = 0, limit: int = 100) -> list[TaskRule]:
        stmt = select(TaskRule).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())

    def update_rule(self, rule: TaskRule) -> TaskRule:
        self._db.flush()
        self._db.refresh(rule)
        return rule

    def delete_rule(self, rule: TaskRule) -> None:
        self._db.delete(rule)
        self._db.flush()
