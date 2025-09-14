from django.urls import path
from . import views
from .views import form_example_view

app_name = 'bookshelf'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('form-example/', form_example_view, name='form_example'),
]
