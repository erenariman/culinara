import urllib.request
import sys

def check_cors():
    url = "http://127.0.0.1:8000/api/v1/ingredients/"
    print(f"Testing Options {url}...")
    req = urllib.request.Request(url, method="OPTIONS")
    req.add_header("Origin", "http://localhost:3000")
    req.add_header("Access-Control-Request-Method", "GET")
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"Status: {response.getcode()}")
            headers = response.info()
            print("Headers:")
            print(headers)
            
            if "Access-Control-Allow-Origin" in headers:
                print("CORS OK: Access-Control-Allow-Origin present")
            else:
                print("CORS FAIL: Access-Control-Allow-Origin missing")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    check_cors()
