# Retrieve Operation

## Python Command
```python
from bookshelf.models import Book
retrieved_book = Book.objects.get(title="1984")
print(f"Retrieved: {retrieved_book.title} by {retrieved_book.author}, published in {retrieved_book.publication_year}")
