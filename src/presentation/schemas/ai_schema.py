from pydantic import BaseModel
from typing import List

# Bu bir DTO'dur. Sadece veri taşır, iş yapmaz.
class DraftItemSchema(BaseModel):
    ingredient_name: str
    amount: float
    unit: str

class AIRecipeDraftSchema(BaseModel):
    title: str
    description: str
    instructions: str
    items: List[DraftItemSchema]