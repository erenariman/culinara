from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User, UserProfile

class UserRepositoryPort(ABC):
    @abstractmethod
    async def save(self, user: User) -> User: pass
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[User]: pass
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool: pass
    
    @abstractmethod
    async def list_all(self, skip: int, limit: int) -> list[User]: pass

    @abstractmethod
    async def update(self, user: User) -> User: pass

class UserProfileRepositoryPort(ABC):
    @abstractmethod
    async def save(self, profile: UserProfile) -> UserProfile: pass
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[UserProfile]: pass
