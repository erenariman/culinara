import uuid
from typing import List
from src.domain.entities.social import Comment, Review
from src.application.ports.repositories.social_repository import SocialRepositoryPort
from src.domain.exceptions import EntityNotFoundError, PermissionDeniedError, ValidationError

class SocialUseCase:
    def __init__(self, social_repo: SocialRepositoryPort):
        self.social_repo = social_repo

    async def post_comment(self, user_id: str, recipe_id: str, text: str) -> Comment:
        # In a real app, we'd enable 'moderation' scanning here using an AI service
        comment = Comment(
            id=str(uuid.uuid4()), 
            user_id=user_id,
            recipe_id=recipe_id,
            text=text
        )
        return await self.social_repo.add_comment(comment)

    async def get_recipe_comments(self, recipe_id: str) -> List[Comment]:
        return await self.social_repo.get_recipe_comments(recipe_id)

    async def delete_comment(self, user_id: str, comment_id: str) -> bool:
        comment = await self.social_repo.get_comment_by_id(comment_id)
        if not comment:
            return False
        
        # Check ownership or admin (assuming usecase doesn't know about admin, but maybe user_id is enough check for now)
        if comment.user_id != user_id:
             raise PermissionDeniedError("Not authorized to delete this comment")
             
        return await self.social_repo.delete_comment(comment_id)

    async def update_comment(self, user_id: str, comment_id: str, text: str) -> Comment:
        comment = await self.social_repo.get_comment_by_id(comment_id)
        if not comment:
            raise EntityNotFoundError("Comment not found")
        
        if comment.user_id != user_id:
             raise PermissionDeniedError("Not authorized to edit this comment")
        
        comment.text = text
        # In a real app, re-run moderation check here
        
        return await self.social_repo.update_comment(comment)

    async def list_all_comments(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        return await self.social_repo.list_all_comments(skip, limit)

    async def get_comment_by_id(self, comment_id: str):
        return await self.social_repo.get_comment_by_id(comment_id)

    async def submit_review(self, user_id: str, recipe_id: str, rating: int, text: str = None, image_url: str = None) -> Review:
        if not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5")
            
        review = Review(
            id=str(uuid.uuid4()),
            user_id=user_id,
            recipe_id=recipe_id,
            rating=rating,
            text=text,
            image_url=image_url
        )
        return await self.social_repo.add_review(review)

    async def toggle_like(self, user_id: str, recipe_id: str) -> bool:
        return await self.social_repo.toggle_like(user_id, recipe_id)
