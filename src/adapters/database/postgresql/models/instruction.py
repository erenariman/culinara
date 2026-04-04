from sqlalchemy import Column, String, Integer, Text, ForeignKey
from .base import Base

class InstructionStepModel(Base):
    __tablename__ = "instruction_steps"

    id = Column(String, primary_key=True, index=True)
    recipe_id = Column(String, ForeignKey("recipes.id"), index=True, nullable=False)
    step_number = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    timer_seconds = Column(Integer, nullable=True) # For UI timers
