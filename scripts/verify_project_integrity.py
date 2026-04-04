import asyncio
import sys
import uuid
import json
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Add project root to path
import os
sys.path.append(os.getcwd())

from src.domain.entities import (
    User as DomainUser, 
    Recipe as DomainRecipe, 
    RecipeStatus, 
    RecipeInstruction,
    UserProfile,
    SkillLevel
)
from src.adapters.database.postgresql.database import get_db
from src.adapters.database.postgresql.models import (
    UserModel, 
    RecipeModel, 
    UserProfileModel,
    RecipeStatus as DBRecipeStatus
)

async def verify_domain_instantiation():
    print("\n[1] Verifying Domain Entities...")
    try:
        # Test User Entity
        u = DomainUser(id="u1", email="test@test.com", username="testuser")
        p = UserProfile(user_id="u1", skill_level=SkillLevel.EXPERT if hasattr(SkillLevel, 'EXPERT') else SkillLevel.ADVANCED)
        u.profile = p
        print("✅ Domain User & Profile instantiated")

        # Test Recipe Entity
        r = DomainRecipe(
            id="r1", 
            title="Test Recipe", 
            description="Desc",
            status=RecipeStatus.PUBLISHED,
            slug="test-recipe"
        )
        r.instructions.append(RecipeInstruction(id="i1", step_number=1, text="Mix"))
        print(f"✅ Domain Recipe instantiated (Status: {r.status})")
        
    except Exception as e:
        print(f"❌ Domain Verification Failed: {e}")
        raise e

async def verify_database_integration():
    print("\n[2] Verifying Database Persistence (ORM Mapping)...")
    async for session in get_db():
        try:
            # 1. Create User
            user_id = str(uuid.uuid4())
            new_user = UserModel(
                id=user_id,
                email=f"integration_{user_id[:8]}@example.com",
                username=f"user_{user_id[:8]}",
                hashed_password="hashed_secret"
            )
            session.add(new_user)
            await session.flush() # Get ID
            print(f"✅ Created User in DB: {new_user.id}")

            # 2. Create Profile
            new_profile = UserProfileModel(
                user_id=new_user.id,
                bio="I am a test robot",
                preferences=json.dumps({"theme": "dark"})
            )
            session.add(new_profile)
            
            # 3. Create Recipe with Enum status
            recipe_id = str(uuid.uuid4())
            new_recipe = RecipeModel(
                id=recipe_id,
                title="Integration Test Spaghetti",
                description="Testing enums",
                instructions="Boil water",
                slug=f"spaghetti-{recipe_id[:8]}",
                status="PUBLISHED", # ORM should handle this string-to-enum if configured, or needs Enum object
                author_id=new_user.id
            )
            session.add(new_recipe)
            await session.flush()
            print(f"✅ Created Recipe in DB: {new_recipe.id}")
            
            # 4. Read back with join
            query = select(UserModel).options(selectinload(UserModel.profile)).where(UserModel.id == new_user.id)
            result = await session.execute(query)
            fetched_user = result.scalar_one()
            
            if fetched_user.profile and fetched_user.profile.bio == "I am a test robot":
                 print("✅ User <-> Profile Relationship verified")
            else:
                 print("❌ User <-> Profile Relationship FAILED")

            # Rollback to clean up
            await session.rollback()
            print("✅ Transaction rolled back (Cleanup successful)")

        except Exception as e:
            await session.rollback()
            print(f"❌ Database Verification Failed: {e}")
            raise e

async def main():
    await verify_domain_instantiation()
    await verify_database_integration()

if __name__ == "__main__":
    asyncio.run(main())
