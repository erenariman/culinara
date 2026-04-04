from sqlalchemy import Column, String, ForeignKey
from .base import Base

class EquipmentModel(Base):
    __tablename__ = "equipments"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    link = Column(String, nullable=True) # Affiliate link potentially

class RecipeEquipmentModel(Base):
    __tablename__ = "recipe_equipments"

    recipe_id = Column(String, ForeignKey("recipes.id"), primary_key=True)
    equipment_id = Column(String, ForeignKey("equipments.id"), primary_key=True)
