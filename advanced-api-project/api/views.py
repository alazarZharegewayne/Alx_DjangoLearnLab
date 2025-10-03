from rest_framework import generics, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    BookListView provides a read-only endpoint that returns a list of all Book instances.
    This view uses DRF's ListAPIView which handles GET requests automatically.
    Permission: AllowAny - Anyone can view the book list without authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    BookDetailView provides a read-only endpoint to retrieve a single Book instance by ID.
    This view uses DRF's RetrieveAPIView which handles GET requests for single objects.
    Permission: AllowAny - Anyone can view book details without authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    BookCreateView provides an endpoint to create new Book instances.
    This view uses DRF's CreateAPIView which handles POST requests.
    Permission: IsAuthenticated - Only authenticated users can create new books.
    Includes custom validation through the BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        Can be extended to add additional logic before saving.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    BookUpdateView provides an endpoint to update existing Book instances.
    This view uses DRF's UpdateAPIView which handles PUT and PATCH requests.
    Permission: IsAuthenticated - Only authenticated users can update books.
    Includes full validation through the BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom method called when updating a book instance.
        Can be extended to add additional logic before saving.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    BookDeleteView provides an endpoint to delete Book instances.
    This view uses DRF's DestroyAPIView which handles DELETE requests.
    Permission: IsAuthenticated - Only authenticated users can delete books.
    Returns 204 No Content on successful deletion.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    Permission: AllowAny - Anyone can view the author list without authentication.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    AuthorDetailView provides a read-only endpoint to retrieve a single Author instance by ID.
    Includes nested book data through the AuthorSerializer.
    Permission: AllowAny - Anyone can view author details without authentication.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
