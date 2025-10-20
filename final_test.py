import requests

print("=== Final Deployment Check ===")
base_url = 'https://kul-setu-backend.onrender.com'

# Test all endpoints systematically
endpoints_to_test = [
    ('GET', '/health', None),
    ('GET', '/family-members', None),
    ('POST', '/init-db', {}),
    ('POST', '/search', {'query': 'test', 'limit': 1}),
    ('POST', '/auth/login', {'email': 'test@test.com', 'password': 'test'}),
]

for method, endpoint, data in endpoints_to_test:
    try:
        if method == 'GET':
            response = requests.get(f'{base_url}{endpoint}', timeout=30)
        else:
            response = requests.post(f'{base_url}{endpoint}', json=data, timeout=30)
        
        print(f"{method} {endpoint}: {response.status_code}")
        
        # Special handling for successful responses
        if response.status_code == 200 and endpoint == '/init-db':
            print("   Database initialization successful!")
            result = response.json()
            print(f"  Message: {result.get('message', 'No message')}")
        elif response.status_code == 200 and endpoint == '/family-members':
            result = response.json()
            print(f"  Found {len(result)} family members")
        elif response.status_code not in [200, 400, 401, 404, 405]:
            print(f"  Error: {response.text[:100]}")
            
    except Exception as e:
        print(f"{method} {endpoint}: Exception - {e}")

print("\\nDeployment check completed.")
