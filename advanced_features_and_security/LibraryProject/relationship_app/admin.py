from django.contrib import admin
from .models import Author, Book, Library, Librarian

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    filter_horizontal = ('books',)  # Better widget for ManyToMany fields

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
