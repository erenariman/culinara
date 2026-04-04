import pytest
import uuid
from typing import Optional, List
from src.application.usecases.user_usecase import UserUseCase
from src.domain.entities.user import User, UserProfile
from src.application.ports.repositories.user_repository import UserRepositoryPort, UserProfileRepositoryPort
from src.application.ports.password_port import PasswordServicePort

# --- Fake Mocks ---
class FakeUserRepository(UserRepositoryPort):
    def __init__(self):
        self.db = {}
        
    async def get_by_email(self, email: str) -> Optional[User]:
        for u in self.db.values():
            if u.email == email:
                return u
        return None

    async def get_by_id(self, id: str) -> Optional[User]:
        return self.db.get(id)

    async def save(self, user: User) -> User:
        self.db[user.id] = user
        return user
        
    async def list_all(self, skip: int, limit: int) -> List[User]:
        return list(self.db.values())[skip:skip+limit]

    async def delete(self, id: str) -> bool:
        if id in self.db:
            del self.db[id]
            return True
        return False

    async def update(self, user: User) -> User:
        return await self.save(user)


class FakeProfileRepository(UserProfileRepositoryPort):
    def __init__(self):
        self.db = {}
        
    async def save(self, profile: UserProfile) -> UserProfile:
        self.db[profile.user_id] = profile
        return profile
        
    async def get_by_user_id(self, user_id: str) -> Optional[UserProfile]:
        return self.db.get(user_id)


class FakePasswordService(PasswordServicePort):
    def get_password_hash(self, password: str) -> str:
        return f"fake_hash_{password}"
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return hashed_password == f"fake_hash_{plain_password}"


@pytest.fixture
def usecase():
    user_repo = FakeUserRepository()
    profile_repo = FakeProfileRepository()
    password_svc = FakePasswordService()
    return UserUseCase(user_repo, profile_repo, password_svc)


@pytest.mark.asyncio
async def test_register_user_success(usecase: UserUseCase):
    user = await usecase.register_user("test@example.com", "tester", "password123")
    
    # User in db
    assert await usecase.user_repo.get_by_email("test@example.com") is not None
    # Hashed pw saved
    assert user.hashed_password == "fake_hash_password123"
    # Profile created
    profile = await usecase.get_user_profile(user.id)
    assert profile is not None

@pytest.mark.asyncio
async def test_register_user_duplicate_email(usecase: UserUseCase):
    await usecase.register_user("test@example.com", "tester", "password123")
    
    with pytest.raises(ValueError) as exc:
        await usecase.register_user("test@example.com", "tester2", "password456")
        
    assert "Email already registered" in str(exc.value)

@pytest.mark.asyncio
async def test_authenticate_user_success(usecase: UserUseCase):
    await usecase.register_user("test@example.com", "tester", "correct_password")
    user = await usecase.authenticate_user("test@example.com", "correct_password")
    
    assert user is not None
    assert user.email == "test@example.com"

@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(usecase: UserUseCase):
    await usecase.register_user("test@example.com", "tester", "correct_password")
    user = await usecase.authenticate_user("test@example.com", "WRONG_PASS")
    
    assert user is None
