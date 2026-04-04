import urllib.request
import ssl

def check_docs():
    url = "http://127.0.0.1:8000/docs"
    print(f"Checking {url}...")
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            print(f"Status: {response.getcode()}")
            print("Server is UP and responding directly.")
            
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    check_docs()
