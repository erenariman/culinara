import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timedelta

from fastapi import FastAPI
from main import app as fastapi_app
from src.infrastructure.security.auth_service import create_access_token
from src.adapters.database.postgresql.database import get_db

# Import Mock Ports
from src.domain.entities.user import User
from src.domain.entities.recipe import Recipe, RecipeStatus

# ==========================================
# GEREKLI MOCK OBJELER VE YAPILAR
# ==========================================

@pytest.fixture
def mock_user():
    return User(
        id="test-user-id",
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
        is_active=True,
        is_superuser=False,
    )

@pytest.fixture
def mock_admin():
    return User(
        id="admin-user-id",
        email="admin@example.com",
        username="adminuser",
        hashed_password="hashed_pass",
        is_active=True,
        is_superuser=True,
    )

@pytest.fixture
def valid_token(mock_user):
    return create_access_token(user_id=mock_user.id, is_superuser=mock_user.is_superuser)

@pytest.fixture
def admin_token(mock_admin):
    return create_access_token(user_id=mock_admin.id, is_superuser=mock_admin.is_superuser)

# ==========================================
# ASENKRON ISTEMCI & UYGULAMA OVERRIDE YAPISI
# ==========================================

@pytest_asyncio.fixture()
async def client():
    from unittest.mock import MagicMock
    async def override_get_db():
        yield MagicMock()
    fastapi_app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    fastapi_app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(valid_token):
    return {"Authorization": f"Bearer {valid_token}"}

@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
