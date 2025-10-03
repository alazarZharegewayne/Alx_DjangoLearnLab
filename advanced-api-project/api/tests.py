from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer
from datetime import datetime

class BaseTestCase(APITestCase):
    """
    Base test case with common setup for all test classes.
    Provides test data and helper methods for API testing.
    """
    
    def setUp(self):
        """Set up test data and client for all test cases."""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Jane Austen")
        self.author3 = Author.objects.create(name="J.K. Rowling")
        
        # Create test books
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
        self.book4 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author3
        )
        
        # Initialize API client
        self.client = APIClient()
        
        # URLs for API endpoints
        self.book_list_url = reverse('api:book-list')
        self.book_create_url = reverse('api:book-create')
        self.author_list_url = reverse('api:author-list')


class BookListViewTests(BaseTestCase):
    """
    Test cases for BookListView including listing, filtering, searching, and ordering.
    """
    
    def test_get_all_books_unauthenticated(self):
        """Test that unauthenticated users can retrieve all books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_filter_books_by_author_name(self):
        """Test filtering books by author name."""
        response = self.client.get(self.book_list_url, {'author_name': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify only Orwell's books are returned
        books_data = response.data
        for book in books_data:
            self.assertIn('Orwell', book['author'])
    
    def test_filter_books_by_publication_year_range(self):
        """Test filtering books by publication year range."""
        response = self.client.get(
            self.book_list_url, 
            {'publication_year_min': 1900, 'publication_year_max': 1950}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only Orwell's books
        
        # Verify publication years are within range
        books_data = response.data
        for book in books_data:
            self.assertGreaterEqual(book['publication_year'], 1900)
            self.assertLessEqual(book['publication_year'], 1950)
    
    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(self.book_list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter and the Philosopher's Stone")
    
    def test_search_books_by_author_name(self):
        """Test searching books by author name."""
        response = self.client.get(self.book_list_url, {'search': 'Austen'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author2.name)
    
    def test_order_books_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [book['title'] for book in response.data]
        expected_titles = sorted([self.book1.title, self.book2.title, self.book3.title, self.book4.title])
        self.assertEqual(titles, expected_titles)
    
    def test_order_books_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        publication_years = [book['publication_year'] for book in response.data]
        expected_years = sorted(publication_years, reverse=True)
        self.assertEqual(publication_years, expected_years)
    
    def test_combined_filter_search_ordering(self):
        """Test combining filtering, searching, and ordering."""
        response = self.client.get(
            self.book_list_url, 
            {
                'author_name': 'Orwell',
                'ordering': 'publication_year'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify ordering by publication year (ascending)
        books_data = response.data
        self.assertEqual(books_data[0]['title'], "Animal Farm")  # 1945
        self.assertEqual(books_data[1]['title'], "1984")  # 1949


class BookDetailViewTests(BaseTestCase):
    """
    Test cases for BookDetailView - retrieving single book instances.
    """
    
    def test_get_single_book_unauthenticated(self):
        """Test that unauthenticated users can retrieve a single book."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.book1.author.name)
    
    def test_get_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        url = reverse('api:book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTests(BaseTestCase):
    """
    Test cases for BookCreateView - creating new book instances.
    """
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books."""
        self.client.force_authenticate(user=self.user)
        
        new_book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, new_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)  # Original 4 + new one
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(response.data['publication_year'], 2023)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        new_book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, new_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4)  # No new book created
    
    def test_create_book_with_future_publication_year(self):
        """Test validation for future publication year."""
        self.client.force_authenticate(user=self.user)
        
        future_year = datetime.now().year + 1
        new_book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, new_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_with_invalid_publication_year(self):
        """Test validation for invalid publication year."""
        self.client.force_authenticate(user=self.user)
        
        new_book_data = {
            'title': 'Ancient Book',
            'publication_year': 500,  # Too early
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, new_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)


class BookUpdateViewTests(BaseTestCase):
    """
    Test cases for BookUpdateView - updating existing book instances.
    """
    
    def test_update_book_authenticated(self):
        """Test that authenticated users can update books."""
        self.client.force_authenticate(user=self.user)
        
        update_url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        updated_data = {
            'title': 'Nineteen Eighty-Four',
            'publication_year': 1949,
            'author': self.author1.id
        }
        
        response = self.client.put(update_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database and verify changes
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Nineteen Eighty-Four')
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        update_url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        updated_data = {
            'title': 'Nineteen Eighty-Four',
            'publication_year': 1949,
            'author': self.author1.id
        }
        
        response = self.client.put(update_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify book was not updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, '1984')  # Original title
    
    def test_partial_update_book(self):
        """Test partial update of book using PATCH."""
        self.client.force_authenticate(user=self.user)
        
        update_url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        partial_data = {
            'title': 'Nineteen Eighty-Four'
        }
        
        response = self.client.patch(update_url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database and verify changes
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Nineteen Eighty-Four')
        self.assertEqual(self.book1.publication_year, 1949)  # Unchanged


class BookDeleteViewTests(BaseTestCase):
    """
    Test cases for BookDeleteView - deleting book instances.
    """
    
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books."""
        self.client.force_authenticate(user=self.user)
        
        delete_url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        initial_count = Book.objects.count()
        
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        
        # Verify book no longer exists
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book1.pk)
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        delete_url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        initial_count = Book.objects.count()
        
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), initial_count)  # Count unchanged


class AuthorViewTests(BaseTestCase):
    """
    Test cases for Author views - listing and retrieving authors with nested books.
    """
    
    def test_get_all_authors(self):
        """Test retrieving all authors with nested book data."""
        response = self.client.get(self.author_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # 3 authors
        
        # Verify nested book data for Orwell (should have 2 books)
        orwell_data = next(author for author in response.data if author['name'] == 'George Orwell')
        self.assertEqual(len(orwell_data['books']), 2)
    
    def test_get_single_author_with_books(self):
        """Test retrieving a single author with nested book data."""
        url = reverse('api:author-detail', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'George Orwell')
        self.assertEqual(len(response.data['books']), 2)
        
        # Verify book titles in nested data
        book_titles = [book['title'] for book in response.data['books']]
        self.assertIn('1984', book_titles)
        self.assertIn('Animal Farm', book_titles)


class PermissionTests(BaseTestCase):
    """
    Test cases specifically for permission enforcement.
    """
    
    def test_read_only_permissions_for_unauthenticated_users(self):
        """Test that unauthenticated users have read-only access."""
        # Should be able to read
        list_response = self.client.get(self.book_list_url)
        detail_response = self.client.get(
            reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        )
        
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        
        # Should NOT be able to write
        create_response = self.client.post(self.book_create_url, {})
        update_response = self.client.put(
            reverse('api:book-update', kwargs={'pk': self.book1.pk}), {}
        )
        delete_response = self.client.delete(
            reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        )
        
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_users_have_write_access(self):
        """Test that authenticated users have write access."""
        self.client.force_authenticate(user=self.user)
        
        # Should be able to create
        new_book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        create_response = self.client.post(self.book_create_url, new_book_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        # Should be able to update
        update_data = {'title': 'Updated Title', 'publication_year': 2023, 'author': self.author1.id}
        update_response = self.client.put(
            reverse('api:book-update', kwargs={'pk': self.book1.pk}), 
            update_data, 
            format='json'
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Should be able to delete
        delete_response = self.client.delete(
            reverse('api:book-delete', kwargs={'pk': self.book2.pk})
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
