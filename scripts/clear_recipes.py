import asyncio
import sys
import os
sys.path.append(os.getcwd())

from src.adapters.database.postgresql.database import AsyncSessionLocal
from sqlalchemy import text

async def clear_recipes():
    print("Clearing all recipes...")
    async with AsyncSessionLocal() as s:
        tables = ['reviews', 'comments', 'recipe_likes', 'recipe_ingredients', 'instruction_steps', 'recipe_tags', 'recipes']
        for t in tables:
            result = await s.execute(text(f'DELETE FROM {t}'))
            print(f"  Cleared {t}: {result.rowcount} rows")
        await s.commit()
        print("All recipe data cleared!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(clear_recipes())
