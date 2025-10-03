from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    Each author can have multiple books associated with them through a one-to-many relationship.
    The related_name='books' allows accessing an author's books via author.books.all()
    """
    name = models.CharField(max_length=100, help_text="Full name of the author")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """
    Book model representing a published book.
    Each book is associated with one author through a foreign key relationship.
    The publication_year field stores the year the book was published.
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="Author who wrote this book"
    )

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-publication_year', 'title']
