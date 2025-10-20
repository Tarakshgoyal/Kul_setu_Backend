import requests

print('=== Debug Endpoint Test ===')
base_url = 'https://kul-setu-backend.onrender.com'

# Test debug endpoint
try:
    response = requests.get(f'{base_url}/debug', timeout=20)
    print(f'Debug endpoint status: {response.status_code}')
    
    if response.status_code == 200:
        debug_data = response.json()
        print('\\n Debug Information:')
        for key, value in debug_data.items():
            print(f'  {key}: {value}')
        
        # Analyze the results
        if not debug_data.get('csv_exists', False):
            print('\\n CSV file not found in deployment!')
        elif not debug_data.get('database_connected', False):
            print('\\n Database connection failed!')
            print(f'Database error: {debug_data.get(\"database_error\", \"Unknown\")}')
        elif not debug_data.get('has_email', False) or not debug_data.get('has_password', False):
            print('\\n CSV missing email/password columns!')
        else:
            print('\\n All components look good - trying init-db again...')
    else:
        print(f'Debug endpoint failed: {response.text[:200]}')
        
except Exception as e:
    print(f'Debug endpoint error: {e}')

# If debug shows everything is OK, try init-db one more time
print('\\n Attempting database initialization with debug info...')
try:
    init_response = requests.post(f'{base_url}/init-db', timeout=60)
    print(f'Init-db status: {init_response.status_code}')
    
    if init_response.status_code == 200:
        print(' SUCCESS! Database initialized!')
        result = init_response.json()
        print(f'Result: {result}')
    else:
        print(f'Init-db failed: {init_response.text[:200]}')
        
except Exception as e:
    print(f'Init-db error: {e}')
