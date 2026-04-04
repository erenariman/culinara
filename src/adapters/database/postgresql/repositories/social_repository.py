import uuid
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.application.ports.repositories.social_repository import SocialRepositoryPort
from src.domain.entities.social import Comment, Follow, Review
from src.adapters.database.postgresql.models.social import (
    CommentModel, ReviewModel, FollowModel, RecipeLikeModel
)


class PostgresSocialRepository(SocialRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Comment ---
    def _comment_to_domain(self, model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            user_id=model.user_id,
            recipe_id=model.recipe_id,
            text=model.text,
            parent_id=model.parent_id,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
        )

    async def add_comment(self, comment: Comment) -> Comment:
        model = CommentModel(
            id=comment.id,
            user_id=comment.user_id,
            recipe_id=comment.recipe_id,
            text=comment.text,
            parent_id=comment.parent_id,
        )
        self.session.add(model)
        await self.session.flush()
        return comment

    async def list_all_comments(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        result = await self.session.execute(
            select(CommentModel)
            .where(CommentModel.deleted_at.is_(None))
            .offset(skip).limit(limit)
        )
        return [self._comment_to_domain(m) for m in result.scalars().all()]

    async def get_recipe_comments(self, recipe_id: str) -> List[Comment]:
        result = await self.session.execute(
            select(CommentModel)
            .where(CommentModel.recipe_id == recipe_id)
            .where(CommentModel.deleted_at.is_(None))
        )
        return [self._comment_to_domain(m) for m in result.scalars().all()]

    async def get_comment_by_id(self, comment_id: str) -> Optional[Comment]:
        result = await self.session.execute(
            select(CommentModel).where(CommentModel.id == comment_id)
        )
        model = result.scalar_one_or_none()
        return self._comment_to_domain(model) if model else None

    async def delete_comment(self, comment_id: str) -> bool:
        result = await self.session.execute(
            select(CommentModel).where(CommentModel.id == comment_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        model.deleted_at = datetime.now()
        await self.session.flush()
        return True

    async def update_comment(self, comment: Comment) -> Comment:
        result = await self.session.execute(
            select(CommentModel).where(CommentModel.id == comment.id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.text = comment.text
            await self.session.flush()
        return comment

    # --- Follow ---
    async def follow_user(self, follow: Follow) -> None:
        model = FollowModel(
            follower_id=follow.follower_id,
            following_id=follow.following_id,
        )
        await self.session.merge(model)
        await self.session.flush()

    # --- Review ---
    async def add_review(self, review: Review) -> Review:
        model = ReviewModel(
            id=review.id,
            user_id=review.user_id,
            recipe_id=review.recipe_id,
            rating=review.rating,
            text=review.text,
            image_url=review.image_url,
        )
        self.session.add(model)
        await self.session.flush()
        return review

    # --- Like ---
    async def toggle_like(self, user_id: str, recipe_id: str) -> bool:
        """Toggle like. Returns True if liked, False if unliked."""
        result = await self.session.execute(
            select(RecipeLikeModel).where(
                RecipeLikeModel.user_id == user_id,
                RecipeLikeModel.recipe_id == recipe_id,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            await self.session.delete(existing)
            await self.session.flush()
            return False
        else:
            model = RecipeLikeModel(user_id=user_id, recipe_id=recipe_id)
            self.session.add(model)
            await self.session.flush()
            return True
