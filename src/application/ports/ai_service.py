from abc import ABC, abstractmethod
from typing import List
from src.application.dtos import AIRecipeDraft

class AIServicePort(ABC):
    """
    Port for AI interaction (Gemini/OpenAI).
    """
    @abstractmethod
    async def generate_draft_recipe(self, ingredients_list: List[str]) -> AIRecipeDraft:
        """
        Sends the list of available ingredients to AI and gets a structured draft.
        Does NOT calculate calories; just returns the structure (items, amounts).
        """
        pass