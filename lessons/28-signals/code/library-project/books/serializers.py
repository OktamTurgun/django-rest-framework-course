from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Author, Genre, BookLog, BorrowHistory, Review
from accounts.models import Profile


class AuthorSerializer(serializers.ModelSerializer):
    """Author serializer with statistics"""
    
    class Meta:
        model = Author
        fields = [
            'id', 'name', 'bio', 'birth_date', 'email',
            'total_books', 'available_books',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['total_books', 'available_books', 'created_at', 'updated_at']


class GenreSerializer(serializers.ModelSerializer):
    """Genre serializer"""
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class BookSerializer(serializers.ModelSerializer):
    """Book serializer with all fields"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    genres_list = GenreSerializer(source='genres', many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn_number', 'description',
            'pages', 'language', 'price', 'stock',
            'is_available', 'published_date',
            'author', 'author_name',
            'genres', 'genres_list',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile  # Changed from UserProfile to Profile
        fields = [
            'id', 'user', 'username', 'email',
            'bio', 'location', 'birth_date', 'phone',  # Original + new
            'is_premium', 'membership_type',
            'avatar', 'avatar_thumbnail',
            'books_borrowed', 'books_returned',
            'subscribed_to_notifications',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'user', 'avatar_thumbnail',
            'books_borrowed', 'books_returned',
            'created_at', 'updated_at'
        ]


class BookLogSerializer(serializers.ModelSerializer):
    """Book log serializer"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = BookLog
        fields = [
            'id', 'book_title', 'book_id', 'action',
            'user', 'user_username', 'timestamp', 'details'
        ]
        read_only_fields = ['timestamp']


class BorrowHistorySerializer(serializers.ModelSerializer):
    """Borrow history serializer"""
    book_title = serializers.CharField(source='book.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = BorrowHistory
        fields = [
            'id', 'book', 'book_title', 'user', 'username',
            'borrowed_at', 'due_date', 'returned_at', 'is_overdue'
        ]
        read_only_fields = ['borrowed_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer"""
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


class BulkImportBookSerializer(serializers.Serializer):
    """Bulk import books serializer"""
    books = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )
    
    def validate_books(self, value):
        """Validate books data"""
        required_fields = ['title', 'author', 'isbn_number', 'price']
        
        for idx, book_data in enumerate(value):
            missing_fields = [field for field in required_fields if field not in book_data]
            if missing_fields:
                raise serializers.ValidationError(
                    f"Book #{idx + 1}: Missing required fields: {', '.join(missing_fields)}"
                )
        
        return value