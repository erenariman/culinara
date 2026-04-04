import pytest
from httpx import AsyncClient
from src.domain.entities.social import Comment
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_add_comment_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/v1/social/comments",
        json={"recipe_id": "recipe123", "text": "Great recipe!"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_add_comment_success(client: AsyncClient, auth_headers, mocker):
    comment_obj = Comment(
        id="comment123",
        user_id="user123",
        recipe_id="recipe123",
        text="Great recipe!",
        created_at=datetime.now(timezone.utc)
    )

    mocker.patch(
        "src.application.usecases.social_manager.SocialUseCase.post_comment",
        return_value=comment_obj
    )

    response = await client.post(
        "/api/v1/social/comments",
        json={"recipe_id": "recipe123", "text": "Great recipe!"},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["id"] == "comment123"
    assert data["data"]["text"] == "Great recipe!"

@pytest.mark.asyncio
async def test_get_all_comments_admin_unauthorized(client: AsyncClient, auth_headers):
    # Standard user trying to access admin route
    response = await client.get("/api/v1/social/admin/comments", headers=auth_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"

@pytest.mark.asyncio
async def test_get_all_comments_admin_success(client: AsyncClient, admin_headers, mocker):
    mocker.patch(
        "src.application.usecases.social_manager.SocialUseCase.list_all_comments",
        return_value=[] # Return empty list, not tuple
    )

    response = await client.get("/api/v1/social/admin/comments", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["total"] == 0
