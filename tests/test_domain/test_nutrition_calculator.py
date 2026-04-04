import pytest
from src.domain.services.nutrition_calculator import NutritionCalculatorService, NutritionInfo
from src.domain.entities.recipe import RecipeItem
from src.domain.entities.ingredient import Ingredient
from src.domain.entities.units import UnitType

def test_nutrition_calculator_empty():
    svc = NutritionCalculatorService()
    
    # Passing an empty item list logic doesn't apply to the individual method,
    # so we mock a 0 gram calculation just to verify it returns zeros.
    ing = Ingredient(
        id="test", name="test", calories_per_100g=10.0,
        protein_per_100g=0, fat_per_100g=0, carbs_per_100g=0, density_g_ml=1
    )
    info = svc.calculate_nutrition(0.0, ing)
    
    assert info.calories == 0.0
    assert info.protein == 0.0
    assert info.fat == 0.0
    assert info.carbs == 0.0

def test_nutrition_calculator_with_items():
    svc = NutritionCalculatorService()
    
    ing = Ingredient(
        id="ing-1",
        name="Tomato",
        calories_per_100g=20.0,
        protein_per_100g=1.0,
        fat_per_100g=0.2,
        carbs_per_100g=4.0,
        density_g_ml=1.0,
        avg_weight_per_piece_g=100.0
    )
    
    grams1 = svc.calculate_grams(2.0, UnitType.PIECE, ing)
    info1 = svc.calculate_nutrition(grams1, ing)
    
    grams2 = svc.calculate_grams(50.0, UnitType.GRAM, ing)
    info2 = svc.calculate_nutrition(grams2, ing)
    
    total_calories = info1.calories + info2.calories
    total_protein = info1.protein + info2.protein
    total_fat = info1.fat + info2.fat
    total_carbs = info1.carbs + info2.carbs
    
    # 250g total weight
    # 20 calories per 100g -> 50 calories total
    assert total_calories == 50.0 
    assert total_protein == 2.5
    assert total_fat == 0.5
    assert total_carbs == 10.0
