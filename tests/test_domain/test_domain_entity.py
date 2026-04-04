import pytest
from src.domain.entities.recipe import Recipe, RecipeItem, RecipeStatus, RecipeInstruction
from src.domain.entities.ingredient import Ingredient
from src.domain.entities.units import UnitType

def test_recipe_entity_creation():
    recipe = Recipe(
        id="test-recipe-1",
        title="Test Recipe",
        description="A pure python domain recipe test"
    )
    assert recipe.id == "test-recipe-1"
    assert recipe.title == "Test Recipe"
    assert recipe.status == RecipeStatus.DRAFT
    assert len(recipe.items) == 0

def test_recipe_item_creation():
    ing = Ingredient(
        id="ing-1",
        name="Tomato",
        calories_per_100g=18.0,
        protein_per_100g=0.9,
        fat_per_100g=0.2,
        carbs_per_100g=3.9,
        density_g_ml=1.0,
        avg_weight_per_piece_g=120.0
    )
    item = RecipeItem(
        ingredient=ing,
        amount=2.0,
        unit=UnitType.PIECE
    )
    assert item.ingredient_name == "Tomato"
    assert item.amount == 2.0
    assert item.unit == UnitType.PIECE
