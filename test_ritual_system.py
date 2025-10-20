"""
Test script for Ritual Reminder System
Tests all ritual endpoints and sample data
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://kul-setu-backend.onrender.com"
# BASE_URL = "http://127.0.0.1:5000"  # Use this for local testing

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_ritual_types():
    """Test getting ritual types"""
    print_section("TEST 1: Get Ritual Types")
    
    response = requests.get(f"{BASE_URL}/rituals/types")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Ritual Types Available: {len(data['ritual_types'])}")
        print("\nRitual Types:")
        for ritual in data['ritual_types']:
            print(f"  - {ritual['label']} ({ritual['value']})")
        
        print(f"\nRecurrence Patterns: {data['recurrence_patterns']}")
        print(f"Pandit Types: {data['pandit_types']}")
    else:
        print(f"❌ Error: {response.text}")

def test_create_ritual():
    """Test creating a new ritual"""
    print_section("TEST 2: Create New Ritual Reminder")
    
    # Create a test ritual
    ritual_data = {
        "familyId": "F01",
        "ritualType": "pooja",
        "ritualName": "Test Ganesh Chaturthi Puja",
        "ritualDate": (datetime.now() + timedelta(days=60)).strftime('%d-%m-%Y'),
        "recurring": True,
        "recurrencePattern": "yearly",
        "location": "Home Temple - Test Location",
        "panditType": "Purohit",
        "kulDevta": "Lord Ganesha",
        "description": "Annual Ganesh Chaturthi celebration with family",
        "notes": "Test ritual - Prepare modaks and flowers",
        "reminderDaysBefore": 10
    }
    
    response = requests.post(f"{BASE_URL}/rituals/create", json=ritual_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Ritual Created Successfully!")
        print(f"Reminder ID: {result.get('reminderId')}")
        return result.get('reminderId')
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_get_family_rituals(family_id="F01"):
    """Test getting rituals for a specific family"""
    print_section(f"TEST 3: Get Rituals for Family {family_id}")
    
    response = requests.get(f"{BASE_URL}/rituals/{family_id}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        rituals = response.json()
        print(f"✅ Found {len(rituals)} rituals for family {family_id}")
        
        if rituals:
            print("\nRituals:")
            for ritual in rituals[:5]:  # Show first 5
                print(f"\n  Reminder ID: {ritual['reminderId']}")
                print(f"  Type: {ritual['ritualType']}")
                print(f"  Name: {ritual['ritualName']}")
                print(f"  Date: {ritual['ritualDate']}")
                print(f"  Location: {ritual['location']}")
                print(f"  Recurring: {ritual['recurring']}")
                
            if len(rituals) > 5:
                print(f"\n  ... and {len(rituals) - 5} more rituals")
        
        return rituals
    else:
        print(f"❌ Error: {response.text}")
        return []

def test_upcoming_rituals():
    """Test getting upcoming rituals"""
    print_section("TEST 4: Get Upcoming Rituals (Next 30 Days)")
    
    response = requests.get(f"{BASE_URL}/rituals/upcoming?daysAhead=30")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        rituals = response.json()
        print(f"✅ Found {len(rituals)} upcoming rituals in next 30 days")
        
        if rituals:
            print("\nUpcoming Rituals:")
            for ritual in rituals:
                print(f"\n  {ritual['ritualName']}")
                print(f"  Date: {ritual['ritualDate']}")
                print(f"  Type: {ritual['ritualType']}")
                print(f"  Location: {ritual['location']}")
    else:
        print(f"❌ Error: {response.text}")

def test_ritual_stats():
    """Test getting ritual statistics"""
    print_section("TEST 5: Get Ritual Statistics")
    
    response = requests.get(f"{BASE_URL}/rituals/stats")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Statistics Retrieved Successfully!")
        print(f"\nTotal Rituals: {stats['total']}")
        print(f"Upcoming: {stats['upcoming']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        
        print("\nRituals by Type:")
        for ritual_type, count in stats['byType'].items():
            print(f"  {ritual_type}: {count}")
    else:
        print(f"❌ Error: {response.text}")

def test_update_ritual(reminder_id):
    """Test updating a ritual"""
    print_section(f"TEST 6: Update Ritual {reminder_id}")
    
    update_data = {
        "notes": "Updated notes - Testing update functionality",
        "reminderDaysBefore": 20
    }
    
    response = requests.put(f"{BASE_URL}/rituals/update/{reminder_id}", json=update_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Ritual Updated Successfully!")
    else:
        print(f"❌ Error: {response.text}")

def test_filter_rituals():
    """Test filtering rituals by type"""
    print_section("TEST 7: Filter Rituals by Type (Barsi)")
    
    response = requests.get(f"{BASE_URL}/rituals/F01?type=barsi&showCompleted=false")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        rituals = response.json()
        print(f"✅ Found {len(rituals)} Barsi rituals")
        
        if rituals:
            print("\nBarsi Rituals:")
            for ritual in rituals:
                print(f"  - {ritual['ritualName']} on {ritual['ritualDate']}")
    else:
        print(f"❌ Error: {response.text}")

def run_all_tests():
    """Run all ritual system tests"""
    print("\n" + "🎉"*30)
    print("RITUAL REMINDER SYSTEM - COMPREHENSIVE TEST")
    print("🎉"*30)
    
    try:
        # Test 1: Get ritual types
        test_ritual_types()
        
        # Test 2: Create new ritual
        new_reminder_id = test_create_ritual()
        
        # Test 3: Get family rituals
        rituals = test_get_family_rituals("F01")
        
        # Test 4: Get upcoming rituals
        test_upcoming_rituals()
        
        # Test 5: Get statistics
        test_ritual_stats()
        
        # Test 6: Update ritual (if we created one)
        if new_reminder_id:
            test_update_ritual(new_reminder_id)
        elif rituals:
            test_update_ritual(rituals[0]['reminderId'])
        
        # Test 7: Filter rituals
        test_filter_rituals()
        
        print("\n" + "="*60)
        print("  ✅ ALL TESTS COMPLETED!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
