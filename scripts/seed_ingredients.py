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
    # ===== YAĞLAR (Oils & Fats) =====
    {"name": "Zeytinyağı", "calories": 884, "protein": 0, "fat": 100, "carbs": 0, "density": 0.92, "avg_weight": 920.0},
    {"name": "Tereyağı", "calories": 717, "protein": 0.8, "fat": 81, "carbs": 0.1, "density": 0.91, "avg_weight": 250.0},
    {"name": "Ayçiçek Yağı", "calories": 884, "protein": 0, "fat": 100, "carbs": 0, "density": 0.92, "avg_weight": 920.0},
    {"name": "Margarin", "calories": 719, "protein": 0.2, "fat": 80, "carbs": 0.7, "density": 0.90, "avg_weight": 250.0},
    {"name": "Susam Yağı", "calories": 884, "protein": 0, "fat": 100, "carbs": 0, "density": 0.92, "avg_weight": 250.0},
    {"name": "Hindistan Cevizi Yağı", "calories": 862, "protein": 0, "fat": 100, "carbs": 0, "density": 0.93, "avg_weight": 250.0},

    # ===== SEBZELER (Vegetables) =====
    {"name": "Domates", "calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9, "density": 0.94, "avg_weight": 110.0},
    {"name": "Soğan", "calories": 40, "protein": 1.1, "fat": 0.1, "carbs": 9.3, "density": 0.90, "avg_weight": 100.0},
    {"name": "Sarımsak", "calories": 149, "protein": 6.4, "fat": 0.5, "carbs": 33, "density": 0.60, "avg_weight": 5.0},
    {"name": "Patates", "calories": 77, "protein": 2, "fat": 0.1, "carbs": 17, "density": 0.75, "avg_weight": 150.0},
    {"name": "Havuç", "calories": 41, "protein": 0.9, "fat": 0.2, "carbs": 9.6, "density": 0.64, "avg_weight": 70.0},
    {"name": "Patlıcan", "calories": 25, "protein": 1, "fat": 0.2, "carbs": 6, "density": 0.60, "avg_weight": 200.0},
    {"name": "Kabak", "calories": 17, "protein": 1.2, "fat": 0.3, "carbs": 3.1, "density": 0.65, "avg_weight": 150.0},
    {"name": "Yeşil Biber", "calories": 20, "protein": 0.9, "fat": 0.2, "carbs": 4.6, "density": 0.50, "avg_weight": 20.0},
    {"name": "Kırmızı Biber", "calories": 31, "protein": 1, "fat": 0.3, "carbs": 6, "density": 0.55, "avg_weight": 100.0},
    {"name": "Ispanak", "calories": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6, "density": 0.40, "avg_weight": 500.0},
    {"name": "Maydanoz", "calories": 36, "protein": 3, "fat": 0.8, "carbs": 6, "density": 0.35, "avg_weight": 50.0},
    {"name": "Dereotu", "calories": 43, "protein": 3.5, "fat": 1.1, "carbs": 7, "density": 0.35, "avg_weight": 50.0},
    {"name": "Taze Soğan", "calories": 32, "protein": 1.8, "fat": 0.2, "carbs": 7.3, "density": 0.40, "avg_weight": 15.0},
    {"name": "Mantar", "calories": 22, "protein": 3.1, "fat": 0.3, "carbs": 3.3, "density": 0.50, "avg_weight": 20.0},
    {"name": "Salatalık", "calories": 15, "protein": 0.7, "fat": 0.1, "carbs": 3.6, "density": 0.96, "avg_weight": 120.0},
    {"name": "Karnabahar", "calories": 25, "protein": 1.9, "fat": 0.3, "carbs": 5, "density": 0.45, "avg_weight": 800.0},
    {"name": "Brokoli", "calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 7, "density": 0.45, "avg_weight": 400.0},
    {"name": "Marul", "calories": 15, "protein": 1.4, "fat": 0.2, "carbs": 2.9, "density": 0.30, "avg_weight": 300.0},
    {"name": "Roka", "calories": 25, "protein": 2.6, "fat": 0.7, "carbs": 3.7, "density": 0.30, "avg_weight": 50.0},
    {"name": "Lahana", "calories": 25, "protein": 1.3, "fat": 0.1, "carbs": 6, "density": 0.38, "avg_weight": 1000.0},
    {"name": "Kırmızı Lahana", "calories": 31, "protein": 1.4, "fat": 0.2, "carbs": 7, "density": 0.40, "avg_weight": 1000.0},
    {"name": "Kereviz", "calories": 14, "protein": 0.7, "fat": 0.2, "carbs": 3, "density": 0.60, "avg_weight": 400.0},
    {"name": "Pirasa", "calories": 61, "protein": 1.5, "fat": 0.3, "carbs": 14, "density": 0.55, "avg_weight": 150.0},
    {"name": "Enginar", "calories": 47, "protein": 3.3, "fat": 0.2, "carbs": 11, "density": 0.60, "avg_weight": 300.0},
    {"name": "Bezelye", "calories": 81, "protein": 5.4, "fat": 0.4, "carbs": 14, "density": 0.75, "avg_weight": 7.0},
    {"name": "Taze Fasulye", "calories": 31, "protein": 1.8, "fat": 0.1, "carbs": 7, "density": 0.55, "avg_weight": 8.0},
    {"name": "Bamya", "calories": 33, "protein": 1.9, "fat": 0.2, "carbs": 7, "density": 0.50, "avg_weight": 10.0},
    {"name": "Turp", "calories": 16, "protein": 0.7, "fat": 0.1, "carbs": 3.4, "density": 0.60, "avg_weight": 30.0},
    {"name": "Pancar", "calories": 43, "protein": 1.6, "fat": 0.2, "carbs": 10, "density": 0.90, "avg_weight": 200.0},
    {"name": "Kurutulmuş Domates", "calories": 258, "protein": 14, "fat": 3, "carbs": 56, "density": 0.45, "avg_weight": 200.0},
    {"name": "Kapari", "calories": 23, "protein": 2.4, "fat": 0.9, "carbs": 1.7, "density": 1.00, "avg_weight": 100.0},
    {"name": "Zeytin (Siyah)", "calories": 115, "protein": 0.8, "fat": 11, "carbs": 6, "density": 0.90, "avg_weight": 4.0},
    {"name": "Zeytin (Yeşil)", "calories": 145, "protein": 1, "fat": 15, "carbs": 3.8, "density": 0.90, "avg_weight": 4.0},
    {"name": "Kornişon Turşu", "calories": 14, "protein": 0.4, "fat": 0.2, "carbs": 2.3, "density": 1.00, "avg_weight": 10.0},
    {"name": "Mısır (Konserve)", "calories": 86, "protein": 3.3, "fat": 1.4, "carbs": 19, "density": 0.90, "avg_weight": 300.0},
    {"name": "Biber (Közlenmiş)", "calories": 28, "protein": 0.9, "fat": 0.2, "carbs": 6, "density": 0.85, "avg_weight": 100.0},
    {"name": "Avokado", "calories": 160, "protein": 2, "fat": 15, "carbs": 9, "density": 0.65, "avg_weight": 200.0},
    {"name": "Tatlı Patates", "calories": 86, "protein": 1.6, "fat": 0.1, "carbs": 20, "density": 0.75, "avg_weight": 200.0},
    {"name": "Semizotu", "calories": 20, "protein": 2, "fat": 0.4, "carbs": 3.4, "density": 0.35, "avg_weight": 50.0},
    {"name": "Pazı", "calories": 19, "protein": 1.8, "fat": 0.2, "carbs": 3.7, "density": 0.40, "avg_weight": 500.0},
    {"name": "Kuşkonmaz", "calories": 20, "protein": 2.2, "fat": 0.1, "carbs": 3.9, "density": 0.50, "avg_weight": 15.0},

    # ===== MEYVELER (Fruits) =====
    {"name": "Limon", "calories": 29, "protein": 1.1, "fat": 0.3, "carbs": 9, "density": 1.03, "avg_weight": 100.0},
    {"name": "Elma", "calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14, "density": 0.80, "avg_weight": 150.0},
    {"name": "Muz", "calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23, "density": 0.90, "avg_weight": 120.0},
    {"name": "Portakal", "calories": 47, "protein": 0.9, "fat": 0.1, "carbs": 12, "density": 0.95, "avg_weight": 180.0},
    {"name": "Çilek", "calories": 32, "protein": 0.7, "fat": 0.3, "carbs": 8, "density": 0.55, "avg_weight": 12.0},
    {"name": "Vişne", "calories": 50, "protein": 1, "fat": 0.3, "carbs": 12, "density": 0.90, "avg_weight": 5.0},
    {"name": "Nar", "calories": 83, "protein": 1.7, "fat": 1.2, "carbs": 19, "density": 0.90, "avg_weight": 250.0},
    {"name": "Kayısı", "calories": 48, "protein": 1.4, "fat": 0.4, "carbs": 11, "density": 0.80, "avg_weight": 40.0},
    {"name": "Şeftali", "calories": 39, "protein": 0.9, "fat": 0.3, "carbs": 10, "density": 0.80, "avg_weight": 150.0},
    {"name": "Üzüm", "calories": 69, "protein": 0.7, "fat": 0.2, "carbs": 18, "density": 0.65, "avg_weight": 5.0},
    {"name": "Karpuz", "calories": 30, "protein": 0.6, "fat": 0.2, "carbs": 8, "density": 0.92, "avg_weight": 5000.0},
    {"name": "Kavun", "calories": 34, "protein": 0.8, "fat": 0.2, "carbs": 8, "density": 0.90, "avg_weight": 2000.0},
    {"name": "Armut", "calories": 57, "protein": 0.4, "fat": 0.1, "carbs": 15, "density": 0.80, "avg_weight": 170.0},
    {"name": "Mandalina", "calories": 53, "protein": 0.8, "fat": 0.3, "carbs": 13, "density": 0.95, "avg_weight": 80.0},
    {"name": "Greyfurt", "calories": 42, "protein": 0.8, "fat": 0.1, "carbs": 11, "density": 0.95, "avg_weight": 250.0},
    {"name": "Hurma", "calories": 277, "protein": 1.8, "fat": 0.2, "carbs": 75, "density": 0.90, "avg_weight": 8.0},
    {"name": "İncir (Taze)", "calories": 74, "protein": 0.8, "fat": 0.3, "carbs": 19, "density": 0.80, "avg_weight": 50.0},
    {"name": "İncir (Kuru)", "calories": 249, "protein": 3.3, "fat": 0.9, "carbs": 64, "density": 0.60, "avg_weight": 15.0},
    {"name": "Kuru Üzüm", "calories": 299, "protein": 3.1, "fat": 0.5, "carbs": 79, "density": 0.70, "avg_weight": 3.0},
    {"name": "Kuru Kayısı", "calories": 241, "protein": 3.4, "fat": 0.5, "carbs": 63, "density": 0.60, "avg_weight": 8.0},

    # ===== SÜT ÜRÜNLERİ / YUMURTA (Dairy & Eggs) =====
    {"name": "Yumurta", "calories": 155, "protein": 13, "fat": 11, "carbs": 1.1, "density": 1.02, "avg_weight": 55.0},
    {"name": "Süt", "calories": 60, "protein": 3.2, "fat": 3.2, "carbs": 4.8, "density": 1.03, "avg_weight": 1000.0},
    {"name": "Yoğurt", "calories": 61, "protein": 3.5, "fat": 3.3, "carbs": 4.7, "density": 1.05, "avg_weight": 500.0},
    {"name": "Beyaz Peynir", "calories": 250, "protein": 15, "fat": 20, "carbs": 2.5, "density": 1.00, "avg_weight": 500.0},
    {"name": "Kaşar Peyniri", "calories": 350, "protein": 25, "fat": 27, "carbs": 2, "density": 1.00, "avg_weight": 250.0},
    {"name": "Süzme Yoğurt", "calories": 97, "protein": 10, "fat": 5, "carbs": 3, "density": 1.06, "avg_weight": 500.0},
    {"name": "Krema", "calories": 196, "protein": 2.1, "fat": 19, "carbs": 3.7, "density": 1.00, "avg_weight": 200.0},
    {"name": "Lor Peyniri", "calories": 71, "protein": 11, "fat": 1, "carbs": 4, "density": 1.00, "avg_weight": 500.0},
    {"name": "Tulum Peyniri", "calories": 350, "protein": 22, "fat": 28, "carbs": 2, "density": 1.00, "avg_weight": 500.0},
    {"name": "Mozzarella", "calories": 280, "protein": 28, "fat": 17, "carbs": 3.1, "density": 1.00, "avg_weight": 125.0},
    {"name": "Labne", "calories": 150, "protein": 8, "fat": 11, "carbs": 4, "density": 1.05, "avg_weight": 200.0},
    {"name": "Çökelek", "calories": 98, "protein": 18, "fat": 1, "carbs": 4, "density": 1.00, "avg_weight": 500.0},
    {"name": "Parmesan", "calories": 431, "protein": 38, "fat": 29, "carbs": 4, "density": 1.00, "avg_weight": 250.0},
    {"name": "Kefir", "calories": 60, "protein": 3.3, "fat": 3.5, "carbs": 4, "density": 1.03, "avg_weight": 500.0},

    # ===== ETLER (Meats) =====
    {"name": "Dana Kıyma", "calories": 250, "protein": 26, "fat": 17, "carbs": 0, "density": 1.00, "avg_weight": 500.0},
    {"name": "Dana Kuşbaşı", "calories": 200, "protein": 28, "fat": 10, "carbs": 0, "density": 1.02, "avg_weight": 500.0},
    {"name": "Tavuk Göğsü", "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "density": 1.04, "avg_weight": 250.0},
    {"name": "Tavuk But", "calories": 209, "protein": 26, "fat": 11, "carbs": 0, "density": 1.05, "avg_weight": 200.0},
    {"name": "Kuzu Eti", "calories": 294, "protein": 25, "fat": 21, "carbs": 0, "density": 1.00, "avg_weight": 500.0},
    {"name": "Sucuk", "calories": 400, "protein": 15, "fat": 35, "carbs": 2, "density": 1.00, "avg_weight": 250.0},
    {"name": "Pastırma", "calories": 234, "protein": 38, "fat": 10, "carbs": 0, "density": 1.00, "avg_weight": 200.0},
    {"name": "Salam", "calories": 300, "protein": 12, "fat": 28, "carbs": 1, "density": 1.00, "avg_weight": 250.0},
    {"name": "Sosis", "calories": 313, "protein": 11, "fat": 28, "carbs": 3.5, "density": 1.00, "avg_weight": 40.0},
    {"name": "Bütün Tavuk", "calories": 215, "protein": 18, "fat": 15, "carbs": 0, "density": 1.05, "avg_weight": 1800.0},
    {"name": "Tavuk Kanat", "calories": 203, "protein": 30, "fat": 8, "carbs": 0, "density": 1.05, "avg_weight": 50.0},
    {"name": "Dana Bonfile", "calories": 218, "protein": 26, "fat": 12, "carbs": 0, "density": 1.02, "avg_weight": 200.0},
    {"name": "Kuzu Pirzola", "calories": 282, "protein": 26, "fat": 19, "carbs": 0, "density": 1.00, "avg_weight": 80.0},
    {"name": "Kavurma", "calories": 300, "protein": 22, "fat": 23, "carbs": 0, "density": 1.00, "avg_weight": 250.0},

    # ===== DENİZ ÜRÜNLERİ (Seafood) =====
    {"name": "Somon", "calories": 208, "protein": 20, "fat": 13, "carbs": 0, "density": 1.05, "avg_weight": 200.0},
    {"name": "Levrek", "calories": 97, "protein": 18, "fat": 2, "carbs": 0, "density": 1.05, "avg_weight": 300.0},
    {"name": "Çupra", "calories": 100, "protein": 19, "fat": 2.5, "carbs": 0, "density": 1.05, "avg_weight": 300.0},
    {"name": "Hamsi", "calories": 131, "protein": 20, "fat": 5, "carbs": 0, "density": 1.05, "avg_weight": 10.0},
    {"name": "Karides", "calories": 99, "protein": 24, "fat": 0.3, "carbs": 0.2, "density": 1.05, "avg_weight": 8.0},
    {"name": "Kalamar", "calories": 92, "protein": 15, "fat": 1.4, "carbs": 3, "density": 1.05, "avg_weight": 150.0},
    {"name": "Midye", "calories": 86, "protein": 12, "fat": 2.2, "carbs": 3.7, "density": 1.05, "avg_weight": 10.0},
    {"name": "Ton Balığı (Konserve)", "calories": 116, "protein": 26, "fat": 0.8, "carbs": 0, "density": 1.00, "avg_weight": 160.0},
    {"name": "Sardalya", "calories": 208, "protein": 25, "fat": 11, "carbs": 0, "density": 1.05, "avg_weight": 30.0},
    {"name": "Alabalık", "calories": 119, "protein": 20, "fat": 3.5, "carbs": 0, "density": 1.05, "avg_weight": 250.0},
    {"name": "Palamut", "calories": 140, "protein": 22, "fat": 5, "carbs": 0, "density": 1.05, "avg_weight": 350.0},
    {"name": "Lüfer", "calories": 124, "protein": 20, "fat": 4.2, "carbs": 0, "density": 1.05, "avg_weight": 300.0},
    {"name": "Ahtapot", "calories": 82, "protein": 15, "fat": 1, "carbs": 2.2, "density": 1.05, "avg_weight": 500.0},

    # ===== TAHILLAR / BAKLAGİLLER (Grains & Legumes) =====
    {"name": "Un", "calories": 364, "protein": 10, "fat": 1, "carbs": 76, "density": 0.55, "avg_weight": 1000.0},
    {"name": "Toz Şeker", "calories": 387, "protein": 0, "fat": 0, "carbs": 100, "density": 0.85, "avg_weight": 1000.0},
    {"name": "Pirinç", "calories": 365, "protein": 7.1, "fat": 0.7, "carbs": 80, "density": 0.82, "avg_weight": 1000.0},
    {"name": "Bulgur", "calories": 342, "protein": 12, "fat": 1.3, "carbs": 76, "density": 0.80, "avg_weight": 1000.0},
    {"name": "Kırmızı Mercimek", "calories": 353, "protein": 24, "fat": 1.1, "carbs": 54, "density": 0.85, "avg_weight": 1000.0},
    {"name": "Makarna", "calories": 370, "protein": 13, "fat": 1.5, "carbs": 75, "density": 0.50, "avg_weight": 500.0},
    {"name": "Nohut", "calories": 364, "protein": 19, "fat": 6, "carbs": 61, "density": 0.80, "avg_weight": 1000.0},
    {"name": "Kuru Fasulye", "calories": 333, "protein": 23, "fat": 0.8, "carbs": 60, "density": 0.80, "avg_weight": 1000.0},
    {"name": "İrmik", "calories": 360, "protein": 12, "fat": 1, "carbs": 73, "density": 0.70, "avg_weight": 500.0},
    {"name": "Nişasta", "calories": 381, "protein": 0.3, "fat": 0.1, "carbs": 91, "density": 0.60, "avg_weight": 200.0},
    {"name": "Yeşil Mercimek", "calories": 352, "protein": 25, "fat": 1, "carbs": 60, "density": 0.85, "avg_weight": 1000.0},
    {"name": "Börülce", "calories": 336, "protein": 24, "fat": 1.3, "carbs": 60, "density": 0.80, "avg_weight": 1000.0},
    {"name": "Barbunya", "calories": 333, "protein": 22, "fat": 1.5, "carbs": 60, "density": 0.80, "avg_weight": 1000.0},
    {"name": "Yulaf Ezmesi", "calories": 389, "protein": 17, "fat": 7, "carbs": 66, "density": 0.40, "avg_weight": 500.0},
    {"name": "Tam Buğday Unu", "calories": 340, "protein": 13, "fat": 2.5, "carbs": 72, "density": 0.55, "avg_weight": 1000.0},
    {"name": "Mısır Unu", "calories": 362, "protein": 7, "fat": 3.9, "carbs": 77, "density": 0.60, "avg_weight": 500.0},
    {"name": "Galeta Unu", "calories": 395, "protein": 13, "fat": 5, "carbs": 72, "density": 0.55, "avg_weight": 200.0},
    {"name": "Arpa Şehriye", "calories": 371, "protein": 13, "fat": 1.3, "carbs": 78, "density": 0.55, "avg_weight": 500.0},
    {"name": "Tel Şehriye", "calories": 370, "protein": 13, "fat": 1.5, "carbs": 75, "density": 0.50, "avg_weight": 500.0},
    {"name": "Pirinç Unu", "calories": 366, "protein": 6, "fat": 1.4, "carbs": 80, "density": 0.60, "avg_weight": 500.0},

    # ===== EKMEK / HAMUR İŞİ (Bread & Dough) =====
    {"name": "Ekmek", "calories": 265, "protein": 9, "fat": 3.2, "carbs": 49, "density": 0.30, "avg_weight": 350.0},
    {"name": "Yufka", "calories": 300, "protein": 8, "fat": 2, "carbs": 63, "density": 0.30, "avg_weight": 100.0},
    {"name": "Milföy Hamuru", "calories": 350, "protein": 5, "fat": 20, "carbs": 37, "density": 0.55, "avg_weight": 500.0},
    {"name": "Bazlama", "calories": 275, "protein": 8, "fat": 3.5, "carbs": 52, "density": 0.40, "avg_weight": 200.0},
    {"name": "Lavaş", "calories": 275, "protein": 9, "fat": 1.2, "carbs": 56, "density": 0.30, "avg_weight": 60.0},
    {"name": "Pide Ekmeği", "calories": 260, "protein": 8, "fat": 2.5, "carbs": 50, "density": 0.35, "avg_weight": 250.0},

    # ===== SALÇALAR / SOSLAR / SIVLAR (Condiments & Sauces) =====
    {"name": "Domates Salçası", "calories": 82, "protein": 4.3, "fat": 0.5, "carbs": 18.9, "density": 1.10, "avg_weight": 830.0},
    {"name": "Biber Salçası", "calories": 95, "protein": 3.5, "fat": 1.2, "carbs": 16.5, "density": 1.15, "avg_weight": 830.0},
    {"name": "Nar Ekşisi", "calories": 300, "protein": 0, "fat": 0, "carbs": 75, "density": 1.20, "avg_weight": 250.0},
    {"name": "Sirke", "calories": 18, "protein": 0, "fat": 0, "carbs": 0.9, "density": 1.01, "avg_weight": 500.0},
    {"name": "Soya Sosu", "calories": 53, "protein": 8, "fat": 0.1, "carbs": 5, "density": 1.10, "avg_weight": 250.0},
    {"name": "Tahin", "calories": 595, "protein": 17, "fat": 54, "carbs": 21, "density": 0.95, "avg_weight": 300.0},
    {"name": "Limon Suyu", "calories": 22, "protein": 0.4, "fat": 0.2, "carbs": 7, "density": 1.03, "avg_weight": 100.0},
    {"name": "Bal", "calories": 304, "protein": 0.3, "fat": 0, "carbs": 82, "density": 1.40, "avg_weight": 450.0},
    {"name": "Pekmez", "calories": 290, "protein": 0, "fat": 0, "carbs": 75, "density": 1.45, "avg_weight": 400.0},
    {"name": "Hardal", "calories": 66, "protein": 4, "fat": 4, "carbs": 5, "density": 1.00, "avg_weight": 200.0},
    {"name": "Mayonez", "calories": 680, "protein": 1, "fat": 75, "carbs": 1, "density": 0.90, "avg_weight": 470.0},
    {"name": "Ketçap", "calories": 112, "protein": 1.7, "fat": 0.1, "carbs": 27, "density": 1.10, "avg_weight": 450.0},
    {"name": "Acı Sos", "calories": 11, "protein": 0.6, "fat": 0.3, "carbs": 1.8, "density": 1.05, "avg_weight": 150.0},
    {"name": "Balsamik Sirke", "calories": 88, "protein": 0.5, "fat": 0, "carbs": 17, "density": 1.06, "avg_weight": 250.0},
    {"name": "Teriyaki Sos", "calories": 89, "protein": 6, "fat": 0, "carbs": 16, "density": 1.10, "avg_weight": 250.0},
    {"name": "Pesto Sos", "calories": 350, "protein": 5, "fat": 33, "carbs": 6, "density": 0.95, "avg_weight": 190.0},
    {"name": "Worcestershire Sos", "calories": 78, "protein": 0, "fat": 0, "carbs": 20, "density": 1.10, "avg_weight": 150.0},
    {"name": "Barbecue Sos", "calories": 172, "protein": 0.8, "fat": 0.6, "carbs": 40, "density": 1.10, "avg_weight": 300.0},

    # ===== BAHARATLAR (Spices & Herbs) =====
    {"name": "Tuz", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 1.20, "avg_weight": 500.0},
    {"name": "Karabiber", "calories": 251, "protein": 10, "fat": 3, "carbs": 64, "density": 0.50, "avg_weight": 100.0},
    {"name": "Pul Biber", "calories": 282, "protein": 12, "fat": 10, "carbs": 50, "density": 0.45, "avg_weight": 100.0},
    {"name": "Kimyon", "calories": 375, "protein": 18, "fat": 22, "carbs": 44, "density": 0.45, "avg_weight": 100.0},
    {"name": "Kekik", "calories": 101, "protein": 6, "fat": 4, "carbs": 24, "density": 0.25, "avg_weight": 50.0},
    {"name": "Nane", "calories": 285, "protein": 20, "fat": 6, "carbs": 52, "density": 0.25, "avg_weight": 50.0},
    {"name": "Kuru Maya", "calories": 325, "protein": 40, "fat": 7, "carbs": 40, "density": 0.80, "avg_weight": 10.0},
    {"name": "Kabartma Tozu", "calories": 100, "protein": 0, "fat": 0, "carbs": 25, "density": 0.90, "avg_weight": 10.0},
    {"name": "Vanilya", "calories": 30, "protein": 0, "fat": 0, "carbs": 12, "density": 0.90, "avg_weight": 5.0},
    {"name": "Sumak", "calories": 349, "protein": 12, "fat": 19, "carbs": 38, "density": 0.50, "avg_weight": 100.0},
    {"name": "Tatlı Toz Biber", "calories": 282, "protein": 14, "fat": 13, "carbs": 54, "density": 0.45, "avg_weight": 100.0},
    {"name": "Zerdeçal (Toz)", "calories": 312, "protein": 10, "fat": 3.3, "carbs": 67, "density": 0.50, "avg_weight": 100.0},
    {"name": "Tarçın (Toz)", "calories": 247, "protein": 4, "fat": 1.2, "carbs": 81, "density": 0.55, "avg_weight": 50.0},
    {"name": "Zencefil (Toz)", "calories": 335, "protein": 9, "fat": 4.2, "carbs": 72, "density": 0.50, "avg_weight": 50.0},
    {"name": "Taze Zencefil", "calories": 80, "protein": 1.8, "fat": 0.8, "carbs": 18, "density": 0.85, "avg_weight": 20.0},
    {"name": "Defne Yaprağı", "calories": 313, "protein": 8, "fat": 8, "carbs": 75, "density": 0.20, "avg_weight": 1.0},
    {"name": "Karanfil", "calories": 274, "protein": 6, "fat": 13, "carbs": 66, "density": 0.40, "avg_weight": 0.5},
    {"name": "Muskat", "calories": 525, "protein": 6, "fat": 36, "carbs": 49, "density": 0.55, "avg_weight": 5.0},
    {"name": "Safran", "calories": 310, "protein": 11, "fat": 6, "carbs": 65, "density": 0.35, "avg_weight": 1.0},
    {"name": "Köri", "calories": 325, "protein": 14, "fat": 14, "carbs": 58, "density": 0.50, "avg_weight": 50.0},
    {"name": "Taze Fesleğen", "calories": 23, "protein": 3.2, "fat": 0.6, "carbs": 2.7, "density": 0.30, "avg_weight": 50.0},
    {"name": "Taze Biberiye", "calories": 131, "protein": 3.3, "fat": 5.9, "carbs": 21, "density": 0.30, "avg_weight": 5.0},
    {"name": "Taze Kekik", "calories": 101, "protein": 5.6, "fat": 1.7, "carbs": 24, "density": 0.30, "avg_weight": 5.0},
    {"name": "Isot", "calories": 260, "protein": 11, "fat": 8, "carbs": 48, "density": 0.45, "avg_weight": 100.0},
    {"name": "Kişniş (Toz)", "calories": 298, "protein": 12, "fat": 18, "carbs": 55, "density": 0.45, "avg_weight": 50.0},
    {"name": "Yenibahar", "calories": 263, "protein": 6, "fat": 9, "carbs": 73, "density": 0.50, "avg_weight": 50.0},
    {"name": "Haşhaş", "calories": 525, "protein": 18, "fat": 42, "carbs": 28, "density": 0.55, "avg_weight": 100.0},
    {"name": "Çörek Otu", "calories": 345, "protein": 16, "fat": 14, "carbs": 52, "density": 0.50, "avg_weight": 100.0},
    {"name": "Susam", "calories": 573, "protein": 18, "fat": 50, "carbs": 23, "density": 0.60, "avg_weight": 100.0},

    # ===== KURUYEMİŞ (Nuts & Seeds) =====
    {"name": "Ceviz İçi", "calories": 654, "protein": 15, "fat": 65, "carbs": 14, "density": 0.45, "avg_weight": 5.0},
    {"name": "Fındık İçi", "calories": 628, "protein": 15, "fat": 61, "carbs": 17, "density": 0.50, "avg_weight": 1.5},
    {"name": "Badem İçi", "calories": 579, "protein": 21, "fat": 49, "carbs": 22, "density": 0.50, "avg_weight": 1.2},
    {"name": "Antep Fıstığı", "calories": 560, "protein": 20, "fat": 45, "carbs": 27, "density": 0.50, "avg_weight": 1.0},
    {"name": "Yer Fıstığı", "calories": 567, "protein": 26, "fat": 49, "carbs": 16, "density": 0.55, "avg_weight": 1.5},
    {"name": "Kaju", "calories": 553, "protein": 18, "fat": 44, "carbs": 30, "density": 0.50, "avg_weight": 2.0},
    {"name": "Çam Fıstığı", "calories": 673, "protein": 14, "fat": 68, "carbs": 13, "density": 0.50, "avg_weight": 0.5},
    {"name": "Ay Çekirdeği", "calories": 584, "protein": 21, "fat": 51, "carbs": 20, "density": 0.55, "avg_weight": 1.0},
    {"name": "Kabak Çekirdeği", "calories": 559, "protein": 30, "fat": 49, "carbs": 11, "density": 0.55, "avg_weight": 1.0},
    {"name": "Hindistan Cevizi (Rendelenmiş)", "calories": 354, "protein": 3.3, "fat": 33, "carbs": 15, "density": 0.35, "avg_weight": 200.0},

    # ===== TATLI MALZEMELERI (Baking & Sweets) =====
    {"name": "Kakao Tozu", "calories": 228, "protein": 20, "fat": 14, "carbs": 58, "density": 0.55, "avg_weight": 200.0},
    {"name": "Bitter Çikolata", "calories": 546, "protein": 5, "fat": 31, "carbs": 60, "density": 1.00, "avg_weight": 80.0},
    {"name": "Sütlü Çikolata", "calories": 535, "protein": 8, "fat": 30, "carbs": 59, "density": 1.00, "avg_weight": 80.0},
    {"name": "Beyaz Çikolata", "calories": 539, "protein": 6, "fat": 32, "carbs": 59, "density": 1.00, "avg_weight": 80.0},
    {"name": "Pudra Şekeri", "calories": 389, "protein": 0, "fat": 0, "carbs": 100, "density": 0.58, "avg_weight": 250.0},
    {"name": "Esmer Şeker", "calories": 380, "protein": 0, "fat": 0, "carbs": 98, "density": 0.85, "avg_weight": 500.0},
    {"name": "Reçel (Çilek)", "calories": 250, "protein": 0.4, "fat": 0.1, "carbs": 63, "density": 1.20, "avg_weight": 380.0},
    {"name": "Nutella", "calories": 539, "protein": 6.3, "fat": 30, "carbs": 58, "density": 1.10, "avg_weight": 400.0},
    {"name": "Fıstık Ezmesi", "calories": 588, "protein": 25, "fat": 50, "carbs": 20, "density": 1.05, "avg_weight": 340.0},
    {"name": "Jelatin (Toz)", "calories": 335, "protein": 86, "fat": 0, "carbs": 0, "density": 0.60, "avg_weight": 10.0},

    # ===== İÇECEK / DİĞER (Beverages & Other) =====
    {"name": "Çay (Kuru)", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 0.30, "avg_weight": 200.0},
    {"name": "Türk Kahvesi", "calories": 2, "protein": 0.1, "fat": 0, "carbs": 0.4, "density": 0.40, "avg_weight": 100.0},
    {"name": "Hindistan Cevizi Sütü", "calories": 197, "protein": 2.3, "fat": 21, "carbs": 2.8, "density": 1.00, "avg_weight": 400.0},
    {"name": "Soda", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 1.00, "avg_weight": 200.0},
    {"name": "Portakal Suyu", "calories": 45, "protein": 0.7, "fat": 0.2, "carbs": 10, "density": 1.04, "avg_weight": 250.0},

    # ===== ASYA MUTFAĞI (Asian Cuisine) =====
    {"name": "Tofu", "calories": 76, "protein": 8, "fat": 4.8, "carbs": 1.9, "density": 1.05, "avg_weight": 300.0},
    {"name": "Sert Tofu", "calories": 144, "protein": 17, "fat": 9, "carbs": 3, "density": 1.05, "avg_weight": 300.0},
    {"name": "Miso Ezmesi", "calories": 199, "protein": 12, "fat": 6, "carbs": 26, "density": 1.10, "avg_weight": 400.0},
    {"name": "Nori (Deniz Yosunu)", "calories": 35, "protein": 6, "fat": 0.3, "carbs": 5, "density": 0.10, "avg_weight": 2.5},
    {"name": "Wasabi", "calories": 109, "protein": 5, "fat": 0.6, "carbs": 24, "density": 1.00, "avg_weight": 43.0},
    {"name": "Pirinç Sirkesi", "calories": 18, "protein": 0, "fat": 0, "carbs": 4, "density": 1.01, "avg_weight": 250.0},
    {"name": "Balık Sosu", "calories": 35, "protein": 5, "fat": 0, "carbs": 4, "density": 1.10, "avg_weight": 250.0},
    {"name": "Hoisin Sosu", "calories": 220, "protein": 3, "fat": 4, "carbs": 44, "density": 1.10, "avg_weight": 250.0},
    {"name": "Sriracha Sos", "calories": 93, "protein": 2, "fat": 1, "carbs": 19, "density": 1.10, "avg_weight": 255.0},
    {"name": "Limon Otu (Sereh)", "calories": 99, "protein": 1.8, "fat": 0.5, "carbs": 25, "density": 0.50, "avg_weight": 20.0},
    {"name": "Galangal", "calories": 71, "protein": 1, "fat": 1, "carbs": 15, "density": 0.80, "avg_weight": 30.0},
    {"name": "Bambu Filizi", "calories": 27, "protein": 2.6, "fat": 0.3, "carbs": 5.2, "density": 0.90, "avg_weight": 200.0},
    {"name": "Soya Filizi", "calories": 31, "protein": 3, "fat": 0.2, "carbs": 6, "density": 0.55, "avg_weight": 200.0},
    {"name": "Pak Çoy", "calories": 13, "protein": 1.5, "fat": 0.2, "carbs": 2.2, "density": 0.55, "avg_weight": 100.0},
    {"name": "Çin Lahanası", "calories": 16, "protein": 1.2, "fat": 0.2, "carbs": 3.2, "density": 0.40, "avg_weight": 500.0},
    {"name": "Edamame", "calories": 121, "protein": 12, "fat": 5, "carbs": 9, "density": 0.70, "avg_weight": 200.0},
    {"name": "Şirataki Erişte", "calories": 9, "protein": 0, "fat": 0, "carbs": 3, "density": 1.00, "avg_weight": 200.0},
    {"name": "Pirinç Eriştesi", "calories": 364, "protein": 3.4, "fat": 0.6, "carbs": 84, "density": 0.50, "avg_weight": 250.0},
    {"name": "Udon Erişte", "calories": 270, "protein": 7, "fat": 1.5, "carbs": 57, "density": 0.55, "avg_weight": 200.0},
    {"name": "Soba Erişte", "calories": 336, "protein": 14, "fat": 0.7, "carbs": 74, "density": 0.55, "avg_weight": 200.0},
    {"name": "Panko (Japon Galeta Unu)", "calories": 350, "protein": 10, "fat": 2, "carbs": 70, "density": 0.20, "avg_weight": 200.0},
    {"name": "Tempura Unu", "calories": 350, "protein": 8, "fat": 1, "carbs": 77, "density": 0.45, "avg_weight": 200.0},
    {"name": "Dashi Toz", "calories": 200, "protein": 10, "fat": 0, "carbs": 40, "density": 0.50, "avg_weight": 50.0},
    {"name": "Kimchi", "calories": 15, "protein": 1.1, "fat": 0.5, "carbs": 2.4, "density": 0.90, "avg_weight": 350.0},
    {"name": "Gochujang (Kore Biberi)", "calories": 228, "protein": 5, "fat": 3, "carbs": 45, "density": 1.10, "avg_weight": 200.0},
    {"name": "Soya Fasulyesi", "calories": 446, "protein": 36, "fat": 20, "carbs": 30, "density": 0.80, "avg_weight": 500.0},
    {"name": "Turp Turşusu (Danmuji)", "calories": 32, "protein": 0.6, "fat": 0.1, "carbs": 7, "density": 0.90, "avg_weight": 200.0},
    {"name": "Sake (Pirinç Şarabı)", "calories": 134, "protein": 0.5, "fat": 0, "carbs": 5, "density": 1.00, "avg_weight": 250.0},
    {"name": "Mirin", "calories": 241, "protein": 0.3, "fat": 0, "carbs": 43, "density": 1.10, "avg_weight": 250.0},
    {"name": "Tamarind Ezmesi", "calories": 239, "protein": 2.8, "fat": 0.6, "carbs": 63, "density": 1.20, "avg_weight": 200.0},
    {"name": "Pirinç Kağıdı", "calories": 310, "protein": 1, "fat": 0, "carbs": 75, "density": 0.15, "avg_weight": 10.0},
    {"name": "Wonton Hamuru", "calories": 291, "protein": 8, "fat": 2, "carbs": 58, "density": 0.45, "avg_weight": 8.0},
    {"name": "Hatcho Miso", "calories": 206, "protein": 17, "fat": 10, "carbs": 12, "density": 1.10, "avg_weight": 300.0},
    {"name": "Tahıl Sirkesi", "calories": 20, "protein": 0, "fat": 0, "carbs": 4, "density": 1.01, "avg_weight": 500.0},
    {"name": "Isıtılmış Susam Yağı", "calories": 884, "protein": 0, "fat": 100, "carbs": 0, "density": 0.92, "avg_weight": 250.0},

    # ===== HİNT MUTFAĞI (Indian Cuisine) =====
    {"name": "Ghee (Sade Yağ)", "calories": 900, "protein": 0, "fat": 100, "carbs": 0, "density": 0.90, "avg_weight": 250.0},
    {"name": "Paneer", "calories": 265, "protein": 18, "fat": 21, "carbs": 1.2, "density": 1.00, "avg_weight": 200.0},
    {"name": "Naan Ekmeği", "calories": 262, "protein": 9, "fat": 5, "carbs": 46, "density": 0.35, "avg_weight": 90.0},
    {"name": "Chapati Unu", "calories": 340, "protein": 11, "fat": 1.7, "carbs": 72, "density": 0.55, "avg_weight": 1000.0},
    {"name": "Garam Masala", "calories": 379, "protein": 12, "fat": 15, "carbs": 60, "density": 0.50, "avg_weight": 50.0},
    {"name": "Kurkuma (Toz)", "calories": 312, "protein": 10, "fat": 3.3, "carbs": 67, "density": 0.50, "avg_weight": 100.0},
    {"name": "Hint Kimyonu (Jeera)", "calories": 375, "protein": 18, "fat": 22, "carbs": 44, "density": 0.45, "avg_weight": 100.0},
    {"name": "Hardal Tohumu", "calories": 508, "protein": 26, "fat": 36, "carbs": 28, "density": 0.70, "avg_weight": 100.0},
    {"name": "Rezene Tohumu", "calories": 345, "protein": 16, "fat": 15, "carbs": 52, "density": 0.45, "avg_weight": 50.0},
    {"name": "Kakule", "calories": 311, "protein": 11, "fat": 7, "carbs": 68, "density": 0.45, "avg_weight": 1.0},
    {"name": "Çemen Tohumu", "calories": 323, "protein": 23, "fat": 6, "carbs": 58, "density": 0.60, "avg_weight": 50.0},
    {"name": "Asafoetida (Şeytan Tersi)", "calories": 297, "protein": 4, "fat": 1, "carbs": 68, "density": 0.60, "avg_weight": 50.0},
    {"name": "Taze Kişniş Yaprağı", "calories": 23, "protein": 2.1, "fat": 0.5, "carbs": 3.7, "density": 0.30, "avg_weight": 50.0},
    {"name": "Hint Yağı (Hardal Yağı)", "calories": 884, "protein": 0, "fat": 100, "carbs": 0, "density": 0.91, "avg_weight": 500.0},
    {"name": "Papadum", "calories": 371, "protein": 20, "fat": 6, "carbs": 60, "density": 0.20, "avg_weight": 15.0},
    {"name": "Chutney (Nane)", "calories": 147, "protein": 1, "fat": 5, "carbs": 26, "density": 1.05, "avg_weight": 200.0},
    {"name": "Tandoori Baharat Karışımı", "calories": 340, "protein": 13, "fat": 10, "carbs": 57, "density": 0.50, "avg_weight": 50.0},
    {"name": "Curry Yaprağı", "calories": 108, "protein": 6.1, "fat": 1, "carbs": 19, "density": 0.20, "avg_weight": 1.0},
    {"name": "Besan (Nohut Unu)", "calories": 356, "protein": 22, "fat": 6.7, "carbs": 58, "density": 0.55, "avg_weight": 500.0},

    # ===== MEKSİKA / LATİN MUTFAĞI (Mexican/Latin Cuisine) =====
    {"name": "Tortilla (Mısır)", "calories": 218, "protein": 5.7, "fat": 3, "carbs": 44, "density": 0.40, "avg_weight": 30.0},
    {"name": "Tortilla (Buğday)", "calories": 306, "protein": 8, "fat": 8, "carbs": 50, "density": 0.40, "avg_weight": 45.0},
    {"name": "Jalapeño Biber", "calories": 29, "protein": 0.9, "fat": 0.4, "carbs": 6.5, "density": 0.55, "avg_weight": 14.0},
    {"name": "Chipotle Biber", "calories": 55, "protein": 2, "fat": 1, "carbs": 10, "density": 0.55, "avg_weight": 5.0},
    {"name": "Guacamole Sosu", "calories": 160, "protein": 2, "fat": 15, "carbs": 9, "density": 0.95, "avg_weight": 200.0},
    {"name": "Salsa Sosu", "calories": 36, "protein": 2, "fat": 0.2, "carbs": 7, "density": 1.00, "avg_weight": 300.0},
    {"name": "Taco Baharatı", "calories": 280, "protein": 10, "fat": 8, "carbs": 46, "density": 0.50, "avg_weight": 30.0},
    {"name": "Kırmızı Barbunya (Kidney)", "calories": 127, "protein": 8.7, "fat": 0.5, "carbs": 23, "density": 0.85, "avg_weight": 400.0},
    {"name": "Siyah Fasulye", "calories": 132, "protein": 8.9, "fat": 0.5, "carbs": 24, "density": 0.85, "avg_weight": 400.0},
    {"name": "Koriander (Taze)", "calories": 23, "protein": 2.1, "fat": 0.5, "carbs": 3.7, "density": 0.30, "avg_weight": 50.0},
    {"name": "Habanero Biber", "calories": 40, "protein": 2, "fat": 0.4, "carbs": 9, "density": 0.55, "avg_weight": 8.0},
    {"name": "Totopos (Mısır Cipsi)", "calories": 489, "protein": 7, "fat": 24, "carbs": 63, "density": 0.25, "avg_weight": 200.0},
    {"name": "Ekşi Krema (Sour Cream)", "calories": 193, "protein": 2.4, "fat": 19, "carbs": 3, "density": 1.00, "avg_weight": 200.0},

    # ===== İTALYAN MUTFAĞI (Italian Cuisine) =====
    {"name": "Ricotta", "calories": 174, "protein": 11, "fat": 13, "carbs": 3, "density": 1.00, "avg_weight": 250.0},
    {"name": "Mascarpone", "calories": 429, "protein": 5, "fat": 44, "carbs": 4, "density": 1.00, "avg_weight": 250.0},
    {"name": "Prosciutto", "calories": 195, "protein": 26, "fat": 10, "carbs": 0, "density": 1.00, "avg_weight": 80.0},
    {"name": "Pancetta", "calories": 393, "protein": 15, "fat": 37, "carbs": 1, "density": 1.00, "avg_weight": 100.0},
    {"name": "Gorgonzola", "calories": 353, "protein": 21, "fat": 29, "carbs": 1, "density": 1.00, "avg_weight": 200.0},
    {"name": "Pecorino", "calories": 393, "protein": 26, "fat": 32, "carbs": 0, "density": 1.00, "avg_weight": 200.0},
    {"name": "Burrata", "calories": 233, "protein": 18, "fat": 18, "carbs": 0, "density": 1.00, "avg_weight": 125.0},
    {"name": "Penne Makarna", "calories": 371, "protein": 13, "fat": 1.5, "carbs": 75, "density": 0.50, "avg_weight": 500.0},
    {"name": "Fusilli Makarna", "calories": 371, "protein": 13, "fat": 1.5, "carbs": 75, "density": 0.50, "avg_weight": 500.0},
    {"name": "Lazanya Yaprağı", "calories": 356, "protein": 12, "fat": 1.6, "carbs": 72, "density": 0.50, "avg_weight": 250.0},
    {"name": "Gnocchi", "calories": 133, "protein": 3, "fat": 0.5, "carbs": 30, "density": 0.85, "avg_weight": 500.0},
    {"name": "Risotto Pirinci (Arborio)", "calories": 358, "protein": 6.5, "fat": 0.5, "carbs": 80, "density": 0.82, "avg_weight": 500.0},
    {"name": "Marsala Şarabı", "calories": 126, "protein": 0, "fat": 0, "carbs": 8, "density": 1.00, "avg_weight": 250.0},
    {"name": "Kapari Meyvesi", "calories": 26, "protein": 2, "fat": 0.9, "carbs": 2, "density": 1.00, "avg_weight": 3.0},
    {"name": "Sardella Fileto", "calories": 210, "protein": 29, "fat": 10, "carbs": 0, "density": 1.00, "avg_weight": 50.0},
    {"name": "İtalyan Fesleğeni", "calories": 23, "protein": 3.2, "fat": 0.6, "carbs": 2.7, "density": 0.30, "avg_weight": 50.0},
    {"name": "Polenta (Mısır Irmiği)", "calories": 362, "protein": 7, "fat": 3.9, "carbs": 77, "density": 0.60, "avg_weight": 500.0},

    # ===== ORTADOĞU / ARAP MUTFAĞI (Middle Eastern Cuisine) =====
    {"name": "Sumak (Toz)", "calories": 239, "protein": 5, "fat": 8, "carbs": 44, "density": 0.50, "avg_weight": 100.0},
    {"name": "Zatar Baharatı", "calories": 276, "protein": 9, "fat": 8, "carbs": 49, "density": 0.40, "avg_weight": 100.0},
    {"name": "Baharat Karışımı (7 Baharat)", "calories": 320, "protein": 10, "fat": 12, "carbs": 55, "density": 0.50, "avg_weight": 50.0},
    {"name": "Ras el Hanout", "calories": 310, "protein": 11, "fat": 10, "carbs": 56, "density": 0.50, "avg_weight": 50.0},
    {"name": "Harissa Ezmesi", "calories": 70, "protein": 3, "fat": 3, "carbs": 8, "density": 1.05, "avg_weight": 200.0},
    {"name": "Tahini Sos", "calories": 595, "protein": 17, "fat": 54, "carbs": 21, "density": 0.95, "avg_weight": 300.0},
    {"name": "Filo Hamuru", "calories": 310, "protein": 6.5, "fat": 7, "carbs": 54, "density": 0.30, "avg_weight": 400.0},
    {"name": "Kadayıf (Taze)", "calories": 269, "protein": 6, "fat": 1, "carbs": 58, "density": 0.30, "avg_weight": 500.0},
    {"name": "Gül Suyu", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 1.00, "avg_weight": 250.0},
    {"name": "Portakal Çiçeği Suyu", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 1.00, "avg_weight": 250.0},
    {"name": "Mahlep", "calories": 400, "protein": 20, "fat": 25, "carbs": 30, "density": 0.50, "avg_weight": 50.0},
    {"name": "Mastik (Damla Sakızı)", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 0.50, "avg_weight": 5.0},
    {"name": "Taze Nane Yaprağı", "calories": 44, "protein": 3.3, "fat": 0.7, "carbs": 8, "density": 0.30, "avg_weight": 50.0},
    {"name": "Acı Biber Ezmesi", "calories": 40, "protein": 2, "fat": 0.4, "carbs": 9, "density": 1.05, "avg_weight": 300.0},

    # ===== FRANSIZ MUTFAĞI (French Cuisine) =====
    {"name": "Dijon Hardalı", "calories": 66, "protein": 4, "fat": 4, "carbs": 5, "density": 1.00, "avg_weight": 200.0},
    {"name": "Brie Peyniri", "calories": 334, "protein": 21, "fat": 28, "carbs": 0.5, "density": 1.00, "avg_weight": 200.0},
    {"name": "Camembert", "calories": 300, "protein": 20, "fat": 24, "carbs": 0.5, "density": 1.00, "avg_weight": 250.0},
    {"name": "Roquefort", "calories": 369, "protein": 22, "fat": 31, "carbs": 2, "density": 1.00, "avg_weight": 100.0},
    {"name": "Crème Fraîche", "calories": 292, "protein": 2.2, "fat": 30, "carbs": 3, "density": 1.00, "avg_weight": 200.0},
    {"name": "Tarhun (Taze)", "calories": 295, "protein": 23, "fat": 7, "carbs": 50, "density": 0.25, "avg_weight": 5.0},
    {"name": "Kaz Ciğeri (Foie Gras)", "calories": 462, "protein": 11, "fat": 44, "carbs": 5, "density": 1.00, "avg_weight": 100.0},
    {"name": "Krep Hamuru (Hazır)", "calories": 229, "protein": 6, "fat": 8, "carbs": 33, "density": 1.00, "avg_weight": 200.0},

    # ===== DAHA FAZLA SEBZE & YEŞİLLİK =====
    {"name": "Bezelye (Dondurulmuş)", "calories": 77, "protein": 5, "fat": 0.3, "carbs": 14, "density": 0.70, "avg_weight": 450.0},
    {"name": "Karışık Sebze (Dondurulmuş)", "calories": 65, "protein": 3, "fat": 0.3, "carbs": 13, "density": 0.65, "avg_weight": 450.0},
    {"name": "Mısır (Taze Koçan)", "calories": 86, "protein": 3.3, "fat": 1.4, "carbs": 19, "density": 0.75, "avg_weight": 200.0},
    {"name": "Acı Biber (Sivri)", "calories": 40, "protein": 2, "fat": 0.4, "carbs": 9, "density": 0.50, "avg_weight": 5.0},
    {"name": "Dolmalık Biber", "calories": 20, "protein": 0.9, "fat": 0.2, "carbs": 4.6, "density": 0.50, "avg_weight": 180.0},
    {"name": "Cherry Domates", "calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9, "density": 0.94, "avg_weight": 15.0},
    {"name": "Kurutulmuş Biber", "calories": 282, "protein": 12, "fat": 10, "carbs": 50, "density": 0.30, "avg_weight": 5.0},
    {"name": "Kuru Soğan (Pul)", "calories": 349, "protein": 10, "fat": 1, "carbs": 83, "density": 0.40, "avg_weight": 100.0},
    {"name": "Sarımsak Tozu", "calories": 331, "protein": 17, "fat": 0.7, "carbs": 73, "density": 0.55, "avg_weight": 100.0},
    {"name": "Soğan Tozu", "calories": 341, "protein": 10, "fat": 1, "carbs": 79, "density": 0.55, "avg_weight": 100.0},
    {"name": "Kabak Çiçeği", "calories": 15, "protein": 1.1, "fat": 0.1, "carbs": 3.3, "density": 0.30, "avg_weight": 10.0},

    {"name": "Arpacık Soğan", "calories": 72, "protein": 2.5, "fat": 0.1, "carbs": 17, "density": 0.85, "avg_weight": 20.0},

    # ===== DAHA FAZLA DENİZ ÜRÜNLERİ =====
    {"name": "İstakoz", "calories": 90, "protein": 19, "fat": 0.9, "carbs": 0.5, "density": 1.05, "avg_weight": 500.0},
    {"name": "Yengeç", "calories": 87, "protein": 18, "fat": 1.1, "carbs": 0, "density": 1.05, "avg_weight": 250.0},
    {"name": "Deniz Tarağı", "calories": 69, "protein": 12, "fat": 0.5, "carbs": 3.2, "density": 1.05, "avg_weight": 15.0},
    {"name": "Uskumru", "calories": 205, "protein": 19, "fat": 14, "carbs": 0, "density": 1.05, "avg_weight": 300.0},
    {"name": "Mezgit", "calories": 82, "protein": 18, "fat": 0.7, "carbs": 0, "density": 1.05, "avg_weight": 250.0},
    {"name": "Dil Balığı", "calories": 86, "protein": 18, "fat": 1.2, "carbs": 0, "density": 1.05, "avg_weight": 200.0},
    {"name": "Somon (Füme)", "calories": 117, "protein": 18, "fat": 4.3, "carbs": 0, "density": 1.00, "avg_weight": 100.0},
    {"name": "Ançüez", "calories": 210, "protein": 29, "fat": 10, "carbs": 0, "density": 1.00, "avg_weight": 5.0},
    {"name": "Surimi (Yengeç Çubuğu)", "calories": 95, "protein": 7, "fat": 1, "carbs": 15, "density": 1.00, "avg_weight": 15.0},

    # ===== TATLI & FIRINDA MALZEME =====
    {"name": "Çikolata Parçacıkları", "calories": 480, "protein": 5, "fat": 26, "carbs": 58, "density": 0.60, "avg_weight": 200.0},
    {"name": "Marshmallow", "calories": 318, "protein": 2, "fat": 0.2, "carbs": 81, "density": 0.30, "avg_weight": 7.0},
    {"name": "Muzlu Süt", "calories": 60, "protein": 2.5, "fat": 1, "carbs": 10, "density": 1.03, "avg_weight": 200.0},
    {"name": "Çilekli Süt", "calories": 58, "protein": 2.5, "fat": 1, "carbs": 10, "density": 1.03, "avg_weight": 200.0},

    {"name": "Karamel Sosu", "calories": 320, "protein": 2, "fat": 8, "carbs": 60, "density": 1.30, "avg_weight": 200.0},
    {"name": "Krem Şanti (Toz)", "calories": 340, "protein": 2, "fat": 12, "carbs": 56, "density": 0.40, "avg_weight": 75.0},
    {"name": "Peynir Altı Suyu Tozu", "calories": 353, "protein": 80, "fat": 1, "carbs": 8, "density": 0.55, "avg_weight": 1000.0},
    {"name": "Kurabiye Hamuru (Hazır)", "calories": 340, "protein": 4, "fat": 15, "carbs": 48, "density": 0.95, "avg_weight": 500.0},
    {"name": "Kruvasan Hamuru", "calories": 406, "protein": 8, "fat": 21, "carbs": 46, "density": 0.65, "avg_weight": 300.0},
    {"name": "Agar Agar", "calories": 306, "protein": 6, "fat": 0, "carbs": 81, "density": 0.50, "avg_weight": 10.0},

    # ===== İÇECEK & SICAK İÇECEK =====
    {"name": "Matcha Tozu", "calories": 324, "protein": 30, "fat": 5, "carbs": 39, "density": 0.50, "avg_weight": 30.0},
    {"name": "Espresso", "calories": 2, "protein": 0.1, "fat": 0, "carbs": 0.4, "density": 1.00, "avg_weight": 30.0},
    {"name": "Kakao (Sıcak İçecek Tozu)", "calories": 380, "protein": 5, "fat": 5, "carbs": 80, "density": 0.55, "avg_weight": 200.0},
    {"name": "Badem Sütü", "calories": 15, "protein": 0.6, "fat": 1.1, "carbs": 0.6, "density": 1.01, "avg_weight": 1000.0},
    {"name": "Yulaf Sütü", "calories": 46, "protein": 1, "fat": 1.5, "carbs": 7, "density": 1.02, "avg_weight": 1000.0},
    {"name": "Soya Sütü", "calories": 33, "protein": 2.9, "fat": 1.8, "carbs": 1.2, "density": 1.02, "avg_weight": 1000.0},
    {"name": "Kefir (Meyve Aromalı)", "calories": 65, "protein": 3, "fat": 1.5, "carbs": 10, "density": 1.03, "avg_weight": 500.0},

    # ===== ÖZEL DİYET / SAĞLIK =====
    {"name": "Chia Tohumu", "calories": 486, "protein": 17, "fat": 31, "carbs": 42, "density": 0.65, "avg_weight": 200.0},
    {"name": "Keten Tohumu", "calories": 534, "protein": 18, "fat": 42, "carbs": 29, "density": 0.65, "avg_weight": 250.0},
    {"name": "Kinoa", "calories": 368, "protein": 14, "fat": 6, "carbs": 64, "density": 0.72, "avg_weight": 500.0},
    {"name": "Amarant", "calories": 371, "protein": 14, "fat": 7, "carbs": 65, "density": 0.75, "avg_weight": 500.0},
    {"name": "Karabuğday", "calories": 343, "protein": 13, "fat": 3.4, "carbs": 72, "density": 0.70, "avg_weight": 500.0},
    {"name": "Hindistan Cevizi Unu", "calories": 400, "protein": 20, "fat": 13, "carbs": 60, "density": 0.45, "avg_weight": 250.0},
    {"name": "Badem Unu", "calories": 571, "protein": 21, "fat": 50, "carbs": 20, "density": 0.45, "avg_weight": 250.0},
    {"name": "Psyllium Kabuğu", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 0.25, "avg_weight": 100.0},
    {"name": "Spirulina (Toz)", "calories": 290, "protein": 57, "fat": 8, "carbs": 24, "density": 0.40, "avg_weight": 100.0},
    {"name": "Arı Poleni", "calories": 315, "protein": 24, "fat": 5, "carbs": 52, "density": 0.55, "avg_weight": 100.0},
    {"name": "Ham Kakao Nibs", "calories": 228, "protein": 14, "fat": 14, "carbs": 58, "density": 0.55, "avg_weight": 200.0},
    {"name": "Hindistan Cevizi Şekeri", "calories": 375, "protein": 1, "fat": 0.5, "carbs": 94, "density": 0.70, "avg_weight": 250.0},
    {"name": "Akçaağaç Şurubu", "calories": 260, "protein": 0, "fat": 0, "carbs": 67, "density": 1.37, "avg_weight": 250.0},
    {"name": "Agave Şurubu", "calories": 310, "protein": 0, "fat": 0, "carbs": 76, "density": 1.40, "avg_weight": 250.0},
    {"name": "Stevia (Doğal Tatlandırıcı)", "calories": 0, "protein": 0, "fat": 0, "carbs": 0, "density": 0.50, "avg_weight": 50.0},
]

async def seed_ingredients():
    print("Connecting to database...")
    async with AsyncSessionLocal() as session:
        repo = PostgresIngredientRepository(session)
        
        added_count = 0
        skipped_count = 0
        error_count = 0
        
        for data in INGREDIENTS_DATA:
            if not data.get("name"):
                continue
            existing = await repo.get_by_name(data["name"])
            if existing:
                skipped_count += 1
                continue
            
            try:
                slug = slugify(data["name"])
                ingredient = Ingredient(
                    id=str(uuid.uuid4()),
                    name=data["name"],
                    calories_per_100g=data["calories"],
                    protein_per_100g=data["protein"],
                    fat_per_100g=data["fat"],
                    carbs_per_100g=data["carbs"],
                    density_g_ml=data["density"],
                    avg_weight_per_piece_g=data["avg_weight"],
                    slug=slug
                )
                await repo.save(ingredient)
                await session.flush()
                added_count += 1
                print(f"  + {data['name']}")
            except Exception as e:
                await session.rollback()
                error_count += 1
                print(f"  ! SKIPPED (slug conflict or error): {data['name']} -> {e}")
        
        await session.commit()
        print(f"\nDone! Added: {added_count}, Skipped: {skipped_count}, Errors: {error_count}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_ingredients())
