from sqlalchemy import select
from sqlalchemy.orm import Session

from app.users.models import User


class UserRepository:
    """Data access layer for User entities."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create_user(self, user: User) -> User:
        self._db.add(user)
        self._db.flush()
        self._db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self._db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self._db.scalars(stmt).first()

    def list_users(self, *, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())

    def update_user(self, user: User) -> User:
        self._db.flush()
        self._db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        self._db.delete(user)
        self._db.flush()
