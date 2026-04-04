import asyncio
import sys
import uuid
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.adapters.database.postgresql.database import get_db
from src.adapters.database.postgresql.models.recipe import RecipeModel, RecipeStatus
from src.adapters.database.postgresql.models.instruction import InstructionStepModel

# Add project root to path
import os
sys.path.append(os.getcwd())

async def test_recipe_steps_raw():
    print("\n--- Testing Raw SQLAlchemy Steps Merge ---")
    async for session in get_db():
        try:
            # 1. Create Recipe
            r_id = str(uuid.uuid4())
            u_id = str(uuid.uuid4()) # Fake user for FK (might fail if foreign key constraint is enforced... yes it is)
            
            # Use an existing user or create one?
            # We need a user to satisfy FK.
            from src.adapters.database.postgresql.models.user import UserModel
            user = UserModel(id=u_id, email=f"raw_{u_id[:8]}", username=f"raw_{u_id[:8]}")
            session.add(user)
            await session.flush()
            print("User created.")

            recipe = RecipeModel(
                id=r_id,
                title="Raw Test",
                description="Raw Desc",
                slug=f"raw-{r_id}",
                status=RecipeStatus.DRAFT.value,
                author_id=u_id
            )
            session.add(recipe)
            await session.flush()
            print("Recipe draft created.")

            # 2. Add Step via Merge (Simulating Repository)
            # Create a detached object representing the updated state
            step_id = str(uuid.uuid4())
            
            # Detached recipe with new step
            steps_list = [
                InstructionStepModel(id=step_id, recipe_id=r_id, step_number=1, text="Step 1")
            ]
            
            detached_recipe = RecipeModel(
                id=r_id,
                title="Raw Test",
                description="Raw Desc",
                slug=f"raw-{r_id}",
                status=RecipeStatus.DRAFT.value,
                author_id=u_id,
                steps=steps_list
            )
            
            print("Merging updated recipe with step...")
            await session.merge(detached_recipe)
            await session.flush()
            print("Merge complete.")
            
            # Verify
            result = await session.execute(
                select(RecipeModel).options(selectinload(RecipeModel.steps)).where(RecipeModel.id == r_id)
            )
            loaded = result.scalar_one()
            print(f"Loaded steps count: {len(loaded.steps)}")
            
            await session.rollback()
            print("Rollback.")

        except Exception as e:
            print(f"❌ RAW TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            await session.rollback()

if __name__ == "__main__":
    import asyncio
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_recipe_steps_raw())
