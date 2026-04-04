import asyncio
from sqlalchemy import text
from src.adapters.database.postgresql.database import get_db

async def migrate_enum():
    print("Starting migration to add 'REJECTED' to recipestatus enum...")
    async for session in get_db():
        try:
            # PostgreSQL command to add value to enum if it doesn't exist
            # Note: Postgres doesn't support "IF NOT EXISTS" for enum values directly in older versions,
            # but 'ALTER TYPE ... ADD VALUE' is the standard way. 
            # If it already exists, it might throw an error, which we can catch.
            await session.execute(text("ALTER TYPE recipestatus ADD VALUE 'REJECTED';"))
            await session.commit()
            print("Successfully added 'REJECTED' to recipestatus enum.")
        except Exception as e:
            print(f"Migration failed (or value might already exist): {e}")

if __name__ == "__main__":
    asyncio.run(migrate_enum())
