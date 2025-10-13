import requests
import json

# Test the schema endpoint
try:
    response = requests.get('https://kul-setu-backend.onrender.com/register/schema')
    if response.status_code == 200:
        schema = response.json()
        print('✅ Schema endpoint working')
        print('Alive required fields:', len(schema['alive']['required_fields']))
        print('Dead required fields:', len(schema['dead']['required_fields']))
        print('Available field options:', list(schema['field_options'].keys()))
    else:
        print('❌ Schema endpoint failed:', response.status_code)
except Exception as e:
    print('❌ Schema test failed:', e)

# Test validation endpoint for alive member
try:
    test_data = {
        'type': 'alive',
        'data': {
            'firstName': 'Test',
            'gender': 'M',
            'generation': 1,
            'dob': '01-01-1990'
        }
    }
    response = requests.post('https://kul-setu-backend.onrender.com/register/validate', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print('✅ Alive validation working:', result['valid'])
    else:
        print('❌ Alive validation failed:', response.status_code)
except Exception as e:
    print('❌ Alive validation test failed:', e)

# Test validation endpoint for dead member
try:
    test_data = {
        'type': 'dead',
        'data': {
            'firstName': 'Test',
            'gender': 'M',
            'generation': 1,
            'dob': '01-01-1950',
            'dod': '01-01-2000',
            'causeOfDeath': 'Old Age'
        }
    }
    response = requests.post('https://kul-setu-backend.onrender.com/register/validate', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print('✅ Dead validation working:', result['valid'])
    else:
        print('❌ Dead validation failed:', response.status_code)
except Exception as e:
    print('❌ Dead validation test failed:', e)