import uuid
from slugify import slugify
from typing import Optional, List
from src.domain.entities.user import User, UserProfile
from src.application.ports.repositories.user_repository import UserRepositoryPort, UserProfileRepositoryPort
from src.application.ports.password_port import PasswordServicePort
from src.domain.exceptions import AlreadyExistsError, EntityNotFoundError

class UserUseCase:
    def __init__(
        self, 
        user_repo: UserRepositoryPort, 
        profile_repo: UserProfileRepositoryPort,
        password_service: PasswordServicePort = None,
    ):
        self.user_repo = user_repo
        self.profile_repo = profile_repo
        self._password_service = password_service

    async def register_user(self, email: str, username: str, password: str) -> User:
        # Check if exists
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise AlreadyExistsError("Email already registered")
        
        # Create Entity
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            username=username,
            slug=f"{slugify(username)}-{uuid.uuid4().hex[:4]}",
            hashed_password=self._password_service.get_password_hash(password)
        )
        
        saved_user = await self.user_repo.save(user)
        
        # Create empty profile
        profile = UserProfile(user_id=saved_user.id)
        await self.profile_repo.save(profile)
        
        return saved_user

    async def delete_account(self, user_id: str) -> bool:
        return await self.user_repo.delete(user_id)

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        return await self.profile_repo.get_by_user_id(user_id)

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.user_repo.get_by_id(user_id)

    async def update_profile(self, user_id: str, bio: str, preferences: dict) -> UserProfile:
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
             # Create if missing
             profile = UserProfile(user_id=user_id)
        
        profile.bio = bio
        profile.preferences = preferences
        
        return await self.profile_repo.save(profile)

    async def list_users(self, skip: int, limit: int) -> list[User]:
        return await self.user_repo.list_all(skip, limit)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Verify credentials. Returns User on success, None on failure."""
        user = await self.user_repo.get_by_email(email)
        if not user or not user.hashed_password:
            return None
        if not self._password_service.verify_password(password, user.hashed_password):
            return None
        return user

    async def update_status(self, user_id: str, is_active: bool) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User not found")
        
        user.is_active = is_active
        return await self.user_repo.update(user)

    async def update_user_admin(
        self, 
        user_id: str, 
        username: Optional[str] = None, 
        password: Optional[str] = None, 
        is_active: Optional[bool] = None, 
        is_superuser: Optional[bool] = None
    ) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User not found")
        
        if username is not None:
            user.username = username
            # Update slug if username changes
            user.slug = f"{slugify(username)}-{uuid.uuid4().hex[:4]}"
        
        if password is not None:
            user.hashed_password = self._password_service.get_password_hash(password)
        
        if is_active is not None:
            user.is_active = is_active
            
        if is_superuser is not None:
            user.is_superuser = is_superuser
            
        return await self.user_repo.update(user)
