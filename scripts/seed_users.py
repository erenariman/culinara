import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import delete
from src.adapters.database.postgresql.database import get_db
from src.infrastructure.di.container import Container

# Imports for Deletion (Reverse Dependency Order)
from src.adapters.database.postgresql.models.logs import ModerationLogModel, SearchLogModel
from src.adapters.database.postgresql.models.gamification import CookLogModel, UserBadgeModel
from src.adapters.database.postgresql.models.social import (
    RecipeLikeModel, CommentModel, ReviewModel, ReportModel, FollowModel, BlockModel
)
from src.adapters.database.postgresql.models.collection import (
    MealPlanModel, CollectionRecipeModel, CollectionModel
)
from src.adapters.database.postgresql.models.tag import RecipeTagModel
from src.adapters.database.postgresql.models.equipment import RecipeEquipmentModel
from src.adapters.database.postgresql.models.recipe import RecipeIngredientModel, RecipeModel
from src.adapters.database.postgresql.models.instruction import InstructionStepModel
from src.adapters.database.postgresql.models.shopping import ShoppingListItemModel, ShoppingListModel
from src.adapters.database.postgresql.models.profile import UserProfileModel
from src.adapters.database.postgresql.models.user import UserModel


async def seed_users():
    print("🌱 Starting Database Seeding...")
    
    async for session in get_db():
        container = Container(session)
        user_uc = container.get_user_usecase()
        user_repo = container.user_repo
        
        print("1. Cleaning up existing data (Reverse Dependency Order)...")
        try:
            # 1. Logs & Gamification
            await session.execute(delete(ModerationLogModel))
            await session.execute(delete(SearchLogModel))
            await session.execute(delete(CookLogModel))
            await session.execute(delete(UserBadgeModel))
            
            # 2. Social
            await session.execute(delete(RecipeLikeModel))
            await session.execute(delete(CommentModel))
            await session.execute(delete(ReviewModel))
            await session.execute(delete(ReportModel))
            await session.execute(delete(FollowModel))
            await session.execute(delete(BlockModel))
            
            # 3. Collections & Plans
            await session.execute(delete(MealPlanModel))
            await session.execute(delete(CollectionRecipeModel))
            await session.execute(delete(CollectionModel))
            
            # 4. Recipes & Related
            await session.execute(delete(RecipeTagModel))
            await session.execute(delete(RecipeEquipmentModel))
            await session.execute(delete(RecipeIngredientModel))
            await session.execute(delete(InstructionStepModel))
            await session.execute(delete(RecipeModel))
            
            # 5. Shopping
            await session.execute(delete(ShoppingListItemModel))
            await session.execute(delete(ShoppingListModel))
            
            # 6. User
            await session.execute(delete(UserProfileModel))
            await session.execute(delete(UserModel))
            
            await session.commit()
            print("   ✅ Existing data cleaned successfully.")
        except Exception as e:
            print(f"   ❌ Error cleaning data: {e}")
            await session.rollback()
            return

        print("2. Creating 'eren' (Normal User)...")
        try:
            eren = await user_uc.register_user(
                email="eren@example.com",
                username="eren",
                password="password" # Default password
            )
            print(f"   ✅ Created 'eren' (ID: {eren.id})")
        except Exception as e:
            print(f"   ❌ Error creating eren: {e}")

        print("3. Creating 'admin' (Superuser)...")
        try:
            admin = await user_uc.register_user(
                email="admin@example.com",
                username="admin",
                password="adminpassword"
            )
            
            # Make admin
            admin.is_superuser = True
            await user_repo.save(admin)
            
            print(f"   ✅ Created 'admin' (ID: {admin.id}) and set as Superuser")
        except Exception as e:
             print(f"   ❌ Error creating admin: {e}")
             
    print("🌱 Seeding Complete.")

if __name__ == "__main__":
    try:
        asyncio.run(seed_users())
    except KeyboardInterrupt:
        print("\nSeeding interrupted.")
    except Exception as e:
        print(f"\nUncaught error: {e}")
