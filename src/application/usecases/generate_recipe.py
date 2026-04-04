import uuid
from typing import List

# Domain Imports
from src.domain.entities.recipe import Recipe, RecipeItem
from src.domain.services.nutrition_calculator import NutritionCalculatorService
from src.domain.entities.units import UnitType

# Ports Imports
from src.application.ports.repositories.recipe_repository import RecipeRepositoryPort
from src.application.ports.repositories.ingredient_repository import  IngredientRepositoryPort
from src.application.ports.ai_service import AIServicePort


class GenerateRecipeFromIngredientsUseCase:
    """
    Orchestrates the flow of:
    1. Getting recipe ideas from AI.
    2. Fetching real ingredient data (density/calories) from DB.
    3. Calculating precise nutrition using Domain Service.
    4. Saving the result.
    """

    def __init__(
            self,
            ai_service: AIServicePort,
            ingredient_repo: IngredientRepositoryPort,
            recipe_repo: RecipeRepositoryPort,
            calculator: NutritionCalculatorService
    ):
        # Dependency Injection: We just hold the tools we need.
        self.ai_service = ai_service
        self.ingredient_repo = ingredient_repo
        self.recipe_repo = recipe_repo
        self.calculator = calculator

    async def execute(self, available_ingredients: List[str]) -> Recipe:
        # 1. Ask AI for a recipe draft
        draft = await self.ai_service.generate_draft_recipe(available_ingredients)

        recipe_items = []
        total_cals = 0.0

        # 2. Process each item from AI
        for item_dto in draft.items:
            # a. Find the real ingredient in DB (to get density/calories)
            ingredient = await self.ingredient_repo.get_by_name(item_dto.ingredient_name)

            if not ingredient:
                # In a real app, handle this gracefully (e.g., create a dummy ingredient)
                print(f"Warning: Ingredient '{item_dto.ingredient_name}' not found in DB.")
                continue

            # b. Convert Unit string to Enum (Simple mapping)
            try:
                unit_enum = UnitType(item_dto.unit)
            except ValueError:
                unit_enum = UnitType.PIECE  # Fallback

            # c. Calculate Physics (The Core Logic)
            grams = self.calculator.calculate_grams(
                amount=item_dto.amount,
                unit=unit_enum,
                ingredient=ingredient
            )

            cals = self.calculator.calculate_calories(grams, ingredient)

            # d. Create Domain Object
            recipe_item = RecipeItem(
                ingredient=ingredient,
                amount=item_dto.amount,
                unit=unit_enum,
                calculated_grams=grams,
                calculated_calories=cals
            )

            recipe_items.append(recipe_item)
            total_cals += cals

        # 3. Construct the Full Recipe Entity
        final_recipe = Recipe(
            id=str(uuid.uuid4()),
            title=draft.title,
            description=draft.description,
            items=recipe_items,
            total_calories=round(total_cals, 2),
            instructions=draft.instructions
        )

        # 4. Save to Database
        return await self.recipe_repo.save(final_recipe)