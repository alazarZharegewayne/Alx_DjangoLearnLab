# Delete Operation

## Python Command
```python
from bookshelf.models import Book
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")
book_to_delete.delete()
print("Book deleted successfully")

# Verify deletion
try:
    Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists")
except Book.DoesNotExist:
    print("Book successfully deleted - no longer exists in database")

# Check all books
all_books = Book.objects.all()
print(f"Books in database: {all_books.count()}")
