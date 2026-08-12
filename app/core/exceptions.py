class AppException(Exception):
    """Base exception for application errors."""


class DatabaseException(AppException):
    """Raised when a database operation fails."""
