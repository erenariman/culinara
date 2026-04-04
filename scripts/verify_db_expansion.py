import asyncio
from sqlalchemy import text
from src.adapters.database.postgresql.database import get_db

async def verify_db():
    print("Verifying Database Schema Expansion...")
    async for session in get_db():
        # Check recipes table columns
        result = await session.execute(text(
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'recipes'"
        ))
        columns = {row[0]: row[1] for row in result.fetchall()}
        
        print("\n[Recipes Table Columns]")
        expected_cols = ["slug", "status", "total_protein", "deleted_at", "view_count"]
        for col in expected_cols:
            if col in columns:
                print(f"✅ Found {col} ({columns[col]})")
            else:
                print(f"❌ MISSING {col}")

        # Check users table columns
        result = await session.execute(text(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"
        ))
        user_cols = [row[0] for row in result.fetchall()]
        if "deleted_at" in user_cols:
             print("\n✅ Found users.deleted_at")
        else:
             print("\n❌ MISSING users.deleted_at")

        # Check existence of new tables
        new_tables = ["shopping_lists", "moderation_logs", "search_logs", "user_profiles"]
        print("\n[New Tables]")
        for table in new_tables:
            result = await session.execute(text(
                f"SELECT to_regclass('public.{table}')"
            ))
            if result.scalar():
                print(f"✅ Found table: {table}")
            else:
                print(f"❌ MISSING table: {table}")
                
if __name__ == "__main__":
    asyncio.run(verify_db())
