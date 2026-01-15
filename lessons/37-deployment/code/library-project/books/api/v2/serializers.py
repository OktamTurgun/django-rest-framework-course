"""
V2 API Serializers
Enhanced with nested objects and computed fields
"""
from rest_framework import serializers
from books.models import Book, Author, Genre, Review
from datetime import date
from django.db.models import Avg


class AuthorSerializerV2(serializers.ModelSerializer):
    """V2: Enhanced author serializer with book count"""
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'email',
            'bio',
            'book_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_book_count(self, obj):
        """Count books by this author"""
        return obj.books.count()


class GenreSerializerV2(serializers.ModelSerializer):
    """V2: Genre serializer"""
    
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookListSerializerV2(serializers.ModelSerializer):
    """V2: Optimized list serializer"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    genre_names = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author_name',
            'genre_names',
            'price',
            'published_date',
            'average_rating',
            'review_count'
        ]
    
    def get_genre_names(self, obj):
        """Get list of genre names"""
        return [genre.name for genre in obj.genres.all()]
    
    def get_average_rating(self, obj):
        """Calculate average rating from reviews"""
        result = obj.reviews.aggregate(avg_rating=Avg('rating'))
        avg = result['avg_rating']
        return round(avg, 2) if avg else 0
    
    def get_review_count(self, obj):
        """Count reviews for this book"""
        return obj.reviews.count()


class BookDetailSerializerV2(serializers.ModelSerializer):
    """V2: Complete book detail serializer with nested objects"""
    author = AuthorSerializerV2(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    genres = GenreSerializerV2(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        source='genres',
        write_only=True
    )
    age_years = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'author_id',
            'genres',
            'genre_ids',
            'description',
            'isbn_number',
            'price',
            'pages',
            'language',
            'published_date',
            'average_rating',
            'review_count',
            'age_years',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_age_years(self, obj):
        """Calculate book age in years"""
        if obj.published_date:
            delta = date.today() - obj.published_date
            return delta.days // 365
        return None
    
    def get_average_rating(self, obj):
        """Calculate average rating from reviews"""
        result = obj.reviews.aggregate(avg_rating=Avg('rating'))
        avg = result['avg_rating']
        return round(avg, 2) if avg else 0
    
    def get_review_count(self, obj):
        """Count reviews for this book"""
        return obj.reviews.count()
    
class ReviewSerializerV2(serializers.ModelSerializer):
    """V2: Review serializer"""
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'book',
            'book_title',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']