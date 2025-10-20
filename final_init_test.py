import requests
from datetime import datetime
import time

print(f'=== Final Database Initialization Test - {datetime.now()} ===')

base_url = 'https://kul-setu-backend.onrender.com'

# First, confirm backend is responsive
print('Testing backend health...')
try:
    health = requests.get(f'{base_url}/health', timeout=15)
    print(f' Health check: {health.status_code}')
    print(f'Response: {health.json()}')
except Exception as e:
    print(f' Health check failed: {e}')
    exit()

# Attempt database initialization with maximum patience
print('\\n Starting database initialization...')
print('This may take 3-5 minutes for 1000 records with 41 columns each...')

try:
    start_time = datetime.now()
    response = requests.post(f'{base_url}/init-db', timeout=300)  # 5 minute timeout
    end_time = datetime.now()
    
    duration = (end_time - start_time).total_seconds()
    print(f'\\n  Request completed in {duration:.1f} seconds')
    print(f'Status Code: {response.status_code}')
    
    if response.status_code == 200:
        print(' DATABASE INITIALIZATION SUCCESSFUL!')
        data = response.json()
        print(f'Response: {data}')
        
        # Verify data was loaded
        print('\\n Verifying data was loaded...')
        members_response = requests.get(f'{base_url}/family-members', timeout=15)
        
        if members_response.status_code == 200:
            members = members_response.json()
            print(f' VERIFIED: {len(members)} family members loaded!')
            
            # Test authentication
            print('\\n Testing authentication...')
            test_login = {
                'email': 'person1.p0001@kulsetufamily.com',
                'password': 'p0001123'
            }
            
            auth_response = requests.post(f'{base_url}/auth/login', json=test_login, timeout=10)
            
            if auth_response.status_code == 200:
                print(' AUTHENTICATION WORKING!')
                user_data = auth_response.json()
                print(f'User: {user_data}')
                print('\\n DEPLOYMENT SUCCESSFUL! All systems working!')
            else:
                print(f' Authentication failed: {auth_response.status_code}')
        else:
            print(f' Data verification failed: {members_response.status_code}')
    
    else:
        print(f' Database initialization failed: {response.status_code}')
        print(f'Error: {response.text[:200]}')
        
except requests.exceptions.Timeout:
    print(' Request timed out after 5 minutes')
    print('Checking if initialization completed anyway...')
    
    try:
        members_check = requests.get(f'{base_url}/family-members', timeout=10)
        if members_check.status_code == 200:
            data = members_check.json()
            print(f' SUCCESS! Data was loaded: {len(data)} members found')
        else:
            print(' Initialization did not complete')
    except:
        print(' Could not verify initialization status')
        
except Exception as e:
    print(f' Database initialization error: {e}')

print(f'\\nTest completed at {datetime.now()}')
