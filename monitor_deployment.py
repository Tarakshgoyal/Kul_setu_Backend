#!/usr/bin/env python3
"""
Monitor backend deployment and test functionality
"""
import requests
import time
import json

BACKEND_URL = "https://kul-setu-backend.onrender.com"

def wait_for_deployment():
    """Wait for the backend to be redeployed and ready"""
    print("⏳ Waiting for backend redeployment...")
    
    for attempt in range(30):  # Wait up to 5 minutes
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=10)
            if response.status_code == 200:
                print(f"✅ Backend is ready! (attempt {attempt + 1})")
                return True
        except:
            pass
        
        print(f"🔄 Attempt {attempt + 1}/30 - Backend not ready yet...")
        time.sleep(10)
    
    print("❌ Timeout waiting for backend deployment")
    return False

def test_endpoints():
    """Test all critical endpoints"""
    print("\n🧪 Testing backend endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test stats endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats endpoint working: {stats.get('total_members', 0)} members")
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
    
    # Test search endpoint
    try:
        response = requests.post(
            f"{BACKEND_URL}/search", 
            json={}, 
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Search endpoint working: {len(results)} results")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")

def main():
    """Main monitoring function"""
    print("🚀 Backend Deployment Monitor")
    print(f"Backend URL: {BACKEND_URL}")
    print("=" * 50)
    
    if wait_for_deployment():
        test_endpoints()
        
        print("\n" + "=" * 50)
        print("🎉 Backend is ready!")
        print("\nYour frontend should now work properly:")
        print("🖥️  Frontend: http://localhost:8081/")
        print("⚙️  Backend: https://kul-setu-backend.onrender.com")
        print("\nTry refreshing your browser to test the application!")
    else:
        print("\n" + "=" * 50)
        print("❌ Backend deployment monitoring failed")
        print("Please check Render dashboard for deployment status")

if __name__ == "__main__":
    main()