import requests
import json

def push_data_to_database():
    """Push updated CSV data to the database via the backend API"""
    
    base_url = "https://kul-setu-backend.onrender.com"
    
    print("=== Pushing Updated Data to DATABASE_URL ===\n")
    
    # First, test if the backend is responsive
    print("Step 1: Testing backend connectivity...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"✅ Backend is online: {response.json()}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False
    
    print("\nStep 2: Initializing database with updated CSV data...")
    try:
        # Call the init-db endpoint to reload CSV data
        response = requests.post(f"{base_url}/init-db", 
                                headers={"Content-Type": "application/json"})
        
        print(f"Init-DB Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Database initialized successfully!")
            print(f"Response: {result}")
            return True
        else:
            print(f"❌ Database initialization failed")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def test_login_after_update():
    """Test login functionality after database update"""
    
    base_url = "https://kul-setu-backend.onrender.com"
    
    print("\n" + "="*50)
    print("Step 3: Testing login with updated credentials...")
    
    # Test credentials from the updated CSV
    test_credentials = [
        ("person1.p0001@kulsetufamily.com", "p0001123"),
        ("person2.p0002@kulsetufamily.com", "p0002123")
    ]
    
    for email, password in test_credentials:
        print(f"\n🔑 Testing login: {email}")
        
        login_data = {
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(f"{base_url}/auth/login", json=login_data)
            print(f"Login Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    user = result.get('user', {})
                    print(f"✅ Login successful!")
                    print(f"   User: {user.get('firstName')} {user.get('lastName')}")
                    print(f"   Person ID: {user.get('personId')}")
                    print(f"   Family ID: {user.get('familyId')}")
                    return True
                else:
                    print(f"❌ Login failed: {result.get('error')}")
            else:
                try:
                    error_data = response.json()
                    print(f"❌ Login failed: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"❌ Login failed: {response.text}")
        
        except Exception as e:
            print(f"❌ Login error: {e}")
    
    return False

def verify_data_integrity():
    """Verify that the data was properly loaded"""
    
    base_url = "https://kul-setu-backend.onrender.com"
    
    print("\n" + "="*50)
    print("Step 4: Verifying data integrity...")
    
    try:
        # Test search to see if data is loaded
        response = requests.post(f"{base_url}/search", 
                                json={}, 
                                headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            members = response.json()
            print(f"✅ Search successful: {len(members)} family members loaded")
            
            if len(members) > 0:
                sample = members[0]
                print(f"   Sample member: {sample.get('firstName')} (ID: {sample.get('personId')})")
                
                # Check if email/password fields exist
                families = {}
                for member in members[:10]:  # Check first 10 members
                    family_id = member.get('familyLineId')
                    if family_id:
                        families[family_id] = families.get(family_id, 0) + 1
                
                print(f"   Found {len(families)} family lines")
                print(f"   Family distribution: {dict(list(families.items())[:3])}")
                return True
            else:
                print("❌ No family members found in database")
                return False
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Data verification error: {e}")
        return False

if __name__ == "__main__":
    success = push_data_to_database()
    
    if success:
        login_success = test_login_after_update()
        data_success = verify_data_integrity()
        
        print("\n" + "="*50)
        print("=== SUMMARY ===")
        print(f"Database Update: {'✅ SUCCESS' if success else '❌ FAILED'}")
        print(f"Login Test: {'✅ SUCCESS' if login_success else '❌ FAILED'}")
        print(f"Data Verification: {'✅ SUCCESS' if data_success else '❌ FAILED'}")
        
        if success and login_success and data_success:
            print("\n🎉 All systems updated successfully!")
            print("You can now login with:")
            print("   Email: person1.p0001@kulsetufamily.com")
            print("   Password: p0001123")
        else:
            print("\n⚠️  Some issues detected. Backend deployment may be needed.")
    else:
        print("\n❌ Database update failed. Check backend deployment.")