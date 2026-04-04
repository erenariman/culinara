from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.database.postgresql.repositories.user_repository import PostgresUserRepository, PostgresUserProfileRepository
from src.adapters.database.postgresql.repositories.recipe_repository import PostgresRecipeRepository
from src.adapters.database.postgresql.repositories.social_repository import PostgresSocialRepository
from src.adapters.database.postgresql.repositories.ingredient_repository import PostgresIngredientRepository
from src.infrastructure.security.password_service import PasswordService

# Use Cases
from src.application.usecases.user_usecase import UserUseCase
from src.application.usecases.recipe_usecase import RecipeUseCase, CreateRecipeCommand
from src.application.usecases.social_usecase import SocialUseCase
from src.application.usecases.ingredient_usecase import IngredientUseCase



class Container:
    """
    DI Container that wires dependencies per request/session.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        
        # Repositories
        self.user_repo = PostgresUserRepository(session)
        self.profile_repo = PostgresUserProfileRepository(session)
        self.recipe_repo = PostgresRecipeRepository(session)
        self.social_repo = PostgresSocialRepository(session)
        self.ingredient_repo = PostgresIngredientRepository(session)
        
    def get_user_usecase(self) -> UserUseCase:
        return UserUseCase(self.user_repo, self.profile_repo, PasswordService())

    def get_recipe_usecase(self) -> RecipeUseCase:
        return RecipeUseCase(self.recipe_repo, self.ingredient_repo)
    

    
    def get_social_usecase(self) -> SocialUseCase:
        return SocialUseCase(self.social_repo)



    def get_ingredient_usecase(self) -> IngredientUseCase:
        return IngredientUseCase(self.ingredient_repo)

