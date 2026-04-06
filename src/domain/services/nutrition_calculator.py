from src.domain.entities.ingredient import Ingredient
from src.domain.entities.units import UnitType
from dataclasses import dataclass

@dataclass
class NutritionInfo:
    calories: float = 0.0
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0

class NutritionCalculatorService:
    """
    Domain service responsible for converting kitchen units to grams
    and calculating nutritional values based on density.
    """

    # Volume standards in Milliliters (ml)
    UNIT_TO_ML = {
        UnitType.ML: 1.0,
        UnitType.TSP: 5.0,
        UnitType.TBS: 15.0,
        UnitType.LITER: 1000.0,
        UnitType.GLASS_TEA: 100.0,
        UnitType.GLASS_WATER: 200.0,
        UnitType.PINCH: 1.0, # ~1g/ml for a standard pinch
    }

    def calculate_grams(self, amount: float, unit: UnitType, ingredient: Ingredient) -> float:
        """
        Converts input amount/unit to grams using the ingredient's density.
        Formula: Mass(g) = Volume(ml) * Density(g/ml)
        """
        if unit == UnitType.GRAM:
            return amount

        if unit == UnitType.KILOGRAM:
            return amount * 1000.0

        # Units that rely on average weight (Piece, Packet, Bunch, Clove)
        if unit in [UnitType.PIECE, UnitType.PACKET, UnitType.BUNCH, UnitType.CLOVE]:
            weight = ingredient.avg_weight_per_piece_g
            if weight is None:
                return 0.0
            return amount * weight

        # Volume-based calculation
        if unit in self.UNIT_TO_ML:
            volume_ml = amount * self.UNIT_TO_ML[unit]
            density = ingredient.density_g_ml or 1.0
            return volume_ml * density
            
        return 0.0

    def calculate_nutrition(self, grams: float, ingredient: Ingredient) -> NutritionInfo:
        """
        Calculates full nutritional breakdown for a given gram amount.
        """
        factor = grams / 100.0
        return NutritionInfo(
            calories=factor * ingredient.calories_per_100g,
            protein=factor * (ingredient.protein_per_100g or 0.0),
            carbs=factor * (ingredient.carbs_per_100g or 0.0),
            fat=factor * (ingredient.fat_per_100g or 0.0)
        )