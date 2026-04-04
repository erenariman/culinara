import pytest
from typing import Optional, List, Tuple
from src.application.usecases.recipe_usecase import RecipeUseCase, CreateRecipeCommand, CreateRecipeItemCommand
from src.domain.entities.recipe import Recipe, RecipeStatus
from src.domain.entities.ingredient import Ingredient
from src.application.ports.repositories.recipe_repository import RecipeRepositoryPort, RecipeFilterParams
from src.application.ports.repositories.ingredient_repository import IngredientRepositoryPort

class FakeRecipeRepository(RecipeRepositoryPort):
    def __init__(self):
        self.db = {}

    async def save(self, recipe: Recipe) -> Recipe:
        self.db[recipe.id] = recipe
        return recipe

    async def get_by_id(self, id: str) -> Optional[Recipe]:
        return self.db.get(id)

    async def list_all(self) -> List[Recipe]:
        return list(self.db.values())

    async def search_recipes(self, filters: RecipeFilterParams) -> Tuple[List[Recipe], int]:
        values = list(self.db.values())
        return values, len(values)

    async def delete(self, id: str) -> bool:
        if id in self.db:
            del self.db[id]
            return True
        return False

class FakeIngredientRepository(IngredientRepositoryPort):
    def __init__(self):
        self.db = {
            "Tomato": Ingredient(
                id="ing-1", name="Tomato", 
                calories_per_100g=20, protein_per_100g=1, 
                fat_per_100g=0, carbs_per_100g=4, 
                density_g_ml=1, avg_weight_per_piece_g=100
            )
        }

    async def save(self, ingredient: Ingredient) -> Ingredient:
        self.db[ingredient.name] = ingredient
        return ingredient

    async def get_by_id(self, id: str) -> Optional[Ingredient]:
        for i in self.db.values():
            if i.id == id:
                return i
        return None

    async def get_by_name(self, name: str) -> Optional[Ingredient]:
        return self.db.get(name)

    async def list_all(self) -> List[Ingredient]:
        return list(self.db.values())

    async def delete(self, id: str) -> bool:
        # Dummy delete
        return True


@pytest.fixture
def recipe_uc():
    return RecipeUseCase(
        recipe_repo=FakeRecipeRepository(),
        ingredient_repo=FakeIngredientRepository()
    )


@pytest.mark.asyncio
async def test_create_recipe(recipe_uc: RecipeUseCase):
    cmd = CreateRecipeCommand(
        title="Tomato Soup",
        description="Fresh tomato soup",
        instructions=[
            "Chop tomatoes",
            {"text": "Boil them", "step_number": 2}
        ],
        items=[
            CreateRecipeItemCommand(ingredient_name="Tomato", amount=3, unit="piece")
        ]
    )
    
    recipe = await recipe_uc.create_recipe(cmd)
    
    assert recipe.title == "Tomato Soup"
    assert len(recipe.items) == 1
    assert len(recipe.instructions) == 2
    
    # Check slug generation
    assert recipe.slug.startswith("tomato-soup")
    assert len(recipe.slug) > len("tomato-soup")
    
    # Check parsing output
    assert recipe.instructions[0].step_number == 1
    assert recipe.instructions[1].step_number == 2
    
    # Check if nutrition is calculated (3 pieces * 100g = 300g -> 60 kcal)
    assert getattr(recipe, 'total_calories', recipe.total_calories) == 60.0

@pytest.mark.asyncio
async def test_publish_recipe(recipe_uc: RecipeUseCase):
    # Setup initial recipe
    cmd = CreateRecipeCommand(title="Draft Recipe", description="", instructions=[], items=[])
    recipe = await recipe_uc.create_recipe(cmd)
    assert recipe.status == RecipeStatus.DRAFT
    
    # Act
    published_recipe = await recipe_uc.publish_recipe(recipe.id)
    
    # Assert
    assert published_recipe.status == RecipeStatus.PUBLISHED
