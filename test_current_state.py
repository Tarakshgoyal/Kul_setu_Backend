import requests
import json

print("=== Testing Current Backend State ===")

base_url = 'https://kul-setu-backend.onrender.com'

# Test search to see what data is available
try:
    search_data = {
        'query': 'person',
        'limit': 5
    }
    response = requests.post(f'{base_url}/search', 
                           json=search_data, 
                           headers={'Content-Type': 'application/json'},
                           timeout=15)
    print(f"Search status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Search results: {data}")
        print(f"Found {len(data.get('results', []))} results")
    else:
        print(f"Search failed: {response.text}")
except Exception as e:
    print(f"Search error: {e}")

# Test the root endpoint
try:
    response = requests.get(f'{base_url}/', timeout=10)
    print(f"\\nRoot endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Root error: {e}")
