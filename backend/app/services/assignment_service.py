from sqlalchemy.orm import Session

from app.assignments.models import TaskAssignment
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.task_rule_repository import TaskRuleRepository
from app.services.rule_engine_service import RuleEngineService
from app.tasks.models import Task
from app.users.models import User


class AssignmentService:
    """Orchestrates eligibility computation and assignment persistence."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._rule_engine_service = RuleEngineService(db)
        self._assignment_repository = AssignmentRepository(db)

    def compute_eligibility(self, task_id: int) -> list[User]:
        eligible_users = self._rule_engine_service.get_eligible_users(task_id)

        self._assignment_repository.delete_task_assignments(task_id)

        for user in eligible_users:
            assignment = TaskAssignment(
                task_id=task_id,
                user_id=user.id,
                is_eligible=True,
            )
            self._assignment_repository.create_assignment(assignment)

        self._db.commit()
        return eligible_users

    def get_eligible_users(self, task_id: int) -> list[User]:
        return self._assignment_repository.get_eligible_users(task_id)

    def get_eligible_tasks(self, user_id: int) -> list[Task]:
        return self._assignment_repository.get_eligible_tasks(user_id)

    def recompute_all_assignments(self) -> None:
        task_rule_repository = TaskRuleRepository(self._db)

        skip = 0
        limit = 100

        while True:
            rules = task_rule_repository.list_rules(
                skip=skip,
                limit=limit,
            )

            if not rules:
                break

            for rule in rules:
                self.compute_eligibility(rule.task_id)

            if len(rules) < limit:
                break

            skip += limit
