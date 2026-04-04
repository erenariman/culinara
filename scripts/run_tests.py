"""
Kapsamlı API Test Scripti
Tüm major endpoint'leri test eder.
"""
import requests
import json
import sys

BASE = "http://localhost:8000"
API = f"{BASE}/api/v1"
PASS = "✅"
FAIL = "❌"
WARN = "⚠️"

results = []

def check(name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((status, name, detail))
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))
    return condition

def section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

# ─── 1. ROOT & DOCS ───────────────────────────────
section("1. Root & Documentation")
try:
    r = requests.get(f"{BASE}/", timeout=5)
    check("Root endpoint", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    check("Root endpoint", False, str(e))

try:
    r = requests.get(f"{BASE}/docs", timeout=5)
    check("Swagger UI (/docs)", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    check("Swagger UI (/docs)", False, str(e))

try:
    r = requests.get(f"{BASE}/openapi.json", timeout=5)
    check("OpenAPI schema", r.status_code == 200)
    if r.status_code == 200:
        schema = r.json()
        paths = list(schema.get("paths", {}).keys())
        check("OpenAPI has paths", len(paths) > 0, f"{len(paths)} paths found")
except Exception as e:
    check("OpenAPI schema", False, str(e))

# ─── 2. USER REGISTER & LOGIN ─────────────────────
section("2. User Registration & Login")

import time
test_email = f"testuser_{int(time.time())}@example.com"
test_username = f"testuser_{int(time.time())}"
test_password = "testpass123"
user_id = None

try:
    r = requests.post(f"{API}/users/register", json={
        "email": test_email,
        "username": test_username,
        "password": test_password
    }, timeout=10)
    ok = check("User registration", r.status_code == 201, f"Status: {r.status_code}")
    if ok:
        data = r.json().get("data", {})
        user_id = data.get("id")
        check("Registration returns user data", bool(user_id), f"user_id: {user_id}")
    else:
        print(f"    Detail: {r.text[:200]}")
except Exception as e:
    check("User registration", False, str(e))

try:
    r = requests.post(f"{API}/users/login", json={
        "email": test_email,
        "password": test_password
    }, timeout=10)
    ok = check("User login", r.status_code == 200, f"Status: {r.status_code}")
    if ok:
        login_data = r.json()
        token = login_data.get("access_token")
        check("Login returns token", bool(token), f"token: {token}")
    else:
        print(f"    Detail: {r.text[:200]}")
except Exception as e:
    check("User login", False, str(e))

# ─── 3. INGREDIENTS ───────────────────────────────
section("3. Ingredients")
ingredient_id = None

try:
    r = requests.get(f"{API}/ingredients/", timeout=10)
    ok = check("List ingredients", r.status_code == 200, f"Status: {r.status_code}")
    if ok:
        data = r.json()
        items = data.get("data", [])
        check("Ingredients response has data field", "data" in data, f"{len(items)} items")
except Exception as e:
    check("List ingredients", False, str(e))

try:
    ingredient_name = f"TestIngredient_{int(time.time())}"
    payload = {
        "name": ingredient_name,
        "calories_per_100g": 150,
        "protein_per_100g": 5.0,
        "carbs_per_100g": 25.0,
        "fat_per_100g": 3.0,
        "density_g_ml": 1.0,
        "avg_weight_per_piece_g": 100.0
    }
    r = requests.post(f"{API}/ingredients/", json=payload, timeout=10)
    ok = check("Create ingredient", r.status_code == 201, f"Status: {r.status_code}")
    if ok:
        ingredient_id = r.json().get("data", {}).get("id")
        check("Ingredient creation returns id", bool(ingredient_id))
    else:
        print(f"    Detail: {r.text[:300]}")
        ingredient_name = None
except Exception as e:
    check("Create ingredient", False, str(e))
    ingredient_name = None

if ingredient_id:
    try:
        r = requests.get(f"{API}/ingredients/{ingredient_id}", timeout=10)
        check("Get ingredient by ID", r.status_code == 200, f"Status: {r.status_code}")
    except Exception as e:
        check("Get ingredient by ID", False, str(e))

# ─── 4. RECIPES ───────────────────────────────────
section("4. Recipes")
recipe_id = None

try:
    r = requests.get(f"{API}/recipes/", timeout=10)
    ok = check("List recipes", r.status_code == 200, f"Status: {r.status_code}")
    if ok:
        data = r.json()
        items = data.get("data", [])
        check("Recipes response has data field", "data" in data, f"{len(items)} items")
except Exception as e:
    check("List recipes", False, str(e))

# Create recipe (requires valid user_id)
if user_id and ingredient_id and ingredient_name:
    try:
        recipe_payload = {
            "title": f"Test Recipe {int(time.time())}",
            "description": "A test recipe",
            "category": "Main Course",
            "diet_type": "Vegetarian",
            "difficulty": "Easy",
            "prep_time_minutes": 10,
            "cook_time_minutes": 20,
            "servings": 2,
            "items": [{"ingredient_name": ingredient_name, "amount": 100, "unit": "gram"}],
            "instructions": ["Step 1: Mix", "Step 2: Cook"]
        }
        headers = {"Authorization": f"Bearer dummy_token_{user_id}"}
        r = requests.post(f"{API}/recipes/", json=recipe_payload, headers=headers, timeout=10)
        ok = check("Create recipe", r.status_code == 201, f"Status: {r.status_code}")
        if ok:
            recipe_id = r.json().get("data", {}).get("id")
            check("Recipe creation returns id", bool(recipe_id))
        else:
            print(f"    Detail: {r.text[:300]}")
    except Exception as e:
        check("Create recipe", False, str(e))
else:
    print(f"  {WARN} Skipping recipe creation — no user_id or ingredient_id")


if recipe_id:
    try:
        r = requests.get(f"{API}/recipes/{recipe_id}", timeout=10)
        ok = check("Get recipe by ID", r.status_code == 200, f"Status: {r.status_code}")
        if ok:
            data = r.json().get("data", {})
            check("Recipe has macros", "total_calories" in data, f"calories: {data.get('total_calories')}")
            check("Recipe has category", "category" in data, f"category: {data.get('category')}")
            check("Recipe has author_name", "author_name" in data)
    except Exception as e:
        check("Get recipe by ID", False, str(e))

# ─── 5. SOCIAL ────────────────────────────────────
section("5. Social (Reviews & Likes)")

if recipe_id and user_id:
    headers = {"Authorization": f"Bearer dummy_token_{user_id}"}
    try:
        r = requests.post(f"{API}/social/recipes/{recipe_id}/reviews", json={
            "rating": 5,
            "text": "Excellent test recipe!"
        }, headers=headers, timeout=10)
        ok = check("Add review", r.status_code == 201, f"Status: {r.status_code}")
        if not ok:
            print(f"    Detail: {r.text[:300]}")
    except Exception as e:
        check("Add review", False, str(e))

    try:
        r = requests.post(f"{API}/social/recipes/{recipe_id}/like", headers=headers, timeout=10)
        ok = check("Like recipe", r.status_code in (200, 201), f"Status: {r.status_code}")
        if not ok:
            print(f"    Detail: {r.text[:300]}")
    except Exception as e:
        check("Like recipe", False, str(e))

    try:
        r = requests.get(f"{API}/recipes/{recipe_id}", timeout=10)
        if r.status_code == 200:
            data = r.json().get("data", {})
            check("Rating aggregation after review", data.get("average_rating") == 5.0, f"avg_rating: {data.get('average_rating')}")
            check("Review count updated", data.get("review_count", 0) >= 1, f"count: {data.get('review_count')}")
    except Exception as e:
        check("Rating aggregation", False, str(e))
else:
    print(f"  {WARN} Skipping social tests — no recipe_id or user_id")

# ─── 6. USERS LIST ────────────────────────────────
section("6. Users List")
try:
    r = requests.get(f"{API}/users/", timeout=10)
    check("List users", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    check("List users", False, str(e))

# ─── CLEANUP ──────────────────────────────────────
section("Cleanup")
if recipe_id and user_id:
    try:
        headers = {"Authorization": f"Bearer dummy_token_{user_id}"}
        r = requests.delete(f"{API}/recipes/{recipe_id}", headers=headers, timeout=10)
        check("Cleanup: delete test recipe", r.status_code in (200, 204), f"Status: {r.status_code}")
    except Exception as e:
        check("Cleanup: delete test recipe", False, str(e))

# ─── SUMMARY ──────────────────────────────────────
section("TEST SUMMARY")
passed = sum(1 for s, _, _ in results if s == PASS)
failed = sum(1 for s, _, _ in results if s == FAIL)
total = len(results)
print(f"\n  Total: {total} | {PASS} Passed: {passed} | {FAIL} Failed: {failed}")

if failed > 0:
    print(f"\n  Failed tests:")
    for status, name, detail in results:
        if status == FAIL:
            print(f"    - {name}: {detail}")

print()
sys.exit(0 if failed == 0 else 1)
