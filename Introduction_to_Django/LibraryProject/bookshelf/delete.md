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
    print("Book successfully deleted")
```

## Output
```
Book deleted successfully
Book successfully deleted
```

## Explanation
This command deletes the book from the database and verifies the deletion.
