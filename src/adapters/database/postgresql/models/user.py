from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from .base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True) # Nullable for OAuth
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True) # Soft Delete

    # Relations
    profile = relationship("UserProfileModel", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Other relationships will be added as we implement linked models to avoid circular import issues
    # kept strictly in those model files where possible using string references
