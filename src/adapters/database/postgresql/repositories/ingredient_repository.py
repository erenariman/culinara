from typing import Optional, List
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories.ingredient_repository import IngredientRepositoryPort
from src.domain.entities.ingredient import Ingredient
from src.adapters.database.postgresql.models.ingredient import IngredientModel
from src.adapters.database.postgresql.models.recipe import RecipeModel, RecipeIngredientModel
from datetime import datetime


class PostgresIngredientRepository(IngredientRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: IngredientModel) -> Ingredient:
        return Ingredient(
            id=model.id,
            name=model.name,
            slug=model.slug,
            calories_per_100g=model.calories_per_100g,
            protein_per_100g=model.protein_per_100g,
            fat_per_100g=model.fat_per_100g,
            carbs_per_100g=model.carbs_per_100g,
            density_g_ml=model.density_g_ml,
            avg_weight_per_piece_g=model.avg_weight_per_piece_g,
        )

    def _to_model(self, ingredient: Ingredient) -> IngredientModel:
        return IngredientModel(
            id=ingredient.id,
            name=ingredient.name,
            slug=ingredient.slug,
            calories_per_100g=ingredient.calories_per_100g,
            protein_per_100g=ingredient.protein_per_100g,
            fat_per_100g=ingredient.fat_per_100g,
            carbs_per_100g=ingredient.carbs_per_100g,
            density_g_ml=ingredient.density_g_ml,
            avg_weight_per_piece_g=ingredient.avg_weight_per_piece_g,
        )

    async def get_by_name(self, name: str) -> Optional[Ingredient]:
        result = await self.session.execute(
            select(IngredientModel)
            .where(IngredientModel.name == name)
            .where(IngredientModel.deleted_at.is_(None))
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_id(self, id: str) -> Optional[Ingredient]:
        result = await self.session.execute(
            select(IngredientModel)
            .where(IngredientModel.id == id)
            .where(IngredientModel.deleted_at.is_(None))
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_all(self) -> List[Ingredient]:
        result = await self.session.execute(
            select(IngredientModel).where(IngredientModel.deleted_at.is_(None))
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, ingredient: Ingredient) -> Ingredient:
        model = self._to_model(ingredient)
        merged = await self.session.merge(model)
        await self.session.flush()
        return self._to_domain(merged)

    async def delete(self, id: str) -> bool:
        # 1. Fetch the model
        result = await self.session.execute(
            select(IngredientModel).where(IngredientModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return False

        # 2. Check for ACTIVE (non-deleted) usages in recipes
        # Subquery to check if there is any RecipeIngredient link where the recipe's deleted_at is NULL
        usage_check = await self.session.execute(
            select(RecipeModel.id)
            .join(RecipeIngredientModel, RecipeModel.id == RecipeIngredientModel.recipe_id)
            .where(RecipeIngredientModel.ingredient_id == id)
            .where(RecipeModel.deleted_at.is_(None))
            .limit(1)
        )
        
        if usage_check.scalar_one_or_none():
            # This will naturally trigger a ForeignKey-like error mapped in main.py
            # But we can also raise a manual IntegrityError or let the DB fail if we try a hard delete.
            # For SOFT delete, we must manually block it here or else it would succeed.
            from sqlalchemy.exc import IntegrityError
            raise IntegrityError(
                "Ingredient is in use", 
                orig=Exception("is still referenced from table \"recipe_ingredients\""), 
                params={}
            )

        # 3. Perform Soft Delete
        model.deleted_at = datetime.now()
        await self.session.flush()
        return True
