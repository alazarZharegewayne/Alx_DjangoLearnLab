# Update Operation

## Python Command
```python
from bookshelf.models import Book
book_to_update = Book.objects.get(title="1984")
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()
print(f"Updated title: {book_to_update.title}")

# Verify the update
updated_book = Book.objects.get(id=book_to_update.id)
print(f"Verified update: {updated_book.title}")
