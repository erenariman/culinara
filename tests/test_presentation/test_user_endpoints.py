import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, mocker):
    # Mocking user_usecase for presentation test
    mock_val = {"id": "123", "email": "new@example.com", "username": "newuser"}
    mocker.patch(
        "src.application.usecases.user_usecase.UserUseCase.register_user",
        return_value=mock_val
    )

    response = await client.post(
        "/api/v1/users/register",
        json={"email": "new@example.com", "username": "newuser", "password": "PassWord123!"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["email"] == "new@example.com"
    assert data["data"]["username"] == "newuser"

@pytest.mark.asyncio
async def test_register_validation_error(client: AsyncClient):
    # Missing parameters
    response = await client.post(
        "/api/v1/users/register",
        json={"email": "not-an-email"}
    )
    assert response.status_code == 422 # Pydantic validation error

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, mocker):
    class MockUser:
        id = "123"
        is_superuser = False
    
    mocker.patch(
        "src.application.usecases.user_usecase.UserUseCase.authenticate_user",
        return_value=MockUser()
    )

    response = await client.post(
        "/api/v1/users/login",
        json={"email": "test@example.com", "password": "correct"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "user"

@pytest.mark.asyncio
async def test_login_unauthorized(client: AsyncClient, mocker):
    # Returns None on authentication failure
    mocker.patch(
        "src.application.usecases.user_usecase.UserUseCase.authenticate_user",
        return_value=None
    )

    response = await client.post(
        "/api/v1/users/login",
        json={"email": "test@example.com", "password": "wrong"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    # Request without token
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_users_admin_unauthorized(client: AsyncClient, auth_headers):
    # Request with normal user token to admin endpoint
    response = await client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"

@pytest.mark.asyncio
async def test_get_users_admin_success(client: AsyncClient, admin_headers, mocker):
    mocker.patch(
        "src.application.usecases.user_usecase.UserUseCase.list_users",
        return_value=[]
    )
    # Request with admin token
    response = await client.get("/api/v1/users/?skip=0&limit=10", headers=admin_headers)
    assert response.status_code == 200
    assert "data" in response.json()

@pytest.mark.asyncio
async def test_get_me_success(client: AsyncClient, auth_headers, mocker):
    from src.domain.entities.user import User
    
    mock_user = User(
        id="123",
        email="test@example.com",
        username="tester1",
        is_superuser=True
    )
    
    mocker.patch(
        "src.application.usecases.user_usecase.UserUseCase.get_user",
        return_value=mock_user
    )
    
    response = await client.get("/api/v1/users/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["is_superuser"] is True
    assert data["data"]["access"] == "admin"
