class AppError(Exception):
    """Base exception for application errors."""


class UserNotFoundError(AppError):
    """Raised when a user cannot be found."""

    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message)


class UserAlreadyExistsError(AppError):
    """Raised when creating a user with an email that already exists."""

    def __init__(self, message: str = "User already exists") -> None:
        super().__init__(message)


class AuthenticationError(AppError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message)


class TaskNotFoundError(AppError):
    """Raised when a task cannot be found."""

    def __init__(self, message: str = "Task not found") -> None:
        super().__init__(message)


class TaskRuleNotFoundError(AppError):
    """Raised when a task has no eligibility rule."""

    def __init__(self, message: str = "Task rule not found") -> None:
        super().__init__(message)


class TaskRuleAlreadyExistsError(AppError):
    """Raised when a task already has an eligibility rule."""

    def __init__(self, message: str = "Task rule already exists") -> None:
        super().__init__(message)
