import asyncio
import sys
import os
import uuid
from datetime import datetime
from slugify import slugify
from sqlalchemy import select

# Add project root to path
sys.path.append(os.getcwd())

from src.adapters.database.postgresql.database import AsyncSessionLocal
from src.adapters.database.postgresql.repositories.recipe_repository import PostgresRecipeRepository
from src.adapters.database.postgresql.repositories.ingredient_repository import PostgresIngredientRepository
from src.adapters.database.postgresql.repositories.user_repository import PostgresUserRepository
from src.domain.entities.recipe import Recipe, RecipeItem, RecipeInstruction, RecipeStatus, RecipeCategory, DifficultyLevel
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
        
        # Mappings for Turkish terms to Domain Enums
        category_map = {
            "Çorba": RecipeCategory.SOUP,
            "Kahvaltılık": RecipeCategory.BREAKFAST,
            "Ana Yemek": RecipeCategory.MAIN_COURSE,
            "Meze": RecipeCategory.APPETIZER,
            "Tatlı": RecipeCategory.DESSERT,
            "Salata": RecipeCategory.SALAD
        }
        
        difficulty_map = {
            "Kolay": DifficultyLevel.EASY,
            "Orta": DifficultyLevel.MEDIUM,
            "Zor": DifficultyLevel.HARD
        }
        
        # Helper to fetch ingredients
        async def get_ing(name):
            ing = await ing_repo.get_by_name(name)
            return ing

        recipes_to_add = [
            {
                "title": "Süzme Mercimek Çorbası",
                "description": "Klasik, pürüzsüz ve besleyici Türk usulü restorant mercimek çorbası.",
                "category": "Çorba",
                "difficulty": "Kolay",
                "diet_type": None,
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
            {
                "title": "Menemen",
                "description": "Kahvaltıların vazgeçilmezi, sulu ve lezzetli domatesli biberli yumurta.",
                "category": "Kahvaltılık",
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
            {
                "title": "Karnıyarık",
                "description": "Patlıcan ve kıymanın enfes uyumu, geleneksel bir ana yemek.",
                "category": "Ana Yemek",
                "difficulty": "Orta",
                "diet_type": None,
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
            {
                "title": "Hatay Usulü Kısır",
                "description": "Bol ekşili, taze yeşillikli ve lezzetli bir Anadolu mezesi.",
                "category": "Meze",
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
            {
                "title": "Zeytinyağlı Taze Fasulye",
                "description": "Hafif, sağlıklı ve tam yaz aylarına uygun bir zeytinyağlı klasiği.",
                "category": "Ana Yemek",
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
            },
            {
                "title": "Ezogelin Çorbası",
                "description": "Anadolu mutfağının en sevilen, bol baharatlı ve doyurucu çorbası.",
                "category": "Çorba",
                "difficulty": "Orta",
                "diet_type": None,
                "prep_time": 10,
                "cook_time": 30,
                "servings": 6,
                "ingredients": [
                    ("Kırmızı Mercimek", 1, UnitType.GLASS_WATER),
                    ("Pirinç", 2, UnitType.TBS),
                    ("Bulgur", 2, UnitType.TBS),
                    ("Domates Salçası", 1, UnitType.TBS),
                    ("Tereyağı", 1, UnitType.TBS),
                    ("Nane", 1, UnitType.TBS),
                    ("Pul Biber", 1, UnitType.TSP),
                    ("Tuz", 1, UnitType.TSP),
                ],
                "steps": [
                    "Mercimek, pirinç ve bulguru yıkayıp tencereye alın.",
                    "Üzerine sıcak su ekleyip tüm bakliyatlar yumuşayana kadar pişirin.",
                    "Ayrı bir tavada tereyağını eritip salça ve baharatları kavurun.",
                    "Sosunu çorbaya ekleyip 5 dakika daha kaynatın."
                ]
            },
            {
                "title": "İzmir Köfte",
                "description": "Fırında patates ve köftenin sosla buluştuğu eşsiz bir lezzet.",
                "category": "Ana Yemek",
                "difficulty": "Orta",
                "diet_type": None,
                "prep_time": 25,
                "cook_time": 40,
                "servings": 4,
                "ingredients": [
                    ("Dana Kıyma", 400, UnitType.GRAM),
                    ("Patates", 3, UnitType.PIECE),
                    ("Soğan", 1, UnitType.PIECE),
                    ("Ekmek", 1, UnitType.PIECE),
                    ("Yumurta", 1, UnitType.PIECE),
                    ("Domates Salçası", 1, UnitType.TBS),
                    ("Tuz", 1, UnitType.TSP),
                    ("Karabiber", 0.5, UnitType.TSP),
                ],
                "steps": [
                    "Kıyma, rendelenmiş soğan, yumurta ve ekmekle köfte harcını yoğurun.",
                    "Patatesleri elma dilim doğrayıp hafifçe kızartın.",
                    "Köftelere şekil verip hafifçe kızartın.",
                    "Fırın tepsisine dizip üzerine salçalı su dökerek fırınlayın."
                ]
            },
            {
                "title": "Tane Tane Pirinç Pilavı",
                "description": "Tam ölçüsünde, asla yapışmayan tereyağlı şehriyeli pilav.",
                "category": "Ana Yemek",
                "difficulty": "Orta",
                "diet_type": "Vejetaryen",
                "prep_time": 20,
                "cook_time": 15,
                "servings": 4,
                "ingredients": [
                    ("Pirinç", 2, UnitType.GLASS_WATER),
                    ("Tereyağı", 2, UnitType.TBS),
                    ("Ayçiçek Yağı", 1, UnitType.TBS),
                    ("Tuz", 1.5, UnitType.TSP),
                ],
                "steps": [
                    "Pirinçleri sıcak tuzlu suda 20 dakika bekletip süzün.",
                    "Yağları tencerede ısıtıp pirinçleri şeffaflaşana kadar kavurun.",
                    "Üzerine 3 su bardağı sıcak su ekleyip suyunu çekene kadar pişirin.",
                    "Demlenmesi için üzerine kağıt havlu koyup 15 dakika bekleyin."
                ]
            },
            {
                "title": "Kabak Mücver",
                "description": "Hafif ve lezzetli, dışı çıtır içi yumuşak kabak kızartması.",
                "category": "Meze",
                "difficulty": "Orta",
                "diet_type": "Vejetaryen",
                "prep_time": 15,
                "cook_time": 15,
                "servings": 4,
                "ingredients": [
                    ("Kabak", 3, UnitType.PIECE),
                    ("Yumurta", 2, UnitType.PIECE),
                    ("Un", 3, UnitType.TBS),
                    ("Beyaz Peynir", 100, UnitType.GRAM),
                    ("Dereotu", 0.5, UnitType.BUNCH),
                    ("Tuz", 1, UnitType.TSP),
                ],
                "steps": [
                    "Kabakları rendeleyip suyunu iyice sıkın.",
                    "Diğer tüm malzemeleri geniş bir kapta karıştırın.",
                    "Kızgın yağda kaşıkla dökerek arkalı önlü kızartın."
                ]
            },
            {
                "title": "Şakşuka",
                "description": "Kızarmış sebzelerin sarımsaklı domates sosuyla buluştuğu klasik meze.",
                "category": "Meze",
                "difficulty": "Kolay",
                "diet_type": "Vegan",
                "prep_time": 15,
                "cook_time": 20,
                "servings": 4,
                "ingredients": [
                    ("Patlıcan", 2, UnitType.PIECE),
                    ("Kabak", 1, UnitType.PIECE),
                    ("Patates", 1, UnitType.PIECE),
                    ("Domates", 3, UnitType.PIECE),
                    ("Sarımsak", 3, UnitType.CLOVE),
                    ("Zeytinyağı", 0.5, UnitType.GLASS_WATER),
                ],
                "steps": [
                    "Tüm sebzeleri küp küp doğrayıp sırasıyla kızartın.",
                    "Sos tavasında sarımsaklı domates sosunu hazırlayın.",
                    "Sebzeleri sosla harmanlayıp servis yapın."
                ]
            },
            {
                "title": "Lübnan Usulü Humus",
                "description": "İpeksi kıvamda, bol tahinli ve sarımsaklı nohut ezmesi.",
                "category": "Meze",
                "difficulty": "Kolay",
                "diet_type": "Vegan",
                "prep_time": 15,
                "cook_time": 0,
                "servings": 4,
                "ingredients": [
                    ("Nohut", 2, UnitType.GLASS_WATER),
                    ("Tahin", 0.5, UnitType.GLASS_TEA),
                    ("Sarımsak", 2, UnitType.CLOVE),
                    ("Limon Suyu", 0.5, UnitType.PIECE),
                    ("Kimyon", 1, UnitType.TSP),
                    ("Zeytinyağı", 2, UnitType.TBS),
                ],
                "steps": [
                    "Haşlanmış nohutların kabuklarını ayıklayın.",
                    "Blenderda tüm malzemeleri pürüzsüz olana kadar geçirin.",
                    "Üzerine zeytinyağı ve pul biber ekleyerek servis yapın."
                ]
            },
            {
                "title": "Klasik Türk Cacığı",
                "description": "Sarımsaklı, naneli ve buz gibi ferahlatıcı yoğurt garnitürü.",
                "category": "Meze",
                "difficulty": "Kolay",
                "diet_type": "Vejetaryen",
                "prep_time": 10,
                "cook_time": 0,
                "servings": 2,
                "ingredients": [
                    ("Yoğurt", 2, UnitType.GLASS_WATER),
                    ("Salatalık", 2, UnitType.PIECE),
                    ("Sarımsak", 1, UnitType.CLOVE),
                    ("Nane", 1, UnitType.TSP),
                    ("Zeytinyağı", 1, UnitType.TBS),
                ],
                "steps": [
                    "Salatalıkları rendeleyin veya minik küpler halinde doğrayın.",
                    "Yoğurdu suyla hafifçe inceltin, sarımsak ekleyin.",
                    "Tüm malzemeleri karıştırıp üzerine kuru nane ve zeytinyağı dökün."
                ]
            },
            {
                "title": "Renkli Biberli Tavuk Sote",
                "description": "Hızlı, pratik ve bol proteinli bir akşam yemeği alternatifi.",
                "category": "Ana Yemek",
                "difficulty": "Kolay",
                "diet_type": None,
                "prep_time": 10,
                "cook_time": 15,
                "servings": 2,
                "ingredients": [
                    ("Tavuk Göğsü", 400, UnitType.GRAM),
                    ("Mantar", 100, UnitType.GRAM),
                    ("Yeşil Biber", 2, UnitType.PIECE),
                    ("Kırmızı Biber", 1, UnitType.PIECE),
                    ("Domates", 1, UnitType.PIECE),
                    ("Ayçiçek Yağı", 2, UnitType.TBS),
                ],
                "steps": [
                    "Tavukları küp küp doğrayıp yüksek ateşte soteleyin.",
                    "Sebzeleri ekleyip sotelemeye devam edin.",
                    "Domatesleri ekleyip suyunu çekene kadar pişirin."
                ]
            },
            {
                "title": "Yayla Çorbası",
                "description": "Midenize dost, yoğurtlu ve naneli ferahlatıcı Anadolu çorbası.",
                "category": "Çorba",
                "difficulty": "Kolay",
                "diet_type": "Vejetaryen",
                "prep_time": 5,
                "cook_time": 20,
                "servings": 4,
                "ingredients": [
                    ("Yoğurt", 1.5, UnitType.GLASS_WATER),
                    ("Pirinç", 2, UnitType.TBS),
                    ("Yumurta", 1, UnitType.PIECE),
                    ("Un", 1, UnitType.TBS),
                    ("Nane", 1, UnitType.TBS),
                    ("Tereyağı", 1, UnitType.TBS),
                ],
                "steps": [
                    "Pirinçleri haşlayın.",
                    "Yoğurt, un ve yumurtayı çırpıp terbiye hazırlayın.",
                    "Terbiyeye çorbanın suyundan ekleyip ılıştırarak tencereye dökün.",
                    "Nane ve tereyağını kızdırıp üzerine gezdirin."
                ]
            },
            {
                "title": "Spaghetti Carbonara",
                "description": "Orijinal İtalyan tarifi: Krema yok, sadece yumurta ve peynirin büyüsü.",
                "category": "Ana Yemek",
                "difficulty": "Orta",
                "diet_type": None,
                "prep_time": 10,
                "cook_time": 10,
                "servings": 2,
                "ingredients": [
                    ("Makarna", 250, UnitType.GRAM),
                    ("Yumurta", 2, UnitType.PIECE),
                    ("Kaşar Peyniri", 50, UnitType.GRAM),
                    ("Karabiber", 1, UnitType.TSP),
                ],
                "steps": [
                    "Makarnayı al dente haşlayın.",
                    "Yumurta ve peyniri çırpıp sosu hazırlayın.",
                    "Sıcak makarnayla sosu hızlıca harmanlayın (yumurtanın pişmemesi için ateşten alın)."
                ]
            }
        ]
        
        for r_data in recipes_to_add:
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
            
            # Map strings to Domain Enums
            category_enum = category_map.get(r_data["category"])
            difficulty_enum = difficulty_map.get(r_data["difficulty"])
            
            recipe = Recipe(
                id=str(uuid.uuid4()),
                title=r_data["title"],
                description=r_data["description"],
                items=items,
                instructions=instructions,
                category=category_enum,
                difficulty=difficulty_enum,
                diet_type=r_data["diet_type"],
                prep_time_minutes=r_data["prep_time"],
                cook_time_minutes=r_data["cook_time"],
                servings=r_data["servings"],
                status=RecipeStatus.PUBLISHED,
                author_id=admin.id,
                slug=slugify(r_data["title"]) + "-" + str(uuid.uuid4())[:4]
            )
            
            await recipe_repo.save(recipe)
        
        await session.commit()
        print("Successfully seeded all 15 recipes with standardized Enum categories.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_recipes())
