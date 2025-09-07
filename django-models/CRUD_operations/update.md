# Update Operation

## Python Command
```python
from bookshelf.models import Book
book_to_update = Book.objects.get(title="1984")
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()
print(f"Updated title: {book_to_update.title}")
```

## Output
```
Updated title: Nineteen Eighty-Four
```

## Explanation
This command retrieves the book, updates its title, and saves the changes.
