import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def verify_expansion():
    print("--- Verifying Recipe Metadata, Macros & Social Expansion ---")

    # 1. Login to get token (using seeded user)
    print("\n[1] Logging in as 'eren'...")
    login_resp = requests.post(f"{BASE_URL}/users/login", json={"email": "eren@example.com", "password": "password123"})
    if login_resp.status_code != 200:
        print(f"❌ Login failed: {login_resp.text}")
        return
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user id
    me_resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
    author_id = me_resp.json()["data"]["id"]
    author_name = me_resp.json()["data"]["username"]
    print(f"   Logged in successfully. User ID: {author_id}")

    # 2. Ensure test ingredient exists
    print("\n[2] Checking Test Ingredient (UnitTester)...")
    ing_name = "ExpTester"
    existing_ing = requests.get(f"{BASE_URL}/ingredients/?search={ing_name}", headers=headers).json()["data"]
    if not any(i['name'] == ing_name for i in existing_ing):
        ing_payload = {
            "name": ing_name,
            "calories_per_100g": 200, # 1g = 2kcal
            "protein_per_100g": 10.0, # 1g = 0.1g protein
            "carbs_per_100g": 20.0,   # 1g = 0.2g carbs
            "fat_per_100g": 5.0,      # 1g = 0.05g fat
            "density_g_ml": 1.0,
            "avg_weight_per_piece_g": 100.0
        }
        res = requests.post(f"{BASE_URL}/ingredients/", json=ing_payload, headers=headers)
        if res.status_code != 201:
             print(f"❌ Ing creation failed: {res.text}")
             return
    print("   Ingredient ready.")

    # 3. Create Recipe with ALL new metadata fields
    print("\n[3] Creating Recipe with Metadata & Macros...")
    recipe_payload = {
        "title": "Expansion Test Recipe",
        "description": "Testing the new UI fields.",
        "category": "Main Course",
        "diet_type": "Vegetarian",
        "difficulty": "Medium",
        "prep_time_minutes": 15,
        "cook_time_minutes": 45,
        "servings": 4,
        "items": [{"ingredient_name": ing_name, "amount": 200, "unit": "gram"}], # 200g
        "instructions": ["Step 1", "Step 2"]
    }
    
    r_resp = requests.post(f"{BASE_URL}/recipes/", json=recipe_payload, headers=headers)
    if r_resp.status_code != 201:
        print(f"❌ Recipe creation failed: {r_resp.text}")
        return
        
    recipe_data = r_resp.json()["data"]
    recipe_id = recipe_data["id"]
    print(f"   Recipe created! ID: {recipe_id}")
    
    # 4. Verify Macros (200g of ExpTester)
    # Expected: Cal = 400, Pro = 20, Carb = 40, Fat = 10
    print("\n[4] Verifying Macronutrients...")
    passed = True
    if recipe_data["total_calories"] != 400.0: passed = False; print(f"   [X] Calories expected 400, got {recipe_data['total_calories']}")
    if recipe_data["total_protein"] != 20.0: passed = False; print(f"   [X] Protein expected 20, got {recipe_data['total_protein']}")
    if recipe_data["total_carbs"] != 40.0: passed = False; print(f"   [X] Carbs expected 40, got {recipe_data['total_carbs']}")
    if recipe_data["total_fat"] != 10.0: passed = False; print(f"   [X] Fat expected 10, got {recipe_data['total_fat']}")
    
    if passed:
        print("   [OK] Macronutrients calculated & saved correctly!")

    # 5. Add a Review (for Social Aggregation Test)
    print("\n[5] Adding a Review...")
    rev_payload = {"rating": 4, "text": "Good test recipe!"}
    res = requests.post(f"{BASE_URL}/social/recipes/{recipe_id}/reviews", json=rev_payload, headers=headers)
    if res.status_code != 201: print(f"   [X] Review add failed: {res.text}")
    print("   Review added. Rating = 4")

    # 6. Fetch Recipe and Verify Meta + Social
    print("\n[6] Fetching Recipe to verify Aggregation (JOINs)...")
    get_resp = requests.get(f"{BASE_URL}/recipes/{recipe_id}")
    fetched = get_resp.json()["data"]
    
    v_passed = True
    if fetched["category"] != "Main Course": v_passed = False; print(f"   [X] Category mismatch: expected 'Main Course', got '{fetched['category']}'")
    if fetched["author_name"] != author_name: v_passed = False; print(f"   [X] Author Name expected '{author_name}', got {fetched['author_name']}")
    if fetched["average_rating"] != 4.0: v_passed = False; print(f"   [X] Rating expected 4.0, got {fetched['average_rating']}")
    if fetched["review_count"] != 1: v_passed = False; print(f"   [X] Review Count expected 1, got {fetched['review_count']}")

    if v_passed:
        print("   [OK] SQL Joins (Author, Rating, Reviews) working perfectly!")

    # Cleanup
    print("\n[7] Cleaning up...")
    requests.delete(f"{BASE_URL}/recipes/{recipe_id}", headers=headers)
    print("   Done.")

if __name__ == "__main__":
    verify_expansion()
