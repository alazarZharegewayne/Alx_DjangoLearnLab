from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library  # Added Library import

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library  # This requires the Library import
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
