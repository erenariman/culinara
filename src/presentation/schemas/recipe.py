from pydantic import BaseModel
from typing import Optional, List, Union
from src.domain.entities.recipe import RecipeStatus

class RecipeCreateItem(BaseModel):
    ingredient_name: str
    amount: float
    unit: str

class InstructionCreate(BaseModel):
    step_number: Optional[int] = None
    text: str

class RecipeCreate(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    category: str
    diet_type: str
    difficulty: str
    prep_time_minutes: int
    cook_time_minutes: int
    servings: int
    video_url: Optional[str] = None
    items: List[RecipeCreateItem] = []
    instructions: List[Union[str, InstructionCreate]] = []

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    diet_type: Optional[str] = None
    difficulty: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    video_url: Optional[str] = None
    items: Optional[List[RecipeCreateItem]] = None
    instructions: Optional[List[Union[str, InstructionCreate]]] = None
    status: Optional[RecipeStatus] = None

class InstructionAdd(BaseModel):
    text: str
    step_number: int

class IngredientAdd(BaseModel):
    ingredient_id: str
    amount: float
    unit: str

class IngredientResponse(BaseModel):
    id: str
    name: str
    slug: Optional[str] = None

class RecipeItemResponse(BaseModel):
    ingredient_name: str
    amount: float
    unit: str
    slug: Optional[str] = None

    class Config:
        from_attributes = True

class InstructionResponse(BaseModel):
    step_number: int
    text: str

    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    id: str
    name: str
    slug: Optional[str] = None
    type: str

    class Config:
        from_attributes = True

class RecipeResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: RecipeStatus
    slug: Optional[str]
    author_id: Optional[str]
    
    # Metadata
    category: Optional[str] = None
    diet_type: Optional[str] = None
    difficulty: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    view_count: int = 0
    
    # Macros
    total_calories: float = 0.0
    total_protein: float = 0.0
    total_carbs: float = 0.0
    total_fat: float = 0.0
    
    # Social (to be populated later)
    average_rating: Optional[float] = None
    review_count: int = 0
    author_name: Optional[str] = None
    
    instructions: List[InstructionResponse] = []
    items: List[RecipeItemResponse] = []
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True
