import asyncio
import sys
import os
import uuid
from slugify import slugify

# Add project root to path
sys.path.append(os.getcwd())

from src.adapters.database.postgresql.database import AsyncSessionLocal
from src.adapters.database.postgresql.repositories.ingredient_repository import PostgresIngredientRepository
from src.domain.entities.ingredient import Ingredient

INGREDIENTS_DATA = [
    # Yağlar (Oils)
    {"name": "Zeytinyağı", "calories": 884, "protein": 0, "fat": 100, "carbs": 0, "density": 0.92, "avg_weight": 920.0}, # Paket/Şişe bazı 
    {"name": "Tereyağı", "calories": 717, "protein": 0.8, "fat": 81, "carbs": 0.1, "density": 0.91, "avg_weight": 250.0},
    {"name": "Ayçiçek Yağı", "calories": 884, "protein": 0, "fat": 100, "carbs": 0, "density": 0.92, "avg_weight": 920.0},
    
    # Sebzeler (Vegetables)
    {"name": "Domates", "calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9, "density": 0.94, "avg_weight": 110.0},
    {"name": "Soğan", "calories": 40, "protein": 1.1, "fat": 0.1, "carbs": 9.3, "density": 0.90, "avg_weight": 100.0},
    {"name": "Sarımsak", "calories": 149, "protein": 6.4, "fat": 0.5, "carbs": 33, "density": 0.60, "avg_weight": 5.0}, # 1 Diş ortalama
    {"name": "Patates", "calories": 77, "protein": 2, "fat": 0.1, "carbs": 17, "density": 0.75, "avg_weight": 150.0},
    {"name": "Havuç", "calories": 41, "protein": 0.9, "fat": 0.2, "carbs": 9.6, "density": 0.64, "avg_weight": 70.0},
    {"name": "Patlıcan", "calories": 25, "protein": 1, "fat": 0.2, "carbs": 6, "density": 0.60, "avg_weight": 200.0},
    {"name": "Kabak", "calories": 17, "protein": 1.2, "fat": 0.3, "carbs": 3.1, "density": 0.65, "avg_weight": 150.0},
    {"name": "Yeşil Biber", "calories": 20, "protein": 0.9, "fat": 0.2, "carbs": 4.6, "density": 0.50, "avg_weight": 20.0},
    {"name": "Kırmızı Biber", "calories": 31, "protein": 1, "fat": 0.3, "carbs": 6, "density": 0.55, "avg_weight": 100.0},
    {"name": "Ispanak", "calories": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6, "density": 0.40, "avg_weight": 500.0}, # Paket/Demet
    {"name": "Maydanoz", "calories": 36, "protein": 3, "fat": 0.8, "carbs": 6, "density": 0.35, "avg_weight": 50.0},
    {"name": "Dereotu", "calories": 43, "protein": 3.5, "fat": 1.1, "carbs": 7, "density": 0.35, "avg_weight": 50.0},
    {"name": "Taze Soğan", "calories": 32, "protein": 1.8, "fat": 0.2, "carbs": 7.3, "density": 0.40, "avg_weight": 15.0},
    {"name": "Mantar", "calories": 22, "protein": 3.1, "fat": 0.3, "carbs": 3.3, "density": 0.50, "avg_weight": 20.0},
    {"name": "Salatalık", "calories": 15, "protein": 0.7, "fat": 0.1, "carbs": 3.6, "density": 0.96, "avg_weight": 120.0},
    {"name": "Karnabahar", "calories": 25, "protein": 1.9, "fat": 0.3, "carbs": 5, "density": 0.45, "avg_weight": 800.0},
    {"name": "Brokoli", "calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 7, "density": 0.45, "avg_weight": 400.0},
    
    # Meyveler (Fruits)
    {"name": "Limon", "calories": 29, "protein": 1.1, "fat": 0.3, "carbs": 9, "density": 1.03, "avg_weight": 100.0},
    {"name": "Elma", "calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14, "density": 0.80, "avg_weight": 150.0},
    {"name": "Muz", "calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23, "density": 0.90, "avg_weight": 120.0},
    {"name": "Portakal", "calories": 47, "protein": 0.9, "fat": 0.1, "carbs": 12, "density": 0.95, "avg_weight": 180.0},
    
    # Süt/Peynir/Yumurta (Dairy/Eggs)
    {"name": "Yumurta", "calories": 155, "protein": 13, "fat": 11, "carbs": 1.1, "density": 1.02, "avg_weight": 55.0},
    {"name": "Süt", "calories": 60, "protein": 3.2, "fat": 3.2, "carbs": 4.8, "density": 1.03, "avg_weight": 1000.0},
    {"name": "Yoğurt", "calories": 61, "protein": 3.5, "fat": 3.3, "carbs": 4.7, "density": 1.05, "avg_weight": 500.0},
    {"name": "Beyaz Peynir", "calories": 250, "protein": 15, "fat": 20, "carbs": 2.5, "density": 1.00, "avg_weight": 500.0},
    {"name": "Kaşar Peyniri", "calories": 350, "protein": 25, "fat": 27, "carbs": 2, "density": 1.00, "avg_weight": 250.0},
    {"name": "Süzme Yoğurt", "calories": 97, "protein": 10, "fat": 5, "carbs": 3, "density": 1.06, "avg_weight": 500.0},
    {"name": "Krema", "calories": 196, "protein": 2.1, "fat": 19, "carbs": 3.7, "density": 1.00, "avg_weight": 200.0},
    
    # Etler (Meats)
    {"name": "Dana Kıyma", "calories": 250, "protein": 26, "fat": 17, "carbs": 0, "density": 1.00, "avg_weight": 500.0},
    {"name": "Dana Kuşbaşı", "calories": 200, "protein": 28, "fat": 10, "carbs": 0, "density": 1.02, "avg_weight": 500.0},
    {"name": "Tavuk Göğsü", "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "density": 1.04, "avg_weight": 250.0},
    {"name": "Tavuk But", "calories": 209, "protein": 26, "fat": 11, "carbs": 0, "density": 1.05, "avg_weight": 200.0},
    {"name": "Kuzu Eti", "calories": 294, "protein": 25, "fat": 21, "carbs": 0, "density": 1.00, "avg_weight": 500.0},
    {"name": "Sucuk", "calories": 400, "protein": 15, "fat": 35, "carbs": 2, "density": 1.00, "avg_weight": 250.0},
    
    # Tahıl/Baklagiller (Dry Goods)
    {"name": "Un", "calories": 364, "protein": 10, "fat": 1, "carbs": 76, "density": 0.55, "avg_weight": 1000.0},
    {"name": "Toz Şeker", "calories": 387, "protein": 0, "fat": 0, "carbs": 100, "density": 0.85, "avg_weight": 1000.0},
    {"name": "Pirinç", "calories": 365, "protein": 7.1, "fat": 0.7, "carbs": 80, "density": 0.82, "avg_weight": 1000.0},
    {"name": "Bulgur", "calories": 342, "protein": 12, "fat": 1.3, "carbs": 76, "density": 0.80, "avg_weight": 1000.0},
    {"name": "Kırmızı Mercimek", "calories": 353, "protein": 24, "fat": 1.1, "carbs": 54, "density": 0.85, "avg_weight": 1000.0},
    {"name": "Makarna", "calories": 370, "protein": 13, "fat": 1.5, "carbs": 75, "density": 0.50, "avg_weight": 500.0}, # Paket
    {"name": "Nohut", "calories": 364, "protein": 19, "fat": 6, "carbs": 61, "density": 0.80, "avg_weight": 1000.0},
    {"name": "Kuru Fasulye", "calories": 333, "protein": 23, "fat": 0.8, "carbs": 60, "density": 0.80, "avg_weight": 1000.0},
    {"name": "İrmik", "calories": 360, "protein": 12, "fat": 1, "carbs": 73, "density": 0.70, "avg_weight": 500.0},
    {"name": "Nişasta", "calories": 381, "protein": 0.3, "fat": 0.1, "carbs": 91, "density": 0.60, "avg_weight": 200.0},
    
    # Salçalar/Sıvılar (Condiments)
    {"name": "Domates Salçası", "calories": 82, "protein": 4.3, "fat": 0.5, "carbs": 18.9, "density": 1.10, "avg_weight": 830.0},
    {"name": "Biber Salçası", "calories": 95, "protein": 3.5, "fat": 1.2, "carbs": 16.5, "density": 1.15, "avg_weight": 830.0},
    {"name": "Nar Ekşisi", "calories": 300, "protein": 0, "fat": 0, "carbs": 75, "density": 1.20, "avg_weight": 250.0},
    {"name": "Sirke", "calories": 18, "protein": 0, "fat": 0, "carbs": 0.9, "density": 1.01, "avg_weight": 500.0},
    {"name": "Soya Sosu", "calories": 53, "protein": 8, "fat": 0.1, "carbs": 5, "density": 1.10, "avg_weight": 250.0},
    
    # Baharatlar (Spices)
    {"name": "Tuz", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 1.20, "avg_weight": 500.0},
    {"name": "Karabiber", "calories": 251, "protein": 10, "fat": 3, "carbs": 64, "density": 0.50, "avg_weight": 100.0},
    {"name": "Pul Biber", "calories": 282, "protein": 12, "fat": 10, "carbs": 50, "density": 0.45, "avg_weight": 100.0},
    {"name": "Kimyon", "calories": 375, "protein": 18, "fat": 22, "carbs": 44, "density": 0.45, "avg_weight": 100.0},
    {"name": "Kekik", "calories": 101, "protein": 6, "fat": 4, "carbs": 24, "density": 0.25, "avg_weight": 50.0},
    {"name": "Nane", "calories": 285, "protein": 20, "fat": 6, "carbs": 52, "density": 0.25, "avg_weight": 50.0},
    {"name": "Kuru Maya", "calories": 325, "protein": 40, "fat": 7, "carbs": 40, "density": 0.80, "avg_weight": 10.0}, # Paket
    {"name": "Kabartma Tozu", "calories": 100, "protein": 0, "fat": 0, "carbs": 25, "density": 0.90, "avg_weight": 10.0}, # Paket
    {"name": "Vanilya", "calories": 30, "protein": 0, "fat": 0, "carbs": 12, "density": 0.90, "avg_weight": 5.0}, # Paket
    {"name": "Sumak", "calories": 349, "protein": 12, "fat": 19, "carbs": 38, "density": 0.50, "avg_weight": 100.0},
    {"name": "Tatlı Toz Biber", "calories": 282, "protein": 14, "fat": 13, "carbs": 54, "density": 0.45, "avg_weight": 100.0},
    
    # Kuruyemiş (Nuts)
    {"name": "Ceviz İçi", "calories": 654, "protein": 15, "fat": 65, "carbs": 14, "density": 0.45, "avg_weight": 5.0},
    {"name": "Fındık İçi", "calories": 628, "protein": 15, "fat": 61, "carbs": 17, "density": 0.50, "avg_weight": 1.5},
    {"name": "Badem İçi", "calories": 579, "protein": 21, "fat": 49, "carbs": 22, "density": 0.50, "avg_weight": 1.2},
    {"name": "Antep Fıstığı", "calories": 560, "protein": 20, "fat": 45, "carbs": 27, "density": 0.50, "avg_weight": 1.0},
]

async def seed_ingredients():
    print("Connecting to database...")
    async with AsyncSessionLocal() as session:
        repo = PostgresIngredientRepository(session)
        
        for data in INGREDIENTS_DATA:
            existing = await repo.get_by_name(data["name"])
            if existing:
                print(f"Ingredient '{data['name']}' already exists. Skipping.")
                continue
            
            print(f"Adding ingredient: {data['name']}...")
            ingredient = Ingredient(
                id=str(uuid.uuid4()),
                name=data["name"],
                calories_per_100g=data["calories"],
                protein_per_100g=data["protein"],
                fat_per_100g=data["fat"],
                carbs_per_100g=data["carbs"],
                density_g_ml=data["density"],
                avg_weight_per_piece_g=data["avg_weight"],
                slug=slugify(data["name"])
            )
            await repo.save(ingredient)
        
        await session.commit()
        print("Successfully seeded all ingredients.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_ingredients())
