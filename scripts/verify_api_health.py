import urllib.request
import json
import sys

def check_health():
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=5) as response:
            status = response.getcode()
            data = response.read()
            print(f"Status Code: {status}")
            print(f"Response: {data.decode('utf-8')}")
            if status == 200:
                sys.exit(0)
            else:
                sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_health()
