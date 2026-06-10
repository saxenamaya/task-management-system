from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.auth.security import create_access_token, hash_password, verify_password
from app.core.exceptions import AuthenticationError, UserAlreadyExistsError
from app.repositories.user_repository import UserRepository
from app.users.models import User


class AuthService:
    """Authentication and registration logic."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._user_repository = UserRepository(db)

    def register_user(self, payload: RegisterRequest) -> User:
        normalized_email = payload.email.strip().lower()

        if self._user_repository.get_by_email(normalized_email) is not None:
            raise UserAlreadyExistsError(
                f"A user with email '{normalized_email}' already exists"
            )

        user = User(
            name=payload.name.strip(),
            email=normalized_email,
            password_hash=hash_password(payload.password),
            role=payload.role,
            department=payload.department.strip(),
            location=payload.location.strip(),
            experience_years=payload.experience_years,
            active_task_count=payload.active_task_count,
        )

        created_user = self._user_repository.create_user(user)
        self._db.commit()
        return created_user

    def login(self, payload: LoginRequest) -> TokenResponse:
        normalized_email = payload.email.strip().lower()
        user = self._user_repository.get_by_email(normalized_email)

        if user is None:
            raise AuthenticationError("Invalid email or password")

        if not verify_password(payload.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")

        access_token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=access_token)
