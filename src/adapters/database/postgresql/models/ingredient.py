from sqlalchemy import Column, String, Float, Text, DateTime, func
from .base import Base

class IngredientModel(Base):
    __tablename__ = "ingredients"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=True)
    calories_per_100g = Column(Float, nullable=False)
    protein_per_100g = Column(Float, nullable=False)
    fat_per_100g = Column(Float, nullable=False)
    carbs_per_100g = Column(Float, nullable=False)
    density_g_ml = Column(Float, nullable=False)
    avg_weight_per_piece_g = Column(Float, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
