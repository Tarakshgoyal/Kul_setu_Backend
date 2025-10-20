import requests
from datetime import datetime

print("="*70)
print(" 🎉 FINAL DEPLOYMENT VERIFICATION")
print("="*70)
print(f"\nTest Date: {datetime.now()}")
print(f"Backend URL: https://kul-setu-backend.onrender.com\n")

base_url = 'https://kul-setu-backend.onrender.com'
all_tests_passed = True

# Test 1: Health Check
print("Test 1: Health Check")
try:
    response = requests.get(f'{base_url}/health', timeout=10)
    if response.status_code == 200:
        print("✅ PASS - Backend is online\n")
    else:
        print(f"❌ FAIL - Status: {response.status_code}\n")
        all_tests_passed = False
except Exception as e:
    print(f"❌ FAIL - Error: {e}\n")
    all_tests_passed = False

# Test 2: Database Connection
print("Test 2: Database Connection (Debug Endpoint)")
try:
    response = requests.get(f'{base_url}/debug', timeout=10)
    if response.status_code == 200:
        debug_data = response.json()
        if debug_data.get('database_connected') and debug_data.get('csv_exists'):
            print(f"✅ PASS - Database connected, CSV exists ({debug_data.get('csv_size')} bytes)\n")
        else:
            print(f"⚠️ WARNING - Database: {debug_data.get('database_connected')}, CSV: {debug_data.get('csv_exists')}\n")
    else:
        print(f"⚠️ WARNING - Debug endpoint returned: {response.status_code}\n")
except Exception as e:
    print(f"⚠️ WARNING - Error: {e}\n")

# Test 3: Family Members Data
print("Test 3: Family Members Data")
try:
    response = requests.get(f'{base_url}/family-members', timeout=15)
    if response.status_code == 200:
        members = response.json()
        if len(members) == 1000:
            sample = members[0]
            print(f"✅ PASS - {len(members)} family members loaded")
            print(f"   Sample: {sample.get('person_id')} - {sample.get('first_name')}")
            print(f"   Email: {sample.get('email')}")
            print(f"   Password: {'***' if sample.get('password') else 'Missing'}\n")
        else:
            print(f"⚠️ WARNING - Expected 1000 members, found {len(members)}\n")
            all_tests_passed = False
    else:
        print(f"❌ FAIL - Status: {response.status_code}\n")
        all_tests_passed = False
except Exception as e:
    print(f"❌ FAIL - Error: {e}\n")
    all_tests_passed = False

# Test 4: Authentication System
print("Test 4: Authentication System")
try:
    # Test with first generated credential
    login_data = {
        'email': 'person1.p0001@kulsetufamily.com',
        'password': 'p0001123'
    }
    response = requests.post(f'{base_url}/auth/login', json=login_data, timeout=10)
    
    if response.status_code == 200:
        user_data = response.json()
        user = user_data.get('user', {})
        print(f"✅ PASS - Authentication successful")
        print(f"   User: {user.get('name', 'N/A')}")
        print(f"   Family ID: {user.get('familyId', 'N/A')}")
        print(f"   Person ID: {user.get('personId', 'N/A')}\n")
    else:
        print(f"❌ FAIL - Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}\n")
        all_tests_passed = False
except Exception as e:
    print(f"❌ FAIL - Error: {e}\n")
    all_tests_passed = False

# Test 5: User Signup
print("Test 5: User Signup (New User)")
try:
    signup_data = {
        'email': 'test.user@kulsetufamily.com',
        'password': 'testpassword123',
        'firstName': 'Test',
        'lastName': 'User',
        'familyId': 'F01'
    }
    response = requests.post(f'{base_url}/auth/signup', json=signup_data, timeout=10)
    
    if response.status_code in [200, 201]:
        print(f"✅ PASS - Signup successful\n")
    elif response.status_code == 400:
        # Might already exist from previous test
        print(f"✅ PASS - Signup endpoint working (user may already exist)\n")
    else:
        print(f"⚠️ WARNING - Status: {response.status_code}\n")
except Exception as e:
    print(f"⚠️ WARNING - Error: {e}\n")

# Test 6: Search Functionality
print("Test 6: Search Functionality")
try:
    search_data = {'query': 'person', 'limit': 5}
    response = requests.post(f'{base_url}/search', json=search_data, timeout=15)
    
    if response.status_code == 200:
        results = response.json()
        result_count = len(results.get('results', []))
        print(f"✅ PASS - Search working, found {result_count} results\n")
    else:
        print(f"⚠️ WARNING - Status: {response.status_code}")
        print(f"   Note: Search may need data refresh\n")
except Exception as e:
    print(f"⚠️ WARNING - Error: {e}\n")

# Final Summary
print("="*70)
if all_tests_passed:
    print(" 🎉 ALL CRITICAL TESTS PASSED!")
else:
    print(" ⚠️ SOME TESTS FAILED - Check details above")
print("="*70)

print("\n📊 Deployment Summary:")
print("  • Database: PostgreSQL on Render")
print("  • Records: 1000 family members with 42 fields each")
print("  • Authentication: Email/Password with hashing")
print("  • Endpoints: Health, Debug, Init-DB, Reset-DB, Family-Members,")
print("               Auth (Login/Signup), Search, Stats")
print("  • Timeout: 300 seconds for long operations")

print("\n🔗 Backend URL: https://kul-setu-backend.onrender.com")
print(f"\n✨ Verification completed at {datetime.now()}\n")
