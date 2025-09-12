from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, register_view
from .views import admin_view, librarian_view, member_view
from .views import add_book, edit_book, delete_book
from .views import dashboard_view, create_content_view, edit_content_view, delete_content_view

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    path('admin/dashboard/', admin_view, name='admin_view'),
    path('librarian/dashboard/', librarian_view, name='librarian_view'),
    path('member/dashboard/', member_view, name='member_view'),
    
    path('books/add/', add_book, name='add_book'),
    path('books/<int:book_id>/edit/', edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', delete_book, name='delete_book'),
    
    path('dashboard/', dashboard_view, name='dashboard'),
    path('content/create/', create_content_view, name='create_content'),
    path('content/<int:content_id>/edit/', edit_content_view, name='edit_content'),
    path('content/<int:content_id>/delete/', delete_content_view, name='delete_content'),
]
