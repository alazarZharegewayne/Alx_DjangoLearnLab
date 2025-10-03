from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters import rest_framework
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    """
    BookListView provides a read-only endpoint that returns a list of all Book instances.
    Enhanced with comprehensive filtering, searching, and ordering capabilities.
    
    Features:
    - Filtering: Filter by title, author name, and publication year ranges
    - Searching: Search across title and author name fields
    - Ordering: Order by any book field, default by publication year (descending)
    
    Permission: IsAuthenticatedOrReadOnly - Read access for all, write for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filtering configuration
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    
    # Search configuration - search across title and author name
    search_fields = ['title', 'author__name']
    
    # Ordering configuration - default ordering and available fields
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['-publication_year']  # Default: newest books first


class BookDetailView(generics.RetrieveAPIView):
    """
    BookDetailView provides a read-only endpoint to retrieve a single Book instance by ID.
    Permission: IsAuthenticatedOrReadOnly - Read access for all, write for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    BookCreateView provides an endpoint to create new Book instances.
    Permission: IsAuthenticated - Only authenticated users can create new books.
    Includes custom validation through the BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        Can be extended to add additional logic before saving.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    BookUpdateView provides an endpoint to update existing Book instances.
    Permission: IsAuthenticated - Only authenticated users can update books.
    Includes full validation through the BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom method called when updating a book instance.
        Can be extended to add additional logic before saving.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    BookDeleteView provides an endpoint to delete Book instances.
    Permission: IsAuthenticated - Only authenticated users can delete books.
    Returns 204 No Content on successful deletion.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        """
        Custom method called when deleting a book instance.
        Can be extended to add additional logic before deletion.
        """
        instance.delete()


class AuthorListView(generics.ListAPIView):
    """
    AuthorListView provides a read-only endpoint that returns a list of all Author instances.
    Includes nested book data through the AuthorSerializer.
    Permission: IsAuthenticatedOrReadOnly - Read access for all, write for authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    AuthorDetailView provides a read-only endpoint to retrieve a single Author instance by ID.
    Includes nested book data through the AuthorSerializer.
    Permission: IsAuthenticatedOrReadOnly - Read access for all, write for authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
