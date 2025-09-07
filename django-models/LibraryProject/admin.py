from django.contrib import admin
from .models import UserProfile, Author, Book, Library, Librarian

admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
