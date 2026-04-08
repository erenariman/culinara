import asyncio
import sys
import os
import uuid
from slugify import slugify

sys.path.append(os.getcwd())

from src.adapters.database.postgresql.database import AsyncSessionLocal
from src.adapters.database.postgresql.repositories.recipe_repository import PostgresRecipeRepository
from src.adapters.database.postgresql.repositories.ingredient_repository import PostgresIngredientRepository
from src.adapters.database.postgresql.repositories.user_repository import PostgresUserRepository
from src.domain.entities.recipe import Recipe, RecipeItem, RecipeInstruction, RecipeStatus, RecipeCategory, DifficultyLevel
from src.domain.entities.units import UnitType
from src.domain.services.nutrition_calculator import NutritionCalculatorService

RECIPES = [
    # ==================== 1. SPAGHETTI CARBONARA ====================
    {
        "title": "Otantik Spaghetti Carbonara",
        "description": "Roma usulü, kremasız, orijinal tarif. Yumurta sarısı, Pecorino peyniri ve çıtır Pancetta ile yapılan bu makarna, İtalyan mutfağının en ikonik lezzetlerinden biridir.",
        "category": "Ana Yemek",
        "difficulty": "Orta",
        "diet_type": None,
        "prep_time": 10,
        "cook_time": 20,
        "servings": 4,
        "ingredients": [
            ("Makarna", 400, UnitType.GRAM),
            ("Pancetta", 200, UnitType.GRAM),
            ("Yumurta", 4, UnitType.PIECE),
            ("Pecorino", 80, UnitType.GRAM),
            ("Parmesan", 40, UnitType.GRAM),
            ("Karabiber", 1, UnitType.TSP),
            ("Sarımsak", 2, UnitType.CLOVE),
            ("Zeytinyağı", 1, UnitType.TBS),
            ("Tuz", 1, UnitType.TBS),
        ],
        "steps": [
            "Bol tuzlu suyu kaynatın ve makarnayı paket üzerinde yazan süreden 1 dakika kısa olacak şekilde al dente haşlayın. 1 su bardağı makarna suyunu ayırın.",
            "Pancetta'yı küçük küpler halinde kesin. Kuru bir tavada, kendi yağında, kıtır kıtır olana kadar orta ateşte 6-8 dakika kavurun.",
            "Sarımsakları bütün olarak tavaya ekleyin, aroması çıkınca çıkarıp atın. Tavayı ocaktan alın.",
            "Geniş bir kasede 4 yumurta sarısını (beyazını ayırın) iyice çırpın. Rendelenmiş Pecorino ve Parmesan peynirlerini ekleyip koyu, kremamsı bir sos elde edene kadar karıştırın. Bol taze çekilmiş karabiber ekleyin.",
            "Süzülen makarnayı Pancetta'lı tavaya alın ve orta-düşük ateşte 30 saniye karıştırın. Tavayı OCAKTAN ALIN.",
            "Peynirli yumurta sosunu sıcak makarnanın üzerine dökün ve enerjik şekilde karıştırın. Sos çok koyulaşırsa 1-2 kaşık makarna suyu ekleyin. Yumurta kesinlikle pişmemeli, ipeksi bir kıvam oluşmalıdır.",
            "Hemen tabağa alıp üzerine ekstra Pecorino rendesi ve taze çekilmiş karabiber serpin. Bekletmeden servis yapın."
        ]
    },
    # ==================== 2. MERCIMEK ÇORBASI ====================
    {
        "title": "Lokanta Usulü Mercimek Çorbası",
        "description": "Türk lokantalarının vazgeçilmezi, ipeksi kıvamda süzme kırmızı mercimek çorbası. Tereyağlı pul biberli sos ile taçlandırılır.",
        "category": "Çorba",
        "difficulty": "Kolay",
        "diet_type": None,
        "prep_time": 10,
        "cook_time": 30,
        "servings": 6,
        "ingredients": [
            ("Kırmızı Mercimek", 2, UnitType.GLASS_WATER),
            ("Soğan", 1, UnitType.PIECE),
            ("Havuç", 1, UnitType.PIECE),
            ("Patates", 1, UnitType.PIECE),
            ("Sarımsak", 2, UnitType.CLOVE),
            ("Domates Salçası", 1, UnitType.TBS),
            ("Un", 1, UnitType.TBS),
            ("Tereyağı", 3, UnitType.TBS),
            ("Zeytinyağı", 2, UnitType.TBS),
            ("Pul Biber", 1, UnitType.TSP),
            ("Kimyon", 0.5, UnitType.TSP),
            ("Tuz", 1.5, UnitType.TSP),
            ("Karabiber", 0.5, UnitType.TSP),
            ("Limon", 1, UnitType.PIECE),
        ],
        "steps": [
            "Mercimekleri birkaç kez durulayıp süzün. Soğanı, havucu ve patatesi kabaca doğrayın.",
            "Derin bir tencerede zeytinyağını ısıtıp soğanları pembeleştirin. Sarımsakları ekleyip 1 dakika daha kavurun.",
            "Unu ekleyip 1 dakika kokusu çıkana kadar kavurun, ardından domates salçasını ilave edip 30 saniye soteleyin.",
            "Doğranmış havuç ve patatesi ekleyin, 2 dakika karıştırın. Yıkanmış mercimekleri tencereye alın.",
            "Üzerini 2-3 parmak geçecek kadar sıcak su ekleyin (yaklaşık 7 su bardağı). Kaynamaya başlayınca köpüğünü alın.",
            "Kısık ateşte, kapağı aralık, mercimekler ve sebzeler tamamen yumuşayana kadar yaklaşık 25 dakika pişirin.",
            "Tuz, karabiber ve kimyonu ekleyin. Blender ile pürüzsüz olana kadar çekin. Kıvam çok koyuysa biraz sıcak su ekleyin.",
            "Sos için küçük bir tavada tereyağını eritip hafifçe köpürmeye başlayınca pul biberi ekleyin, 10 saniye sonra ocaktan alın.",
            "Çorbayı kaselere paylaştırın, üzerine pul biberli tereyağı gezdirin ve yanında limon dilimi ile servis yapın."
        ]
    },
    # ==================== 3. MENEMEN ====================
    {
        "title": "Klasik Türk Menemeni",
        "description": "Kahvaltı sofralarının yıldızı, sulu kıvamlı, bol domatesli ve biberli geleneksel menemen. Taze ekmek ile birlikte sunulur.",
        "category": "Kahvaltılık",
        "difficulty": "Kolay",
        "diet_type": "Vejetaryen",
        "prep_time": 10,
        "cook_time": 12,
        "servings": 2,
        "ingredients": [
            ("Yumurta", 4, UnitType.PIECE),
            ("Domates", 4, UnitType.PIECE),
            ("Yeşil Biber", 3, UnitType.PIECE),
            ("Soğan", 0.5, UnitType.PIECE),
            ("Sarımsak", 1, UnitType.CLOVE),
            ("Zeytinyağı", 3, UnitType.TBS),
            ("Tereyağı", 1, UnitType.TBS),
            ("Domates Salçası", 0.5, UnitType.TSP),
            ("Tuz", 1, UnitType.TSP),
            ("Karabiber", 0.5, UnitType.TSP),
            ("Pul Biber", 0.5, UnitType.TSP),
            ("Kekik", 0.5, UnitType.TSP),
        ],
        "steps": [
            "Domatesleri kaynar suya atıp kabuklarını soyun, minik küpler halinde doğrayın. Biberleri çekirdeklerini çıkarıp ince ince kıyın. Soğanı ince yarım ay şeklinde dilimleyin.",
            "Geniş, sığ bir tavada zeytinyağı ve tereyağını birlikte ısıtın.",
            "Soğanları yumuşayana kadar 2-3 dakika soteleyin. Ardından biberleri ekleyip 2 dakika daha kavurun.",
            "Dövülmüş sarımsağı ve domates salçasını ekleyip 30 saniye çevirin.",
            "Doğranmış domatesleri tavaya alın, tuz ve baharatları ekleyin. Domateslerin suyu çekene kadar orta ateşte, ara sıra karıştırarak 5-6 dakika pişirin.",
            "Yumurtaları doğrudan sosun üzerine kırın. İsterseniz hafifçe karıştırın (Türk usulü), isterseniz olduğu gibi bırakıp üzerini kapatarak yumurtanın beyazı pişene kadar bekletin (Şakşuka usulü).",
            "Yumurtaların üzeri hâlâ hafif kremamsıyken ocaktan alın — tavada pişmeye devam edecektir. Üzerine taze kekik serpin ve taze ekmekle hemen servis yapın."
        ]
    },
    # ==================== 4. KARNIYARIK ====================
    {
        "title": "Geleneksel Karnıyarık",
        "description": "Türk mutfağının şaheseri: Kızartılmış patlıcanların arasına yerleştirilen bol soğanlı, sarımsaklı kıyma harcı ve fırında domates sosla pişirilmesi.",
        "category": "Ana Yemek",
        "difficulty": "Orta",
        "diet_type": None,
        "prep_time": 30,
        "cook_time": 35,
        "servings": 4,
        "ingredients": [
            ("Patlıcan", 4, UnitType.PIECE),
            ("Dana Kıyma", 300, UnitType.GRAM),
            ("Soğan", 2, UnitType.PIECE),
            ("Sarımsak", 3, UnitType.CLOVE),
            ("Domates", 3, UnitType.PIECE),
            ("Yeşil Biber", 4, UnitType.PIECE),
            ("Domates Salçası", 1.5, UnitType.TBS),
            ("Biber Salçası", 0.5, UnitType.TBS),
            ("Zeytinyağı", 3, UnitType.TBS),
            ("Ayçiçek Yağı", 1, UnitType.GLASS_TEA),
            ("Maydanoz", 0.5, UnitType.BUNCH),
            ("Tuz", 1.5, UnitType.TSP),
            ("Karabiber", 0.5, UnitType.TSP),
            ("Pul Biber", 0.5, UnitType.TSP),
            ("Kimyon", 0.25, UnitType.TSP),
        ],
        "steps": [
            "Patlıcanları alacalı soyun (bir şerit soyun, bir şerit bırakın). Tuzlu suda 15-20 dakika bekletip acısını alın, ardından kurulayın.",
            "Kızartma yağını 170°C'ye ısıtıp patlıcanları her tarafı altın rengi olana kadar kızartın. Kağıt havlu üzerine alıp fazla yağını süzdürün.",
            "İç harç için: Zeytinyağında ince doğranmış soğanları pembeleşene kadar kavurun. Kıymayı ekleyip, sürekli karıştırarak suyunu çekene ve renk alana kadar 5-6 dakika pişirin.",
            "Dövülmüş sarımsakları, ince doğranmış biberlerin yarısını, domates ve biber salçalarını ekleyip 2 dakika kavurun.",
            "Küp doğranmış 1 domates, tuz, karabiber, pul biber ve kimyonu ilave edip 3-4 dakika daha pişirin. Kıyılmış maydanozun yarısını ekleyip karıştırın.",
            "Fırın tepsisine kızartılmış patlıcanları dizin. Her birinin ortasını bıçakla uzunlamasına yarıp kaşıkla hafifçe açın.",
            "Hazırlanan kıymalı harcı patlıcanların arasına cömertçe doldurun. Her patlıcanın üzerine birer domates dilimi ve biber yerleştirin.",
            "Sos için: 1 yemek kaşığı salçayı 1 su bardağı sıcak suda eritin, tepsinin dibine dökün.",
            "Önceden ısıtılmış 180°C fırında 25-30 dakika, domatesler yumuşayana ve sos koyulaşana kadar pişirin. Kalan maydanozla süsleyip servis yapın."
        ]
    },
    # ==================== 5. PAD THAI ====================
    {
        "title": "Pad Thai",
        "description": "Tayland sokak lezzetinin en ünlüsü: Wokta sote edilmiş pirinç eriştesi, karides, tofu, yer fıstığı ve taze limon ile.",
        "category": "Ana Yemek",
        "difficulty": "Orta",
        "diet_type": None,
        "prep_time": 20,
        "cook_time": 10,
        "servings": 2,
        "ingredients": [
            ("Pirinç Eriştesi", 200, UnitType.GRAM),
            ("Karides", 150, UnitType.GRAM),
            ("Sert Tofu", 100, UnitType.GRAM),
            ("Yumurta", 2, UnitType.PIECE),
            ("Soya Filizi", 100, UnitType.GRAM),
            ("Taze Soğan", 3, UnitType.PIECE),
            ("Sarımsak", 2, UnitType.CLOVE),
            ("Yer Fıstığı", 30, UnitType.GRAM),
            ("Balık Sosu", 2, UnitType.TBS),
            ("Tamarind Ezmesi", 1, UnitType.TBS),
            ("Toz Şeker", 1, UnitType.TBS),
            ("Sriracha Sos", 1, UnitType.TSP),
            ("Ayçiçek Yağı", 2, UnitType.TBS),
            ("Limon", 1, UnitType.PIECE),
            ("Pul Biber", 0.5, UnitType.TSP),
        ],
        "steps": [
            "Pirinç eriştesini ılık suda 20-25 dakika yumuşayana kadar bekletin, süzün.",
            "Pad Thai sosunu hazırlayın: Tamarind ezmesi, balık sosu, şeker ve sriracha'yı küçük bir kasede karıştırın.",
            "Tofu'yu küçük küpler halinde kesin. Wok veya geniş tavada 1 yemek kaşığı yağı kızdırıp tofu'yu her tarafı altın rengi olana kadar kızartın, tabağa alın.",
            "Aynı wok'a kalan yağı ekleyin, doğranmış sarımsağı 15 saniye kavurun. Karidesleri ekleyip her iki tarafı da pembe olana kadar 2 dakika pişirin.",
            "Yumurtaları wok'un bir köşesine kırıp 30 saniye karıştırarak scramble yapın.",
            "Süzülmüş eriştleri ve hazırladığınız sosu wok'a ekleyin. Maşayla karıştırarak eriştelerin sosu emmesini sağlayın, 2-3 dakika pişirin.",
            "Kızarmış tofu'yu, soya filizlerini ve doğranmış taze soğanın yeşil kısımlarını ekleyip 1 dakika daha karıştırın.",
            "Tabağa alıp üzerine kaba dövülmüş yer fıstığı, pul biber ve limon dilimi ile servis yapın."
        ]
    },
    # ==================== 6. BUTTER CHICKEN ====================
    {
        "title": "Butter Chicken (Murgh Makhani)",
        "description": "Hint mutfağının dünya çapında en sevilen yemeği: Baharatlı yoğurtlu marine edilmiş tavuk, tereyağlı ve kremalı domates sosunda. Naan ekmeğiyle mükemmel.",
        "category": "Ana Yemek",
        "difficulty": "Orta",
        "diet_type": None,
        "prep_time": 30,
        "cook_time": 30,
        "servings": 4,
        "ingredients": [
            ("Tavuk Göğsü", 600, UnitType.GRAM),
            ("Yoğurt", 0.5, UnitType.GLASS_WATER),
            ("Domates", 4, UnitType.PIECE),
            ("Soğan", 1, UnitType.PIECE),
            ("Sarımsak", 4, UnitType.CLOVE),
            ("Taze Zencefil", 1, UnitType.PIECE),
            ("Tereyağı", 3, UnitType.TBS),
            ("Krema", 0.5, UnitType.GLASS_WATER),
            ("Garam Masala", 1, UnitType.TBS),
            ("Zerdeçal (Toz)", 1, UnitType.TSP),
            ("Kimyon", 1, UnitType.TSP),
            ("Pul Biber", 1, UnitType.TSP),
            ("Toz Şeker", 1, UnitType.TSP),
            ("Tuz", 1.5, UnitType.TSP),
            ("Taze Kişniş Yaprağı", 0.5, UnitType.BUNCH),
        ],
        "steps": [
            "Marine: Tavuk göğüslerini büyük küpler halinde kesin. Yoğurt, garam masala'nın yarısı, zerdeçal, kimyon ve 1 çay kaşığı tuz ile marine edip buzdolabında en az 30 dakika (ideal 2 saat) bekletin.",
            "Marine edilmiş tavukları yüksek ateşte ızgarada veya tavada her tarafı güzelce kavrulana kadar 3-4 dakika pişirin. Tam olarak pişmesi gerekmez, sosta da pişecektir. Kenara alın.",
            "Sos: Domatesleri kaynar suya atıp kabuklarını soyun, kabaca doğrayın.",
            "Geniş tencerede tereyağının yarısını eritin. Doğranmış soğanı ve rendlenmiş zencefili 5-6 dakika kavurun. Dövülmüş sarımsakları ekleyip 1 dakika daha pişirin.",
            "Domatesleri, kalan garam masala, pul biber ve şekeri ekleyin. Kısık ateşte 10-12 dakika, domatesler tamamen eriyene kadar pişirin.",
            "Sosu blender'dan geçirip pürüzsüz hale getirin. Tencereye geri dökün.",
            "Tavuk parçalarını sosa ekleyin, kalan tereyağını ve kremayı ilave edin. Kısık ateşte 10-12 dakika, tavuklar tamamen pişene ve sos koyulaşana kadar pişirin.",
            "Tuz ayarını yapın. Tabağa alıp üzerine taze kişniş yaprakları serpin ve yanında sıcak naan ekmeği veya basmati pilavıyla servis yapın."
        ]
    },
    # ==================== 7. HATAY USULÜ KISIR ====================
    {
        "title": "Hatay Usulü Kısır",
        "description": "Hatay'ın meşhur kısırı: Bol nar ekşili, acılı, taze yeşilliklerle dolu, meze sofralarının olmazsa olmazı.",
        "category": "Meze",
        "difficulty": "Kolay",
        "diet_type": "Vegan",
        "prep_time": 25,
        "cook_time": 0,
        "servings": 8,
        "ingredients": [
            ("Bulgur", 2, UnitType.GLASS_WATER),
            ("Taze Soğan", 6, UnitType.PIECE),
            ("Domates", 2, UnitType.PIECE),
            ("Salatalık", 1, UnitType.PIECE),
            ("Maydanoz", 1, UnitType.BUNCH),
            ("Taze Nane Yaprağı", 0.5, UnitType.BUNCH),
            ("Domates Salçası", 2, UnitType.TBS),
            ("Biber Salçası", 1, UnitType.TBS),
            ("Nar Ekşisi", 3, UnitType.TBS),
            ("Zeytinyağı", 0.5, UnitType.GLASS_TEA),
            ("Limon Suyu", 2, UnitType.TBS),
            ("Pul Biber", 1, UnitType.TBS),
            ("Kimyon", 1, UnitType.TSP),
            ("Tuz", 1, UnitType.TSP),
            ("Isot", 0.5, UnitType.TSP),
        ],
        "steps": [
            "İnce bulguru derin bir kaba alın, üzerine 2 su bardağı kaynar su dökün. Üzerini streç filmle kapatıp 15-20 dakika şişmesini bekleyin.",
            "Bulgur şişerken salçaları, zeytinyağını, nar ekşisini ve limon suyunu küçük bir kapta karıştırıp sos olarak hazırlayın.",
            "Şişen bulgura hazırladığınız sosu dökün ve elinizle iyice yoğurun, tüm sıvının bulgura eşit şekilde dağılmasını sağlayın.",
            "Pul biber, kimyon, ısot ve tuzu ekleyip tekrar yoğurun. Bulgur güzel bir kızıl renk almalıdır.",
            "Taze soğanları ince ince kıyın. Domatesleri küçük küpler halinde doğrayın. Salatalığı minik küpler kesin. Maydanoz ve naneyi ince kıyın.",
            "Tüm doğranmış yeşillikleri ve sebzeleri bulgura ekleyip karıştırın. Tat kontrolü yapıp gerekirse nar ekşisi veya tuz ekleyin.",
            "En az 15 dakika buzdolabında dinlendirin. Marul yapraklarının içine koyarak veya tabağa alıp yanında limon dilimi ile servis yapın."
        ]
    },
    # ==================== 8. LAZANYA ====================
    {
        "title": "Klasik İtalyan Lazanya",
        "description": "Katman katman bolonez sos, beşamel ve erimiş peynirle hazırlanan fırın lazanya. Hafta sonu sofralarının gözdesi.",
        "category": "Ana Yemek",
        "difficulty": "Zor",
        "diet_type": None,
        "prep_time": 30,
        "cook_time": 45,
        "servings": 6,
        "ingredients": [
            ("Lazanya Yaprağı", 250, UnitType.GRAM),
            ("Dana Kıyma", 400, UnitType.GRAM),
            ("Soğan", 1, UnitType.PIECE),
            ("Sarımsak", 3, UnitType.CLOVE),
            ("Havuç", 1, UnitType.PIECE),
            ("Domates Salçası", 2, UnitType.TBS),
            ("Domates", 3, UnitType.PIECE),
            ("Mozzarella", 250, UnitType.GRAM),
            ("Parmesan", 60, UnitType.GRAM),
            ("Tereyağı", 3, UnitType.TBS),
            ("Un", 3, UnitType.TBS),
            ("Süt", 2.5, UnitType.GLASS_WATER),
            ("Zeytinyağı", 2, UnitType.TBS),
            ("Tuz", 1.5, UnitType.TSP),
            ("Karabiber", 0.5, UnitType.TSP),
            ("Kekik", 1, UnitType.TSP),
            ("Muskat", 0.25, UnitType.TSP),
        ],
        "steps": [
            "Bolonez sos: Soğan, sarımsak ve havucu minik küpler halinde doğrayın. Zeytinyağında soğanı 3-4 dakika kavurun, havuç ve sarımsağı ekleyip 2 dakika daha soteleyin.",
            "Kıymayı ekleyip suyunu çekene kadar yüksek ateşte 5-6 dakika parçalayarak kavurun. Salçayı ekleyip 1 dakika kavurun.",
            "Rendelenmiş domatesleri, kekik, tuz ve karabiberi ekleyin. Kısık ateşte, ara sıra karıştırarak 15-20 dakika sos koyulaşana kadar pişirin.",
            "Beşamel sos: Ayrı bir tencerede tereyağını eritip unu ekleyin, sürekli karıştırarak 2 dakika kavurun (roux). Soğuk sütü yavaş yavaş ekleyip her seferinde pürüzsüz olana kadar çırpın.",
            "Kısık ateşte, sürekli karıştırarak sos 5-7 dakikada koyu bir kıvam alana kadar pişirin. Tuz, karabiber ve muskat ekleyin.",
            "Montaj: Fırın kabının tabanına ince bir kat beşamel sürün. Lazanya yapraklarını dizin. Üzerine bolonez sos, beşamel ve doğranmış mozzarella sırasıyla yayın.",
            "Bu katmanlama işlemini 3-4 kez tekrarlayın. En üst kat beşamel ve bol peynir (mozzarella + rendelenmiş parmesan) olsun.",
            "Üzerini alüminyum folyo ile kapatıp önceden ısıtılmış 180°C fırında 25 dakika pişirin. Folyoyu kaldırıp 15-20 dakika daha, peynir güzelce kızarana kadar pişirin.",
            "Fırından çıkarıp 10-15 dakika dinlendirin (bu süre çok önemli, katmanların oturması gerekir). Sonra dilimleyip servis yapın."
        ]
    },
    # ==================== 9. SOMON TERİYAKİ ====================
    {
        "title": "Teriyaki Somon",
        "description": "Parlak teriyaki glazesiyle kaplanmış, dışı karamelize içi sulu somon fileto. Yanında buharda pişmiş pirinç ve sebzelerle.",
        "category": "Ana Yemek",
        "difficulty": "Kolay",
        "diet_type": None,
        "prep_time": 10,
        "cook_time": 12,
        "servings": 2,
        "ingredients": [
            ("Somon", 400, UnitType.GRAM),
            ("Soya Sosu", 3, UnitType.TBS),
            ("Mirin", 2, UnitType.TBS),
            ("Bal", 1, UnitType.TBS),
            ("Pirinç Sirkesi", 1, UnitType.TBS),
            ("Sarımsak", 2, UnitType.CLOVE),
            ("Taze Zencefil", 1, UnitType.PIECE),
            ("Susam", 1, UnitType.TBS),
            ("Ayçiçek Yağı", 1, UnitType.TBS),
            ("Taze Soğan", 2, UnitType.PIECE),
            ("Nişasta", 1, UnitType.TSP),
        ],
        "steps": [
            "Teriyaki sos: Soya sosu, mirin, bal, pirinç sirkesi, rendelenmiş sarımsak ve zencefili bir kasede karıştırın.",
            "Nişastayı 1 yemek kaşığı soğuk suyla eritip sosa ekleyin (pişince koyulaşacak).",
            "Somon filetolarını kağıt havluyla kurulayıp tuzlayın. Derisiz tarafta bıçakla çapraz çizikler atın.",
            "Tavada yağı orta-yüksek ateşte kızdırın. Somonu derisi üste gelecek şekilde tavaya yerleştirin, 3-4 dakika hiç oynatmadan pişirin.",
            "Çevirip deri tarafını 2 dakika pişirin. Ateşi kısıp hazırladığınız teriyaki sosun yarısını tavaya dökün.",
            "Sosu kaşıkla somon üzerine gezdirerek, sos koyulaşana ve balıklar parlak bir kaplama alana kadar 2-3 dakika daha pişirin.",
            "Tabağa alıp üzerine kalan sosu, susam ve doğranmış taze soğan serpin. Yanında buharda pişmiş pirinç ile servis yapın."
        ]
    },
    # ==================== 10. KÜNEFE ====================
    {
        "title": "Antep Usulü Künefe",
        "description": "Antep fıstıklı, bol şerbetli, çıtır kadayıflı ve uzayan peynirli sıcak tatlı. Türk tatlı kültürünün en sevilen temsilcisi.",
        "category": "Tatlı",
        "difficulty": "Orta",
        "diet_type": "Vejetaryen",
        "prep_time": 20,
        "cook_time": 25,
        "servings": 6,
        "ingredients": [
            ("Kadayıf (Taze)", 300, UnitType.GRAM),
            ("Mozzarella", 200, UnitType.GRAM),
            ("Tereyağı", 100, UnitType.GRAM),
            ("Toz Şeker", 2, UnitType.GLASS_WATER),
            ("Limon Suyu", 1, UnitType.TSP),
            ("Antep Fıstığı", 50, UnitType.GRAM),
            ("Gül Suyu", 1, UnitType.TBS),
        ],
        "steps": [
            "Şerbet: 2 su bardağı şeker ve 1.5 su bardağı suyu tencerede kaynatın. Limon suyunu ekleyip kısık ateşte 10-12 dakika pişirin. Gül suyunu ekleyip soğumaya bırakın. Şerbet soğuk olmalıdır.",
            "Mozzarella peynirini 2-3 saat suda bekletip tuzunu alın. Süzüp rendeleyin ya da ince ince doğrayın.",
            "Kadayıfı ince ince açıp didikleyin, çok uzun telleri makasla kısaltın.",
            "Tereyağını eritip kadayıfın üzerine dökün ve ellerinizle her teli yağlayarak iyice karıştırın.",
            "Künefe kalıbının (veya tava) tabanına kadayıfın yarısını sıkıştırarak yayın. Üzerine peyniri eşit şekilde dağıtın (kenarlardan 1cm boşluk bırakın). Kalan kadayıfı üzerine yayıp bastırın.",
            "Kısık ateşte, altı kızarana kadar 10-12 dakika pişirin. Bir tabak yardımıyla çevirip diğer tarafını da 8-10 dakika kızartın.",
            "Her iki tarafı da altın sarısı olduğunda soğuk şerbeti yavaş yavaş üzerine dökün. Dövülmüş Antep fıstığı ile süsleyip hemen sıcak servis yapın."
        ]
    },
    # ==================== 11. ÇILBIR ====================
    {
        "title": "Osmanlı Çılbırı",
        "description": "Osmanlı saray mutfağından gelen zarif kahvaltılık: Sarımsaklı yoğurt yatağı üzerinde poşe yumurta, üzerine pul biberli tereyağı.",
        "category": "Kahvaltılık",
        "difficulty": "Orta",
        "diet_type": "Vejetaryen",
        "prep_time": 5,
        "cook_time": 10,
        "servings": 2,
        "ingredients": [
            ("Yumurta", 4, UnitType.PIECE),
            ("Süzme Yoğurt", 1, UnitType.GLASS_WATER),
            ("Sarımsak", 1, UnitType.CLOVE),
            ("Tereyağı", 2, UnitType.TBS),
            ("Pul Biber", 1, UnitType.TSP),
            ("Sirke", 1, UnitType.TBS),
            ("Tuz", 0.5, UnitType.TSP),
            ("Dereotu", 0.25, UnitType.BUNCH),
            ("Sumak", 0.5, UnitType.TSP),
        ],
        "steps": [
            "Süzme yoğurdu bir kasede ezilmiş sarımsak ve bir tutam tuzla iyice karıştırın. Oda sıcaklığında olmalıdır (buzdolabından 15 dakika önce çıkarın).",
            "Geniş bir tencerede suyu kaynatıp sirkеуі ekleyin. Ateşi kısıp suyu hafifçe çalkalar hale getirin.",
            "Yumurtaları teker teker bir kaseye kırıp nazikçe suyun içine bırakın. 3-3.5 dakika pişirin (beyazı pişmiş, sarısı akıcı olmalı). Kevgirle çıkarıp kağıt havluya alın.",
            "Küçük bir tavada tereyağını eritip hafifçe köpürmeye başlayınca pul biberi ekleyin, 10 saniye sonra hemen ocaktan alın.",
            "Servis tabağına sarımsaklı yoğurdu yayın, üzerine poşe yumurtaları yerleştirin.",
            "Pul biberli tereyağını yumurtaların üzerine gezdirin. Sumak ve doğranmış taze dereotu serpin. Sıcak ekmek veya pide ile hemen servis yapın."
        ]
    },
    # ==================== 12. ZEYTİNYAĞLI ENGINAR ====================
    {
        "title": "Zeytinyağlı Enginar",
        "description": "İstanbul mutfağının bahar klasiği: Havuç, bezelye ve patatesle zenginleştirilmiş, limonlu zeytinyağlı enginar. Soğuk servis edilir.",
        "category": "Meze",
        "difficulty": "Orta",
        "diet_type": "Vegan",
        "prep_time": 25,
        "cook_time": 35,
        "servings": 4,
        "ingredients": [
            ("Enginar", 4, UnitType.PIECE),
            ("Havuç", 2, UnitType.PIECE),
            ("Patates", 1, UnitType.PIECE),
            ("Bezelye", 0.5, UnitType.GLASS_WATER),
            ("Soğan", 1, UnitType.PIECE),
            ("Limon", 2, UnitType.PIECE),
            ("Zeytinyağı", 0.5, UnitType.GLASS_TEA),
            ("Toz Şeker", 1, UnitType.TSP),
            ("Un", 1, UnitType.TBS),
            ("Dereotu", 0.5, UnitType.BUNCH),
            ("Tuz", 1, UnitType.TSP),
        ],
        "steps": [
            "Limonlu su hazırlayın (1 limonun suyu + su + 1 yemek kaşığı un karıştırın). Enginarların dış yapraklarını koparın, iç kısmını kazıyıp limonlu suya atın.",
            "Soğanı ince doğrayın, havuçları yuvarlak dilimleyin, patatesi küçük küpler halinde kesin.",
            "Geniş ve sığ bir tencerede zeytinyağını ısıtıp soğanları 3-4 dakika kavurun.",
            "Havuç ve patatesleri ekleyip 2-3 dakika soteleyin. Şekeri serpin.",
            "Enginarları limonlu sudan çıkarıp tencereye yerleştirin, iç kısımları yukarı bakacak şekilde. Bezelyeleri aralarına dağıtın.",
            "Üzerlerine 1 limonun suyunu sıkın, 1 su bardağı sıcak su ekleyin ve tuzlayın.",
            "Üzerini yağlı kağıtla kapatıp (temas edecek şekilde) kısık ateşte 30-35 dakika, sebzeler yumuşayana kadar pişirin.",
            "Ocaktan alıp tencerede tamamen soğumaya bırakın. Tabağa alıp üzerine dereotu serpin ve limon dilimi ile soğuk servis yapın."
        ]
    },
    # ==================== 13. TAVUKFAJİTA ====================
    {
        "title": "Tavuklu Fajita",
        "description": "Meksika mutfağından renkli biberler ve baharatlı tavukla hazırlanan canlı fajita. Tortilla, guacamole ve ekşi krema eşliğinde.",
        "category": "Ana Yemek",
        "difficulty": "Kolay",
        "diet_type": None,
        "prep_time": 15,
        "cook_time": 12,
        "servings": 4,
        "ingredients": [
            ("Tavuk Göğsü", 500, UnitType.GRAM),
            ("Kırmızı Biber", 1, UnitType.PIECE),
            ("Yeşil Biber", 1, UnitType.PIECE),
            ("Soğan", 1, UnitType.PIECE),
            ("Sarımsak", 2, UnitType.CLOVE),
            ("Tortilla (Buğday)", 4, UnitType.PIECE),
            ("Zeytinyağı", 3, UnitType.TBS),
            ("Limon", 1, UnitType.PIECE),
            ("Kimyon", 1, UnitType.TSP),
            ("Tatlı Toz Biber", 1, UnitType.TSP),
            ("Pul Biber", 0.5, UnitType.TSP),
            ("Tuz", 1, UnitType.TSP),
            ("Karabiber", 0.5, UnitType.TSP),
            ("Ekşi Krema (Sour Cream)", 4, UnitType.TBS),
        ],
        "steps": [
            "Tavukları ince şeritler halinde kesin. Kimyon, tatlı toz biber, pul biber, tuz, karabiber ve 1 yemek kaşığı zeytinyağı ile marine edip 10 dakika bekletin.",
            "Biberleri ve soğanı uzun, ince şeritler halinde kesin.",
            "Geniş bir tavayı veya woku yüksek ateşte ısıtın. Kalan yağı ekleyip marine tavukları, hiç oynatmadan 2-3 dakika pişirin. Çevirip 2 dakika daha pişirin. Tabağa alın.",
            "Aynı tavada biberleri ve soğanı yüksek ateşte, hafif yanık lekeler oluşacak şekilde 3-4 dakika soteleyin. Biraz çıtır kalmalılar.",
            "Tavukları tekrar tavaya ekleyin, dövülmüş sarımsağı ilave edip 1 dakika karıştırın. Limon suyunu sıkın.",
            "Tortillaları kuru bir tavada veya doğrudan ateşte her iki tarafını 20-30 saniye ısıtın.",
            "Sıcak tortillaların içine tavuk-biber karışımını koyun, üzerine ekşi krema ekleyin. Dürüm yaparak hemen servis edin."
        ]
    },
    # ==================== 14. YAYLA ÇORBASI ====================
    {
        "title": "Yayla Çorbası",
        "description": "Anadolu'nun ferahlatıcı yoğurt çorbası: Naneyi tereyağında kavurup üzerine gezdirdiğiniz, pirinçli terbiyeli yoğurt çorbası.",
        "category": "Çorba",
        "difficulty": "Kolay",
        "diet_type": "Vejetaryen",
        "prep_time": 5,
        "cook_time": 25,
        "servings": 4,
        "ingredients": [
            ("Yoğurt", 2, UnitType.GLASS_WATER),
            ("Pirinç", 3, UnitType.TBS),
            ("Yumurta", 1, UnitType.PIECE),
            ("Un", 1, UnitType.TBS),
            ("Tereyağı", 2, UnitType.TBS),
            ("Nane", 1, UnitType.TBS),
            ("Tuz", 1.5, UnitType.TSP),
            ("Karabiber", 0.5, UnitType.TSP),
        ],
        "steps": [
            "Pirinçleri yıkayıp 4 su bardağı suyla tencereye alın, kaynamaya başlayınca kısık ateşte 15 dakika, pirinçler yumuşayana kadar pişirin.",
            "Terbiye: Geniş bir kasede yoğurdu, unu ve yumurtayı çırpıcı ile pürüzsüz olana kadar iyice çırpın (topak kalmamalı).",
            "Pirinçli suyun bir kepçesini alıp yavaş yavaş, sürekli çırparak yoğurt karışımına ekleyin. Bu işlemi 2-3 kepçe ile tekrarlayın (terbiye ılıştırma).",
            "Ilıştırılmış terbiyeyi sürekli karıştırarak tencereye dökün. Kısık ateşte, sürekli karıştırarak, kaynamaya yakın 5-7 dakika pişirin. KAYNAMASIN, yoksa kesilir.",
            "Tuz ve karabiber ekleyin.",
            "Sos: Küçük bir tavada tereyağını eritip hafifçe kızarmaya başlayınca kuru naneyi ekleyin, 5 saniye sonra ocaktan alın.",
            "Çorbayı kaselere paylaştırıp üzerine naneli tereyağı gezdirerek sıcak servis yapın."
        ]
    },
    # ==================== 15. EZOGELİN ÇORBASI ====================
    {
        "title": "Ezogelin Çorbası",
        "description": "Gaziantep'in gelin çorbası: Kırmızı mercimek, bulgur ve pirinçle doyurucu, salçalı ve baharatlı geleneksel Anadolu çorbası.",
        "category": "Çorba",
        "difficulty": "Kolay",
        "diet_type": "Vegan",
        "prep_time": 10,
        "cook_time": 30,
        "servings": 6,
        "ingredients": [
            ("Kırmızı Mercimek", 1, UnitType.GLASS_WATER),
            ("Bulgur", 3, UnitType.TBS),
            ("Pirinç", 2, UnitType.TBS),
            ("Soğan", 1, UnitType.PIECE),
            ("Domates Salçası", 1.5, UnitType.TBS),
            ("Biber Salçası", 0.5, UnitType.TBS),
            ("Tereyağı", 2, UnitType.TBS),
            ("Zeytinyağı", 1, UnitType.TBS),
            ("Nane", 1, UnitType.TBS),
            ("Pul Biber", 1, UnitType.TSP),
            ("Kimyon", 0.5, UnitType.TSP),
            ("Karabiber", 0.5, UnitType.TSP),
            ("Tuz", 1.5, UnitType.TSP),
        ],
        "steps": [
            "Kırmızı mercimek, bulgur ve pirinci bol suda yıkayıp süzün.",
            "Tencerede zeytinyağını ısıtıp ince doğranmış soğanı 3-4 dakika kavurun.",
            "Domates ve biber salçalarını ekleyip 1 dakika kavurun, kokusu çıksın.",
            "Yıkanmış mercimek, bulgur ve pirinci tencereye ekleyin. 7 su bardağı sıcak su ilave edin.",
            "Kaynamaya başlayınca ateşi kısıp köpüğünü alın. Kapağı aralık, 25 dakika tüm malzemeler yumuşayana kadar pişirin.",
            "Tuz, karabiber ve kimyonu ekleyip karıştırın. Kıvam çok koyuysa sıcak su ekleyin.",
            "Sos için: Tereyağını küçük bir tavada eritip pul biber ve naneyi ekleyin, 10 saniye çevirip ocaktan alın.",
            "Çorbayı kaselere alıp üzerine pul biberli-naneli tereyağı gezdirin. Yanında limon ve ekmek ile servis yapın."
        ]
    },
]

# =====================================================================

CATEGORY_MAP = {
    "Çorba": RecipeCategory.SOUP,
    "Kahvaltılık": RecipeCategory.BREAKFAST,
    "Ana Yemek": RecipeCategory.MAIN_COURSE,
    "Meze": RecipeCategory.APPETIZER,
    "Tatlı": RecipeCategory.DESSERT,
    "Salata": RecipeCategory.SALAD
}
DIFFICULTY_MAP = {
    "Kolay": DifficultyLevel.EASY,
    "Orta": DifficultyLevel.MEDIUM,
    "Zor": DifficultyLevel.HARD
}

async def seed_recipes():
    print("Connecting to database...")
    nutrition_service = NutritionCalculatorService()

    async with AsyncSessionLocal() as session:
        recipe_repo = PostgresRecipeRepository(session)
        ing_repo = PostgresIngredientRepository(session)
        user_repo = PostgresUserRepository(session)

        admin = await user_repo.get_by_email("admin@example.com")
        if not admin:
            print("Admin user not found!")
            return

        async def get_ing(name):
            return await ing_repo.get_by_name(name)

        for r in RECIPES:
            print(f"\n{'='*50}")
            print(f"Processing: {r['title']}")

            items = []
            total_cal = total_pro = total_carb = total_fat = 0.0
            missing = []

            for ing_name, amount, unit in r["ingredients"]:
                ing = await get_ing(ing_name)
                if not ing:
                    missing.append(ing_name)
                    continue
                items.append(RecipeItem(ingredient=ing, amount=amount, unit=unit))
                grams = nutrition_service.calculate_grams(amount, unit, ing)
                info = nutrition_service.calculate_nutrition(grams, ing)
                total_cal += info.calories
                total_pro += info.protein
                total_carb += info.carbs
                total_fat += info.fat

            if missing:
                print(f"  ⚠ Missing ingredients: {', '.join(missing)}")

            instructions = [
                RecipeInstruction(id=str(uuid.uuid4()), step_number=i+1, text=text)
                for i, text in enumerate(r["steps"])
            ]

            recipe = Recipe(
                id=str(uuid.uuid4()),
                title=r["title"],
                description=r["description"],
                items=items,
                instructions=instructions,
                category=CATEGORY_MAP.get(r["category"]),
                difficulty=DIFFICULTY_MAP.get(r["difficulty"]),
                diet_type=r["diet_type"],
                prep_time_minutes=r["prep_time"],
                cook_time_minutes=r["cook_time"],
                servings=r["servings"],
                total_calories=round(total_cal, 1),
                total_protein=round(total_pro, 1),
                total_carbs=round(total_carb, 1),
                total_fat=round(total_fat, 1),
                status=RecipeStatus.PUBLISHED,
                author_id=admin.id,
                slug=slugify(r["title"]) + "-" + uuid.uuid4().hex[:6]
            )

            await recipe_repo.save(recipe)
            print(f"  ✓ Saved | {len(items)} ingredients, {len(instructions)} steps")
            print(f"    Calories: {round(total_cal,1)} | Protein: {round(total_pro,1)}g | Carbs: {round(total_carb,1)}g | Fat: {round(total_fat,1)}g")

        await session.commit()
        print(f"\n{'='*50}")
        print(f"Done! Successfully seeded {len(RECIPES)} recipes.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_recipes())
