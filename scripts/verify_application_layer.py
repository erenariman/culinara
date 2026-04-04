import asyncio
import sys
import uuid
from src.infrastructure.di.container import Container
from src.adapters.database.postgresql.database import get_db
from src.application.usecases.recipe_usecase import CreateRecipeCommand, CreateRecipeItemCommand

# Add project root to path
import os
sys.path.append(os.getcwd())

async def verify_user_registration_flow():
    print("\n[1] Testing User Registration via DI Container...")
    
    # Simulate a Request Lifetime
    async for session in get_db():
        try:
            # 1. Instantiate Container with Session
            container = Container(session)
            
            # 2. Get Use Case from Container (DI happening here)
            user_uc = container.get_user_usecase()
            
            # 3. Execute Business Logic
            unique_id = str(uuid.uuid4())[:8]
            email = f"app_layer_{unique_id}@test.com"
            username = f"app_user_{unique_id}"
            
            print(f"   Attempting to register: {email}")
            user = await user_uc.register_user(
                email=email,
                username=username,
                password="securepassword123"
            )
            
            print(f"✅ User Registered: ID={user.id}, Email={user.email}")
            
            # 4. Verify Profile Creation (Side effect of use case)
            profile = await user_uc.get_user_profile(user.id)
            if profile:
                print(f"✅ Profile confirmed for user: {profile.user_id}")
            else:
                print("❌ Profile creation failed")
                
            # Rollback to keep DB clean
            await session.rollback()
            print("   (Rolled back transaction)")
            
        except Exception as e:
            print(f"❌ Application Verification Failed: {e}")
            await session.rollback()
            # raise e

async def verify_recipe_flow():
    print("\n[2] Testing Recipe Creation via DI Container...")
    async for session in get_db():
        try:
            container = Container(session)
            user_uc = container.get_user_usecase()
            recipe_uc = container.get_recipe_usecase()
            
            # Setup User
            unique_id = str(uuid.uuid4())[:8]
            user = await user_uc.register_user(f"chef_{unique_id}@test.com", f"chef_{unique_id}", "pw")
            
            # Create Recipe Draft
            print("   Creating Recipe Draft...")
            cmd = CreateRecipeCommand(
                author_id=user.id,
                title="Application Layer Pie",
                description="Delicious architecture",
                instructions=[],
                items=[]
            )
            recipe = await recipe_uc.create_recipe(cmd)
            print(f"✅ Draft Created: {recipe.title} (Status: {recipe.status})")
            
            # Add Instruction
            updated_recipe = await recipe_uc.add_instruction(recipe.id, " Mix Layers", 1)
            print(f"✅ Instruction Added. Steps: {len(updated_recipe.instructions)}")
            
            # Create Dummy Ingredient directly for test
            from src.adapters.database.postgresql.models.ingredient import IngredientModel
            ing_id = str(uuid.uuid4())
            ing_model = IngredientModel(
                id=ing_id, 
                name="Test Salt", 
                calories_per_100g=0, 
                protein_per_100g=0, 
                fat_per_100g=0, 
                carbs_per_100g=0,
                density_g_ml=1.2
            )
            session.add(ing_model)
            await session.flush()
            print("   Created Dummy Ingredient: " + ing_model.name)
            
            # Add Ingredient
            print("   Adding Ingredient...")
            updated_recipe = await recipe_uc.add_ingredient(recipe.id, ing_id, 100, "gram")
            print(f"✅ Ingredient Added. Items: {len(updated_recipe.items)}")
            
            # Publish
            published_recipe = await recipe_uc.publish_recipe(recipe.id)
            print(f"✅ Recipe Published. Status: {published_recipe.status}")
            
            await session.rollback()
            print("   (Rolled back transaction)")

        except Exception as e:
             print(f"❌ Recipe Flow Failed: {e}")
             await session.rollback()

async def verify_shopping_flow():
    print("\n[3] Testing Shopping List Flow via DI Container...")
    async for session in get_db():
        try:
            container = Container(session)
            user_uc = container.get_user_usecase()
            shop_uc = container.get_shopping_usecase()
            
            # Setup User
            user_id = str(uuid.uuid4())
            # We assume user exists or FK might fail if constraint enforced. 
            # Ideally we register user first.
            user = await user_uc.register_user(f"shopper_{user_id[:8]}@test.com", f"shopper_{user_id}", "pw")
            
            # Create List
            sl = await shop_uc.create_list(user.id, "Weekly Groceries")
            print(f"✅ Shopping List Created: {sl.title}")
            
            # Add items
            sl = await shop_uc.add_item(sl.id, "Milk", 2, "liters")
            sl = await shop_uc.add_item(sl.id, "Eggs", 12, "pcs")
            print(f"✅ Items Added. Count: {len(sl.items)}")
            
            await session.rollback()
            print("   (Rolled back transaction)")
        except Exception as e:
            print(f"❌ Shopping Flow Failed: {e}")
            await session.rollback()

async def verify_social_flow():
    print("\n[4] Testing Social Flow via DI Container...")
    async for session in get_db():
        try:
            container = Container(session)
            user_uc = container.get_user_usecase()
            recipe_uc = container.get_recipe_usecase()
            social_uc = container.get_social_usecase()

            # Setup User & Recipe
            u_id = str(uuid.uuid4())
            user = await user_uc.register_user(f"social_{u_id[:8]}@test.com", f"social_{u_id}", "pw")
            
            cmd = CreateRecipeCommand(
                author_id=user.id,
                title="Social Recipe", 
                description="Desc",
                instructions=[],
                items=[]
            )
            r = await recipe_uc.create_recipe(cmd)
            
            # Post Comment
            comment = await social_uc.post_comment(user.id, r.id, "Looks yummy!")
            print(f"✅ Comment Posted: {comment.text}")
            
            # Retrieve Comments
            comments = await social_uc.get_recipe_comments(r.id)
            print(f"✅ Comments Retrieved. Count: {len(comments)}")
            
            await session.rollback()
        except Exception as e:
            print(f"❌ Social Flow Failed: {e}")
            await session.rollback()

async def verify_organization_flow():
    print("\n[5] Testing Organization (Collections) Flow via DI Container...")
    async for session in get_db():
        try:
            container = Container(session)
            user_uc = container.get_user_usecase()
            org_uc = container.get_organization_usecase()
            
            # Setup User
            user_id = str(uuid.uuid4())
            user = await user_uc.register_user(f"org_{user_id[:8]}@test.com", f"org_{user_id}", "pw")
            
            # Create Collection
            coll = await org_uc.create_collection(user.id, "Weekend Party", "Recipes for the party", True)
            print(f"✅ Collection Created: {coll.title}")
            
            # Fetch
            colls = await org_uc.get_user_collections(user.id)
            print(f"✅ Collections Retrieved. Count: {len(colls)}")
            
            await session.rollback()
        except Exception as e:
            print(f"❌ Organization Flow Failed: {e}")
            import traceback
            traceback.print_exc()
            await session.rollback()

async def main():
    await verify_user_registration_flow()
    await verify_recipe_flow()
    await verify_shopping_flow()
    await verify_social_flow()
    await verify_organization_flow()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
