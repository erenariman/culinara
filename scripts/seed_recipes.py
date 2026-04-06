import asyncio
import sys
import os
import uuid
from datetime import datetime
from slugify import slugify

# Add project root to path
sys.path.append(os.getcwd())

from src.adapters.database.postgresql.database import AsyncSessionLocal
from src.adapters.database.postgresql.repositories.recipe_repository import PostgresRecipeRepository
from src.adapters.database.postgresql.repositories.ingredient_repository import PostgresIngredientRepository
from src.adapters.database.postgresql.repositories.user_repository import PostgresUserRepository
from src.domain.entities.recipe import Recipe, RecipeItem, RecipeInstruction, RecipeStatus
from src.domain.entities.units import UnitType

async def seed_recipes():
    print("Connecting to database...")
    async with AsyncSessionLocal() as session:
        recipe_repo = PostgresRecipeRepository(session)
        ing_repo = PostgresIngredientRepository(session)
        user_repo = PostgresUserRepository(session)
        
        # 1. Get Admin User
        admin = await user_repo.get_by_email("admin@example.com")
        if not admin:
            print("Admin user not found. Please run seed_admin.py first.")
            return
        
        print(f"Using admin user: {admin.username} (ID: {admin.id})")
        
        # Helpers to fetch ingredients
        async def get_ing(name):
            ing = await ing_repo.get_by_name(name)
            if not ing:
                print(f"CRITICAL: Ingredient '{name}' not found!")
            return ing

        # RECIPES DATA
        recipes_to_add = [
            # 1. Mercimek Çorbası
            {
                "title": "Süzme Mercimek Çorbası",
                "description": "Klasik, pürüzsüz ve besleyici Türk usulü restorant mercimek çorbası.",
                "category": "Çorba",
                "difficulty": "Kolay",
                "diet_type": "Hepçil",
                "prep_time": 10,
                "cook_time": 25,
                "servings": 4,
                "ingredients": [
                    ("Kırmızı Mercimek", 1, UnitType.GLASS_WATER),
                    ("Soğan", 1, UnitType.PIECE),
                    ("Havuç", 1, UnitType.PIECE),
                    ("Un", 1, UnitType.TBS),
                    ("Tereyağı", 2, UnitType.TBS),
                    ("Zeytinyağı", 1, UnitType.TBS),
                    ("Tuz", 1, UnitType.TSP),
                    ("Karabiber", 0.5, UnitType.TSP),
                ],
                "steps": [
                    "Mercimekleri iyice yıkayıp süzün.",
                    "Soğan ve havucu rastgele doğrayın.",
                    "Tencerede yağı eritip soğan ve havucu soteleyin.",
                    "Unu ekleyip kokusu çıkana kadar kavurun.",
                    "Mercimekleri ve sıcak suyu ekleyip mercimekler yumuşayana kadar pişirin.",
                    "Pişen çorbayı pürüzsüz olana kadar blenderdan geçirin."
                ]
            },
            # 2. Menemen
            {
                "title": "Menemen",
                "description": "Kahvaltıların vazgeçilmezi, sulu ve lezzetli domatesli biberli yumurta.",
                "category": "Kahvaltı",
                "difficulty": "Kolay",
                "diet_type": "Vejetaryen",
                "prep_time": 5,
                "cook_time": 10,
                "servings": 2,
                "ingredients": [
                    ("Yumurta", 3, UnitType.PIECE),
                    ("Domates", 3, UnitType.PIECE),
                    ("Yeşil Biber", 3, UnitType.PIECE),
                    ("Zeytinyağı", 2, UnitType.TBS),
                    ("Tuz", 1, UnitType.TSP),
                    ("Karabiber", 0.5, UnitType.TSP),
                ],
                "steps": [
                    "Biberleri ince ince doğrayıp yağda yumuşayana kadar kavurun.",
                    "Doğranmış domatesleri ekleyip suyunu biraz çekene kadar pişirin.",
                    "Yumurtaları bir kasede çırpıp tavaya ekleyin.",
                    "Yumurtalar çok kurumadan ocaktan alın."
                ]
            },
            # 3. Karnıyarık
            {
                "title": "Karnıyarık",
                "description": "Patlıcan ve kıymanın enfes uyumu, geleneksel bir ana yemek.",
                "category": "Ana Yemek",
                "difficulty": "Orta",
                "diet_type": "Hepçil",
                "prep_time": 30,
                "cook_time": 30,
                "servings": 4,
                "ingredients": [
                    ("Patlıcan", 4, UnitType.PIECE),
                    ("Dana Kıyma", 200, UnitType.GRAM),
                    ("Soğan", 1, UnitType.PIECE),
                    ("Sarımsak", 2, UnitType.CLOVE),
                    ("Yeşil Biber", 2, UnitType.PIECE),
                    ("Domates Salçası", 1, UnitType.TBS),
                    ("Zeytinyağı", 4, UnitType.TBS),
                    ("Tuz", 1, UnitType.TSP),
                ],
                "steps": [
                    "Patlıcanları alacalı soyup kızartın.",
                    "İç harcı için soğan, kıyma, sarımsak ve biberleri soteleyin.",
                    "Patlıcanların ortasını yarıp kıymalı harcı doldurun.",
                    "Salçalı su hazırlayıp üzerine dökün ve fırında pişirin."
                ]
            },
            # 4. Kısır
            {
                "title": "Hatay Usulü Kısır",
                "description": "Bol ekşili, taze yeşillikli ve lezzetli bir Anadolu mezesi.",
                "category": "Salata / Meze",
                "difficulty": "Kolay",
                "diet_type": "Vegan",
                "prep_time": 20,
                "cook_time": 0,
                "servings": 6,
                "ingredients": [
                    ("Bulgur", 2, UnitType.GLASS_WATER),
                    ("Taze Soğan", 4, UnitType.PIECE),
                    ("Maydanoz", 1, UnitType.BUNCH),
                    ("Dereotu", 0.5, UnitType.BUNCH),
                    ("Domates Salçası", 1, UnitType.TBS),
                    ("Biber Salçası", 1, UnitType.TBS),
                    ("Nar Ekşisi", 3, UnitType.TBS),
                    ("Zeytinyağı", 0.5, UnitType.GLASS_TEA),
                    ("Tuz", 1, UnitType.TSP),
                ],
                "steps": [
                    "Bulguru sıcak suyla ıslatıp şişmesini bekleyin.",
                    "Salçaları ve yağı ekleyip bulgura iyice yedirin.",
                    "İnce kıyılmış yeşillikleri ve nar ekşisini ekleyin.",
                    "Tüm malzemeleri karıştırıp soğuk servis yapın."
                ]
            },
            # 5. Zeytinyağlı Taze Fasulye
            {
                "title": "Zeytinyağlı Taze Fasulye",
                "description": "Hafif, sağlıklı ve tam yaz aylarına uygun bir zeytinyağlı klasiği.",
                "category": "Zeytinyağlı",
                "difficulty": "Kolay",
                "diet_type": "Vegan",
                "prep_time": 15,
                "cook_time": 40,
                "servings": 4,
                "ingredients": [
                    ("Soğan", 1, UnitType.PIECE),
                    ("Domates", 2, UnitType.PIECE),
                    ("Zeytinyağı", 4, UnitType.TBS),
                    ("Toz Şeker", 1, UnitType.TSP),
                    ("Tuz", 1, UnitType.TSP),
                ],
                "steps": [
                    "Fasulyeleri ayıklayıp boyuna kesin.",
                    "Soğanları yemeklik doğrayıp yağda pembeleşene kadar kavurun.",
                    "Domatesleri ve fasulyeleri ekleyin.",
                    "Şeker ve tuzu ekleyip fasulyeler yumuşayana kadar kendi suyunda pişirin."
                ]
            }
        ]
        
        for r_data in recipes_to_add:
            existing = await session.execute(
                select(recipe_repo.__getattribute__('session').bind.__class__).where(recipe_repo.__getattribute__('session').bind.__class__.title == r_data["title"])
            ) if hasattr(recipe_repo, 'get_by_title') else None
            # Simplest check for seeding
            
            print(f"Processing recipe: {r_data['title']}...")
            
            items = []
            for ing_name, amount, unit in r_data["ingredients"]:
                ing = await get_ing(ing_name)
                if ing:
                    items.append(RecipeItem(ingredient=ing, amount=amount, unit=unit))
            
            instructions = []
            for idx, text in enumerate(r_data["steps"]):
                instructions.append(RecipeInstruction(
                    id=str(uuid.uuid4()),
                    step_number=idx + 1,
                    text=text
                ))
            
            recipe = Recipe(
                id=str(uuid.uuid4()),
                title=r_data["title"],
                description=r_data["description"],
                items=items,
                instructions=instructions,
                category=r_data["category"],
                difficulty=r_data["difficulty"],
                diet_type=r_data["diet_type"],
                prep_time_minutes=r_data["prep_time"],
                cook_time_minutes=r_data["cook_time"],
                servings=r_data["servings"],
                status=RecipeStatus.PUBLISHED,
                author_id=admin.id,
                slug=slugify(r_data["title"])
            )
            
            await recipe_repo.save(recipe)
        
        await session.commit()
        print("Successfully seeded all recipes.")

from sqlalchemy import select

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_recipes())
