import requests
from datetime import datetime

print(f"=== Database Initialization - {datetime.now()} ===")
print("Attempting database initialization with extended timeout...")
print("This may take several minutes for 1000+ records...")

base_url = 'https://kul-setu-backend.onrender.com'

try:
    # Very long timeout for processing 1000+ records
    response = requests.post(f'{base_url}/init-db', timeout=300)  # 5 minutes
    
    print(f"\\nResponse received at {datetime.now()}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(" Database initialization successful!")
        data = response.json()
        print(f"Response: {data}")
        
        # Test if data is now available
        print("\\nTesting data availability...")
        members_response = requests.get(f'{base_url}/family-members', timeout=30)
        print(f"Family members endpoint: {members_response.status_code}")
        
        if members_response.status_code == 200:
            members_data = members_response.json()
            print(f" Successfully loaded {len(members_data)} family members!")
        
    else:
        print(f" Database initialization failed: {response.status_code}")
        print(f"Response: {response.text[:300]}")
        
except requests.exceptions.Timeout:
    print(" Request timed out after 5 minutes")
    print("The server might still be processing. Let's check if data was loaded...")
    
    # Check if data was loaded despite timeout
    try:
        members_response = requests.get(f'{base_url}/family-members', timeout=15)
        if members_response.status_code == 200:
            members_data = members_response.json()
            print(f" Data was loaded! Found {len(members_data)} family members")
        else:
            print("Data was not loaded yet.")
    except:
        print("Could not check data status.")
        
except Exception as e:
    print(f" Error: {e}")

print(f"\\nCompleted at {datetime.now()}")
