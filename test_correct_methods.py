import requests

print("=== Testing Endpoints with Correct Methods ===")

base_url = 'https://kul-setu-backend.onrender.com'

# Test family-members (should be GET)
try:
    response = requests.get(f'{base_url}/family-members', timeout=10)
    print(f"GET /family-members: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} family members")
    else:
        print(f"Response: {response.text[:100]}")
except Exception as e:
    print(f"GET /family-members: Error - {e}")

# Test init-db (should be POST)  
try:
    print("\\nTrying database initialization...")
    response = requests.post(f'{base_url}/init-db', timeout=60)
    print(f"POST /init-db: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data}")
    else:
        print(f"Error: {response.text[:200]}")
except Exception as e:
    print(f"POST /init-db: Error - {e}")
