from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.exceptions import UserNotFoundError
from app.db.database import get_db
from app.repositories.task_repository import TaskRepository
from app.services.user_service import UserService
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.users.models import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    user_service = UserService(db)
    task_repository = TaskRepository(db)

    try:
        user_service.get_user_by_id(payload.created_by)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    task = Task(
        title=payload.title.strip(),
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
        created_by=payload.created_by,
    )

    created_task = task_repository.create_task(task)
    db.commit()

    return created_task

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> Task:
    task_repository = TaskRepository(db)

    task = task_repository.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    task.title = payload.title
    task.description = payload.description
    task.status = payload.status
    task.priority = payload.priority
    task.due_date = payload.due_date

    updated_task = task_repository.update_task(task)

    db.commit()

    return updated_task

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    task_repository = TaskRepository(db)

    task = task_repository.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    task_repository.delete_task(task)

    db.commit()