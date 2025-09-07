from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books  # from .views import list_books
from .views import LibraryDetailView
from .views import register_view  # views.register

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),  # views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # LoginView.as_view(template_name=
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # LogoutView.as_view(template_name=
]
