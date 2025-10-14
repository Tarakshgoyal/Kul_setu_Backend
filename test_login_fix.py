import requests

def test_init_db_and_login():
    """Test initializing database and login functionality"""
    
    base_url = "https://kul-setu-backend.onrender.com"
    
    print("=== Testing Database Initialization and Login ===\n")
    
    # Step 1: Initialize database
    print("Step 1: Initializing database...")
    try:
        response = requests.post(f"{base_url}/init-db")
        print(f"Init DB Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Init DB Response: {result}")
        else:
            print(f"Init DB failed: {response.text}")
            return
    except Exception as e:
        print(f"Init DB error: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Step 2: Test login with a CSV user
    print("Step 2: Testing login with CSV user...")
    
    test_credentials = [
        ("person1.p0001@kulsetufamily.com", "p0001123"),
        ("person2.p0002@kulsetufamily.com", "p0002123"),
        ("person10.p0010@kulsetufamily.com", "p0010123")
    ]
    
    for email, password in test_credentials:
        print(f"\nTrying login: {email}")
        login_data = {
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(f"{base_url}/auth/login", json=login_data)
            print(f"Login Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Login successful!")
                print(f"   User: {result.get('user', {}).get('firstName')} (ID: {result.get('user', {}).get('personId')})")
                print(f"   Family: {result.get('user', {}).get('familyId')}")
                break  # Success, stop testing
            else:
                print(f"❌ Login failed: {response.json() if response.headers.get('content-type') == 'application/json' else response.text}")
        except Exception as e:
            print(f"Login error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Step 3: Test search to verify data is loaded
    print("Step 3: Testing search functionality...")
    try:
        response = requests.post(f"{base_url}/search", 
                               json={}, 
                               headers={"Content-Type": "application/json"})
        print(f"Search Status: {response.status_code}")
        if response.status_code == 200:
            members = response.json()
            print(f"✅ Search successful! Found {len(members)} family members")
            if len(members) > 0:
                sample = members[0]
                print(f"   Sample member: {sample.get('firstName')} (ID: {sample.get('personId')})")
        else:
            print(f"❌ Search failed: {response.text}")
    except Exception as e:
        print(f"Search error: {e}")

if __name__ == "__main__":
    test_init_db_and_login()