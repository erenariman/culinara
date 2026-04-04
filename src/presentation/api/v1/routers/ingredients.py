from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.presentation.api import deps
from src.presentation.schemas.ingredient_schema import IngredientCreate, IngredientResponse, IngredientUpdate
from src.application.usecases.ingredient_usecase import IngredientUseCase, CreateIngredientCommand, UpdateIngredientCommand
from src.presentation.schemas.response import ApiResponse
from src.domain.exceptions import EntityNotFoundError

router = APIRouter()

@router.post("/", response_model=ApiResponse[IngredientResponse], status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    ingredient_in: IngredientCreate,
    usecase: IngredientUseCase = Depends(deps.get_ingredient_usecase)
):
    command = CreateIngredientCommand(
        name=ingredient_in.name,
        calories_per_100g=ingredient_in.calories_per_100g,
        protein_per_100g=ingredient_in.protein_per_100g,
        fat_per_100g=ingredient_in.fat_per_100g,
        carbs_per_100g=ingredient_in.carbs_per_100g,
        density_g_ml=ingredient_in.density_g_ml,
        avg_weight_per_piece_g=ingredient_in.avg_weight_per_piece_g
    )
    return ApiResponse(data=await usecase.create_ingredient(command))

@router.get("/", response_model=ApiResponse[List[IngredientResponse]])
async def list_ingredients(
    usecase: IngredientUseCase = Depends(deps.get_ingredient_usecase)
):
    ingredients = await usecase.list_ingredients()
    return ApiResponse(data=ingredients, total=len(ingredients))

@router.get("/{id}", response_model=ApiResponse[IngredientResponse])
async def get_ingredient(
    id: str,
    usecase: IngredientUseCase = Depends(deps.get_ingredient_usecase)
):
    ingredient = await usecase.get_ingredient(id)
    if not ingredient:
        raise EntityNotFoundError("Ingredient not found")
    return ApiResponse(data=ingredient)

@router.patch("/{id}", response_model=ApiResponse[IngredientResponse])
async def update_ingredient(
    id: str,
    ingredient_in: IngredientUpdate,
    usecase: IngredientUseCase = Depends(deps.get_ingredient_usecase)
):
    command = UpdateIngredientCommand(
        name=ingredient_in.name,
        calories_per_100g=ingredient_in.calories_per_100g,
        protein_per_100g=ingredient_in.protein_per_100g,
        fat_per_100g=ingredient_in.fat_per_100g,
        carbs_per_100g=ingredient_in.carbs_per_100g,
        density_g_ml=ingredient_in.density_g_ml,
        avg_weight_per_piece_g=ingredient_in.avg_weight_per_piece_g
    )
    
    updated_ingredient = await usecase.update_ingredient(id, command)
    if not updated_ingredient:
        raise EntityNotFoundError("Ingredient not found")
        
    return ApiResponse(data=updated_ingredient)

@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_ingredient(
    id: str,
    usecase: IngredientUseCase = Depends(deps.get_ingredient_usecase)
):
    success = await usecase.delete_ingredient(id)
    if not success:
        raise EntityNotFoundError("Ingredient not found")
    return ApiResponse(success=True)
