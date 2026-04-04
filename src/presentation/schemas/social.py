from pydantic import BaseModel
from typing import List, Optional

class CommentCreate(BaseModel):
    recipe_id: str
class CommentCreate(BaseModel):
    recipe_id: str
    text: str

class CommentUpdate(BaseModel):
    text: str

class CommentResponse(BaseModel):
    id: str
    user_id: str
    text: str

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    rating: int  # 1-5
    text: Optional[str] = None
    image_url: Optional[str] = None

class ReviewResponse(BaseModel):
    id: str
    user_id: str
    recipe_id: str
    rating: int
    text: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
