# Create Operation

## Python Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
```

## Output
```
Book created: 1984 by George Orwell (1949)
```

## Explanation
This command creates a new Book instance with the specified attributes and saves it to the database.
