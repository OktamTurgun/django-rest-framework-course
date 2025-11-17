"""
Basic Nested Serializer Example

Bu misol ForeignKey relationship bilan basic nested serializerni ko'rsatadi.
Author va Book modellari o'rtasidagi bog'lanish.
"""

from rest_framework import serializers
from django.db import models

# ==================== MODELS ====================

class Author(models.Model):
    """Muallif modeli"""
    name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    
    class Meta:
        db_table = 'authors'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Kitob modeli"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField()
    
    class Meta:
        db_table = 'books'
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


# ==================== SERIALIZERS ====================

# 1. ODDIY SERIALIZER (nested bo'lmagan)
class BookSimpleSerializer(serializers.ModelSerializer):
    """Oddiy serializer - faqat author ID ni qaytaradi"""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


"""
Response:
{
    "id": 1,
    "title": "Django Guide",
    "author": 1,  # <-- Faqat ID
    "price": "29.99"
}
"""


# 2. NESTED SERIALIZER (read-only)
class AuthorSerializer(serializers.ModelSerializer):
    """Author serializer"""
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio']


class BookNestedSerializer(serializers.ModelSerializer):
    """Nested serializer - author ma'lumotlarini to'liq qaytaradi"""
    author = AuthorSerializer(read_only=True)  # <-- Nested!
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'subtitle', 'author', 'isbn', 'price', 'published_date']


"""
Response:
{
    "id": 1,
    "title": "Django Guide",
    "subtitle": "Complete Tutorial",
    "author": {              # <-- To'liq author ma'lumotlari!
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "bio": "Django expert"
    },
    "isbn": "978-1234567890",
    "price": "29.99",
    "published_date": "2024-01-15"
}
"""


# 3. REVERSE NESTED (Author ichida Books)
class AuthorWithBooksSerializer(serializers.ModelSerializer):
    """Author serializer with nested books"""
    books = BookSimpleSerializer(many=True, read_only=True)  # <-- related_name='books'
    total_books = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'books', 'total_books']
    
    def get_total_books(self, obj):
        """Jami kitoblar sonini hisoblash"""
        return obj.books.count()


"""
Response:
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "Django expert",
    "books": [
        {
            "id": 1,
            "title": "Django Guide",
            "author": 1,
            "price": "29.99"
        },
        {
            "id": 2,
            "title": "Advanced Django",
            "author": 1,
            "price": "39.99"
        }
    ],
    "total_books": 2
}
"""


# ==================== VIEWS ====================

from rest_framework import generics
from rest_framework.permissions import AllowAny


class BookListView(generics.ListCreateAPIView):
    """Kitoblar ro'yxati - nested serializer bilan"""
    queryset = Book.objects.all()
    serializer_class = BookNestedSerializer
    permission_classes = [AllowAny]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Kitob detali - nested serializer bilan"""
    queryset = Book.objects.all()
    serializer_class = BookNestedSerializer
    permission_classes = [AllowAny]


class AuthorListView(generics.ListAPIView):
    """Mualliflar ro'yxati - barcha kitoblari bilan"""
    queryset = Author.objects.all()
    serializer_class = AuthorWithBooksSerializer
    permission_classes = [AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """Muallif detali - barcha kitoblari bilan"""
    queryset = Author.objects.all()
    serializer_class = AuthorWithBooksSerializer
    permission_classes = [AllowAny]


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]


# ==================== USAGE ====================

"""
1. Kitoblar ro'yxatini olish (author ma'lumotlari bilan):
   GET /api/books/

2. Bitta kitobni olish (author ma'lumotlari bilan):
   GET /api/books/1/

3. Mualliflar ro'yxatini olish (barcha kitoblari bilan):
   GET /api/authors/

4. Bitta muallifni olish (barcha kitoblari bilan):
   GET /api/authors/1/
"""


# ==================== MUHIM ESLATMALAR ====================

"""
1. READ-ONLY:
   - Nested serializer default ravishda read-only
   - Yaratish/yangilashda ishlatish uchun alohida kod kerak

2. PERFORMANCE:
   - N+1 query problem bo'lishi mumkin
   - select_related() va prefetch_related() ishlatish kerak

3. CIRCULAR IMPORT:
   - Ikki model bir-birini nested qilsa, circular import muammosi
   - SerializerMethodField yoki lazy import ishlatish kerak
"""