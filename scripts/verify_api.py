from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
import asyncio

from main import app
from src.presentation.api import deps
from src.domain.entities.ingredient import Ingredient
from src.domain.entities.recipe import Recipe

# Mock Use Cases
mock_ingredient_usecase = AsyncMock()
mock_recipe_usecase = AsyncMock()

# Note: In main.py, we already have overrides for REPOS. 
# But for testing integration, we want to mock USECASES to isolate the API layer testing.
# The routers depend on `get_ingredient_usecase` and `get_recipe_usecase`.
# Even though main.py wires the repos, we can still override the usecases directly here for unit testing routers.

app.dependency_overrides[deps.get_ingredient_usecase] = lambda: mock_ingredient_usecase
app.dependency_overrides[deps.get_recipe_usecase] = lambda: mock_recipe_usecase

client = TestClient(app)

def verify_ingredient_api():
    print("Verifying POST /api/v1/ingredients...")
    mock_ingredient_usecase.create_ingredient.return_value = Ingredient(
        id="123", name="Tomato", calories_per_100g=18, protein_per_100g=0.9,
        fat_per_100g=0.2, carbs_per_100g=3.9, density_g_ml=1.0
    )
    
    response = client.post("/api/v1/ingredients/", json={
        "name": "Tomato",
        "calories_per_100g": 18,
        "protein_per_100g": 0.9,
        "fat_per_100g": 0.2,
        "carbs_per_100g": 3.9,
        "density_g_ml": 1.0
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Tomato"
    print("Ingredient API verified.")

def verify_recipe_api():
    print("Verifying POST /api/v1/recipes...")
    mock_recipe_usecase.create_recipe.return_value = Recipe(
        id="456", title="Salad", description="Healthy", instructions="Cut and mix",
        items=[], total_calories=50, total_cost=0
    )
    
    response = client.post("/api/v1/recipes/", json={
        "title": "Salad",
        "description": "Healthy",
        "instructions": "Cut and mix",
        "items": []
    })
        
    assert response.status_code == 201
    assert response.json()["title"] == "Salad"
    print("Recipe API verified.")

if __name__ == "__main__":
    verify_ingredient_api()
    verify_recipe_api()
    print("All API endpoints verified!")
