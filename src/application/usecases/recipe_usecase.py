import uuid
from slugify import slugify
from dataclasses import dataclass
from typing import List, Optional, Union, Dict

from src.domain.entities.recipe import Recipe, RecipeItem, RecipeInstruction, RecipeStatus
from src.domain.entities.ingredient import Ingredient
from src.domain.entities.units import UnitType
from src.application.ports.repositories.recipe_repository import RecipeRepositoryPort
from src.application.ports.repositories.ingredient_repository import IngredientRepositoryPort
from src.domain.exceptions import EntityNotFoundError, ValidationError, AlreadyExistsError

@dataclass
class CreateRecipeItemCommand:
    ingredient_name: str
    amount: float
    unit: str

@dataclass
class CreateRecipeCommand:
    title: str
    description: str
    instructions: List[Union[str, dict]]
    items: List[CreateRecipeItemCommand]
    author_id: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    diet_type: Optional[str] = None
    difficulty: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    video_url: Optional[str] = None

@dataclass
class UpdateRecipeCommand:
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[List[Union[str, dict]]] = None
    items: Optional[List[CreateRecipeItemCommand]] = None
    image_url: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    diet_type: Optional[str] = None
    difficulty: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    video_url: Optional[str] = None

from src.domain.services.nutrition_calculator import NutritionCalculatorService, NutritionInfo

class RecipeUseCase:
    def __init__(self, recipe_repo: RecipeRepositoryPort, ingredient_repo: IngredientRepositoryPort, nutrition_service: NutritionCalculatorService = None):
        self.recipe_repo = recipe_repo
        self.ingredient_repo = ingredient_repo
        self.nutrition_service = nutrition_service or NutritionCalculatorService()

    def _parse_instructions(self, instructions: List[Union[str, dict]]) -> List[RecipeInstruction]:
        """Convert raw instruction data (str or dict) into RecipeInstruction objects."""
        result = []
        for index, item in enumerate(instructions):
            if isinstance(item, str):
                text = item
                step_num = index + 1
            else:
                text = item.get("text", "")
                step_num = item.get("step_number", index + 1) or (index + 1)
            result.append(RecipeInstruction(
                id=str(uuid.uuid4()),
                step_number=step_num,
                text=text
            ))
        return result

    def _calculate_nutrition(self, items: List[RecipeItem]) -> NutritionInfo:
        total_nutrition = NutritionInfo()
        for item in items:
            try:
                grams = self.nutrition_service.calculate_grams(item.amount, item.unit, item.ingredient)
                info = self.nutrition_service.calculate_nutrition(grams, item.ingredient)
                total_nutrition.calories += info.calories
                total_nutrition.protein += info.protein
                total_nutrition.carbs += info.carbs
                total_nutrition.fat += info.fat
            except ValueError:
                continue
                
        total_nutrition.calories = round(total_nutrition.calories, 2)
        total_nutrition.protein = round(total_nutrition.protein, 2)
        total_nutrition.carbs = round(total_nutrition.carbs, 2)
        total_nutrition.fat = round(total_nutrition.fat, 2)
        return total_nutrition

    async def _resolve_items(self, items_cmd: List[CreateRecipeItemCommand]) -> List[RecipeItem]:
        merged_items = {}
        for item_cmd in items_cmd:
            ingredient = await self.ingredient_repo.get_by_name(item_cmd.ingredient_name)
            if not ingredient:
                raise EntityNotFoundError(f"Ingredient '{item_cmd.ingredient_name}' not found.")
            
            try:
                unit = UnitType(item_cmd.unit)
            except ValueError:
                 raise ValidationError(f"Invalid unit: {item_cmd.unit}")

            if unit == UnitType.PIECE and not ingredient.avg_weight_per_piece_g:
                raise ValidationError(f"Ingredient '{ingredient.name}' cannot be used in 'piece' unit because average weight is not defined.")

            key = ingredient.id
            if key in merged_items:
                existing_item = merged_items[key]
                if existing_item.unit != unit:
                    raise ValidationError(f"Ingredient '{ingredient.name}' is added multiple times with different units. Please combine them.")
                existing_item.amount += item_cmd.amount
            else:
                recipe_item = RecipeItem(
                    ingredient=ingredient,
                    amount=item_cmd.amount,
                    unit=unit
                )
                merged_items[key] = recipe_item
        return list(merged_items.values())

    async def create_recipe(self, command: CreateRecipeCommand) -> Recipe:
        recipe_items = await self._resolve_items(command.items)
        
        instruction_objs = self._parse_instructions(command.instructions)

        nutrition = self._calculate_nutrition(recipe_items)
        
        recipe = Recipe(
            id=str(uuid.uuid4()),
            title=command.title,
            slug=f"{slugify(command.title)}-{uuid.uuid4().hex[:6]}",
            description=command.description or "",
            instructions=instruction_objs,
            items=recipe_items,
            total_calories=nutrition.calories,
            total_protein=nutrition.protein,
            total_carbs=nutrition.carbs,
            total_fat=nutrition.fat,
            total_cost=0.0,
            image_url=command.image_url or "",
            author_id=command.author_id,
            category=command.category,
            diet_type=command.diet_type,
            difficulty=command.difficulty,
            prep_time_minutes=command.prep_time_minutes,
            cook_time_minutes=command.cook_time_minutes,
            servings=command.servings,
            video_url=command.video_url
        )
        
        return await self.recipe_repo.save(recipe)

    async def update_recipe(self, id: str, command: UpdateRecipeCommand) -> Optional[Recipe]:
        recipe = await self.recipe_repo.get_by_id(id)
        if not recipe:
            return None

        if command.title is not None:
            recipe.title = command.title
        if command.description is not None:
            recipe.description = command.description
        if command.image_url is not None:
            recipe.image_url = command.image_url
            
        if command.category is not None:
            recipe.category = command.category
        if command.diet_type is not None:
            recipe.diet_type = command.diet_type
        if command.difficulty is not None:
            recipe.difficulty = command.difficulty
        if command.prep_time_minutes is not None:
            recipe.prep_time_minutes = command.prep_time_minutes
        if command.cook_time_minutes is not None:
            recipe.cook_time_minutes = command.cook_time_minutes
        if command.servings is not None:
            recipe.servings = command.servings
        if command.video_url is not None:
            recipe.video_url = command.video_url
        
        if command.status is not None:
             from src.domain.entities.recipe import RecipeStatus
             try:
                 recipe.status = RecipeStatus(command.status)
             except ValueError:
                 raise ValidationError(f"Invalid status: {command.status}")

        if command.instructions is not None:
            instruction_objs = self._parse_instructions(command.instructions)
            recipe.instructions = instruction_objs

        if command.items is not None:
            recipe.items = await self._resolve_items(command.items)
            nutrition = self._calculate_nutrition(recipe.items)
            recipe.total_calories = nutrition.calories
            recipe.total_protein = nutrition.protein
            recipe.total_carbs = nutrition.carbs
            recipe.total_fat = nutrition.fat

        return await self.recipe_repo.save(recipe)

    async def get_recipe(self, id: str) -> Optional[Recipe]:
        return await self.recipe_repo.get_by_id(id)

    async def update_status(self, recipe_id: str, status: str) -> Optional[Recipe]:
        command = UpdateRecipeCommand(status=status)
        return await self.update_recipe(recipe_id, command)

    async def delete_recipe(self, id: str) -> bool:
        return await self.recipe_repo.delete(id)

    async def list_recipes(self) -> List[Recipe]:
        return await self.recipe_repo.list_all()

    async def search_recipes(self, filters: "src.application.ports.repositories.recipe_repository.RecipeFilterParams") -> "Tuple[List[Recipe], int]":
        return await self.recipe_repo.search_recipes(filters)

    async def add_instruction(self, recipe_id: str, text: str, step_number: int) -> Recipe:
        recipe = await self.recipe_repo.get_by_id(recipe_id)
        if not recipe:
            raise EntityNotFoundError("Recipe not found")
        
        # Add instruction
        instruction = RecipeInstruction(
            id=str(uuid.uuid4()),
            step_number=step_number,
            text=text
        )
        recipe.instructions.append(instruction)
        # Re-sort/re-number might be needed, but for now just append
        # Ideally, we should handle step numbers carefully
        
        return await self.recipe_repo.save(recipe)

    async def add_ingredient(self, recipe_id: str, ingredient_id: str, amount: float, unit: str) -> Recipe:
         recipe = await self.recipe_repo.get_by_id(recipe_id)
         if not recipe:
             raise EntityNotFoundError("Recipe not found")

         ingredient = await self.ingredient_repo.get_by_id(ingredient_id)
         if not ingredient:
             raise EntityNotFoundError("Ingredient not found")
         
         try:
             unit_enum = UnitType(unit)
         except ValueError:
             raise ValidationError(f"Invalid unit: {unit}")
         
         if unit_enum == UnitType.PIECE and not ingredient.avg_weight_per_piece_g:
             raise ValidationError(f"Ingredient '{ingredient.name}' cannot be used in 'piece' unit because average weight is not defined.")
         
         # Check if exists and update, or add new
         # Simplified: just add for now or merge
         # Reuse logic from _resolve_items would be better but it takes Command objects
         
         # Let's create a temporary command item structure to reuse _resolve_items logic if possible, 
         # but _resolve_items does bulk.
         
         # Manual Add/Merge
         existing = next((i for i in recipe.items if i.ingredient.id == ingredient.id), None)
         if existing:
             if existing.unit != unit_enum:
                  raise AlreadyExistsError(f"Ingredient is already added with unit {existing.unit}")
             existing.amount += amount
         else:
             recipe.items.append(RecipeItem(
                 ingredient=ingredient,
                 amount=amount,
                 unit=unit_enum
             ))

         # Always recalculate nutrition after any change
         nutrition = self._calculate_nutrition(recipe.items)
         recipe.total_calories = nutrition.calories
         recipe.total_protein = nutrition.protein
         recipe.total_carbs = nutrition.carbs
         recipe.total_fat = nutrition.fat

         return await self.recipe_repo.save(recipe)

    async def publish_recipe(self, recipe_id: str) -> Recipe:
        return await self.update_status(recipe_id, RecipeStatus.PUBLISHED.value)
