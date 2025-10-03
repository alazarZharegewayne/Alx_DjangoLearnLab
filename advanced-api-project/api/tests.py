"""
Unit tests for Django REST Framework APIs
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BookModelTest(TestCase):
    """Test the Book model"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_book_creation(self):
        """Test book creation and string representation"""
        self.assertEqual(str(self.book), "Test Book by Test Author")
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.publication_year, 2020)
        self.assertEqual(self.book.author.name, "Test Author")


class AuthorModelTest(TestCase):
    """Test the Author model"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
    
    def test_author_creation(self):
        """Test author creation and string representation"""
        self.assertEqual(str(self.author), "Test Author")
        self.assertEqual(self.author.name, "Test Author")


class BookSerializerTest(TestCase):
    """Test the Book serializer"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.valid_data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author.id
        }
    
    def test_valid_serializer(self):
        """Test serializer with valid data"""
        serializer = BookSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_invalid_future_year(self):
        """Test serializer validation for future publication year"""
        invalid_data = self.valid_data.copy()
        invalid_data['publication_year'] = 2030  # Future year
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)


class BookListViewTest(APITestCase):
    """Test Book list view with filtering, searching, ordering"""
    
    def setUp(self):
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Jane Austen")
        
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Pride and Prejudice",
            publication_year=1813,
            author=self.author2
        )
        
        self.url = reverse('api:book-list')
    
    def test_get_all_books(self):
        """Test retrieving all books"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_filter_by_author(self):
        """Test filtering books by author name"""
        response = self.client.get(self.url, {'author_name': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_books(self):
        """Test searching books"""
        response = self.client.get(self.url, {'search': '1984'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_order_books_by_title(self):
        """Test ordering books by title"""
        response = self.client.get(self.url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['1984', 'Animal Farm', 'Pride and Prejudice'])
    
    def test_order_books_by_year_desc(self):
        """Test ordering books by publication year descending"""
        response = self.client.get(self.url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1949, 1945, 1813])


class BookDetailViewTest(APITestCase):
    """Test Book detail view"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        self.url = reverse('api:book-detail', kwargs={'pk': self.book.pk})
    
    def test_get_book_detail(self):
        """Test retrieving single book detail"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['publication_year'], 2020)
    
    def test_get_nonexistent_book(self):
        """Test retrieving non-existent book returns 404"""
        url = reverse('api:book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTest(APITestCase):
    """Test Book create view with authentication"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.url = reverse('api:book-create')
        self.valid_data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
    
    def test_create_book_authenticated(self):
        """Test creating book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_create_book_validation(self):
        """Test book creation validation"""
        self.client.force_authenticate(user=self.user)
        invalid_data = self.valid_data.copy()
        invalid_data['publication_year'] = 2030  # Future year
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookUpdateViewTest(APITestCase):
    """Test Book update view"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Original Book",
            publication_year=2020,
            author=self.author
        )
        self.url = reverse('api:book-update', kwargs={'pk': self.book.pk})
        self.update_data = {
            'title': 'Updated Book',
            'publication_year': 2021,
            'author': self.author.id
        }
    
    def test_update_book_authenticated(self):
        """Test updating book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books"""
        response = self.client.put(self.url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookDeleteViewTest(APITestCase):
    """Test Book delete view"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        self.url = reverse('api:book-delete', kwargs={'pk': self.book.pk})
    
    def test_delete_book_authenticated(self):
        """Test deleting book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)


class AuthorViewTest(APITestCase):
    """Test Author views"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        self.list_url = reverse('api:author-list')
        self.detail_url = reverse('api:author-detail', kwargs={'pk': self.author.pk})
    
    def test_get_authors_list(self):
        """Test retrieving authors list"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_author_detail(self):
        """Test retrieving author detail with nested books"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Test Book')
