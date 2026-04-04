import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_endpoint(endpoint):
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing {url}...")
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            status = response.getcode()
            print(f"[{endpoint}] Status: {status}")
            data = response.read()
            print(f"[{endpoint}] Data length: {len(data)}")
    except Exception as e:
        print(f"[{endpoint}] Failed: {e}")

if __name__ == "__main__":
    test_endpoint("/recipes/")
    test_endpoint("/ingredients/")
