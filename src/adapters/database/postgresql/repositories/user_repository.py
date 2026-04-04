import json
from typing import Optional, List
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.ports.repositories.user_repository import UserRepositoryPort, UserProfileRepositoryPort
from src.domain.entities.user import User, UserProfile
from src.adapters.database.postgresql.models.user import UserModel
from src.adapters.database.postgresql.models.profile import UserProfileModel
from src.adapters.database.postgresql.models.recipe import RecipeModel
from src.adapters.database.postgresql.models.social import CommentModel
from datetime import datetime
from src.domain.exceptions import ConflictError
from sqlalchemy import update


class PostgresUserRepository(UserRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: UserModel) -> User:
        profile = None
        if model.profile:
            profile = UserProfile(
                user_id=model.id,
                bio=model.profile.bio,
                avatar_url=model.profile.avatar_url,
                preferences=json.loads(model.profile.preferences) if isinstance(model.profile.preferences, str) else (model.profile.preferences or {}),
            )
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            slug=model.slug,
            is_active=model.is_active,
            is_superuser=model.is_superuser,
            hashed_password=model.hashed_password,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
            profile=profile,
        )

    def _to_model(self, user: User) -> UserModel:
        return UserModel(
            id=user.id,
            email=user.email,
            username=user.username,
            slug=user.slug,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            deleted_at=user.deleted_at,
        )

    async def save(self, user: User) -> User:
        model = self._to_model(user)
        await self.session.merge(model)
        await self.session.flush()
        return user

    async def get_by_id(self, id: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel)
            .options(selectinload(UserModel.profile))
            .where(UserModel.id == id)
            .where(UserModel.deleted_at.is_(None))
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel)
            .options(selectinload(UserModel.profile))
            .where(UserModel.email == email)
            .where(UserModel.deleted_at.is_(None))
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def delete(self, id: str) -> bool:
        # 1. Fetch user
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        user = result.scalar_one_or_none()
        if not user:
             return False
        
        # 2. Perform Cascade Soft Delete
        # Note: We now allow deleting a user with recipes by soft-deleting the recipes too.
        now = datetime.now()
        
        # a. Cascade to Recipes
        await self.session.execute(
            update(RecipeModel)
            .where(RecipeModel.author_id == id)
            .where(RecipeModel.deleted_at.is_(None))
            .values(deleted_at=now)
        )
        
        # b. Cascade to Comments
        await self.session.execute(
            update(CommentModel)
            .where(CommentModel.user_id == id)
            .where(CommentModel.deleted_at.is_(None))
            .values(deleted_at=now)
        )

        # 3. Perform User Soft Delete
        user.deleted_at = now
        user.is_active = False # Deactivate on soft delete
        await self.session.flush()
        return True

    async def list_all(self, skip: int, limit: int) -> list[User]:
        result = await self.session.execute(
            select(UserModel)
            .options(selectinload(UserModel.profile))
            .where(UserModel.deleted_at.is_(None))
            .offset(skip).limit(limit)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def update(self, user: User) -> User:
        return await self.save(user)


class PostgresUserProfileRepository(UserProfileRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, profile: UserProfile) -> UserProfile:
        model = UserProfileModel(
            user_id=profile.user_id,
            bio=profile.bio,
            avatar_url=profile.avatar_url,
            preferences=json.dumps(profile.preferences) if isinstance(profile.preferences, dict) else profile.preferences,
        )
        await self.session.merge(model)
        await self.session.flush()
        return profile

    async def get_by_user_id(self, user_id: str) -> Optional[UserProfile]:
        result = await self.session.execute(
            select(UserProfileModel).where(UserProfileModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return UserProfile(
            user_id=model.user_id,
            bio=model.bio,
            avatar_url=model.avatar_url,
            preferences=json.loads(model.preferences) if isinstance(model.preferences, str) else (model.preferences or {}),
        )
