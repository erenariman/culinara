import unittest
import sys
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.application.usecases.recipe_usecase import RecipeUseCase, CreateRecipeCommand, CreateRecipeItemCommand
from src.domain.entities.ingredient import Ingredient
from src.domain.entities.recipe import Recipe

class MockRecipeRepository:
    def __init__(self):
        self.save = AsyncMock()
        self.get_by_id = AsyncMock()
        self.list_all = AsyncMock()

class MockIngredientRepository:
    def __init__(self):
        self.get_by_name = AsyncMock()

class TestDuplicateIngredients(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.recipe_repo = MockRecipeRepository()
        self.ingredient_repo = MockIngredientRepository()
        self.use_case = RecipeUseCase(self.recipe_repo, self.ingredient_repo)

    async def test_create_recipe_duplicate_ingredients(self):
        # Setup Ingredient
        tomato = Ingredient(
            id="3", name="Tomato", calories_per_100g=18, protein_per_100g=0.9, 
            fat_per_100g=0.2, carbs_per_100g=3.9, density_g_ml=1.0, 
            avg_weight_per_piece_g=120.0
        )
        self.ingredient_repo.get_by_name.side_effect = lambda name: tomato if name == "Tomato" else None
        
        # Determine behavior of save. In real DB, this would raise IntegrityError.
        # But here we are testing Logic. 
        # Wait, if logic doesn't merge, it sends 2 items to Repo.
        self.recipe_repo.save.side_effect = lambda r: r

        command = CreateRecipeCommand(
            title="Tomato Soup",
            description="Test",
            instructions=["Step 1"],
            items=[
                CreateRecipeItemCommand(ingredient_name="Tomato", amount=2, unit="piece"),
                CreateRecipeItemCommand(ingredient_name="Tomato", amount=3, unit="piece")
            ],
            author_id="user1"
        )

        recipe = await self.use_case.create_recipe(command)
        
        # Logic should merge: 2 + 3 = 5
        self.assertEqual(len(recipe.items), 1, "Logic should merge duplicates")
        self.assertEqual(recipe.items[0].amount, 5.0, "Amount should be summed")

        print("\n[INFO] Generated Recipe Items:")
        for item in recipe.items:
            print(f"- {item.ingredient.name}: {item.amount} {item.unit}")

if __name__ == '__main__':
    unittest.main()
