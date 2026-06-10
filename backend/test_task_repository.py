"""Manual test script for TaskRepository.

Run from backend/:
    python test_task_repository.py
"""

import sys
from datetime import date

from app.db.database import SessionLocal
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.tasks.models import Task, TaskPriority, TaskStatus
from app.users.models import User


def format_user(user: User) -> str:
    return f"User(id={user.id}, name={user.name!r}, email={user.email!r})"


def format_task(task: Task) -> str:
    return (
        f"Task(id={task.id}, title={task.title!r}, status={task.status.value}, "
        f"priority={task.priority.value}, created_by={task.created_by}, "
        f"due_date={task.due_date})"
    )


def find_existing_user(user_repo: UserRepository) -> User | None:
    users = user_repo.list_users(limit=1)
    return users[0] if users else None


def main() -> None:
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        task_repo = TaskRepository(db)

        print("=== 1. Find existing user ===")
        creator = find_existing_user(user_repo)
        if creator is None:
            print("No users found in the database. Create a user first.")
            sys.exit(1)
        print(format_user(creator))

        print("\n=== 2. Create task ===")
        new_task = Task(
            title="TaskRepository Test Task",
            description="Created by test_task_repository.py",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            due_date=date(2026, 6, 30),
            created_by=creator.id,
        )
        created_task = task_repo.create_task(new_task)
        db.commit()
        print(format_task(created_task))

        print("\n=== 3. Fetch task by ID ===")
        fetched_task = task_repo.get_task_by_id(created_task.id)
        if fetched_task is None:
            print(f"Task with id {created_task.id} not found.")
            sys.exit(1)
        print(format_task(fetched_task))

        print("\n=== 4. List tasks ===")
        all_tasks = task_repo.list_tasks()
        print(f"Total tasks: {len(all_tasks)}")
        for task in all_tasks:
            print(f"  - {format_task(task)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
