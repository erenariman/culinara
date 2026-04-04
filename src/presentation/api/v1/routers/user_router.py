from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from src.config.rate_limit import limiter
from src.application.usecases.user_usecase import UserUseCase
from src.presentation.api.deps import get_user_usecase, get_current_user_id, get_admin_user_id
from src.presentation.schemas.user import UserCreate, UserResponse, UserLogin, ProfileUpdate, UserUpdateAdmin
from src.presentation.schemas.response import ApiResponse
from src.domain.exceptions import EntityNotFoundError, InvalidCredentialsError
from src.infrastructure.security.auth_service import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=ApiResponse[UserResponse], status_code=201)
@limiter.limit("3/minute")
async def register(
    request: Request,
    user_in: UserCreate,
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    user = await user_uc.register_user(
        email=str(user_in.email),
        username=user_in.username,
        password=user_in.password
    )
    return ApiResponse(data=user)

@router.post("/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    user_in: UserLogin,
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    user = await user_uc.authenticate_user(str(user_in.email), user_in.password)
    if not user:
        raise InvalidCredentialsError("Invalid email or password")

    role = "admin" if user.is_superuser else "user"
    token = create_access_token(user_id=user.id, is_superuser=user.is_superuser)

    return {
        "status": "ok",
        "type": "account",
        "currentAuthority": role,
        "access_token": token,
        "token_type": "bearer",
        "role": role,
        "user_id": user.id,
    }

@router.get("/me", response_model=ApiResponse[UserResponse])
async def read_users_me(
    user_id: str = Depends(get_current_user_id),
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    """Get current user profile."""
    user = await user_uc.get_user(user_id)
    if not user:
        raise EntityNotFoundError("User not found")
    return ApiResponse(data=user)

@router.patch("/me", response_model=ApiResponse[UserResponse])
async def update_my_profile(
    profile_in: ProfileUpdate,
    user_id: str = Depends(get_current_user_id),
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    await user_uc.update_profile(
        user_id,
        profile_in.bio,
        profile_in.preferences or {}
    )
    user = await user_uc.get_user(user_id)
    return ApiResponse(data=user)

@router.delete("/me", response_model=ApiResponse[None])
async def delete_my_account(
    user_id: str = Depends(get_current_user_id),
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    success = await user_uc.delete_account(user_id)
    if not success:
        raise EntityNotFoundError("User not found")
    return ApiResponse(success=True)

@router.delete("/{user_id}", response_model=ApiResponse[None])
async def delete_user(
    user_id: str,
    admin_id: str = Depends(get_admin_user_id),
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    """Admin Only: Delete any user"""
    success = await user_uc.delete_account(user_id)
    if not success:
        raise EntityNotFoundError("User not found")
    return ApiResponse(success=True)

@router.patch("/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user_admin(
    user_id: str,
    user_update: UserUpdateAdmin,
    admin_id: str = Depends(get_admin_user_id),
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    """Admin Only: Update any user details (username, password, etc)"""
    user = await user_uc.update_user_admin(
        user_id=user_id,
        username=user_update.username,
        password=user_update.password,
        is_active=user_update.is_active,
        is_superuser=user_update.is_superuser
    )
    return ApiResponse(data=user)

@router.get("/", response_model=ApiResponse[List[UserResponse]])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    admin_id: str = Depends(get_admin_user_id),
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    """Admin Only: List all users"""
    users = await user_uc.list_users(skip, limit)
    return ApiResponse(data=users, total=len(users))

@router.patch("/{user_id}/status", response_model=ApiResponse[UserResponse])
async def update_user_status(
    user_id: str,
    is_active: bool,
    admin_id: str = Depends(get_admin_user_id),
    user_uc: UserUseCase = Depends(get_user_usecase)
):
    """Admin Only: Ban/Unban user"""
    user = await user_uc.update_status(user_id, is_active)
    return ApiResponse(data=user)
