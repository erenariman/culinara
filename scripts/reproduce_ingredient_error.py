import urllib.request
import json
import ssl

def check_ingredients():
    url = "http://127.0.0.1:8000/api/v1/ingredients/"
    print(f"GET {url}...")
    try:
        # Create context to ignore SSL if needed (though using http here)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ctx) as response:
            status = response.getcode()
            print(f"Status: {status}")
            data = response.read().decode('utf-8')
            
            if status == 200:
                json_data = json.loads(data)
                print("Success. First 2 items:")
                print(json.dumps(json_data[:2], indent=2))
            else:
                print("Error Response:")
                print(data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Failed: {e.code}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    check_ingredients()
