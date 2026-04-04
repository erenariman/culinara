import asyncio
import httpx
import uuid

BASE_URL = "http://127.0.0.1:8000/api/v1"

def get_data(resp):
    try:
        data = resp.json()
    except:
        return None
    if isinstance(data, dict) and "data" in data and "success" in data:
        return data["data"]
    return data

async def verify_ingredients(client):
    print("\n--- Verifying Ingredients ---")
    # 1. Create
    ing_name = f"TestIngredient_{uuid.uuid4().hex[:8]}"
    resp = await client.post(f"{BASE_URL}/ingredients/", json={
        "name": ing_name,
        "calories_per_100g": 100,
        "protein_per_100g": 10,
        "fat_per_100g": 10,
        "carbs_per_100g": 10,
        "density_g_ml": 1.0
    })
    if resp.status_code != 201:
        print(f"❌ Create failed: {resp.text}")
        return
    ing_id = get_data(resp)["id"]
    print(f"✅ Created Ingredient: {ing_id}")

    # 2. Update (Patch)
    resp = await client.patch(f"{BASE_URL}/ingredients/{ing_id}", json={
        "calories_per_100g": 200
    })
    if resp.status_code != 200 or get_data(resp)["calories_per_100g"] != 200:
        print(f"❌ Update failed: {resp.text}")
        return
    print(f"✅ Updated Ingredient")

    # 3. Delete
    resp = await client.delete(f"{BASE_URL}/ingredients/{ing_id}")
    if resp.status_code != 200 or not resp.json().get("success"):
        print(f"❌ Delete failed: {resp.text}")
        return
    print(f"✅ Deleted Ingredient")
    
    # Verify Gone
    resp = await client.get(f"{BASE_URL}/ingredients/{ing_id}")
    if resp.status_code != 404:
        print(f"❌ Ingredient still exists after delete! {resp.status_code}")
        return
    print(f"✅ Ingredient confirmed gone")

async def verify_recipes(client):
    print("\n--- Verifying Recipes ---")
    # 1. Create
    resp = await client.post(f"{BASE_URL}/recipes/", json={
        "title": "Test Recipe",
        "description": "Test Desc",
        "instructions": ["Step 1"],
        "items": []
    })
    if resp.status_code != 201:
        print(f"❌ Create failed: {resp.text}")
        return
    rec_id = get_data(resp)["id"]
    print(f"✅ Created Recipe: {rec_id}")

    # 2. Update (Patch)
    resp = await client.patch(f"{BASE_URL}/recipes/{rec_id}", json={
        "description": "Updated Desc"
    })
    if resp.status_code != 200 or get_data(resp)["description"] != "Updated Desc":
        # Note: Depending on implementation, PUT/PATCH might return modified object.
        # My implementation returns RecipeResponse.
        print(f"❌ Update failed: {resp.text}")
        return
    print(f"✅ Updated Recipe")

    # 3. Delete
    resp = await client.delete(f"{BASE_URL}/recipes/{rec_id}")
    if resp.status_code != 200 or not resp.json().get("success"):
        print(f"❌ Delete failed: {resp.text}")
        return
    print(f"✅ Deleted Recipe")
    
    # Verify Gone
    resp = await client.get(f"{BASE_URL}/recipes/{rec_id}")
    if resp.status_code != 404:
        print(f"❌ Recipe still exists after delete! {resp.status_code}")
        return
    print(f"✅ Recipe confirmed gone")
    return rec_id

async def verify_shopping(client, user_id):
    print("\n--- Verifying Shopping ---")
    # 1. Create List
    # user_id passed in
    resp = await client.post(f"{BASE_URL}/shopping/?user_id={user_id}", json={
        "name": "Test List"
    })
    if resp.status_code != 200:
         print(f"❌ Create List failed: {resp.text}")
         return
    list_id = get_data(resp)["id"]
    print(f"✅ Created List: {list_id}")

    # 2. Add Item
    resp = await client.post(f"{BASE_URL}/shopping/{list_id}/items", json={
        "text": "Milk", 
        "amount": 1, 
        "unit": "liter"
    })
    if resp.status_code != 200:
         print(f"❌ Add Item failed: {resp.text}")
         return
    item_id = get_data(resp)["items"][0]["id"]
    print(f"✅ Added Item: {item_id}")

    # 3. Update Item
    resp = await client.patch(f"{BASE_URL}/shopping/{list_id}/items/{item_id}", json={
        "amount": 2
    })
    if resp.status_code != 200: # My implementation returns 200 with list
         print(f"❌ Update Item failed: {resp.text}")
         return
    # Check if updated in response
    items = get_data(resp)["items"]
    updated_item = next(i for i in items if i["id"] == item_id)
    if updated_item["amount"] != 2:
        print(f"❌ Update Item content mismatch: {updated_item}")
        return
    print(f"✅ Updated Item")

    # 4. Remove Item
    resp = await client.delete(f"{BASE_URL}/shopping/{list_id}/items/{item_id}")
    if resp.status_code != 200: # Returns list
         print(f"❌ Remove Item failed: {resp.text}")
         return
    if len(get_data(resp)["items"]) != 0:
        print(f"❌ Item not removed")
        return
    print(f"✅ Removed Item")

    # 5. Delete List
    resp = await client.delete(f"{BASE_URL}/shopping/{list_id}")
    if resp.status_code != 200 or not resp.json().get("success"):
         print(f"❌ Delete List failed: {resp.text}")
         return
    print(f"✅ Deleted List")

    # Verify logic: List should be gone
    resp = await client.get(f"{BASE_URL}/shopping/?user_id={user_id}")
    lists = get_data(resp)
    if len(lists) > 0:
        print(f"❌ List still exists after delete! {lists}")
    else:
        print(f"✅ List confirmed gone")

async def verify_social(client, user_id, recipe_id):
    print("\n--- Verifying Social ---")
    # user_id passsed in
    # 1. Post Comment
    resp = await client.post(f"{BASE_URL}/social/comments?user_id={user_id}", json={
        "recipe_id": recipe_id,
        "text": "Nice!"
    })
    if resp.status_code != 200:
         print(f"❌ Post Comment failed: {resp.text}")
         return
    comment_id = get_data(resp)["id"]
    print(f"✅ Posted Comment: {comment_id}")

    # 2. Update Comment
    resp = await client.patch(f"{BASE_URL}/social/comments/{comment_id}?user_id={user_id}", json={
        "text": "Super!"
    })
    if resp.status_code != 200 or get_data(resp)["text"] != "Super!":
         print(f"❌ Update Comment failed: {resp.text}")
         return
    print(f"✅ Updated Comment")

    # 3. Delete Comment
    resp = await client.delete(f"{BASE_URL}/social/comments/{comment_id}?user_id={user_id}")
    if resp.status_code != 200 or not resp.json().get("success"):
         print(f"❌ Delete Comment failed: {resp.text}")
         return
    print(f"✅ Deleted Comment")

    # Verify Gone
    resp = await client.get(f"{BASE_URL}/social/comments/{comment_id}?user_id={user_id}")
    if resp.status_code != 404:
        print(f"❌ Comment still exists after delete! {resp.status_code}")
        return
    print(f"✅ Comment confirmed gone")

async def verify_organization(client, user_id, recipe_id):
    print("\n--- Verifying Organization ---")
    # user_id passed in
    # 1. Create Collection
    resp = await client.post(f"{BASE_URL}/collections/?user_id={user_id}", json={
        "name": "My Favorites"
    })
    if resp.status_code != 200:
         print(f"❌ Create Collection failed: {resp.text}")
         return
    coll_id = get_data(resp)["id"]
    print(f"✅ Created Collection: {coll_id}")

    # 2. Update Collection
    resp = await client.patch(f"{BASE_URL}/collections/{coll_id}?user_id={user_id}", json={
        "name": "Updated Name"
    })
    if resp.status_code != 200 or get_data(resp)["title"] != "Updated Name":
         print(f"❌ Update Collection failed: {resp.text}")
         return
    print(f"✅ Updated Collection")

    print(f"✅ Updated Collection")

    # 3. Add Recipe
    resp = await client.post(f"{BASE_URL}/collections/{coll_id}/recipes/{recipe_id}?user_id={user_id}")
    if resp.status_code != 200:
         print(f"❌ Add Recipe failed: {resp.text}")
         return
    print(f"✅ Added Recipe")
    
    # 4. Remove Recipe
    resp = await client.delete(f"{BASE_URL}/collections/{coll_id}/recipes/{recipe_id}?user_id={user_id}")
    if resp.status_code != 200 or not resp.json().get("success"):
         print(f"❌ Remove Recipe failed: {resp.text}")
         return
    print(f"✅ Removed Recipe")

    # 5. Delete Collection
    resp = await client.delete(f"{BASE_URL}/collections/{coll_id}?user_id={user_id}")
    if resp.status_code != 200 or not resp.json().get("success"):
         print(f"❌ Delete Collection failed: {resp.text}")
         return
    print(f"✅ Deleted Collection")

    # Verify Gone
    resp = await client.get(f"{BASE_URL}/collections/{coll_id}?user_id={user_id}")
    if resp.status_code != 404:
        print(f"❌ Collection still exists after delete! {resp.status_code}")
        return
    print(f"✅ Collection confirmed gone")

async def verify_users(client, user_id):
    print("\n--- Verifying Users ---")
    # user_id passed in
    # 1. Update Profile (PATCH /me)
    resp = await client.patch(f"{BASE_URL}/users/me?user_id={user_id}", json={
        "bio": "New Bio"
    })
    if resp.status_code != 200:
         print(f"❌ Update Profile failed: {resp.text}")
         return
    print(f"✅ Updated Profile")

    # 2. Delete Account (DELETE /me)
    # Be careful not to delete real data if possible, but here we use mock
    resp = await client.delete(f"{BASE_URL}/users/me?user_id={user_id}")
    if resp.status_code != 200 or not resp.json().get("success"):
         print(f"❌ Delete Account failed: {resp.text}")
         return
    print(f"✅ Deleted Account")

    # Verify Gone
    resp = await client.get(f"{BASE_URL}/users/me?user_id={user_id}")
    if resp.status_code != 404:
        print(f"❌ User still exists after delete! {resp.status_code}")
        return
    print(f"✅ User confirmed gone")

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Register a user first
        print("\n--- Registering User ---")
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        email = f"{username}@example.com"
        resp = await client.post(f"{BASE_URL}/users/register", json={
            "username": username,
            "email": email,
            "password": "password123"
        })
        if resp.status_code != 200:
             print(f"❌ Register failed: {resp.text}")
             return
        user_id = get_data(resp)["id"]
        print(f"✅ Registered User: {user_id}")

        await verify_ingredients(client)
        rec_id = await verify_recipes(client)
        # Note: verify_recipes deletes the recipe at the end! 
        # So providing rec_id to others will fail FK if they check existence.
        # I should modify verify_recipes NOT to delete it, or Create another one.
        # Let's create a persistent one for testing.
        
        print("\n--- Creating Shared Recipe ---")
        resp = await client.post(f"{BASE_URL}/recipes/", json={
             "title": "Shared Recipe", "description": "For testing", "instructions": [], "items": []
        })
        shared_rec_id = get_data(resp)["id"]

        await verify_shopping(client, user_id)
        await verify_social(client, user_id, shared_rec_id)
        await verify_organization(client, user_id, shared_rec_id)
        await verify_users(client, user_id)
        
        # Cleanup shared recipe
        await client.delete(f"{BASE_URL}/recipes/{shared_rec_id}")

if __name__ == "__main__":
    asyncio.run(main())
