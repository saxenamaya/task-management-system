from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.assignment_service import AssignmentService
from app.users.models import User
from app.users.schemas import UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> User:
    user_repository = UserRepository(db)

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found",
        )

    user.department = payload.department
    user.experience_years = payload.experience_years
    user.location = payload.location
    user.active_task_count = payload.active_task_count

    updated_user = user_repository.update_user(user)

    db.commit()

    assignment_service = AssignmentService(db)
    assignment_service.recompute_all_assignments()

    return updated_user
