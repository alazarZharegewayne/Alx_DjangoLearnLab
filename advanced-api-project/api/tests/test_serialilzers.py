from django.test import TestCase
from ..models import Author, Book
from ..serializers import BookSerializer, AuthorSerializer
from datetime import datetime


class SerializerTests(TestCase):
    """Test cases for serializers"""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.book_data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author.id
        }
    
    def test_book_serializer_valid_data(self):
        """Test book serializer with valid data"""
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())
    
    def test_book_serializer_invalid_future_year(self):
        """Test book serializer with future publication year"""
        future_year = datetime.now().year + 1
        invalid_data = self.book_data.copy()
        invalid_data['publication_year'] = future_year
        
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
    
    def test_author_serializer_with_books(self):
        """Test author serializer includes nested books"""
        Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        
        serializer = AuthorSerializer(self.author)
        self.assertIn('books', serializer.data)
        self.assertEqual(len(serializer.data['books']), 1)
