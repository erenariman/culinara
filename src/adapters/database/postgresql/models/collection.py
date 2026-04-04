from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Enum as SAEnum, func, Integer, Date
from sqlalchemy.orm import relationship
import enum

from .base import Base

class MealType(str, enum.Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"

class CollectionModel(Base):
    __tablename__ = "collections"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=True)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    cover_image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True) # Soft Delete
    
    # Simple Many-to-Many link table defined explicitly or via association object
    recipes = relationship("RecipeModel", secondary="collection_recipes")

class CollectionRecipeModel(Base):
    __tablename__ = "collection_recipes"

    collection_id = Column(String, ForeignKey("collections.id"), primary_key=True)
    recipe_id = Column(String, ForeignKey("recipes.id"), primary_key=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

class MealPlanModel(Base):
    __tablename__ = "meal_plans"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    meal_type = Column(SAEnum(MealType), nullable=False)
    recipe_id = Column(String, ForeignKey("recipes.id"), nullable=False)
    
    servings_planned = Column(Integer, default=1)
    is_cooked = Column(Boolean, default=False)
