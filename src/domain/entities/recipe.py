from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

from .ingredient import Ingredient
from .units import UnitType

@dataclass
class RecipeItem:
    """
    Represents a specific amount of an ingredient used in a recipe.
    Example: '2 cups of Flour'
    """
    ingredient: Ingredient
    amount: float
    unit: UnitType
    # Calculated values (not stored, but computed)
    calculated_grams: float = 0.0
    calculated_calories: float = 0.0
    
    @property
    def ingredient_name(self) -> str:
        return self.ingredient.name

@dataclass
class RecipeTag:
    id: str
    name: str
    type: str
    slug: str = ""

@dataclass
class RecipeInstruction:
    id: str
    step_number: int
    text: str
    image_url: Optional[str] = None
    timer_seconds: Optional[int] = None

class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class RecipeCategory(str, Enum):
    BREAKFAST = "BREAKFAST"
    MAIN_COURSE = "MAIN_COURSE"
    DESSERT = "DESSERT"
    APPETIZER = "APPETIZER"
    SALAD = "SALAD"
    SOUP = "SOUP"

class RecipeStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    MODERATION = "MODERATION"
    REJECTED = "REJECTED"

@dataclass
class Recipe:
    """
    Represents a full recipe with instructions and nutritional info.
    """
    id: str
    title: str
    description: str
    items: List[RecipeItem] = field(default_factory=list)
    instructions: List[RecipeInstruction] = field(default_factory=list)
    tags: List[RecipeTag] = field(default_factory=list)
    
    # Nutrition & Stats
    total_calories: float = 0.0
    total_protein: float = 0.0
    total_carbs: float = 0.0
    total_fat: float = 0.0
    total_cost: float = 0.0
    
    # Metadata
    slug: str = ""
    status: RecipeStatus = RecipeStatus.DRAFT
    view_count: int = 0
    difficulty: Optional[DifficultyLevel] = None
    category: Optional[RecipeCategory] = None
    diet_type: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    video_url: Optional[str] = None
    image_url: str = ""
    
    # Auditing
    author_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    # Transient Fields (Aggregated from relations, not primarily stored in recipes table)
    author_name: Optional[str] = None
    average_rating: Optional[float] = None
    review_count: int = 0