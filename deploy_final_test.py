import requests
from datetime import datetime

print(f'=== Database Initialization - {datetime.now()} ===')
base_url = 'https://kul-setu-backend.onrender.com'

print('Starting database initialization...')
print('This may take several minutes for 1000 records...')

try:
    response = requests.post(f'{base_url}/init-db', timeout=240)
    
    print(f'Status Code: {response.status_code}')
    
    if response.status_code == 200:
        print('✅ DATABASE INITIALIZATION SUCCESSFUL!')
        data = response.json()
        print(f'Response: {data}')
        
        # Verify data was loaded
        print('\nVerifying data...')
        members_response = requests.get(f'{base_url}/family-members', timeout=15)
        
        if members_response.status_code == 200:
            members = members_response.json()
            print(f'✅ {len(members)} family members loaded!')
            
            # Test authentication
            print('\nTesting authentication...')
            test_login = {
                'email': 'person1.p0001@kulsetufamily.com',
                'password': 'p0001123'
            }
            
            auth_response = requests.post(f'{base_url}/auth/login', json=test_login, timeout=10)
            
            if auth_response.status_code == 200:
                print('✅ AUTHENTICATION WORKING!')
                user_data = auth_response.json()
                user_info = user_data.get('user', {})
                print(f'Logged in as: {user_info}')
                print('\n🎉 DEPLOYMENT COMPLETE! All systems operational!')
            else:
                print(f'Authentication test status: {auth_response.status_code}')
                print(f'Response: {auth_response.text[:100]}')
        else:
            print(f'Family members status: {members_response.status_code}')
    else:
        print(f'❌ Database initialization failed: {response.status_code}')
        print(f'Error: {response.text[:300]}')
        
except requests.exceptions.Timeout:
    print('Request timed out. Checking if data was loaded anyway...')
    try:
        members_check = requests.get(f'{base_url}/family-members', timeout=10)
        if members_check.status_code == 200:
            data = members_check.json()
            print(f'✅ Data was loaded! Found {len(data)} members')
        else:
            print(f'Data check status: {members_check.status_code}')
    except:
        print('Could not verify data status')
        
except Exception as e:
    print(f'Error: {e}')

print(f'\nCompleted at {datetime.now()}')
