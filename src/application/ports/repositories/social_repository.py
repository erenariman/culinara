from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.social import Comment, Follow, Review

class SocialRepositoryPort(ABC):
    @abstractmethod
    async def add_comment(self, comment: Comment) -> Comment: pass
    
    @abstractmethod
    async def list_all_comments(self, skip: int, limit: int) -> List[Comment]: pass

    @abstractmethod
    async def get_recipe_comments(self, recipe_id: str) -> List[Comment]: pass
    @abstractmethod
    async def get_comment_by_id(self, comment_id: str) -> Optional[Comment]: pass
    @abstractmethod
    async def delete_comment(self, comment_id: str) -> bool: pass
    @abstractmethod
    async def update_comment(self, comment: Comment) -> Comment: pass
    @abstractmethod
    async def follow_user(self, follow: Follow) -> None: pass
    
    @abstractmethod
    async def add_review(self, review: Review) -> Review: pass

    @abstractmethod
    async def toggle_like(self, user_id: str, recipe_id: str) -> bool:
        """Toggle like on a recipe. Returns True if liked, False if unliked."""
        pass

