class RecipeAppError(Exception):
    code: str = "UNSPECIFIED_ERROR"
    status_code: int = 500

    def __init__(self, message: str | None = None):
        self.message = (
            message if message is not None else "An unexpected error occurred."
        )
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message}

class DomainError(RecipeAppError):
    status_code = 400

class EntityNotFoundError(DomainError):
    code = "ENTITY_NOT_FOUND"
    status_code = 404

    def __init__(self, message: str = "The requested entity was not found."):
        super().__init__(message)

class UserNotFoundError(EntityNotFoundError):
    code = "USER_NOT_FOUND"

    def __init__(self, message: str = "The requested user was not found."):
        super().__init__(message)

class InvalidCredentialsError(DomainError):
    code = "INVALID_CREDENTIALS"
    status_code = 401

    def __init__(self, message: str = "Incorrect email or password."):
        super().__init__(message)

class InvalidTokenError(InvalidCredentialsError):
    code = "INVALID_TOKEN"

    def __init__(self, message: str = "Token is invalid or expired."):
        super().__init__(message)

class AlreadyExistsError(DomainError):
    code = "ALREADY_EXISTS"
    status_code = 409  # Conflict

    def __init__(self, message: str = "The entity already exists."):
        super().__init__(message)

class UserAlreadyExistsError(AlreadyExistsError):
    code = "USER_ALREADY_EXISTS"

    def __init__(self, message: str = "A user with the given details already exists."):
        super().__init__(message)

class ConflictError(RecipeAppError):
    code = "RESOURCE_CONFLICT"
    status_code = 409

    def __init__(self, message: str = "This resource is in use or was modified elsewhere."):
        super().__init__(message)

class PermissionDeniedError(RecipeAppError):
    code = "PERMISSION_DENIED"
    status_code = 403

    def __init__(
        self, message: str = "You do not have permission to perform this action."
    ):
        super().__init__(message)

class ValidationError(DomainError):
    code = "VALIDATION_ERROR"
    status_code = 400

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message)

class DatabaseError(RecipeAppError):
    code = "DATABASE_ERROR"
    status_code = 503

    def __init__(
        self, message: str = "A database error occurred. Please try again later."
    ):
        super().__init__(message)
