"""
V1 API Serializers
Author as string format (legacy)
"""
from rest_framework import serializers
from books.models import Book, Author, Genre


class AuthorSerializerV1(serializers.ModelSerializer):
    """V1: Simple author serializer"""
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']


class BookSerializerV1(serializers.ModelSerializer):
    """
    V1 Book Serializer
    - Author as string (legacy format)
    - Simple field structure
    """
    author = serializers.CharField(source='author.name', read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',  # String format
            'author_id',
            'price',
            'published_date',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class BookListSerializerV1(serializers.ModelSerializer):
    """V1: Minimal book list serializer"""
    author = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']