from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters for author and publication year
    list_filter = ('author', 'publication_year')
    
    # Enable search by title and author
    search_fields = ('title', 'author')
    
    # Organize the detail view into fieldsets
    fieldsets = (
        (None, {
            'fields': ('title', 'author')
        }),
        ('Publication Details', {
            'fields': ('publication_year',),
            'classes': ('collapse',)  # This makes the section collapsible
        }),
    )
