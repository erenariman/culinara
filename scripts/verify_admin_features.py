import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.di.container import Container
from src.adapters.database.postgresql.database import get_db
from src.domain.entities.user import User
from src.domain.entities.social import Comment, EntityType

async def verify_admin_features():
    print("\n[1] Initializing DI Container...")
    
    async for session in get_db():
        container = Container(session)
        
        # Get UseCases
        user_uc = container.get_user_usecase()
        social_uc = container.get_social_usecase()
        
        print("\n[2] Testing User Listing (Admin)...")
        try:
            users = await user_uc.list_users(0, 100)
            print(f"✅ Users Retrieved: {len(users)}")
            for u in users[:3]:
                print(f"   - {u.username} ({u.email}) Active: {u.is_active}")
        except Exception as e:
            print(f"❌ User Listing Failed: {e}")

        print("\n[3] Testing Comment Listing (Admin)...")
        try:
            comments = await social_uc.list_all_comments(0, 100)
            print(f"✅ Comments Retrieved (Initial): {len(comments)}")
            
            if len(comments) == 0:
                print("   No comments found. Attempting to create one for verification...")
                recipe_uc = container.get_recipe_usecase()
                
                # Get a user and recipe
                users = await user_uc.list_users(0, 1)
                recipes = await recipe_uc.list_recipes()
                
                if users and recipes:
                    user = users[0]
                    recipe = recipes[0]
                    print(f"   Posting comment as {user.username} on recipe {recipe.title}...")
                    await social_uc.post_comment(user.id, recipe.id, "Admin Verification Comment")
                    
                    # Fetch again
                    comments = await social_uc.list_all_comments(0, 100)
                    print(f"✅ Comments Retrieved (After Post): {len(comments)}")
                else:
                    print("⚠️ Cannot create comment: No users or recipes found.")

            for c in comments[:3]:
                # Handle created_at potentially being None if old data
                date_str = c.created_at.isoformat() if hasattr(c, 'created_at') and c.created_at else "N/A"
                print(f"   - [{date_str}] {c.text[:30]}...")
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ Comment Listing Failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(verify_admin_features())
    except KeyboardInterrupt:
        print("\nTest interrupted.")
    except Exception as e:
        print(f"\nUncaught error: {e}")
