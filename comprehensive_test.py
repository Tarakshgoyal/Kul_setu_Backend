import requests
import time

print("=== Comprehensive Backend Test ===")

# Test basic connectivity
try:
    health = requests.get('https://kul-setu-backend.onrender.com/health')
    print(f"Health Check: {health.status_code} - {health.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# Test family members endpoint
try:
    members = requests.get('https://kul-setu-backend.onrender.com/family-members')
    print(f"Family Members: {members.status_code}")
    if members.status_code == 200:
        data = members.json()
        print(f"Found {len(data)} family members")
    else:
        print(f"Error: {members.text[:100]}")
except Exception as e:
    print(f"Family members failed: {e}")

# Test init-db with shorter timeout
try:
    print("Trying database initialization...")
    init_db = requests.post('https://kul-setu-backend.onrender.com/init-db', timeout=45)
    print(f"Init DB: {init_db.status_code}")
    if init_db.status_code == 200:
        print(f"Success: {init_db.json()}")
    else:
        print(f"Failed: {init_db.text[:200]}")
except requests.exceptions.Timeout:
    print("Database initialization timed out (might still be working)")
except Exception as e:
    print(f"Init DB failed: {e}")
