import requests
from datetime import datetime

print(f'=== Database Initialization Attempt - {datetime.now()} ===')
base_url = 'https://kul-setu-backend.onrender.com'

# Test with very detailed error reporting
try:
    print('Sending initialization request...')
    response = requests.post(f'{base_url}/init-db', timeout=240)
    
    print(f'Status: {response.status_code}')
    print(f'Headers: {dict(response.headers)}')
    
    if response.status_code == 200:
        print(' SUCCESS!')
        data = response.json()
        print(f'Response: {data}')
        
        # Test data
        members = requests.get(f'{base_url}/family-members', timeout=15)
        if members.status_code == 200:
            print(f' {len(members.json())} members loaded!')
    else:
        print(f' Failed')
        # Try to get JSON error if available
        try:
            error_data = response.json()
            print(f'Error details: {error_data}')
        except:
            print(f'HTML Error: {response.text[:500]}')
            
except Exception as e:
    print(f'Exception: {e}')

print(f'Completed: {datetime.now()}')
