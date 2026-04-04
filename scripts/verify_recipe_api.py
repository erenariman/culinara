import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1/recipes"

def print_result(name, response, expected_status=200):
    if response.status_code == expected_status:
        print(f"✅ {name}: Success ({response.status_code})")
        return True
    else:
        print(f"❌ {name}: Failed ({response.status_code})")
        print(f"   Response: {response.text}")
        return False

def verify_recipe_api():
    print("--- Verifying Recipe API ---")

    # 1. List Recipes
    resp = requests.get(f"{BASE_URL}/")
    print_result("List Recipes", resp)

    # 1.5 Create Ingredient (Dependency)
    ingredient_payload = {
        "name": "Tomato",
        "calories_per_100g": 18,
        "protein_per_100g": 0.9,
        "fat_per_100g": 0.2,
        "carbs_per_100g": 3.9,
        "density_g_ml": 1.0,
        "avg_weight_per_piece_g": 100.0
    }
    # Check if exists first
    # Check if exists first - iterating to find exact match
    ingredients_data = requests.get(f"http://localhost:8000/api/v1/ingredients/?search=Tomato").json()["data"]
    # We need to make sure "Tomato" exists exactly, search might return "Tomato Soup" etc.
    tomato_exists = any(i['name'] == "Tomato" for i in ingredients_data)
    
    if not tomato_exists:
        print("   Creating dependency ingredient 'Tomato'...")
        resp = requests.post("http://localhost:8000/api/v1/ingredients/", json=ingredient_payload)
        if resp.status_code != 201:
             print(f"   Failed to create ingredient: {resp.text}")

    # 2. Create Recipe (String Instructions)
    payload_str = {
        "title": "Test Recipe String Instructions",
        "description": "Created with string instructions",
        "instructions": ["Step 1", "Step 2"],
        "items": [
            {"ingredient_name": "Tomato", "amount": 1, "unit": "piece"}
        ]
    }
    resp = requests.post(f"{BASE_URL}/", json=payload_str)
    if not print_result("Create Recipe (String Instructions)", resp, 201):
        return
    recipe_id_str = resp.json()["data"]["id"]

    # 3. Create Recipe (Object Instructions - The Fix)
    payload_obj = {
        "title": "Test Recipe Object Instructions",
        "description": "Created with object instructions",
        "instructions": [
            {"step_number": 1, "text": "Mix ingredients"},
            {"step_number": 2, "text": "Cook for 20 mins"}
        ],
        "items": [
            {"ingredient_name": "Tomato", "amount": 2, "unit": "piece"}
        ]
    }
    resp = requests.post(f"{BASE_URL}/", json=payload_obj)
    if not print_result("Create Recipe (Object Instructions)", resp, 201):
        return
    recipe_id_obj = resp.json()["data"]["id"]

    # 4. Get Recipe
    resp = requests.get(f"{BASE_URL}/{recipe_id_obj}")
    print_result(f"Get Recipe {recipe_id_obj}", resp)
    data = resp.json()["data"]
    # Verify instructions structure in response
    print(f"   Instructions check: {data['instructions']}")

    # 5. Update Recipe
    update_payload = {
        "title": "Updated Title",
        "instructions": [
            {"step_number": 1, "text": "New Step 1"},
            {"step_number": 2, "text": "New Step 2"}
        ]
    }
    resp = requests.patch(f"{BASE_URL}/{recipe_id_obj}", json=update_payload)
    print_result("Update Recipe", resp)

    # 6. Delete Recipes
    resp = requests.delete(f"{BASE_URL}/{recipe_id_str}")
    print_result(f"Delete Recipe {recipe_id_str}", resp)
    
    resp = requests.delete(f"{BASE_URL}/{recipe_id_obj}")
    print_result(f"Delete Recipe {recipe_id_obj}", resp)

if __name__ == "__main__":
    verify_recipe_api()
