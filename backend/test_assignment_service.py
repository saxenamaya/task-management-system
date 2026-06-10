"""Manual test script for AssignmentService.

Run from backend/:
    python test_assignment_service.py
"""

import sys

from app.auth.security import hash_password
from app.db.database import SessionLocal
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.task_rule_repository import TaskRuleRepository
from app.repositories.user_repository import UserRepository
from app.rule_engine.models import TaskRule
from app.services.assignment_service import AssignmentService
from app.rule_engine.models import TaskRule  # noqa: F401 — register task_rules for ORM
from app.tasks.models import Task  # noqa: F401 — register tasks for ORM
from app.users.models import User, UserRole

USER_1_EMAIL = "qa.eligible@example.com"
USER_2_EMAIL = "finance.ineligible@example.com"

RULE_DEPARTMENT = "QA"
RULE_MIN_EXPERIENCE = 3
RULE_MAX_ACTIVE_TASKS = 5
RULE_LOCATION = "Bangalore"


def format_user(user: User) -> str:
    return (
        f"User(id={user.id}, name={user.name!r}, department={user.department!r}, "
        f"experience_years={user.experience_years}, "
        f"active_task_count={user.active_task_count}, location={user.location!r})"
    )


def format_task(task: Task) -> str:
    return f"Task(id={task.id}, title={task.title!r})"


def upsert_sample_user(
    user_repo: UserRepository,
    *,
    email: str,
    name: str,
    department: str,
    experience_years: int,
    active_task_count: int,
    location: str,
) -> User:
    user = user_repo.get_by_email(email)
    if user is None:
        user = User(
            name=name,
            email=email,
            password_hash=hash_password("testpassword"),
            role=UserRole.USER,
            department=department,
            experience_years=experience_years,
            active_task_count=active_task_count,
            location=location,
        )
        return user_repo.create_user(user)

    user.name = name
    user.department = department
    user.experience_years = experience_years
    user.active_task_count = active_task_count
    user.location = location
    return user_repo.update_user(user)


def delete_existing_rule_for_task(
    rule_repo: TaskRuleRepository,
    task_id: int,
) -> None:
    existing_rule = rule_repo.get_rule_by_task_id(task_id)
    if existing_rule is not None:
        rule_repo.delete_rule(existing_rule)


def main() -> None:
    db = SessionLocal()
    try:
        task_repo = TaskRepository(db)
        rule_repo = TaskRuleRepository(db)
        user_repo = UserRepository(db)
        assignment_repo = AssignmentRepository(db)
        service = AssignmentService(db)

        print("=== 1. Create sample users ===")
        user_1 = upsert_sample_user(
            user_repo,
            email=USER_1_EMAIL,
            name="QA Eligible User",
            department="QA",
            experience_years=5,
            active_task_count=2,
            location="Bangalore",
        )
        user_2 = upsert_sample_user(
            user_repo,
            email=USER_2_EMAIL,
            name="Finance Ineligible User",
            department="Finance",
            experience_years=2,
            active_task_count=7,
            location="Delhi",
        )
        db.commit()
        print(f"User 1: {format_user(user_1)}")
        print(f"User 2: {format_user(user_2)}")

        print("\n=== 2. Find existing task ===")
        tasks = task_repo.list_tasks(limit=1)
        if not tasks:
            print("No tasks found. Run test_task_repository.py first.")
            sys.exit(1)
        task = tasks[0]
        print(format_task(task))

        print("\n=== 3. Setup task rule ===")
        delete_existing_rule_for_task(rule_repo, task.id)
        rule_repo.create_rule(
            TaskRule(
                task_id=task.id,
                department=RULE_DEPARTMENT,
                min_experience=RULE_MIN_EXPERIENCE,
                max_active_tasks=RULE_MAX_ACTIVE_TASKS,
                location=RULE_LOCATION,
            )
        )
        db.commit()
        print(
            f"Rule: department={RULE_DEPARTMENT!r}, min_experience={RULE_MIN_EXPERIENCE}, "
            f"max_active_tasks={RULE_MAX_ACTIVE_TASKS}, location={RULE_LOCATION!r}"
        )

        print("\n=== 4. compute_eligibility ===")
        computed_users = service.compute_eligibility(task.id)
        print(f"Computed eligible users: {len(computed_users)}")
        for user in computed_users:
            print(f"  - {format_user(user)}")

        print("\n=== 5. get_eligible_users ===")
        stored_users = service.get_eligible_users(task.id)
        print(f"Stored eligible users: {len(stored_users)}")
        for user in stored_users:
            print(f"  - {format_user(user)}")

        print("\n=== 6. get_eligible_tasks ===")
        eligible_tasks = service.get_eligible_tasks(user_1.id)
        print(f"Eligible tasks for User 1: {len(eligible_tasks)}")
        for eligible_task in eligible_tasks:
            print(f"  - {format_task(eligible_task)}")

        print("\n=== 7. Verify persisted assignments ===")
        assignments = assignment_repo.list_assignments(task.id)
        print(f"Assignment rows: {len(assignments)}")
        for assignment in assignments:
            print(
                f"  - task_id={assignment.task_id}, user_id={assignment.user_id}, "
                f"is_eligible={assignment.is_eligible}"
            )

        computed_ids = {user.id for user in computed_users}
        stored_ids = {user.id for user in stored_users}
        assignment_user_ids = {a.user_id for a in assignments if a.is_eligible}

        checks = [
            ("User 1 is eligible", user_1.id in computed_ids),
            ("User 2 is not eligible", user_2.id not in computed_ids),
            ("compute matches get_eligible_users", computed_ids == stored_ids),
            ("assignments match eligible users", assignment_user_ids == computed_ids),
            ("User 1 has eligible task", any(t.id == task.id for t in eligible_tasks)),
            ("all assignments marked eligible", all(a.is_eligible for a in assignments)),
        ]

        print("\n=== 8. Verification ===")
        all_passed = True
        for label, passed in checks:
            status = "PASS" if passed else "FAIL"
            print(f"  {status} - {label}")
            if not passed:
                all_passed = False

        if all_passed:
            print("\nAssignmentService test passed.")
        else:
            sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
