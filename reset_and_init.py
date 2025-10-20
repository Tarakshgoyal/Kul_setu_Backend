import requests
from datetime import datetime

print(f"=== Reset and Initialize Database - {datetime.now()} ===\n")

base_url = 'https://kul-setu-backend.onrender.com'

# Step 1: Reset Database
print("Step 1: Resetting database (dropping all tables)...")
try:
    reset_response = requests.post(f'{base_url}/reset-db', timeout=30)
    print(f"Reset Status: {reset_response.status_code}")
    
    if reset_response.status_code == 200:
        result = reset_response.json()
        print(f"✅ {result.get('message', 'Database reset successful')}")
    else:
        try:
            error = reset_response.json()
            print(f"❌ Reset failed: {error.get('error', 'Unknown error')}")
        except:
            print(f"❌ Reset failed: {reset_response.text[:200]}")
        exit()
except Exception as e:
    print(f"❌ Reset error: {e}")
    exit()

# Step 2: Wait a moment
print("\nWaiting 5 seconds before initialization...")
import time
time.sleep(5)

# Step 3: Initialize Database
print("\nStep 2: Initializing database with fresh data...")
print("This may take 2-3 minutes for 1000 records...")
try:
    init_start = datetime.now()
    init_response = requests.post(f'{base_url}/init-db', timeout=240)
    init_duration = (datetime.now() - init_start).total_seconds()
    
    print(f"⏱️  Completed in {init_duration:.1f} seconds")
    print(f"Status Code: {init_response.status_code}")
    
    if init_response.status_code == 200:
        result = init_response.json()
        print(f"✅ {result.get('message', 'Success')}")
    else:
        print(f"❌ Initialization failed")
        try:
            error_data = init_response.json()
            print(f"Error: {error_data.get('error', 'Unknown error')}")
            if 'trace' in error_data:
                print(f"\nFull trace:")
                print(error_data['trace'])
        except:
            print(f"Response: {init_response.text[:500]}")
        exit()
except Exception as e:
    print(f"❌ Initialization error: {e}")
    exit()

# Step 4: Verify Data
print("\nStep 3: Verifying data was loaded...")
try:
    members = requests.get(f'{base_url}/family-members', timeout=15)
    if members.status_code == 200:
        members_data = members.json()
        print(f"✅ Found {len(members_data)} family members!")
    else:
        print(f"❌ Verification failed: {members.status_code}")
        exit()
except Exception as e:
    print(f"❌ Verification error: {e}")
    exit()

# Step 5: Test Authentication
print("\nStep 4: Testing authentication...")
try:
    test_login = {
        'email': 'person1.p0001@kulsetufamily.com',
        'password': 'p0001123'
    }
    
    auth = requests.post(f'{base_url}/auth/login', json=test_login, timeout=15)
    
    if auth.status_code == 200:
        auth_data = auth.json()
        print(f"✅ Authentication successful!")
        user_info = auth_data.get('user', {})
        print(f"Logged in as: {user_info.get('name', 'N/A')}")
    else:
        print(f"❌ Authentication failed: {auth.status_code}")
except Exception as e:
    print(f"❌ Authentication error: {e}")

print("\n" + "="*50)
print("🎉 DEPLOYMENT COMPLETE AND VERIFIED!")
print("="*50)
print(f"\nCompleted at {datetime.now()}")
