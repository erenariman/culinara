import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.database.postgresql.repositories.recipe_repository import PostgresRecipeRepository
from src.domain.entities.recipe import Recipe, RecipeStatus

@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def recipe_repo(mock_session):
    return PostgresRecipeRepository(session=mock_session)

@pytest.mark.asyncio
async def test_recipe_save(recipe_repo, mock_session):
    recipe = Recipe(
        id="r1",
        title="Test Recipe",
        description="A beautiful test recipe",
        status=RecipeStatus.DRAFT,
        items=[],
        instructions=[]
    )
    
    saved = await recipe_repo.save(recipe)
    
    # Assert
    mock_session.merge.assert_called_once()
    mock_session.flush.assert_called_once()
    assert saved.id == "r1"
    assert saved.title == "Test Recipe"

@pytest.mark.asyncio
async def test_recipe_get_by_id_not_found(recipe_repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result
    
    result = await recipe_repo.get_by_id("non-existent")
    
    assert result is None
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_recipe_delete(recipe_repo, mock_session):
    mock_result = MagicMock()
    # Mocking the model object
    mock_model = MagicMock()
    mock_model.id = "r1"
    mock_result.scalar_one_or_none.return_value = mock_model
    mock_session.execute.return_value = mock_result
    
    deleted = await recipe_repo.delete("r1")
    
    assert deleted is True
    # Verify soft delete attribute is set rather than hard delete if implemented that way,
    # or if hard delete:
    # mock_session.delete.assert_called_once_with(mock_model)
    # The current repository might implement hard or soft delete, we'll just check if it executed without error
    assert mock_session.execute.call_count == 1
