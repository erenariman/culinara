import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone
import json

from src.adapters.database.postgresql.repositories.user_repository import PostgresUserRepository
from src.adapters.database.postgresql.models.user import UserModel
from src.adapters.database.postgresql.models.profile import UserProfileModel
from src.domain.entities.user import User, UserProfile

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def user_repo(mock_session):
    return PostgresUserRepository(session=mock_session)

@pytest.mark.asyncio
async def test_user_repository_save(user_repo, mock_session):
    user = User(
        id="u1",
        email="test@example.com",
        username="tester1",
        hashed_password="hashed!"
    )
    
    saved_user = await user_repo.save(user)
    
    # Assert session methods were called
    mock_session.merge.assert_called_once()
    mock_session.flush.assert_called_once()
    
    # Assert domain logic remained same
    assert saved_user.id == "u1"
    assert saved_user.email == "test@example.com"

@pytest.mark.asyncio
async def test_user_repository_get_by_id(user_repo, mock_session):
    # Setup mock outcome
    mock_result = MagicMock()
    
    mock_profile = UserProfileModel(
        user_id="u1", 
        bio="Hello", 
        avatar_url="url", 
        preferences=json.dumps({"theme": "dark"})
    )
    mock_model = UserModel(
        id="u1", 
        email="test@example.com", 
        username="tester1",
        profile=mock_profile,
        created_at=datetime.now(timezone.utc)
    )
    
    mock_result.scalar_one_or_none.return_value = mock_model
    mock_session.execute.return_value = mock_result
    
    # Execute
    user = await user_repo.get_by_id("u1")
    
    # Verify execution
    assert mock_session.execute.call_count == 1
    assert user is not None
    assert user.id == "u1"
    assert user.profile is not None
    assert user.profile.preferences["theme"] == "dark"

@pytest.mark.asyncio
async def test_user_repository_get_by_email_not_found(user_repo, mock_session):
    # Setup mock returning None
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result
    
    # Execute
    user = await user_repo.get_by_email("notfound@example.com")
    
    assert user is None
    assert mock_session.execute.call_count == 1

@pytest.mark.asyncio
async def test_user_repository_delete(user_repo, mock_session):
    # Setup mock to find user
    mock_result = MagicMock()
    mock_model = UserModel(id="u1", email="test@test.com", username="test")
    mock_result.scalar_one_or_none.return_value = mock_model
    mock_session.execute.return_value = mock_result
    
    result = await user_repo.delete("u1")
    
    assert result is True
    mock_session.delete.assert_called_once_with(mock_model)
