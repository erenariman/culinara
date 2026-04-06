import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.adapters.database.postgresql.database import AsyncSessionLocal
from src.adapters.database.postgresql.repositories.user_repository import PostgresUserRepository, PostgresUserProfileRepository
from src.infrastructure.security.password_service import PasswordService
from src.application.usecases.user_usecase import UserUseCase

async def seed_admin():
    print("Connecting to DB...")
    
    async with AsyncSessionLocal() as session:
        user_repo = PostgresUserRepository(session)
        profile_repo = PostgresUserProfileRepository(session)
        password_service = PasswordService()
        
        user_uc = UserUseCase(
            user_repo=user_repo, 
            profile_repo=profile_repo, 
            password_service=password_service
        )
        
        email = "admin@example.com"
        password = "ant.design" 
        
        existing = await user_repo.get_by_email(email)
        if existing:
            print(f"User {email} already exists.")
            return

        print(f"Creating user {email}...")
        try:
            user = await user_uc.register_user(
                email=email,
                username="admin",
                password=password
            )
            # Manually set is_superuser and is_active if register doesn't
            # Re-fetch model to update (or just update entity if repo supports)
            # Our User entity has is_superuser. register_user default is False usually.
            
            user.is_superuser = True
            user.is_active = True
            await repo.update(user)
            await session.commit()
            
            print(f"Successfully created admin user: {user.id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_admin())
