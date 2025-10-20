import requests

print("=== Testing Available Endpoints ===")

# Test available endpoints
endpoints = [
    ('GET', '/health'),
    ('GET', '/'),
    ('POST', '/search'),
    ('GET', '/members'),
    ('POST', '/register'),
    ('POST', '/auth/login'),
    ('POST', '/auth/signup')
]

base_url = 'https://kul-setu-backend.onrender.com'

for method, endpoint in endpoints:
    try:
        if method == 'GET':
            response = requests.get(f'{base_url}{endpoint}', timeout=10)
        else:
            response = requests.post(f'{base_url}{endpoint}', json={}, timeout=10)
        print(f"{method} {endpoint}: {response.status_code}")
    except Exception as e:
        print(f"{method} {endpoint}: Error - {e}")
