from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books
from .views import LibraryDetailView
from .views import register_view
from .views import admin_view, librarian_view, member_view
from .views import add_book, edit_book, delete_book  # ADD THESE IMPORTS

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Role-based URLs
    path('admin/dashboard/', admin_view, name='admin_view'),
    path('librarian/dashboard/', librarian_view, name='librarian_view'),
    path('member/dashboard/', member_view, name='member_view'),
    
    # ADD THESE PERMISSION-BASED BOOK MANAGEMENT URLS
    path('books/add/', add_book, name='add_book'),
    path('books/<int:book_id>/edit/', edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', delete_book, name='delete_book'),
]
