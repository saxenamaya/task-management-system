from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.repositories.user_repository import UserRepository
from app.users.models import User, UserRole


class UserService:
    """Application logic for user management."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._user_repository = UserRepository(db)

    def create_user(
        self,
        *,
        name: str,
        email: str,
        password: str,
        role: UserRole,
        department: str,
        location: str,
        experience_years: int = 0,
        active_task_count: int = 0,
    ) -> User:
        normalized_email = email.strip().lower()

        if self._user_repository.get_by_email(normalized_email) is not None:
            raise UserAlreadyExistsError(
                f"A user with email '{normalized_email}' already exists"
            )

        user = User(
            name=name.strip(),
            email=normalized_email,
            password_hash=hash_password(password),
            role=role,
            department=department.strip(),
            location=location.strip(),
            experience_years=experience_years,
            active_task_count=active_task_count,
        )

        created_user = self._user_repository.create_user(user)
        self._db.commit()
        return created_user

    def get_user_by_id(self, user_id: int) -> User:
        user = self._user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

    def get_user_by_email(self, email: str) -> User:
        normalized_email = email.strip().lower()
        user = self._user_repository.get_by_email(normalized_email)
        if user is None:
            raise UserNotFoundError(
                f"User with email '{normalized_email}' not found"
            )
        return user

    def list_users(self, *, skip: int = 0, limit: int = 100) -> list[User]:
        if skip < 0:
            raise ValueError("skip must be greater than or equal to 0")
        if limit < 1:
            raise ValueError("limit must be greater than or equal to 1")

        return self._user_repository.list_users(skip=skip, limit=limit)
