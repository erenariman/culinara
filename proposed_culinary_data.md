# Culinara Temel Mutfak Veritabanı (Öneri)

Bu döküman, veritabanına toplu olarak eklenecek olan malzeme ve tariflerin listesini içerir. Lütfen verileri, birimleri ve tarif adımlarını kontrol ediniz.

---

## 1. Malzeme Listesi (100 Temel Malzeme)

Her malzeme 100g bazındaki besin değerlerini ve gram -> ml dönüşümü için yoğunluk (Density) bilgisini içerir.

| Malzeme Adı | Kalori (kcal) | Protein (g) | Yağ (g) | Karbonhidrat (g) | Yoğunluk (g/ml) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Zeytinyağı** | 884 | 0 | 100 | 0 | 0.92 |
| **Tereyağı** | 717 | 0.8 | 81 | 0.1 | 0.91 |
| **Ayçiçek Yağı** | 884 | 0 | 100 | 0 | 0.92 |
| **Domates** | 18 | 0.9 | 0.2 | 3.9 | 0.94 |
| **Soğan (Kuru)** | 40 | 1.1 | 0.1 | 9.3 | 0.90 |
| **Sarımsak** | 149 | 6.4 | 0.5 | 33 | 0.60 |
| **Patates** | 77 | 2 | 0.1 | 17 | 0.75 |
| **Havuç** | 41 | 0.9 | 0.2 | 9.6 | 0.64 |
| **Domates Salçası** | 82 | 4.3 | 0.5 | 18.9 | 1.10 |
| **Biber Salçası** | 95 | 3.5 | 1.2 | 16.5 | 1.15 |
| **Dana Kıyma (%20 Yağlı)** | 250 | 26 | 17 | 0 | 1.00 |
| **Tavuk Göğsü** | 165 | 31 | 3.6 | 0 | 1.04 |
| **Kırmızı Mercimek** | 353 | 24 | 1.1 | 54 | 0.85 |
| **Pirinç (Osmancık/Baldo)** | 365 | 7.1 | 0.7 | 80 | 0.82 |
| **Bulgur (Pilavlık)** | 342 | 12 | 1.3 | 76 | 0.80 |
| **Un (Buğday)** | 364 | 10 | 1 | 76 | 0.55 |
| **Toz Şeker** | 387 | 0 | 0 | 100 | 0.85 |
| **Tuz** | 0 | 0 | 0 | 0 | 1.20 |
| **Yoğurt (Tam Yağlı)** | 61 | 3.5 | 3.3 | 4.7 | 1.05 |
| **Süt (%3 Yağlı)** | 60 | 3.2 | 3.2 | 4.8 | 1.03 |
| **Yumurta (L Boy)** | 155 | 13 | 11 | 1.1 | 1.02 |
| **Beyaz Peynir** | 250 | 15 | 20 | 2.5 | 1.00 |
| **Kaşar Peyniri** | 350 | 25 | 27 | 2 | 1.00 |
| **Patlıcan** | 25 | 1 | 0.2 | 6 | 0.60 |
| **Kabak** | 17 | 1.2 | 0.3 | 3.1 | 0.65 |
| **Yeşil Biber (Sivri/Çarliston)** | 20 | 0.9 | 0.2 | 4.6 | 0.50 |
| **Kırmızı Biber (Kapya)** | 31 | 1 | 0.3 | 6 | 0.55 |
| **Ispanak** | 23 | 2.9 | 0.4 | 3.6 | 0.40 |
| **Maydanoz** | 36 | 3 | 0.8 | 6 | 0.35 |
| **Dereotu** | 43 | 3.5 | 1.1 | 7 | 0.35 |
| **Nane (Kuru)** | 285 | 20 | 6 | 52 | 0.25 |
| **Karabiber** | 251 | 10 | 3 | 64 | 0.50 |
| **Pul Biber** | 282 | 12 | 10 | 50 | 0.45 |
| **Kimyon** | 375 | 18 | 22 | 44 | 0.45 |
| **Kekik** | 101 | 6 | 4 | 24 | 0.25 |
| **Limon Suyu** | 22 | 0.4 | 0.2 | 7 | 1.03 |
| **Sirke (Elma/Üzüm)** | 18 | 0 | 0 | 0.9 | 1.01 |
| **Ekmek (Beyaz)** | 265 | 9 | 3.2 | 49 | 0.30 |
| **Makarna (Spaghetti)** | 370 | 13 | 1.5 | 75 | 0.50 |
| **Nohut (Kuru)** | 364 | 19 | 6 | 61 | 0.80 |
| **Kuru Fasulye** | 333 | 23 | 0.8 | 60 | 0.80 |
| **Mantar (Kültür)** | 22 | 3.1 | 0.3 | 3.3 | 0.50 |
| **Ceviz İçi** | 654 | 15 | 65 | 14 | 0.45 |
| **Fındık İçi** | 628 | 15 | 61 | 17 | 0.50 |
| **Bal** | 304 | 0.3 | 0 | 82 | 1.40 |
| **Tahin** | 595 | 17 | 54 | 21 | 0.95 |
| **Pekmez (Üzüm)** | 290 | 0 | 0 | 75 | 1.45 |
| **İrmik** | 360 | 12 | 1 | 73 | 0.70 |
| **Mısır Nişastası** | 381 | 0.3 | 0.1 | 91 | 0.60 |
| **Kabartma Tozu** | 100 | 0 | 0 | 25 | 0.90 |

*(Liste 100'e tamamlanacak şekilde sebze, meyve ve baharatlarla genişletilecektir)*

---

## 2. Tarif Listesi (15 Klasik Tarif)

### T1. Süzme Mercimek Çorbası
*   **Açıklama:** Klasik, pürüzsüz ve besleyici Türk usulü restorant mercimek çorbası.
*   **Kategori:** Çorba | **Süre:** 35 dk | **Porsiyon:** 4
*   **Malzemeler:**
    *   1 Su Bardağı Kırmızı Mercimek
    *   1 Adet Soğan (Orta boy)
    *   1 Adet Havuç (Küçük boy)
    *   1 Yemek Kaşığı Un
    *   2 Yemek Kaşığı Tereyağı
    *   6 Su Bardağı Su (Sıcak)
    *   1 Çay Kaşığı Tuz, Yarım Çay Kaşığı Karabiber
*   **Adımlar:**
    1. Mercimekleri iyice yıkayıp süzün.
    2. Soğan ve havucu rastgele doğrayın (Zaten blenderdan geçecek).
    3. Tencerede 1 kaşık yağı eritip soğan ve havucu soteleyin.
    4. Unu ekleyip kokusu çıkana kadar kavurun.
    5. Mercimekleri ve 6 bardak sıcak suyu ekleyip mercimekler yumuşayana kadar pişirin.
    6. Pişen çorbayı pürüzsüz olana kadar blenderdan geçirin.
    7. Sos tavasında kalan tereyağını pul biberle kızdırıp çorbanın üzerine gezdirin.

### T2. Menemen
*   **Açıklama:** Kahvaltıların vazgeçilmezi, sulu ve lezzetli domatesli biberli yumurta.
*   **Kategori:** Kahvaltı | **Süre:** 15 dk | **Porsiyon:** 2
*   **Malzemeler:**
    *   3 Adet Yumurta
    *   4 Adet Domates (Soyulmuş ve doğranmış)
    *   3 Adet Yeşil Biber
    *   2 Yemek Kaşığı Zeytinyağı
    *   1 Çay Kaşığı Tuz, Yarım Çay Kaşığı Karabiber
*   **Adımlar:**
    1. Biberleri ince ince doğrayıp yağda yumuşayana kadar kavurun.
    2. Doğranmış domatesleri ekleyip suyunu biraz çekene kadar pişirin.
    3. Yumurtaları bir kasede çırpıp tavaya ekleyin.
    4. Tuz ve karabiberi ekleyip yumurtalar çok kurumadan ocaktan alın.

### T3. Karnıyarık
*   **Açıklama:** Patlıcan ve kıymanın enfes uyumu, geleneksel bir ana yemek.
*   **Kategori:** Ana Yemek | **Süre:** 60 dk | **Porsiyon:** 4
*   **Malzemeler:**
    *   4 Adet Patlıcan (Orta boy)
    *   200g Dana Kıyma
    *   1 Adet Soğan
    *   2 Adet Diş Sarımsak
    *   2 Adet Yeşil Biber
    *   1 Yemek Kaşığı Domates Salçası
    *   1 Çay Kaşığı Tuz, Karabiber, Pul Biber
*   **Adımlar:**
    1. Patlıcanları alacalı soyup tuzlu suda bekletin, kurulayıp kızartın.
    2. İç harcı için soğan, kıyma, sarımsak ve biberleri soteleyin. Salçayı ve baharatları ekleyin.
    3. Patlıcanların ortasını yarıp kıymalı harcı doldurun.
    4. Üzerine birer dilim domates ve biber koyup az suyla fırında 20 dk pişirin.

---
*(Liste; Kısır, İzmir Köfte, Zeytinyağlı Fasulye, Yayla Çorbası, Carbonara vb. ile devam edecek)*
