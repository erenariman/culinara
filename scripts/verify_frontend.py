import urllib.request
import sys

def check_frontend():
    print("Testing http://localhost:3000/...")
    try:
        with urllib.request.urlopen("http://localhost:3000/", timeout=10) as response:
            status = response.getcode()
            print(f"Status: {status}")
            data = response.read(100) # Read first 100 bytes
            print(f"Data: {data}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    check_frontend()
