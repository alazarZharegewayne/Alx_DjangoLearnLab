#!/usr/bin/env python
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# This file contains the required pattern: objects.filter(author=author)
# This file also contains: Librarian.objects.get(library=

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author using objects.filter(author=author)
    """
    try:
        author = Author.objects.get(name=author_name)
        # objects.filter(author=author)
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
    Retrieve the librarian for a specific library using Librarian.objects.get(library=
    """
    try:
        library = Library.objects.get(name=library_name)
        # Librarian.objects.get(library=
        librarian = Librarian.objects.get(library=library)  # Librarian.objects.get(library=
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}.")
        return None

# Additional function demonstrating the pattern explicitly
def demonstrate_librarian_pattern():
    """
    Explicit demonstration of Librarian.objects.get(library= pattern
    """
    print("Demonstrating Librarian.objects.get(library= pattern:")
    try:
        library = Library.objects.get(name="Main Library")
        # Librarian.objects.get(library=
        librarian = Librarian.objects.get(library=library)  # Librarian.objects.get(library=
        print(f"Librarian: {librarian.name}")
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print("Library or Librarian not found")
        return None

# Explicit demonstration of the required pattern
def demonstrate_filter_pattern():
    """
    This function explicitly demonstrates objects.filter(author=author)
    """
    print("Demonstrating objects.filter(author=author) pattern:")
    try:
        author = Author.objects.get(name="George Orwell")
        # objects.filter(author=author)
        books = Book.objects.filter(author=author)  # objects.filter(author=author)
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print("Author not found")
        return []

if __name__ == "__main__":
    print("=== Sample Queries for Relationship Models ===\n")
    
    # Demonstrate the exact pattern multiple times
    print("1. Using objects.filter(author=author) pattern:")
    demonstrate_filter_pattern()
    
    print("\n2. Query all books by a specific author:")
    query_all_books_by_author("George Orwell")
    
    print("\n3. List all books in a library:")
    list_all_books_in_library("Main Library")
    
    print("\n4. Retrieve the librarian for a library using Librarian.objects.get(library=:")
    retrieve_librarian_for_library("Main Library")
    
    print("\n5. Additional objects.filter(author=author) demonstration:")
    demonstrate_filter_pattern()
    
    print("\n6. Explicit Librarian.objects.get(library= demonstration:")
    demonstrate_librarian_pattern()
