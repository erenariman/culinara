from sqlalchemy import select, func, desc, asc, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple

from src.application.ports.repositories.recipe_repository import RecipeRepositoryPort, RecipeFilterParams
from src.domain.entities.recipe import Recipe, RecipeItem, RecipeInstruction, RecipeStatus, RecipeTag
from src.domain.entities.ingredient import Ingredient
from src.domain.entities.units import UnitType
from src.adapters.database.postgresql.models.recipe import RecipeModel, RecipeIngredientModel
from src.adapters.database.postgresql.models.ingredient import IngredientModel
from src.adapters.database.postgresql.models.instruction import InstructionStepModel
from src.adapters.database.postgresql.models.social import ReviewModel, RecipeLikeModel
from src.adapters.database.postgresql.models.user import UserModel


class PostgresRecipeRepository(RecipeRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: RecipeModel) -> Recipe:
        items = []
        if model.ingredients:
            for ri in model.ingredients:
                if ri.ingredient:
                    ingredient = Ingredient(
                        id=ri.ingredient.id,
                        name=ri.ingredient.name,
                        calories_per_100g=ri.ingredient.calories_per_100g,
                        protein_per_100g=ri.ingredient.protein_per_100g,
                        fat_per_100g=ri.ingredient.fat_per_100g,
                        carbs_per_100g=ri.ingredient.carbs_per_100g,
                        density_g_ml=ri.ingredient.density_g_ml,
                        avg_weight_per_piece_g=ri.ingredient.avg_weight_per_piece_g,
                    )
                    try:
                        unit = UnitType(ri.unit)
                    except ValueError:
                        unit = UnitType.GRAM
                    items.append(RecipeItem(
                        ingredient=ingredient,
                        amount=ri.amount,
                        unit=unit,
                    ))

        instructions = []
        if model.steps:
            for step in sorted(model.steps, key=lambda s: s.step_number):
                instructions.append(RecipeInstruction(
                    id=step.id,
                    step_number=step.step_number,
                    text=step.text,
                    image_url=step.image_url,
                    timer_seconds=step.timer_seconds,
                ))

        tags = []
        if model.tags:
            for model_tag in model.tags:
                tags.append(RecipeTag(
                    id=model_tag.id,
                    name=model_tag.name,
                    slug=model_tag.slug or "",
                    type=model_tag.type
                ))

        # Calculate aggregates from relations
        author_name = None
        average_rating = None
        review_count = 0

        recipe = Recipe(
            id=model.id,
            title=model.title,
            description=model.description or "",
            items=items,
            instructions=instructions,
            tags=tags,
            total_calories=model.total_calories or 0.0,
            total_protein=model.total_protein or 0.0,
            total_carbs=model.total_carbs or 0.0,
            total_fat=model.total_fat or 0.0,
            total_cost=model.total_cost or 0.0,
            slug=model.slug or "",
            status=RecipeStatus(model.status) if model.status else RecipeStatus.DRAFT,
            view_count=model.view_count or 0,
            difficulty=model.difficulty,
            category=model.category,
            diet_type=model.diet_type,
            prep_time_minutes=model.prep_time_minutes,
            cook_time_minutes=model.cook_time_minutes,
            servings=model.servings,
            video_url=model.video_url,
            image_url=model.image_url or "",
            author_id=model.author_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
        
        # Set author name if available (from JOIN)
        if hasattr(model, 'author') and model.author:
            recipe.author_name = model.author.username
        else:
            # Fallback for manual logic if needed, but joinedload is primary now
            recipe.author_name = model.author_username if hasattr(model, 'author_username') else None

        return recipe

    def _to_model(self, recipe: Recipe) -> RecipeModel:
        model = RecipeModel(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            instructions=recipe.description[:100] if recipe.description else "",
            image_url=recipe.image_url,
            video_url=recipe.video_url,
            total_calories=recipe.total_calories,
            total_protein=recipe.total_protein,
            total_carbs=recipe.total_carbs,
            total_fat=recipe.total_fat,
            total_cost=recipe.total_cost,
            slug=recipe.slug,
            status=recipe.status,
            view_count=recipe.view_count,
            difficulty=recipe.difficulty,
            category=recipe.category,
            diet_type=recipe.diet_type,
            prep_time_minutes=recipe.prep_time_minutes,
            cook_time_minutes=recipe.cook_time_minutes,
            servings=recipe.servings,
            author_id=recipe.author_id,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at,
            deleted_at=recipe.deleted_at,
        )

        # Ingredients
        model.ingredients = []
        for item in recipe.items:
            model.ingredients.append(RecipeIngredientModel(
                recipe_id=recipe.id,
                ingredient_id=item.ingredient.id,
                amount=item.amount,
                unit=item.unit.value if isinstance(item.unit, UnitType) else item.unit,
            ))

        # Instructions
        model.steps = []
        for inst in recipe.instructions:
            model.steps.append(InstructionStepModel(
                id=inst.id,
                recipe_id=recipe.id,
                step_number=inst.step_number,
                text=inst.text,
                image_url=inst.image_url,
                timer_seconds=inst.timer_seconds,
            ))

        return model

    async def save(self, recipe: Recipe) -> Recipe:
        model = self._to_model(recipe)
        await self.session.merge(model)
        await self.session.flush()
        return recipe

    async def get_by_id(self, id: str) -> Optional[Recipe]:
        result = await self.session.execute(
            select(RecipeModel)
            .options(
                selectinload(RecipeModel.ingredients).selectinload(RecipeIngredientModel.ingredient),
                selectinload(RecipeModel.steps),
                selectinload(RecipeModel.reviews),
                selectinload(RecipeModel.likes),
                selectinload(RecipeModel.tags),
                joinedload(RecipeModel.author), # Explicit JOIN
            )
            .where(RecipeModel.id == id)
            .where(RecipeModel.deleted_at.is_(None))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        recipe = self._to_domain(model)

        # Aggregate review data
        if model.reviews:
            ratings = [r.rating for r in model.reviews]
            recipe.review_count = len(ratings)
            recipe.average_rating = sum(ratings) / len(ratings) if ratings else None

        return recipe

    async def list_all(self) -> List[Recipe]:
        result = await self.session.execute(
            select(RecipeModel)
            .options(
                selectinload(RecipeModel.ingredients).selectinload(RecipeIngredientModel.ingredient),
                selectinload(RecipeModel.steps),
                selectinload(RecipeModel.tags),
                joinedload(RecipeModel.author),
            )
            .where(RecipeModel.deleted_at.is_(None))
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def search_recipes(self, filters: RecipeFilterParams) -> Tuple[List[Recipe], int]:
        query = (
            select(RecipeModel)
            .options(
                selectinload(RecipeModel.ingredients).selectinload(RecipeIngredientModel.ingredient),
                selectinload(RecipeModel.steps),
                selectinload(RecipeModel.reviews),
                selectinload(RecipeModel.tags),
                joinedload(RecipeModel.author),
            )
            .where(RecipeModel.deleted_at.is_(None))
        )

        # Filters
        if filters.category:
            query = query.where(RecipeModel.category == filters.category)
        if filters.difficulty:
            query = query.where(RecipeModel.difficulty == filters.difficulty)
        if filters.dietary_preference:
            query = query.where(RecipeModel.diet_type == filters.dietary_preference)
        if filters.max_prep_time:
            query = query.where(RecipeModel.prep_time_minutes <= filters.max_prep_time)
        if filters.search:
            search_pattern = f"%{filters.search}%"
            query = query.where(RecipeModel.title.ilike(search_pattern))

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()

        # Sorting
        sort_column = getattr(RecipeModel, filters.sort_by, RecipeModel.created_at)
        if filters.order == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        # Pagination
        offset = (filters.page - 1) * filters.limit
        query = query.offset(offset).limit(filters.limit)

        result = await self.session.execute(query)
        models = result.scalars().unique().all()

        recipes = []
        for model in models:
            recipe = self._to_domain(model)
            if model.reviews:
                ratings = [r.rating for r in model.reviews]
                recipe.review_count = len(ratings)
                recipe.average_rating = sum(ratings) / len(ratings) if ratings else None
            recipes.append(recipe)

        return recipes, total

    async def delete(self, id: str) -> bool:
        result = await self.session.execute(
            select(RecipeModel).where(RecipeModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        from datetime import datetime
        model.deleted_at = datetime.now()
        await self.session.flush()
        return True
