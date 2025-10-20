import requests
from datetime import datetime

print(f"=== Testing After Path Fix - {datetime.now()} ===")

base_url = 'https://kul-setu-backend.onrender.com'

# Test health first
try:
    health = requests.get(f'{base_url}/health', timeout=10)
    print(f"Health check: {health.status_code}")
except Exception as e:
    print(f"Health check error: {e}")

# Test database initialization
try:
    print("\\nAttempting database initialization...")
    response = requests.post(f'{base_url}/init-db', timeout=120)
    
    print(f"Init DB Status: {response.status_code}")
    
    if response.status_code == 200:
        print(" Database initialization successful!")
        data = response.json()
        print(f"Response: {data}")
        
        # Test data availability
        members_response = requests.get(f'{base_url}/family-members', timeout=15)
        if members_response.status_code == 200:
            members_data = members_response.json()
            print(f" Successfully loaded {len(members_data)} family members!")
            
            # Test authentication
            test_login = {
                'email': 'person1.p0001@kulsetufamily.com', 
                'password': 'p0001123'
            }
            auth_response = requests.post(f'{base_url}/auth/login', json=test_login, timeout=10)
            print(f"Login test: {auth_response.status_code}")
            if auth_response.status_code == 200:
                print(" Authentication working!")
        
    else:
        print(f" Database initialization failed: {response.text[:200]}")
        
except Exception as e:
    print(f"Database initialization error: {e}")

print(f"\\nCompleted at {datetime.now()}")
