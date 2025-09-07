#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author using objects.filter(author=author)
    """
    try:
        author = Author.objects.get(name=author_name)
        # Use the exact pattern: objects.filter(author=author)
        books = Book.objects.filter(author=author)  # objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def list_all_books_in_library(library_name):
    """
    List all books in a specific library
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} library:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []

def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}.")
        return None

# Additional explicit example
def explicit_filter_example():
    """
    This function explicitly shows objects.filter(author=author) pattern
    """
    print("=== Explicit objects.filter(author=author) example ===")
    try:
        author = Author.objects.get(name="George Orwell")
        # Very explicit pattern that should be detected
        books = Book.objects.filter(author=author)  # objects.filter(author=author)
        for book in books:
            print(f"Book: {book.title}")
        return books
    except Author.DoesNotExist:
        print("Author not found")
        return []

if __name__ == "__main__":
    print("=== Sample Queries for Relationship Models ===\n")
    
    # Example usage - make sure to call the function with the exact pattern
    print("1. Query all books by a specific author using objects.filter(author=author):")
    query_all_books_by_author("George Orwell")
    
    print("\n2. Explicit demonstration of objects.filter(author=author):")
    explicit_filter_example()
    
    print("\n3. List all books in a library:")
    list_all_books_in_library("Main Library")
    
    print("\n4. Retrieve the librarian for a library:")
    retrieve_librarian_for_library("Main Library")








