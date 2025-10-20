import requests
import json

print("=== Testing Database Initialization ===")

# Test the init-db endpoint with more detailed error handling
try:
    response = requests.post('https://kul-setu-backend.onrender.com/init-db', timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text[:500]}")
    
    if response.status_code == 200:
        print(" Database initialized successfully!")
        data = response.json()
        print(f"Message: {data.get('message', 'No message')}")
    else:
        print(" Database initialization failed")
        
except requests.exceptions.Timeout:
    print(" Request timed out")
except requests.exceptions.ConnectionError:
    print(" Connection error")
except Exception as e:
    print(f" Error: {e}")
