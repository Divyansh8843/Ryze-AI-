import requests
import time
import sys

def check_health(url):
    print(f"Checking health of {url}...")
    try:
        response = requests.get(f"{url}/")
        if response.status_code == 200:
            print("✅ Root Health Check Passed:", response.json())
            return True
        else:
            print(f"❌ Root Health Check Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return False

def check_generate(url):
    print(f"\nChecking Generation Endpoint {url}/generate...")
    try:
        payload = {"prompt": "Create a blue dashboard for Ryze AI"}
        start = time.time()
        response = requests.post(f"{url}/generate", json=payload, timeout=10)
        end = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generation Successful in {round((end-start)*1000)}ms")
            print("Intent:", data.get('meta', {}).get('intent'))
            print("Review Plan:", data.get('plan')[:50] + "...")
            return True
        else:
            print(f"❌ Generation Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5001"
        
    print(f"--- Ryze AI Service Sanity Check for {base_url} ---\n")
    
    health = check_health(base_url)
    gen = check_generate(base_url)
    
    if health and gen:
        print("\n🎉 Service is FULLY FUNCTIONAL!")
        sys.exit(0)
    else:
        print("\n⚠️ Service has issues.")
        sys.exit(1)
