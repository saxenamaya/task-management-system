from sqlalchemy.orm import Session

from app.core.exceptions import TaskRuleNotFoundError
from app.repositories.task_rule_repository import TaskRuleRepository
from app.repositories.user_repository import UserRepository
from app.rule_engine.models import TaskRule
from app.users.models import User


class RuleEngineService:
    """Evaluates user eligibility against task assignment rules."""

    def __init__(self, db: Session) -> None:
        self._user_repository = UserRepository(db)
        self._task_rule_repository = TaskRuleRepository(db)

    def is_user_eligible(self, user: User, rule: TaskRule) -> bool:
        if rule.department is not None and user.department != rule.department:
            return False

        if rule.min_experience is not None and user.experience_years < rule.min_experience:
            return False

        if (
            rule.max_active_tasks is not None
            and user.active_task_count >= rule.max_active_tasks
        ):
            return False

        if rule.location is not None and user.location != rule.location:
            return False

        return True

    def get_eligible_users(self, task_id: int) -> list[User]:
        rule = self._task_rule_repository.get_rule_by_task_id(task_id)
        if rule is None:
            raise TaskRuleNotFoundError(
                f"No eligibility rule found for task id {task_id}"
            )

        return [
            user
            for user in self._list_all_users()
            if self.is_user_eligible(user, rule)
        ]

    def _list_all_users(self) -> list[User]:
        users: list[User] = []
        skip = 0
        limit = 100

        while True:
            batch = self._user_repository.list_users(skip=skip, limit=limit)
            if not batch:
                break

            users.extend(batch)

            if len(batch) < limit:
                break

            skip += limit

        return users
