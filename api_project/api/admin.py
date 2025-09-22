from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['author']
    search_fields = ['title', 'author']

# Alternative method
# admin.site.register(Book, BookAdmin)
