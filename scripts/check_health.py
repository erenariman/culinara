import requests
import sys

try:
    print("Checking server health...")
    resp = requests.get("http://localhost:8000/api/v1/recipes/", timeout=5)
    print(f"Server responded with: {resp.status_code}")
except Exception as e:
    print(f"Server check failed: {e}")
