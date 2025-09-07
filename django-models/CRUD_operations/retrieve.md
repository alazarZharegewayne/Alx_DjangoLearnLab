# Retrieve Operation

## Python Command
```python
from bookshelf.models import Book
retrieved_book = Book.objects.get(title="Nineteen Eighty-Four")
print(f"Retrieved: {retrieved_book.title} by {retrieved_book.author}")
```

## Output
```
Retrieved: Nineteen Eighty-Four by George Orwell
```

## Explanation
This command retrieves the book from the database using the title as a lookup field.
