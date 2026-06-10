"""Integration test for AssignmentService using existing task and rule.

Run from backend/:
    python test_assignment_integration.py

Prerequisites:
    - At least one task with a task rule in the database
    - Run test_rule_engine.py or test_assignment_service.py first if needed
"""

import sys

from app.assignments.models import TaskAssignment  # noqa: F401 — register ORM
from app.db.database import SessionLocal
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.task_rule_repository import TaskRuleRepository
from app.rule_engine.models import TaskRule
from app.services.assignment_service import AssignmentService
from app.tasks.models import Task
from app.users.models import User  # noqa: F401 — register ORM


def format_user(user: User) -> str:
    return (
        f"User(id={user.id}, name={user.name!r}, department={user.department!r}, "
        f"experience_years={user.experience_years}, "
        f"active_task_count={user.active_task_count}, location={user.location!r})"
    )


def format_rule(rule: TaskRule) -> str:
    return (
        f"TaskRule(task_id={rule.task_id}, department={rule.department!r}, "
        f"min_experience={rule.min_experience}, "
        f"max_active_tasks={rule.max_active_tasks}, location={rule.location!r})"
    )


def find_task_with_rule(
    task_repo: TaskRepository,
    rule_repo: TaskRuleRepository,
) -> tuple[Task, TaskRule] | None:
    for rule in rule_repo.list_rules():
        task = task_repo.get_task_by_id(rule.task_id)
        if task is not None:
            return task, rule
    return None


def main() -> None:
    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        rule_repo = TaskRuleRepository(db)
        assignment_repo = AssignmentRepository(db)
        service = AssignmentService(db)

        print("=== 1. Use existing task and rule ===")
        result = find_task_with_rule(task_repo, rule_repo)
        if result is None:
            print("No task with a rule found. Run test_rule_engine.py first.")
            sys.exit(1)

        task, rule = result
        print(f"Task: id={task.id}, title={task.title!r}")
        print(f"Rule: {format_rule(rule)}")

        print("\n=== 2. Compute eligibility and persist assignments ===")
        computed_users = service.compute_eligibility(task.id)
        print(f"Computed {len(computed_users)} eligible user(s)")

        print("\n=== 3. Read assignments back ===")
        assignments = assignment_repo.list_assignments(task.id)
        print(f"Persisted assignment rows: {len(assignments)}")
        for assignment in assignments:
            print(
                f"  - task_id={assignment.task_id}, user_id={assignment.user_id}, "
                f"is_eligible={assignment.is_eligible}"
            )

        print("\n=== 4. Read eligible users ===")
        eligible_users = service.get_eligible_users(task.id)
        print(f"Eligible users: {len(eligible_users)}")
        for user in eligible_users:
            print(f"  - {format_user(user)}")

        print("\n=== 5. Verify ===")
        if len(assignments) < 1:
            print("FAIL - No assignments persisted")
            sys.exit(1)

        if not all(assignment.is_eligible for assignment in assignments):
            print("FAIL - Not all assignments are marked eligible")
            sys.exit(1)

        stored_user_ids = {user.id for user in eligible_users}
        assignment_user_ids = {assignment.user_id for assignment in assignments}
        if stored_user_ids != assignment_user_ids:
            print("FAIL - Eligible users do not match persisted assignments")
            sys.exit(1)

        print("PASS - At least one assignment exists and data is consistent")
        print("\nAssignmentService integration test passed.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
