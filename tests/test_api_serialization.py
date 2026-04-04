import unittest
import sys
import os
from datetime import datetime
import uuid

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.entities.recipe import Recipe, RecipeItem, RecipeInstruction, RecipeStatus
from src.domain.entities.ingredient import Ingredient
from src.domain.entities.units import UnitType
from src.presentation.schemas.recipe import RecipeResponse

class TestApiSerialization(unittest.TestCase):
    def test_recipe_serialization(self):
        print("\n[INFO] Setting up Recipe Entity...")
        
        # Setup Ingredient
        tomato = Ingredient(
            id="3", name="Tomato", calories_per_100g=18, protein_per_100g=0.9, 
            fat_per_100g=0.2, carbs_per_100g=3.9, density_g_ml=1.0, 
            avg_weight_per_piece_g=120.0
        )

        # Setup RecipeItem
        item = RecipeItem(
            ingredient=tomato,
            amount=2.0,
            unit=UnitType.PIECE
        )
        
        # Setup RecipeInstruction
        instruction = RecipeInstruction(
            id=str(uuid.uuid4()),
            step_number=1,
            text="Chop tomatoes"
        )

        # Setup Recipe
        recipe = Recipe(
            id=str(uuid.uuid4()),
            title="Tomato Soup",
            description="Delicious soup",
            status=RecipeStatus.DRAFT,
            slug=None,
            author_id="user1",
            instructions=[instruction],
            items=[item], # This contains RecipeItem objects
            image_url="http://img.com/1.jpg"
        )

        print("[INFO] Attempting to validate with RecipeResponse schema...")
        try:
            # this simulates what FastAPI does when returning the response
            response_model = RecipeResponse.model_validate(recipe)
            print("[SUCCESS] Serialization successful!")
            print(response_model.model_dump())
        except Exception as e:
            print(f"\n[ERROR] Serialization FAILED: {e}")
            # If model_validate doesn't exist (Pydantic v1), try from_orm
            try:
                print("[INFO] Retrying with from_orm (Pydantic v1 fallback)...")
                response_model = RecipeResponse.from_orm(recipe)
                print("[SUCCESS] Serialization successful with from_orm!")
            except Exception as e2:
                print(f"[ERROR] from_orm FAILED: {e2}")
                raise e

if __name__ == '__main__':
    unittest.main()
