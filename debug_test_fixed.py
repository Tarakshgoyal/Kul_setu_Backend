import requests

print('=== Debug Endpoint Test ===')
base_url = 'https://kul-setu-backend.onrender.com'

# Test debug endpoint
try:
    response = requests.get(f'{base_url}/debug', timeout=20)
    print(f'Debug endpoint status: {response.status_code}')
    
    if response.status_code == 200:
        debug_data = response.json()
        print('Debug Information:')
        for key, value in debug_data.items():
            print(f'  {key}: {value}')
        
        # Analyze the results
        csv_exists = debug_data.get('csv_exists', False)
        db_connected = debug_data.get('database_connected', False)
        has_email = debug_data.get('has_email', False)
        has_password = debug_data.get('has_password', False)
        
        if not csv_exists:
            print('CSV file not found in deployment!')
        elif not db_connected:
            print('Database connection failed!')
            db_error = debug_data.get('database_error', 'Unknown')
            print(f'Database error: {db_error}')
        elif not has_email or not has_password:
            print('CSV missing email/password columns!')
        else:
            print('All components look good!')
    else:
        print(f'Debug endpoint failed: {response.text[:200]}')
        
except Exception as e:
    print(f'Debug endpoint error: {e}')
