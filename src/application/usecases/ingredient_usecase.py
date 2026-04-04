import uuid
from slugify import slugify
from dataclasses import dataclass
from typing import List, Optional

from src.domain.entities.ingredient import Ingredient
from src.application.ports.repositories.ingredient_repository import IngredientRepositoryPort

@dataclass
class CreateIngredientCommand:
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float
    density_g_ml: float
    avg_weight_per_piece_g: Optional[float] = None

@dataclass
class UpdateIngredientCommand:
    name: Optional[str] = None
    calories_per_100g: Optional[float] = None
    protein_per_100g: Optional[float] = None
    fat_per_100g: Optional[float] = None
    carbs_per_100g: Optional[float] = None
    density_g_ml: Optional[float] = None
    avg_weight_per_piece_g: Optional[float] = None

class IngredientUseCase:
    def __init__(self, ingredient_repo: IngredientRepositoryPort):
        self.ingredient_repo = ingredient_repo

    async def create_ingredient(self, command: CreateIngredientCommand) -> Ingredient:
        # Check if exists by name first? 
        # For simplicity, assuming unique constraint will be handled or we just check here.
        existing = await self.ingredient_repo.get_by_name(command.name)
        if existing:
            raise ValueError(f"Ingredient with name '{command.name}' already exists.")

        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name=command.name,
            slug=f"{slugify(command.name)}-{uuid.uuid4().hex[:4]}",
            calories_per_100g=command.calories_per_100g,
            protein_per_100g=command.protein_per_100g,
            fat_per_100g=command.fat_per_100g,
            carbs_per_100g=command.carbs_per_100g,
            density_g_ml=command.density_g_ml,
            avg_weight_per_piece_g=command.avg_weight_per_piece_g
        )
        return await self.ingredient_repo.save(ingredient)

    async def get_ingredient(self, id: str) -> Optional[Ingredient]:
        return await self.ingredient_repo.get_by_id(id)

    async def list_ingredients(self) -> List[Ingredient]:
        return await self.ingredient_repo.list_all()

    async def update_ingredient(self, id: str, command: UpdateIngredientCommand) -> Optional[Ingredient]:
        ingredient = await self.ingredient_repo.get_by_id(id)
        if not ingredient:
            return None

        if command.name is not None:
            ingredient.name = command.name
        if command.calories_per_100g is not None:
            ingredient.calories_per_100g = command.calories_per_100g
        if command.protein_per_100g is not None:
            ingredient.protein_per_100g = command.protein_per_100g
        if command.fat_per_100g is not None:
            ingredient.fat_per_100g = command.fat_per_100g
        if command.carbs_per_100g is not None:
            ingredient.carbs_per_100g = command.carbs_per_100g
        if command.density_g_ml is not None:
            ingredient.density_g_ml = command.density_g_ml
        if command.avg_weight_per_piece_g is not None:
            ingredient.avg_weight_per_piece_g = command.avg_weight_per_piece_g
        
        return await self.ingredient_repo.save(ingredient)

    async def delete_ingredient(self, id: str) -> bool:
        return await self.ingredient_repo.delete(id)
