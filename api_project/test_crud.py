import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/books_all/'

def test_crud_operations():
    print("Testing CRUD Operations...")
    
    # 1. List all books
    print("\n1. Listing all books:")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 2. Create a new book
    print("\n2. Creating a new book:")
    new_book = {
        "title": "Test Book from Python",
        "author": "Test Author",
        "published_date": "2024-01-15",
        "isbn": "9780000000000",
        "page_count": 200
    }
    response = requests.post(BASE_URL, json=new_book)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        book_data = response.json()
        book_id = book_data['id']
        print(f"Created book with ID: {book_id}")
        print(f"Book data: {book_data}")
        
        # 3. Retrieve the specific book
        print(f"\n3. Retrieving book ID {book_id}:")
        response = requests.get(f"{BASE_URL}{book_id}/")
        print(f"Status: {response.status_code}")
        print(f"Book data: {response.json()}")
        
        # 4. Update the book
        print(f"\n4. Updating book ID {book_id}:")
        updated_book = {
            "title": "Updated Test Book",
            "author": "Updated Author",
            "published_date": "2024-01-15",
            "isbn": "9780000000000",
            "page_count": 250
        }
        response = requests.put(f"{BASE_URL}{book_id}/", json=updated_book)
        print(f"Status: {response.status_code}")
        print(f"Updated book: {response.json()}")
        
        # 5. Delete the book
        print(f"\n5. Deleting book ID {book_id}:")
        response = requests.delete(f"{BASE_URL}{book_id}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 204:
            print("Book deleted successfully")
    
    # Final list to confirm
    print("\n6. Final list of books:")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Books count: {len(response.json())}")

if __name__ == "__main__":
    test_crud_operations()
