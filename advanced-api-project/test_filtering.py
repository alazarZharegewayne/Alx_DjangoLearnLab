import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_filtering_search_ordering():
    print("Testing Filtering, Searching, and Ordering Features...")
    
    # Test 1: Basic book list
    print("\n1. Testing Basic Book List:")
    response = requests.get(f"{BASE_URL}/books/")
    print(f"Status: {response.status_code}")
    print(f"Total books: {len(response.json())}")
    
    # Test 2: Filtering by author name
    print("\n2. Testing Filtering by Author Name:")
    response = requests.get(f"{BASE_URL}/books/?author_name=Orwell")
    print(f"Status: {response.status_code}")
    books = response.json()
    print(f"Books by Orwell: {len(books)}")
    for book in books:
        print(f"  - {book['title']} ({book['publication_year']})")
    
    # Test 3: Filtering by publication year range
    print("\n3. Testing Filtering by Publication Year Range:")
    response = requests.get(f"{BASE_URL}/books/?publication_year_min=1970&publication_year_max=2000")
    print(f"Status: {response.status_code}")
    books = response.json()
    print(f"Books from 1970-2000: {len(books)}")
    for book in books:
        print(f"  - {book['title']} ({book['publication_year']})")
    
    # Test 4: Searching across title and author
    print("\n4. Testing Search Functionality:")
    response = requests.get(f"{BASE_URL}/books/?search=Harry")
    print(f"Status: {response.status_code}")
    books = response.json()
    print(f"Books matching 'Harry': {len(books)}")
    for book in books:
        print(f"  - {book['title']} by {book['author']}")
    
    # Test 5: Ordering by title
    print("\n5. Testing Ordering by Title:")
    response = requests.get(f"{BASE_URL}/books/?ordering=title")
    print(f"Status: {response.status_code}")
    books = response.json()
    print(f"First 3 books ordered by title:")
    for book in books[:3]:
        print(f"  - {book['title']}")
    
    # Test 6: Ordering by publication year (descending)
    print("\n6. Testing Ordering by Publication Year (descending):")
    response = requests.get(f"{BASE_URL}/books/?ordering=-publication_year")
    print(f"Status: {response.status_code}")
    books = response.json()
    print(f"First 3 books ordered by newest first:")
    for book in books[:3]:
        print(f"  - {book['title']} ({book['publication_year']})")
    
    # Test 7: Combined filtering, searching, and ordering
    print("\n7. Testing Combined Features:")
    response = requests.get(f"{BASE_URL}/books/?author_name=Rowling&ordering=publication_year")
    print(f"Status: {response.status_code}")
    books = response.json()
    print(f"Rowling books ordered by publication year:")
    for book in books:
        print(f"  - {book['title']} ({book['publication_year']})")
    
    print("\n=== All filtering, searching, and ordering tests completed ===")

if __name__ == "__main__":
    test_filtering_search_ordering()
