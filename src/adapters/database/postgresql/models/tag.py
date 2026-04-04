from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class TagModel(Base):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=True)
    type = Column(String, nullable=False)  # e.g., "Cuisine", "Diet", "Meal"

class RecipeTagModel(Base):
    __tablename__ = "recipe_tags"

    recipe_id = Column(String, ForeignKey("recipes.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)
