import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_all_endpoints():
    print("Testing API Endpoints...")
    
    # Test 1: List books (should work without auth)
    print("\n1. Testing Book List (GET /books/):")
    response = requests.get(f"{BASE_URL}/books/")
    print(f"Status: {response.status_code}")
    print(f"Books found: {len(response.json())}")
    
    # Test 2: Book detail (should work without auth)
    print("\n2. Testing Book Detail (GET /books/1/):")
    response = requests.get(f"{BASE_URL}/books/1/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        book_data = response.json()
        print(f"Book: {book_data['title']} by {book_data['author']}")
    
    # Test 3: Create book without auth (should fail)
    print("\n3. Testing Book Create without auth (should fail):")
    new_book = {
        "title": "Test Book Creation",
        "publication_year": 2024,
        "author": 1
    }
    response = requests.post(f"{BASE_URL}/books/create/", json=new_book)
    print(f"Status: {response.status_code} (Should be 403 Forbidden)")
    
    # Test 4: List authors
    print("\n4. Testing Author List (GET /authors/):")
    response = requests.get(f"{BASE_URL}/authors/")
    print(f"Status: {response.status_code}")
    print(f"Authors found: {len(response.json())}")
    
    # Test 5: Author detail with nested books
    print("\n5. Testing Author Detail with nested books:")
    response = requests.get(f"{BASE_URL}/authors/1/")
    if response.status_code == 200:
        author_data = response.json()
        print(f"Author: {author_data['name']}")
        print(f"Books by this author: {len(author_data['books'])}")
    
    print("\n=== All endpoint tests completed ===")

if __name__ == "__main__":
    test_all_endpoints()
