from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, model_validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    slug: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    access: Optional[str] = None

    @model_validator(mode='after')
    def set_access_level(self) -> 'UserResponse':
        if self.access is None:
            self.access = "admin" if self.is_superuser else "user"
        return self

    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    preferences: Optional[Dict] = {}

class UserUpdateAdmin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
