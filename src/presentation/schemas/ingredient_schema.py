from typing import Optional
from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float
    density_g_ml: float
    avg_weight_per_piece_g: Optional[float] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    calories_per_100g: Optional[float] = None
    protein_per_100g: Optional[float] = None
    fat_per_100g: Optional[float] = None
    carbs_per_100g: Optional[float] = None
    density_g_ml: Optional[float] = None
    avg_weight_per_piece_g: Optional[float] = None

class IngredientResponse(IngredientBase):
    id: str
    slug: Optional[str] = None

    class Config:
        from_attributes = True
