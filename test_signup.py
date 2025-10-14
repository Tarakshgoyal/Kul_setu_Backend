import requests
import json

# Test the updated signup endpoint with person ID
def test_signup_with_person_id():
    url = "https://kul-setu-backend.onrender.com/auth/signup"
    
    # Test 1: Signup with existing family ID and person ID
    print("Test 1: Signup with family ID and person ID")
    test_data = {
        "email": "test.user@example.com",
        "password": "testpassword123",
        "firstName": "Test",
        "lastName": "User",
        "familyId": "F01",  # Assuming F01 exists
        "personId": "P0001"  # Assuming P0001 exists in F01
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Signup with family ID but no person ID (should generate new person ID)
    print("Test 2: Signup with family ID only")
    test_data2 = {
        "email": "test.user2@example.com",
        "password": "testpassword123",
        "firstName": "Test2",
        "lastName": "User2",
        "familyId": "F01",
        "personId": None
    }
    
    try:
        response = requests.post(url, json=test_data2)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Signup with no family ID or person ID (should create new family)
    print("Test 3: Signup with no family ID or person ID")
    test_data3 = {
        "email": "test.user3@example.com",
        "password": "testpassword123",
        "firstName": "Test3",
        "lastName": "User3",
        "familyId": None,
        "personId": None
    }
    
    try:
        response = requests.post(url, json=test_data3)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_signup_with_person_id()