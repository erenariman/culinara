from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.presentation.api import deps
from src.presentation.api.deps import get_social_usecase, get_current_user_id, get_admin_user_id
from src.application.usecases.social_usecase import SocialUseCase
from src.presentation.schemas.social import CommentCreate, CommentResponse, CommentUpdate, ReviewCreate, ReviewResponse
from src.presentation.schemas.response import ApiResponse
from src.domain.exceptions import EntityNotFoundError

router = APIRouter(prefix="/social", tags=["Social"])

@router.post("/recipes/{recipe_id}/reviews", response_model=ApiResponse[ReviewResponse], status_code=201)
async def submit_review(
    recipe_id: str,
    review_in: ReviewCreate,
    user_id: str = Depends(get_current_user_id),
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    review = await social_uc.submit_review(
        user_id=user_id,
        recipe_id=recipe_id,
        rating=review_in.rating,
        text=review_in.text,
        image_url=review_in.image_url
    )
    return ApiResponse(data=review)

@router.post("/comments", response_model=ApiResponse[CommentResponse], status_code=201)
async def post_comment(
    comment_in: CommentCreate,
    user_id: str = Depends(get_current_user_id),
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    return ApiResponse(data=await social_uc.post_comment(user_id, comment_in.recipe_id, comment_in.text))

@router.get("/comments", response_model=ApiResponse[List[CommentResponse]])
async def get_comments(
    recipe_id: str,
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    comments = await social_uc.get_recipe_comments(recipe_id)
    return ApiResponse(data=comments, total=len(comments))

@router.get("/comments/{comment_id}", response_model=ApiResponse[CommentResponse])
async def get_comment(
    comment_id: str,
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    # We need to expose get_comment_by_id in UseCase first
    # Or just use repo directly if we are lazy, but let's check UseCase
    # Assuming UseCase has it or we add it. 
    # Let's check social_manager.py again? 
    # Actually, let's just implement it in UseCase if missing or access repo via UC if public.
    # SocialUseCase has social_repo public.
    comment = await social_uc.get_comment_by_id(comment_id)
    if not comment:
        raise EntityNotFoundError("Comment not found")
    return ApiResponse(data=comment)

@router.delete("/comments/{comment_id}", response_model=ApiResponse[None])
async def delete_comment(
    comment_id: str,
    user_id: str = Depends(get_current_user_id),
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    success = await social_uc.delete_comment(user_id, comment_id)
    if not success:
         raise EntityNotFoundError("Comment not found")
    return ApiResponse(success=True)

@router.patch("/comments/{comment_id}", response_model=ApiResponse[CommentResponse])
async def update_comment(
    comment_id: str,
    comment_in: CommentUpdate,
    user_id: str = Depends(get_current_user_id),
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    return ApiResponse(data=await social_uc.update_comment(user_id, comment_id, comment_in.text))

@router.get("/admin/comments", response_model=ApiResponse[List[CommentResponse]])
async def list_all_comments(
    admin_id: str = Depends(get_admin_user_id),
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    """
    Admin Only: List all comments for moderation
    """
    try:
        comments = await social_uc.list_all_comments()
        return ApiResponse(data=comments, total=len(comments))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recipes/{recipe_id}/like", response_model=ApiResponse[bool])
async def toggle_like(
    recipe_id: str,
    user_id: str = Depends(get_current_user_id),
    social_uc: SocialUseCase = Depends(get_social_usecase)
):
    """
    Toggle like on a recipe. Returns True if liked, False if unliked.
    """
    is_liked = await social_uc.toggle_like(user_id, recipe_id)
    return ApiResponse(data=is_liked)
