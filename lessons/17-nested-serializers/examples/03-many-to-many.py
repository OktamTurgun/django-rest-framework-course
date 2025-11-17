"""
Many-to-Many Relationships Example

Kitob va Janrlar o'rtasidagi ko'p-ko'p bog'lanish.
"""

from rest_framework import serializers
from django.db import models

# ==================== MODELS ====================

class Genre(models.Model):
    """Janr modeli"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Author(models.Model):
    """Muallif modeli"""
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Kitob modeli - ManyToMany genres bilan"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField()
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


# ==================== 1. BASIC MANY-TO-MANY ====================

class GenreSerializer(serializers.ModelSerializer):
    """Genre serializer"""
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class BookWithGenresSerializer(serializers.ModelSerializer):
    """Kitob serializer - nested genres bilan"""
    genres = GenreSerializer(many=True, read_only=True)  # <-- many=True!
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genres', 'price', 'published_date']


"""
GET Response:
{
    "id": 1,
    "title": "Django Mastery",
    "author": 1,
    "genres": [                    # <-- Array!
        {
            "id": 1,
            "name": "Programming",
            "description": "Computer programming books"
        },
        {
            "id": 2,
            "name": "Web Development",
            "description": "Web development tutorials"
        }
    ],
    "price": "34.99",
    "published_date": "2024-01-15"
}
"""


# ==================== 2. WRITABLE MANY-TO-MANY (IDs) ====================

class BookCreateSerializer(serializers.ModelSerializer):
    """Kitob yaratish - genre IDs bilan"""
    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,                        # <-- many=True!
        queryset=Genre.objects.all(),
        source='genres',                  # <-- 'genres' maydoniga bog'lanadi
        write_only=True
    )
    
    # Read uchun nested serializer
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre_ids', 'genres', 'price', 'published_date']


"""
POST Request:
{
    "title": "Advanced Python",
    "author": 1,
    "genre_ids": [1, 2, 3],        # <-- Genre IDs array
    "price": "29.99",
    "published_date": "2024-06-01"
}

GET Response:
{
    "id": 2,
    "title": "Advanced Python",
    "author": 1,
    "genres": [                    # <-- To'liq ma'lumotlar
        {"id": 1, "name": "Programming", ...},
        {"id": 2, "name": "Web Development", ...},
        {"id": 3, "name": "Backend", ...}
    ],
    "price": "29.99",
    "published_date": "2024-06-01"
}
"""


# ==================== 3. REVERSE MANY-TO-MANY ====================

class GenreWithBooksSerializer(serializers.ModelSerializer):
    """Genre serializer - barcha kitoblari bilan"""
    books = serializers.SerializerMethodField()
    total_books = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'books', 'total_books']
    
    def get_books(self, obj):
        """Ushbu janrdagi barcha kitoblar"""
        books = obj.books.all()[:5]  # Faqat 5 ta
        return [{
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'price': str(book.price)
        } for book in books]


"""
GET /api/genres/1/ Response:
{
    "id": 1,
    "name": "Programming",
    "description": "Computer programming books",
    "books": [
        {
            "id": 1,
            "title": "Django Mastery",
            "author": "John Doe",
            "price": "34.99"
        },
        {
            "id": 2,
            "title": "Python Guide",
            "author": "Jane Smith",
            "price": "29.99"
        }
    ],
    "total_books": 15
}
"""


# ==================== 4. THROUGH MODEL (Qo'shimcha ma'lumot bilan) ====================

class BookGenre(models.Model):
    """Through model - qo'shimcha ma'lumotlar bilan"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)  # <-- Asosiy janr
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['book', 'genre']


# Model o'zgartirish:
class BookWithThroughModel(models.Model):
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(
        Genre, 
        through='BookGenre',  # <-- Through model
        related_name='books_through'
    )


class BookGenreSerializer(serializers.ModelSerializer):
    """Through model serializer"""
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    
    class Meta:
        model = BookGenre
        fields = ['genre', 'genre_name', 'is_primary', 'added_date']


class BookWithThroughSerializer(serializers.ModelSerializer):
    """Kitob serializer - through model bilan"""
    book_genres = BookGenreSerializer(
        source='bookgenre_set',  # <-- Through modelga murojaat
        many=True,
        read_only=True
    )
    
    class Meta:
        model = BookWithThroughModel
        fields = ['id', 'title', 'book_genres']


"""
GET Response:
{
    "id": 1,
    "title": "Django Mastery",
    "book_genres": [
        {
            "genre": 1,
            "genre_name": "Programming",
            "is_primary": true,          # <-- Qo'shimcha ma'lumot!
            "added_date": "2024-01-15T10:30:00Z"
        },
        {
            "genre": 2,
            "genre_name": "Web Development",
            "is_primary": false,
            "added_date": "2024-01-15T10:30:00Z"
        }
    ]
}
"""


# ==================== 5. WRITABLE THROUGH MODEL ====================

class BookGenreCreateSerializer(serializers.Serializer):
    """Through model uchun yaratish serializer"""
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    is_primary = serializers.BooleanField(default=False)


class BookCreateWithThroughSerializer(serializers.ModelSerializer):
    """Kitob yaratish - through model bilan"""
    genres_data = BookGenreCreateSerializer(many=True, write_only=True)
    book_genres = BookGenreSerializer(source='bookgenre_set', many=True, read_only=True)
    
    class Meta:
        model = BookWithThroughModel
        fields = ['id', 'title', 'genres_data', 'book_genres']
    
    def create(self, validated_data):
        """Through model bilan kitob yaratish"""
        genres_data = validated_data.pop('genres_data')
        book = BookWithThroughModel.objects.create(**validated_data)
        
        for genre_data in genres_data:
            BookGenre.objects.create(
                book=book,
                genre=genre_data['genre'],
                is_primary=genre_data.get('is_primary', False)
            )
        
        return book


"""
POST Request:
{
    "title": "Advanced Django",
    "genres_data": [
        {
            "genre": 1,
            "is_primary": true       # <-- Qo'shimcha ma'lumot
        },
        {
            "genre": 2,
            "is_primary": false
        }
    ]
}
"""


# ==================== VIEWS ====================

from rest_framework import generics, status
from rest_framework.response import Response


class BookListCreateView(generics.ListCreateAPIView):
    """Kitoblar ro'yxati va yaratish"""
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookWithGenresSerializer


class GenreListView(generics.ListAPIView):
    """Janrlar ro'yxati - kitoblari bilan"""
    queryset = Genre.objects.all()
    serializer_class = GenreWithBooksSerializer


# ==================== PERFORMANCE OPTIMIZATION ====================

class OptimizedBookListView(generics.ListAPIView):
    """Optimized queryset - N+1 problem yo'q"""
    serializer_class = BookWithGenresSerializer
    
    def get_queryset(self):
        return Book.objects.prefetch_related('genres')  # <-- Prefetch!


"""
Muhim: 
- prefetch_related() - ManyToMany uchun
- select_related() - ForeignKey uchun

prefetch_related('genres') ishlatmasangiz:
- 1 query kitoblar uchun
- N queries har bir kitobning janrlari uchun
- Jami: N+1 queries (SEKIN!)

prefetch_related('genres') bilan:
- 1 query kitoblar uchun
- 1 query barcha janrlar uchun
- Jami: 2 queries (TEZ!)
"""


# ==================== FILTERING ====================

class GenreFilterView(generics.ListAPIView):
    """Janr bo'yicha kitoblarni filtrlash"""
    serializer_class = BookWithGenresSerializer
    
    def get_queryset(self):
        genre_name = self.request.query_params.get('genre', None)
        if genre_name:
            return Book.objects.filter(genres__name__icontains=genre_name)
        return Book.objects.all()


"""
GET /api/books/?genre=programming

Response: Programming janrida kitoblar
"""


# ==================== SUMMARY ====================

"""
╔════════════════════════╦════════════════════════════════════════════╗
║ Scenario               ║ Best Approach                              ║
╠════════════════════════╬════════════════════════════════════════════╣
║ Read only              ║ Nested serializer (many=True)              ║
║ Create/Update with IDs ║ PrimaryKeyRelatedField (many=True)         ║
║ Extra data needed      ║ Through model                              ║
║ Performance            ║ prefetch_related()                         ║
║ Reverse relation       ║ related_name with SerializerMethodField   ║
╚════════════════════════╩════════════════════════════════════════════╝

Muhim qoidalar:
1. Read uchun: nested serializer
2. Write uchun: PrimaryKeyRelatedField
3. Through model: qo'shimcha ma'lumotlar uchun
4. prefetch_related(): har doim ishlating!
"""