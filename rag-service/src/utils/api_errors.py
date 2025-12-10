from pydantic import BaseModel
from typing import Optional

class ErrorDetail(BaseModel):
    """
    Standardized error detail format.
    """
    code: str
    message: str
    target: Optional[str] = None # Optional: field or resource that caused the error

class APIError(BaseModel):
    """
    Unified API error response format.
    """
    error: ErrorDetail

# Custom Exceptions for mapping internal issues to API-safe errors
class BaseAPIException(Exception):
    """Base class for custom API exceptions."""
    def __init__(self, code: str, message: str, status_code: int = 500, target: Optional[str] = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.target = target
        super().__init__(message)

    def to_api_error(self) -> APIError:
        return APIError(error=ErrorDetail(code=self.code, message=self.message, target=self.target))

class BadRequestException(BaseAPIException):
    def __init__(self, message: str = "Bad Request", code: str = "BAD_REQUEST", target: Optional[str] = None):
        super().__init__(code, message, 400, target)

class UnauthorizedException(BaseAPIException):
    def __init__(self, message: str = "Unauthorized", code: str = "UNAUTHORIZED", target: Optional[str] = None):
        super().__init__(code, message, 401, target)

class ForbiddenException(BaseAPIException):
    def __init__(self, message: str = "Forbidden", code: str = "FORBIDDEN", target: Optional[str] = None):
        super().__init__(code, message, 403, target)

class NotFoundException(BaseAPIException):
    def __init__(self, message: str = "Not Found", code: str = "NOT_FOUND", target: Optional[str] = None):
        super().__init__(code, message, 404, target)

class TooManyRequestsException(BaseAPIException):
    def __init__(self, message: str = "Too Many Requests", code: str = "TOO_MANY_REQUESTS", target: Optional[str] = None):
        super().__init__(code, message, 429, target)

class InternalServerErrorException(BaseAPIException):
    def __init__(self, message: str = "Internal Server Error", code: str = "INTERNAL_SERVER_ERROR", target: Optional[str] = None):
        super().__init__(code, message, 500, target)

# Example usage (for demonstration)
def main():
    try:
        raise BadRequestException(message="Invalid session ID provided.", target="session_id")
    except BaseAPIException as e:
        print(f"Caught API Exception: {e.to_api_error().model_dump_json(indent=2)}")

    try:
        raise TooManyRequestsException(message="Rate limit exceeded for your session.")
    except BaseAPIException as e:
        print(f"Caught API Exception: {e.to_api_error().model_dump_json(indent=2)}")

if __name__ == "__main__":
    main()
