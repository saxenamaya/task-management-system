from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.assignments.schemas import EligibleTasksResponse, EligibleUsersResponse
from app.core.exceptions import TaskRuleNotFoundError, UserNotFoundError
from app.db.database import get_db
from app.repositories.task_repository import TaskRepository
from app.services.assignment_service import AssignmentService
from app.services.user_service import UserService

router = APIRouter(tags=["assignments"])


@router.post(
    "/tasks/{task_id}/compute-eligibility",
    response_model=EligibleUsersResponse,
    status_code=status.HTTP_200_OK,
)
def compute_eligibility(
    task_id: int,
    db: Session = Depends(get_db),
) -> EligibleUsersResponse:
    task_repository = TaskRepository(db)
    assignment_service = AssignmentService(db)

    if task_repository.get_task_by_id(task_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    try:
        eligible_users = assignment_service.compute_eligibility(task_id)
    except TaskRuleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return EligibleUsersResponse(
        task_id=task_id,
        count=len(eligible_users),
        eligible_users=eligible_users,
    )


@router.get(
    "/tasks/{task_id}/eligible-users",
    response_model=EligibleUsersResponse,
    status_code=status.HTTP_200_OK,
)
def get_eligible_users(
    task_id: int,
    db: Session = Depends(get_db),
) -> EligibleUsersResponse:
    task_repository = TaskRepository(db)
    assignment_service = AssignmentService(db)

    if task_repository.get_task_by_id(task_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    eligible_users = assignment_service.get_eligible_users(task_id)
    return EligibleUsersResponse(
        task_id=task_id,
        count=len(eligible_users),
        eligible_users=eligible_users,
    )


@router.get(
    "/users/{user_id}/eligible-tasks",
    response_model=EligibleTasksResponse,
    status_code=status.HTTP_200_OK,
)
def get_eligible_tasks(
    user_id: int,
    db: Session = Depends(get_db),
) -> EligibleTasksResponse:
    user_service = UserService(db)
    assignment_service = AssignmentService(db)

    try:
        user_service.get_user_by_id(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    eligible_tasks = assignment_service.get_eligible_tasks(user_id)
    return EligibleTasksResponse(
        user_id=user_id,
        count=len(eligible_tasks),
        eligible_tasks=eligible_tasks,
    )
