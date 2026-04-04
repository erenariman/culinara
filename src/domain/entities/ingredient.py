from dataclasses import dataclass
from typing import Optional

@dataclass
class Ingredient:
    """
    Represents a raw food ingredient (e.g., 'Tomato', 'Flour').

    Attributes:
        density_g_ml: Critical for converting volume to mass.
                Water = 1.0, Flour = 0.55, Oil = 0.92
    """
    id: str
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float
    density_g_ml: float
    avg_weight_per_piece_g: Optional[float] = None
    slug: str = ""