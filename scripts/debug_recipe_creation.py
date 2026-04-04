import asyncio
import sys
import os
import requests

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000/api/v1/recipes/"

def test_recipe_creation():
    print("--- Debugging Recipe Creation ---")

    # 1. Test with Instructions as Strings (Expected)
    payload_valid = {
        "title": "Debug Recipe Valid",
        "description": "Testing valid payload",
        "instructions": ["Step 1", "Step 2"],
        "items": [
            {"ingredient_name": "Tomato", "amount": 1, "unit": "piece"}
        ]
    }
    
    print("\n[1] Testing Valid Payload (instructions=['Step 1'])...")
    try:
        resp = requests.post(BASE_URL, json=payload_valid)
        print(f"Status: {resp.status_code}")
        if resp.status_code != 201:
            print(f"Response: {resp.text}")
        else:
            print("✅ Success")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test with Instructions as Objects (Suspected Frontend Payload)
    payload_invalid = {
        "title": "Debug Recipe Invalid",
        "description": "Testing invalid payload",
        "instructions": [{"step_number": 1, "text": "Step 1"}, {"step_number": 2, "text": "Step 2"}],
        "items": [
            {"ingredient_name": "Tomato", "amount": 1, "unit": "piece"}
        ]
    }

    print("\n[2] Testing Invalid Payload (instructions=[{text: 'Step 1'}])...")
    try:
        resp = requests.post(BASE_URL, json=payload_invalid)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_recipe_creation()
