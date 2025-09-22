import requests
import json

BASE_URL = 'http://127.0.0.1:8000'
API_BASE = f'{BASE_URL}/api'

def test_authentication():
    print("Testing Authentication and Permissions...")
    
    # Test 1: Try to access without token (should fail)
    print("\n1. Testing access without authentication:")
    response = requests.get(f"{API_BASE}/books_all/")
    print(f"Status: {response.status_code} (Should be 403 or 401)")
    
    # Test 2: Get authentication token
    print("\n2. Getting authentication token:")
    auth_data = {
        "username": "admin",  # Replace with your username
        "password": "admin"   # Replace with your password
    }
    response = requests.post(f"{BASE_URL}/api-token-auth/", json=auth_data)
    if response.status_code == 200:
        token = response.json()['token']
        print(f"Token obtained: {token[:10]}...")
        
        headers = {'Authorization': f'Token {token}'}
        
        # Test 3: Access with token (should succeed)
        print("\n3. Testing access with authentication token:")
        response = requests.get(f"{API_BASE}/books_all/", headers=headers)
        print(f"Status: {response.status_code} (Should be 200)")
        
        # Test 4: Create book with authentication
        print("\n4. Testing book creation with authentication:")
        new_book = {
            "title": "Authenticated Book",
            "author": "Auth Author",
            "published_date": "2024-01-01",
            "isbn": "9781111111111",
            "page_count": 150
        }
        response = requests.post(f"{API_BASE}/books_all/", json=new_book, headers=headers)
        print(f"Status: {response.status_code}")
        
    else:
        print("Failed to get token")
    
    # Test 5: User registration
    print("\n5. Testing user registration:")
    user_data = {
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com"
    }
    response = requests.post(f"{API_BASE}/register/", json=user_data)
    print(f"Registration Status: {response.status_code}")

if __name__ == "__main__":
    test_authentication()
