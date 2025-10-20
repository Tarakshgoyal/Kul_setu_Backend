import requests

print("=== Checking if Data Was Loaded ===")
base_url = 'https://kul-setu-backend.onrender.com'

# Check if family members are now available
try:
    response = requests.get(f'{base_url}/family-members', timeout=15)
    print(f"Family Members: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f" Found {len(data)} family members!")
        
        # Check if any member has email/password data
        if len(data) > 0:
            sample_member = data[0]
            has_email = 'Email' in sample_member
            has_password = 'Password' in sample_member
            print(f"Sample member has Email: {has_email}")
            print(f"Sample member has Password: {has_password}")
            print(f"Sample member keys: {list(sample_member.keys())[:10]}...")
            
        # Test authentication with generated credentials
        print("\\nTesting authentication with generated credentials...")
        test_login = {
            'email': 'person1.p0001@kulsetufamily.com',
            'password': 'p0001123'
        }
        
        auth_response = requests.post(f'{base_url}/auth/login', json=test_login, timeout=10)
        print(f"Login test: {auth_response.status_code}")
        
        if auth_response.status_code == 200:
            print(" Authentication working!")
            auth_data = auth_response.json()
            print(f"Login response: {auth_data}")
        else:
            print(f"Login failed: {auth_response.text[:100]}")
            
    else:
        print(f"No family members found: {response.text[:100]}")
        
except Exception as e:
    print(f"Error checking family members: {e}")
