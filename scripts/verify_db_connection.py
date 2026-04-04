import asyncio
from sqlalchemy import text
from src.adapters.database.postgresql.database import get_db

async def check_db():
    print("Attempting to connect to DB...")
    try:
        async for session in get_db():
            result = await session.execute(text("SELECT 1"))
            print(f"DB Connection Successful: {result.scalar()}")
            break
    except Exception as e:
        print(f"DB Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_db())
