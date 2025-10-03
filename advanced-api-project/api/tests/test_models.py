from django.test import TestCase
from ..models import Author, Book


class ModelTests(TestCase):
    """Test cases for models"""
    
    def test_create_author(self):
        """Test creating an author"""
        author = Author.objects.create(name='Test Author')
        self.assertEqual(str(author), 'Test Author')
        self.assertEqual(author.name, 'Test Author')
    
    def test_create_book(self):
        """Test creating a book"""
        author = Author.objects.create(name='Test Author')
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=author
        )
        self.assertEqual(str(book), 'Test Book by Test Author')
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publication_year, 2020)
        self.assertEqual(book.author, author)
    
    def test_author_book_relationship(self):
        """Test author-book relationship"""
        author = Author.objects.create(name='Test Author')
        book1 = Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=author
        )
        book2 = Book.objects.create(
            title='Book 2', 
            publication_year=2021,
            author=author
        )
        
        self.assertEqual(author.books.count(), 2)
        self.assertIn(book1, author.books.all())
        self.assertIn(book2, author.books.all())
