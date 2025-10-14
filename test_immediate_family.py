import requests
import json

def test_immediate_family_flow():
    base_url = "http://127.0.0.1:5000"
    
    print("=== Testing Immediate Family Tree Functionality ===\n")
    
    # Step 1: Create a test user with existing family and person ID
    print("Step 1: Creating test user with Family ID and Person ID")
    signup_data = {
        "email": "john.smith@example.com",
        "password": "password123",
        "firstName": "John",
        "lastName": "Smith",
        "familyId": "F01",
        "personId": "P0001"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/signup", json=signup_data)
        print(f"Signup Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"User created: {result}")
        else:
            print(f"Signup failed: {response.text}")
    except Exception as e:
        print(f"Signup error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Step 2: Login with the test user
    print("Step 2: Logging in with test user")
    login_data = {
        "email": "john.smith@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Login successful: {result}")
            user_data = result.get('user', {})
            print(f"User Family ID: {user_data.get('familyId')}")
            print(f"User Person ID: {user_data.get('personId')}")
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Login error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Step 3: Get family members to check immediate family
    print("Step 3: Getting family members")
    try:
        response = requests.post(f"{base_url}/search", 
                               json={}, 
                               headers={"Content-Type": "application/json"})
        print(f"Search Status: {response.status_code}")
        if response.status_code == 200:
            members = response.json()
            print(f"Total members found: {len(members)}")
            
            # Find P0001 and their immediate family
            user_member = next((m for m in members if m.get('personId') == 'P0001'), None)
            if user_member:
                print(f"\nUser member found: {user_member.get('firstName')} (ID: {user_member.get('personId')})")
                print(f"Spouse ID: {user_member.get('spouseId')}")
                print(f"Generation: {user_member.get('generation')}")
                
                # Find spouse
                spouse = None
                if user_member.get('spouseId'):
                    spouse = next((m for m in members if m.get('personId') == user_member.get('spouseId')), None)
                    if spouse:
                        print(f"Spouse: {spouse.get('firstName')} (ID: {spouse.get('personId')})")
                
                # Find children
                children = [m for m in members if 
                          m.get('fatherId') == 'P0001' or m.get('motherId') == 'P0001' or
                          (spouse and (m.get('fatherId') == spouse.get('personId') or m.get('motherId') == spouse.get('personId')))]
                
                print(f"Children found: {len(children)}")
                for child in children:
                    print(f"  - {child.get('firstName')} (ID: {child.get('personId')})")
                
                print(f"\nImmediate family size: {1 + (1 if spouse else 0) + len(children)} members")
            else:
                print("User member P0001 not found in database")
        else:
            print(f"Search failed: {response.text}")
    except Exception as e:
        print(f"Search error: {e}")

if __name__ == "__main__":
    test_immediate_family_flow()