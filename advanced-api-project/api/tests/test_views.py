from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Author, Book


class BookAPITests(APITestCase):
    """Test cases for Book API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        self.client = APIClient()
    
    def test_get_books_list(self):
        """Test retrieving list of books"""
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_book_detail(self):
        """Test retrieving single book detail"""
        url = reverse('api:book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_create_book_authenticated(self):
        """Test creating book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        url = reverse('api:book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """Test updating book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Updated Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_book_authenticated(self):
        """Test deleting book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AuthorAPITests(APITestCase):
    """Test cases for Author API endpoints"""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
    
    def test_get_authors_list(self):
        """Test retrieving list of authors"""
        url = reverse('api:author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_author_detail(self):
        """Test retrieving single author detail"""
        url = reverse('api:author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')


class FilterSearchOrderTests(APITestCase):
    """Test cases for filtering, searching, and ordering"""
    
    def setUp(self):
        self.author1 = Author.objects.create(name='George Orwell')
        self.author2 = Author.objects.create(name='Jane Austen')
        
        Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author1
        )
        Book.objects.create(
            title='Animal Farm', 
            publication_year=1945,
            author=self.author1
        )
        Book.objects.create(
            title='Pride and Prejudice',
            publication_year=1813,
            author=self.author2
        )
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author_name': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_books(self):
        """Test searching books"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': '1984'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_order_books(self):
        """Test ordering books"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], '1984')
