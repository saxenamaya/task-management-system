"""Manual test script for TaskRuleRepository.

Run from backend/:
    python test_task_rule_repository.py
"""

import sys

from app.db.database import SessionLocal
from app.repositories.task_repository import TaskRepository
from app.repositories.task_rule_repository import TaskRuleRepository
from app.rule_engine.models import TaskRule
from app.tasks.models import Task
from app.users.models import User  # noqa: F401 — register users table for FK resolution

EXPECTED_DEPARTMENT = "QA"
EXPECTED_MIN_EXPERIENCE = 3
EXPECTED_MAX_ACTIVE_TASKS = 5
EXPECTED_LOCATION = "Bangalore"


def format_task(task: Task) -> str:
    return f"Task(id={task.id}, title={task.title!r})"


def format_rule(rule: TaskRule) -> str:
    return (
        f"TaskRule(id={rule.id}, task_id={rule.task_id}, "
        f"department={rule.department!r}, min_experience={rule.min_experience}, "
        f"max_active_tasks={rule.max_active_tasks}, location={rule.location!r})"
    )


def delete_existing_rule_for_task(
    rule_repo: TaskRuleRepository,
    task_id: int,
) -> bool:
    """Delete the eligibility rule for a task, if present."""
    existing_rule = rule_repo.get_rule_by_task_id(task_id)
    if existing_rule is None:
        return False

    rule_repo.delete_rule(existing_rule)
    return True


def verify_rules_match(created_rule: TaskRule, fetched_rule: TaskRule) -> bool:
    checks = [
        ("id", fetched_rule.id == created_rule.id),
        ("task_id", fetched_rule.task_id == created_rule.task_id),
        ("department", fetched_rule.department == created_rule.department),
        ("min_experience", fetched_rule.min_experience == created_rule.min_experience),
        ("max_active_tasks", fetched_rule.max_active_tasks == created_rule.max_active_tasks),
        ("location", fetched_rule.location == created_rule.location),
    ]

    print("\n=== 5. Verify fetched rule matches created rule ===")
    all_passed = True
    for field_name, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"  {status} - {field_name}")
        if not passed:
            all_passed = False

    return all_passed


def main() -> None:
    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        rule_repo = TaskRuleRepository(db)

        print("=== 1. Find existing task ===")
        tasks = task_repo.list_tasks(limit=1)
        if not tasks:
            print("No tasks found in the database. Create a task first.")
            sys.exit(1)

        task = tasks[0]
        print(format_task(task))

        print("\n=== 2. Delete existing rule for task ===")
        deleted = delete_existing_rule_for_task(rule_repo, task.id)
        db.commit()
        if deleted:
            print(f"Deleted existing rule for task id={task.id}")
        else:
            print(f"No existing rule for task id={task.id}")

        print("\n=== 3. Create fresh rule ===")
        new_rule = TaskRule(
            task_id=task.id,
            department=EXPECTED_DEPARTMENT,
            min_experience=EXPECTED_MIN_EXPERIENCE,
            max_active_tasks=EXPECTED_MAX_ACTIVE_TASKS,
            location=EXPECTED_LOCATION,
        )
        created_rule = rule_repo.create_rule(new_rule)
        db.commit()
        print(format_rule(created_rule))

        print("\n=== 4. Fetch rule by task_id ===")
        fetched_rule = rule_repo.get_rule_by_task_id(task.id)
        if fetched_rule is None:
            print(f"No rule found for task id {task.id}.")
            sys.exit(1)
        print(format_rule(fetched_rule))

        if verify_rules_match(created_rule, fetched_rule):
            print("\nFetched rule matches created rule.")
        else:
            print("\nFetched rule does not match created rule.")
            sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
