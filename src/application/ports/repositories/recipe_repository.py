from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from dataclasses import dataclass
from src.domain.entities.recipe import Recipe

@dataclass
class RecipeFilterParams:
    page: int = 1
    limit: int = 10
    category: Optional[str] = None
    difficulty: Optional[str] = None
    dietary_preference: Optional[str] = None
    max_prep_time: Optional[int] = None
    search: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    order: Optional[str] = "desc"

class RecipeRepositoryPort(ABC):
    """
    Port for accessing Recipe storage.
    """
    @abstractmethod
    async def save(self, recipe: Recipe) -> Recipe:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Recipe]:
        pass

    @abstractmethod
    async def list_all(self) -> List[Recipe]:
        pass

    @abstractmethod
    async def search_recipes(self, filters: RecipeFilterParams) -> Tuple[List[Recipe], int]:
        """
        Returns a tuple of (recipes, total_count).
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass