import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    BookFilter provides comprehensive filtering options for the Book model.
    Allows users to filter books by title, author name, and publication year ranges.
    """
    title = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        help_text="Filter books by title (case-insensitive contains)"
    )
    
    author_name = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains',
        help_text="Filter books by author name (case-insensitive contains)"
    )
    
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text="Filter books by exact publication year"
    )
    
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        help_text="Filter books published in or after this year"
    )
    
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        help_text="Filter books published in or before this year"
    )

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'publication_year']
