from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    total: Optional[int] = None
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    total_records: int = 0
    total_pages: int = 0
    current_page: int = 1
    limit: int = 10
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None
