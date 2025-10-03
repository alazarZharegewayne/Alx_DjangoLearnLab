from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization and deserialization of Book instances.
    Includes custom validation for publication_year to ensure it's not in the future.
    This serializer converts Book model instances to JSON and validates incoming data.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']

    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication year is not in the future.
        This method is automatically called by DRF when validating publication_year data.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid year (1000 or later)."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization and deserialization of Author instances.
    Includes nested BookSerializer to dynamically serialize related books.
    The 'books' field uses BookSerializer to create a nested relationship where
    each author's response includes a list of their associated books.
    This demonstrates handling nested objects in DRF serializers.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id', 'books']
