import requests

print('=== Checking Deployed Code Version ===')
base_url = 'https://kul-setu-backend.onrender.com'

# Check if reset-db endpoint exists (it's in our latest code)
try:
    response = requests.post(f'{base_url}/reset-db', timeout=10)
    print(f'Reset-DB endpoint: {response.status_code} (endpoint exists)')
except Exception as e:
    print(f'Reset-DB endpoint error: {e}')

# Try to get more detailed error from init-db
try:
    print('\nTrying init-db with detailed error capture...')
    response = requests.post(f'{base_url}/init-db', timeout=60)
    print(f'Status: {response.status_code}')
    content_type = response.headers.get('Content-Type', 'Unknown')
    print(f'Content-Type: {content_type}')
    
    # Try to parse as JSON first
    try:
        data = response.json()
        print(f'JSON Response: {data}')
        if 'error' in data:
            print(f'\nError: {data["error"]}')
        if 'trace' in data:
            print(f'\nTrace:\n{data["trace"]}')
    except:
        print(f'HTML Response (first 500 chars): {response.text[:500]}')
        
except Exception as e:
    print(f'Error: {e}')
