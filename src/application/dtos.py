from dataclasses import dataclass
from typing import List

@dataclass
class DraftItemDTO:
    ingredient_name: str
    amount: float
    unit: str

@dataclass
class AIRecipeDraft:
    """
    Raw data structure returned by the AI Service.
    """
    title: str
    description: str
    instructions: str
    items: List[DraftItemDTO]
