import requests

print("=== Testing Sync Users Endpoint ===")

try:
    response = requests.post('https://kul-setu-backend.onrender.com/sync-users', timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
