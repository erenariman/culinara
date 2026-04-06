from sqlalchemy import Column, String, Float, Text, ForeignKey, Integer, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from src.domain.entities.recipe import RecipeStatus, DifficultyLevel, RecipeCategory

class RecipeIngredientModel(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(String, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(String, ForeignKey("ingredients.id"), primary_key=True)
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    display_text = Column(String, nullable=True)
    is_optional = Column(Boolean, default=False)

    ingredient = relationship("IngredientModel")


class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True, nullable=True) # SEO Friendly
    status = Column(SAEnum(RecipeStatus), default=RecipeStatus.DRAFT)
    
    description = Column(Text, nullable=False)
    instructions = Column(Text, default="") # Simple summary
    image_url = Column(String, default="")
    video_url = Column(String, nullable=True)
    
    # Economics & Nutrition (Cached)
    total_calories = Column(Float, default=0.0)
    total_protein = Column(Float, default=0.0)
    total_carbs = Column(Float, default=0.0)
    total_fat = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    # Metadata
    servings = Column(Integer, nullable=True)
    prep_time_minutes = Column(Integer, nullable=True)
    cook_time_minutes = Column(Integer, nullable=True)
    difficulty = Column(SAEnum(DifficultyLevel), nullable=True)
    category = Column(SAEnum(RecipeCategory), nullable=True)
    diet_type = Column(String, nullable=True) # Vegan, Vegetarian
    view_count = Column(Integer, default=0)
    
    author_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True) # Soft Delete

    ingredients = relationship("RecipeIngredientModel", cascade="all, delete-orphan")
    steps = relationship("InstructionStepModel", cascade="all, delete-orphan")
    tags = relationship("TagModel", secondary="recipe_tags")
    equipments = relationship("EquipmentModel", secondary="recipe_equipments")
    
    # Social relationships with cascade delete
    reviews = relationship("ReviewModel", cascade="all, delete-orphan")
    comments = relationship("CommentModel", cascade="all, delete-orphan")
    likes = relationship("RecipeLikeModel", cascade="all, delete-orphan")
    
    author = relationship("UserModel", foreign_keys=[author_id], lazy="noload")
