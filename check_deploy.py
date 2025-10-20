import requests

print('=== Checking Deployment Status ===')
base_url = 'https://kul-setu-backend.onrender.com'

# Check debug endpoint
try:
    debug = requests.get(f'{base_url}/debug', timeout=20)
    print(f'Debug endpoint: {debug.status_code}')
    
    if debug.status_code == 200:
        info = debug.json()
        print('Debug info:')
        for key, value in info.items():
            print(f'  {key}: {value}')
    
    # Now try init-db with extended timeout
    print('\nAttempting database initialization...')
    init = requests.post(f'{base_url}/init-db', timeout=240)
    
    print(f'Init-db: {init.status_code}')
    if init.status_code == 200:
        print('SUCCESS!')
        print(init.json())
    else:
        print(f'Failed: {init.text[:200]}')
        
except Exception as e:
    print(f'Error: {e}')
