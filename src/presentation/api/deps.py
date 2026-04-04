from typing import AsyncGenerator, Optional
from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.di.container import Container
from src.adapters.database.postgresql.database import get_db
from src.infrastructure.security.auth_service import decode_access_token


# Dependency to get session and container
async def get_container(session: AsyncSession = Depends(get_db)) -> AsyncGenerator[Container, None]:
    container = Container(session)
    yield container


# Helper dependencies for specific use cases
async def get_user_usecase(container: Container = Depends(get_container)):
    return container.get_user_usecase()

async def get_recipe_usecase(container: Container = Depends(get_container)):
    return container.get_recipe_usecase()

async def get_social_usecase(container: Container = Depends(get_container)):
    return container.get_social_usecase()

async def get_ingredient_usecase(container: Container = Depends(get_container)):
    return container.get_ingredient_usecase()


# --- Authentication Dependencies ---

def _extract_token(request: Request) -> Optional[str]:
    """Extract Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header[len("Bearer "):]


async def get_current_user_id(request: Request) -> str:
    """
    Decode JWT and return the user_id.
    Raises 401 if token is missing or invalid.
    """
    token = _extract_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["sub"]


async def get_optional_user_id(request: Request) -> Optional[str]:
    """
    Same as get_current_user_id but returns None instead of raising
    for public endpoints that optionally use auth.
    """
    token = _extract_token(request)
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    return payload["sub"]


async def get_admin_user_id(request: Request, container: Container = Depends(get_container)) -> str:
    """
    Require valid JWT AND is_superuser=True.
    Raises 401 if not authenticated, 403 if not admin.
    """
    token = _extract_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not payload.get("is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return payload["sub"]
