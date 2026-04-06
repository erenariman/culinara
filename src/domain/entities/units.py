from enum import Enum

class UnitType(str, Enum):
    GRAM = "gram"
    ML = "ml"
    PIECE = "piece"
    TBS = "tablespoon"
    TSP = "teaspoon"
    GLASS_WATER = "glass_water"
    GLASS_TEA = "glass_tea"
    KILOGRAM = "kg"
    LITER = "l"
    PACKET = "packet"
    BUNCH = "bunch"
    CLOVE = "clove"
    PINCH = "pinch"
