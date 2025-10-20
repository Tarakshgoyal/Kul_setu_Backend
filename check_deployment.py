import requests

print("=== Checking Deployment Progress ===")

# Check if new endpoints are available
new_endpoints = ['/family-members', '/auth/login', '/auth/signup', '/init-db']
base_url = 'https://kul-setu-backend.onrender.com'

for endpoint in new_endpoints:
    try:
        response = requests.get(f'{base_url}{endpoint}', timeout=5)
        print(f"{endpoint}: {response.status_code} (Available)")
    except:
        try:
            response = requests.post(f'{base_url}{endpoint}', json={}, timeout=5)
            print(f"{endpoint}: {response.status_code} (Available)")
        except Exception as e:
            print(f"{endpoint}: Not available yet")
