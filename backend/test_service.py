"""Manual test script for UserService duplicate prevention.

Run from backend/:
    python test_service.py
"""

from app.core.exceptions import UserAlreadyExistsError
from app.db.database import Base, SessionLocal, engine
from app.services.user_service import UserService
from app.users.models import User, UserRole

TEST_EMAIL = "test.duplicate@example.com"


def format_user(user: User) -> str:
    return (
        f"id={user.id}, name={user.name!r}, email={user.email!r}, "
        f"role={user.role.value}, department={user.department!r}"
    )


def main() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    duplicate_blocked = False

    try:
        service = UserService(db)

        print("=== Test 1: Create user ===")
        try:
            created_user = service.create_user(
                name="Test User",
                email=TEST_EMAIL,
                password="testpassword123",
                role=UserRole.USER,
                department="QA",
                location="Remote",
                experience_years=2,
            )
            print("PASS - User created successfully")
        except UserAlreadyExistsError:
            created_user = service.get_user_by_email(TEST_EMAIL)
            print("PASS - User already exists from a previous run")
        print(f"  {format_user(created_user)}")

        print("\n=== Test 2: Attempt duplicate user creation ===")
        try:
            service.create_user(
                name="Duplicate User",
                email=TEST_EMAIL,
                password="anotherpassword",
                role=UserRole.ADMIN,
                department="HR",
                location="Berlin",
            )
            print("FAIL - Duplicate user was created (should not happen)")
        except UserAlreadyExistsError as exc:
            duplicate_blocked = True
            print("PASS - Duplicate creation blocked")
            print(f"  Exception: {exc}")

        print("\n=== Test 3: Verify duplicate prevention ===")
        stored_user = service.get_user_by_email(TEST_EMAIL)
        users_with_email = [
            user for user in service.list_users() if user.email == TEST_EMAIL.lower()
        ]

        if duplicate_blocked and len(users_with_email) == 1:
            print("PASS - Exactly one user exists for the test email")
            print(f"  {format_user(stored_user)}")
        else:
            print("FAIL - Duplicate prevention verification failed")
            print(f"  duplicate_blocked={duplicate_blocked}")
            print(f"  users_with_email_count={len(users_with_email)}")

        print("\n=== Summary ===")
        if duplicate_blocked and len(users_with_email) == 1:
            print("All UserService duplicate-prevention checks passed.")
        else:
            print("One or more checks failed.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
