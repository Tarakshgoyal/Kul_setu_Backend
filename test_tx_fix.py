import requests
from datetime import datetime

print(f'=== Testing After Transaction Fix - {datetime.now()} ===')

base_url = 'https://kul-setu-backend.onrender.com'

# Verify backend is running
print('Checking backend health...')
try:
    health = requests.get(f'{base_url}/health', timeout=15)
    print(f'Health: {health.status_code}')
except Exception as e:
    print(f'Health check failed: {e}')
    exit()

# Attempt database initialization
print('Initializing database with transaction fixes...')

try:
    start_time = datetime.now()
    response = requests.post(f'{base_url}/init-db', timeout=180)
    end_time = datetime.now()
    
    duration = (end_time - start_time).total_seconds()
    print(f'Completed in {duration:.1f} seconds')
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        print('DATABASE INITIALIZATION SUCCESSFUL!')
        result = response.json()
        print(f'Result: {result}')
        
        # Verify data was loaded
        print('Verifying family members...')
        members = requests.get(f'{base_url}/family-members', timeout=15)
        
        if members.status_code == 200:
            data = members.json()
            print(f'{len(data)} family members loaded!')
            
            # Test authentication
            print('Testing authentication...')
            login_data = {
                'email': 'person1.p0001@kulsetufamily.com',
                'password': 'p0001123'
            }
            
            auth = requests.post(f'{base_url}/auth/login', json=login_data, timeout=10)
            
            if auth.status_code == 200:
                print('AUTHENTICATION WORKING!')
                user_info = auth.json()
                user_data = user_info.get('user', {})
                first_name = user_data.get('first_name', 'Unknown')
                print(f'Logged in as: {first_name}')
                print('ALL SYSTEMS OPERATIONAL!')
            else:
                print(f'Authentication status: {auth.status_code}')
        else:
            print(f'Family members status: {members.status_code}')
    else:
        print(f'Initialization failed: {response.status_code}')
        print(f'Response: {response.text[:300]}')
        
except requests.exceptions.Timeout:
    print('Request timed out - checking data status...')
    try:
        members = requests.get(f'{base_url}/family-members', timeout=10)
        if members.status_code == 200:
            print(f'Data loaded: {len(members.json())} members')
        else:
            print('Data not loaded yet')
    except:
        print('Could not verify status')
        
except Exception as e:
    print(f'Error: {e}')

print(f'Test completed at {datetime.now()}')
