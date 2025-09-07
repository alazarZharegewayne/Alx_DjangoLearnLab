from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books  # from .views import list_books
from .views import LibraryDetailView
from .views import register_view  # views.register
from .views import admin_view, librarian_view, member_view  # Add role-based views
from .views import add_book, edit_book, delete_book  # ADD THESE NEW IMPORTS

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),  # views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # LoginView.as_view(template_name=
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # LogoutView.as_view(template_>
    
    # Role-based URLs
    path('admin/dashboard/', admin_view, name='admin_view'),
    path('librarian/dashboard/', librarian_view, name='librarian_view'),
    path('member/dashboard/', member_view, name='member_view'),
    
    # NEW PERMISSION-BASED BOOK MANAGEMENT URLS
    path('books/add/', add_book, name='add_book'),
    path('books/<int:book_id>/edit/', edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', delete_book, name='delete_book'),
]
