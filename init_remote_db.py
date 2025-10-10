#!/usr/bin/env python3
"""
Remote database initialization script
This script calls the backend API to initialize the database
"""
import requests
import json

BACKEND_URL = "https://kul-setu-backend.onrender.com"

def test_health():
    """Test if the backend is responsive"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=30)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach backend: {e}")
        return False

def initialize_database():
    """Initialize the remote database"""
    try:
        print("🔄 Initializing remote database...")
        response = requests.post(f"{BACKEND_URL}/init-db", timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Database initialized: {data.get('message')}")
            return True
        else:
            print(f"❌ Database initialization failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def check_stats():
    """Check database statistics"""
    try:
        print("📊 Checking database stats...")
        response = requests.get(f"{BACKEND_URL}/stats", timeout=30)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Database stats:")
            print(f"   Total members: {stats.get('total_members', 0)}")
            print(f"   Total families: {stats.get('total_families', 0)}")
            if stats.get('families'):
                print("   Family breakdown:")
                for family_id, count in stats.get('families', {}).items():
                    print(f"     {family_id}: {count} members")
            return True
        else:
            print(f"❌ Stats check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Stats check error: {e}")
        return False

def test_search():
    """Test the search functionality"""
    try:
        print("🔍 Testing search functionality...")
        response = requests.post(
            f"{BACKEND_URL}/search", 
            json={},  # Empty search should return all members
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Search test successful: {len(results)} members returned")
            if results:
                print(f"   Sample member: {results[0].get('firstName', 'Unknown')}")
            return True
        else:
            print(f"❌ Search test failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Search test error: {e}")
        return False

def main():
    """Main initialization routine"""
    print("🚀 Starting remote database initialization...")
    print(f"Backend URL: {BACKEND_URL}")
    print("=" * 50)
    
    # Step 1: Test health
    if not test_health():
        print("❌ Cannot proceed - backend is not responding")
        return False
    
    # Step 2: Initialize database
    if not initialize_database():
        print("❌ Database initialization failed")
        return False
    
    # Step 3: Check stats
    if not check_stats():
        print("⚠️  Stats check failed, but database might still be working")
    
    # Step 4: Test search
    if not test_search():
        print("⚠️  Search test failed, but database might still be working")
    
    print("=" * 50)
    print("🎉 Remote database setup completed!")
    print("\nYour frontend should now be able to connect to the backend.")
    print(f"Frontend URL: http://localhost:8081/")
    print(f"Backend URL: {BACKEND_URL}")
    
    return True

if __name__ == "__main__":
    main()