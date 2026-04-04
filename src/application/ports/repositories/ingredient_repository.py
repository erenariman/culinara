from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.ingredient import Ingredient


class IngredientRepositoryPort(ABC):
    """
    Port for accessing Ingredient data (Density, Calories, etc.).
    """
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Ingredient]:
        """Finds an ingredient by its name (e.g., 'Tomato')."""
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Ingredient]:
        pass

    @abstractmethod
    async def list_all(self) -> List[Ingredient]:
        pass

    @abstractmethod
    async def save(self, ingredient: Ingredient) -> Ingredient:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass