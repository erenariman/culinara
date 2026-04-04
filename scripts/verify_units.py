import requests
import sys

BASE_URL = "http://localhost:8000/api/v1/recipes"
ING_URL = "http://localhost:8000/api/v1/ingredients"

def verify_units():
    print("--- Verifying Unit Conversions ---")

    # 1. Create/Get Ingredient (Olive Oil: ~884 kcal/100g, Density ~0.92 g/ml)
    # Let's use water/test-liquid for simplicity: 100 kcal/100g, density 1.0
    ing_name = "UnitTester"
    payload = {
        "name": ing_name,
        "calories_per_100g": 100, # 1g = 1kcal
        "density_g_ml": 1.0,
        "avg_weight_per_piece_g": 1.0,
        "protein_per_100g": 0.0,
        "fat_per_100g": 0.0,
        "carbs_per_100g": 0.0,
    }
    
    
    # Check if exists first
    existing = requests.get(f"{ING_URL}/?search={ing_name}").json()["data"]
    if not any(i['name'] == ing_name for i in existing):
        print(f"   Creating {ing_name}...")
        resp = requests.post(f"{ING_URL}/", json=payload)
        if resp.status_code != 201:
            print(f"❌ Failed to create ingredient: {resp.text}")
            return
    else:
        print(f"   {ing_name} already exists.")

    # 2. Test Cases
    cases = [
        {"unit": "tablespoon", "amount": 1, "expected_g": 15, "expected_cal": 15.0},
        {"unit": "teaspoon", "amount": 1, "expected_g": 5, "expected_cal": 5.0},
        {"unit": "cup", "amount": 1, "expected_g": 240, "expected_cal": 240.0},
    ]

    for case in cases:
        print(f"\nTesting {case['amount']} {case['unit']}...")
        r_payload = {
            "title": f"Test {case['unit']}",
            "description": "desc",
            "instructions": ["step 1"],
            "items": [{"ingredient_name": ing_name, "amount": case['amount'], "unit": case['unit']}]
        }
        
        resp = requests.post(f"{BASE_URL}/", json=r_payload)
        if resp.status_code != 201:
            print(f"❌ Creation failed: {resp.text}")
            continue

        data = resp.json()["data"]
        cal = data["total_calories"]
        
        print(f"   Calculated: {cal}, Expected: {case['expected_cal']}")
        if abs(cal - case['expected_cal']) < 0.1:
            print("✅ OK")
        else:
            print("❌ FAIL")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/{data['id']}")

if __name__ == "__main__":
    verify_units()
