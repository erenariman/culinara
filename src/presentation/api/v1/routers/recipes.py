from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
import math
from src.presentation.api import deps
from src.presentation.api.deps import get_current_user_id, get_optional_user_id, get_admin_user_id
from src.presentation.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse, InstructionAdd, IngredientAdd
from src.application.usecases.recipe_usecase import RecipeUseCase, CreateRecipeCommand, CreateRecipeItemCommand, UpdateRecipeCommand
from src.presentation.schemas.response import ApiResponse, PaginatedResponse
from src.application.ports.repositories.recipe_repository import RecipeFilterParams
from src.domain.exceptions import EntityNotFoundError

router = APIRouter()

@router.get("", response_model=PaginatedResponse[List[RecipeResponse]])
async def list_recipes(
    status_filter: Optional[str] = None,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Recipe category"),
    difficulty: Optional[str] = Query(None, description="Recipe difficulty"),
    dietary_preference: Optional[str] = Query(None, description="Dietary preference or diet type"),
    max_prep_time: Optional[int] = Query(None, description="Maximum preparation time in minutes"),
    search: Optional[str] = Query(None, alias="q", description="Search in title or description"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field (created_at, rating, prep_time)"),
    order: Optional[str] = Query("desc", description="Sort order (asc, desc)"),
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    filters = RecipeFilterParams(
        page=page,
        limit=limit,
        category=category,
        difficulty=difficulty,
        dietary_preference=dietary_preference,
        max_prep_time=max_prep_time,
        search=search,
        sort_by=sort_by,
        order=order
    )
    
    recipes, total_count = await usecase.search_recipes(filters)
    
    if status_filter:
        recipes = [r for r in recipes if r.status.value == status_filter]
        total_count = len(recipes)
        
    total_pages = math.ceil(total_count / limit) if limit > 0 else 0

    return PaginatedResponse(
        data=recipes,
        total_records=total_count,
        total_pages=total_pages,
        current_page=page,
        limit=limit
    )

@router.get("/{recipe_id}", response_model=ApiResponse[RecipeResponse])
async def get_recipe(
    recipe_id: str,
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    recipe = await usecase.get_recipe(recipe_id)
    if not recipe:
        raise EntityNotFoundError("Recipe not found")
    return ApiResponse(data=recipe)

@router.post("", response_model=ApiResponse[RecipeResponse], status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_in: RecipeCreate,
    author_id: str = Depends(get_current_user_id),
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    # Map Pydantic items to Command items
    card_items = [
        CreateRecipeItemCommand(
            ingredient_name=item.ingredient_name,
            amount=item.amount,
            unit=item.unit
        ) for item in recipe_in.items
    ]

    # Map instructions
    instructions_data = []
    for i in recipe_in.instructions:
        if isinstance(i, str):
            instructions_data.append(i)
        else:
            instructions_data.append(i.model_dump())

    command = CreateRecipeCommand(
        title=recipe_in.title,
        description=recipe_in.description,
        instructions=instructions_data,
        items=card_items,
        author_id=author_id,
        image_url=recipe_in.image_url,
        category=recipe_in.category,
        diet_type=recipe_in.diet_type,
        difficulty=recipe_in.difficulty,
        prep_time_minutes=recipe_in.prep_time_minutes,
        cook_time_minutes=recipe_in.cook_time_minutes,
        servings=recipe_in.servings,
        video_url=recipe_in.video_url
    )

    return ApiResponse(data=await usecase.create_recipe(command))

@router.patch("/{recipe_id}", response_model=ApiResponse[RecipeResponse])
@router.put("/{recipe_id}", response_model=ApiResponse[RecipeResponse])
async def update_recipe(
    recipe_id: str,
    recipe_in: RecipeUpdate,
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    # Map items if present
    update_items = None
    if recipe_in.items is not None:
        update_items = [
            CreateRecipeItemCommand(
                ingredient_name=item.ingredient_name,
                amount=item.amount,
                unit=item.unit
            ) for item in recipe_in.items
        ]

    # Map instructions if present
    instructions_data = None
    if recipe_in.instructions is not None:
        instructions_data = []
        for i in recipe_in.instructions:
            if isinstance(i, str):
                instructions_data.append(i)
            else:
                instructions_data.append(i.model_dump())

    command = UpdateRecipeCommand(
        title=recipe_in.title,
        description=recipe_in.description,
        instructions=instructions_data,
        items=update_items,
        image_url=recipe_in.image_url,
        status=recipe_in.status.value if recipe_in.status else None,
        category=recipe_in.category,
        diet_type=recipe_in.diet_type,
        difficulty=recipe_in.difficulty,
        prep_time_minutes=recipe_in.prep_time_minutes,
        cook_time_minutes=recipe_in.cook_time_minutes,
        servings=recipe_in.servings,
        video_url=recipe_in.video_url
    )

    updated = await usecase.update_recipe(recipe_id, command)
    if not updated:
        raise EntityNotFoundError("Recipe not found")
    return ApiResponse(data=updated)

@router.post("/{recipe_id}/instructions", response_model=ApiResponse[RecipeResponse])
async def add_instruction(
    recipe_id: str,
    step_in: InstructionAdd,
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    return ApiResponse(data=await usecase.add_instruction(recipe_id, step_in.text, step_in.step_number))

@router.post("/{recipe_id}/ingredients", response_model=ApiResponse[RecipeResponse])
async def add_ingredient(
    recipe_id: str,
    ing_in: IngredientAdd,
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    return ApiResponse(data=await usecase.add_ingredient(
        recipe_id, ing_in.ingredient_id, ing_in.amount, ing_in.unit
    ))

@router.post("/{recipe_id}/publish", response_model=ApiResponse[RecipeResponse])
async def publish(
    recipe_id: str,
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    return ApiResponse(data=await usecase.publish_recipe(recipe_id))

@router.patch("/admin/{recipe_id}/status", response_model=ApiResponse[RecipeResponse])
async def update_recipe_status(
    recipe_id: str,
    status: str,
    admin_id: str = Depends(get_admin_user_id),
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    updated_recipe = await usecase.update_status(recipe_id, status)
    if not updated_recipe:
         raise EntityNotFoundError("Recipe not found")
    return ApiResponse(data=updated_recipe)

@router.delete("/{recipe_id}", response_model=ApiResponse[None])
async def delete_recipe(
    recipe_id: str,
    usecase: RecipeUseCase = Depends(deps.get_recipe_usecase)
):
    success = await usecase.delete_recipe(recipe_id)
    if not success:
        raise EntityNotFoundError("Recipe not found")
    return ApiResponse(success=True)
