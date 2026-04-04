import pytest
from httpx import AsyncClient
from src.domain.entities.recipe import Recipe, RecipeStatus
import uuid

@pytest.mark.asyncio
async def test_get_recipes_public(client: AsyncClient, mocker):
    mocker.patch(
        "src.application.usecases.recipe_usecase.RecipeUseCase.search_recipes",
        return_value=([], 0) # empty list, total count
    )

    response = await client.get("/api/v1/recipes")
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["total_records"] == 0

@pytest.mark.asyncio
async def test_create_recipe_unauthorized(client: AsyncClient):
    # Missing auth_headers -> gets 401
    response = await client.post(
        "/api/v1/recipes",
        json={
            "title": "My Recipe",
            "description": "Test description",
            "category": "Dinner",
            "diet_type": "None",
            "difficulty": "Easy",
            "prep_time_minutes": 10,
            "cook_time_minutes": 20,
            "servings": 2,
            "instructions": ["Step 1"],
            "items": []
        }
    )
    print("CREATE RECIPE UNAUTH RESPONSE:", response.text)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_create_recipe_success(client: AsyncClient, auth_headers, mocker):
    recipe_obj = Recipe(
        id="recipe123",
        title="My Recipe",
        description="Test description",
        status=RecipeStatus.DRAFT,
        items=[],
        instructions=[]
    )

    mocker.patch(
        "src.application.usecases.recipe_usecase.RecipeUseCase.create_recipe",
        return_value=recipe_obj
    )

    response = await client.post(
        "/api/v1/recipes",
        json={
            "title": "My Recipe",
            "description": "Test description",
            "category": "Dinner",
            "diet_type": "None",
            "difficulty": "Easy",
            "prep_time_minutes": 10,
            "cook_time_minutes": 20,
            "servings": 2,
            "instructions": ["Step 1"],
            "items": []
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["id"] == "recipe123"
    assert data["data"]["title"] == "My Recipe"

@pytest.mark.asyncio
async def test_update_recipe_status_unauthorized(client: AsyncClient, auth_headers):
    # Try admin endpoint with standard user auth_headers -> gets 403
    response = await client.patch(
        "/api/v1/recipes/admin/recipe123/status",
        json={"status": "published"},
        headers=auth_headers
    )
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"

@pytest.mark.asyncio
async def test_update_recipe_status_admin(client: AsyncClient, admin_headers, mocker):
    recipe_obj = Recipe(
        id="recipe123",
        title="Some Recipe",
        description="Admin test description",
        status=RecipeStatus.PUBLISHED,
        items=[],
        instructions=[]
    )

    mocker.patch(
        "src.application.usecases.recipe_usecase.RecipeUseCase.update_status",
        return_value=recipe_obj
    )

    response = await client.patch(
        "/api/v1/recipes/admin/recipe123/status?status=published",
        headers=admin_headers
    )
    
    print("PATCH STATUS RESPONSE:", response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == "recipe123"
    assert data["data"]["status"] == "PUBLISHED"
