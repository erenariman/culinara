import sys
import asyncio
from src.presentation.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_startup():
    print("Verifying API Startup...")
    response = client.get("/health")
    if response.status_code == 200:
        print(f"✅ API Startup Successful. Health: {response.json()}")
    else:
        print(f"❌ API Startup Failed: {response.status_code} - {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_startup()
