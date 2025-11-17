"""
Writable Nested Serializers Example

Nested serializerlarni yaratish va yangilash uchun ishlatish.
"""

from rest_framework import serializers
from django.db import models, transaction

# ==================== MODELS ====================

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField()


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField()


# ==================== 1. BASIC WRITABLE NESTED ====================

class BookCreateSerializer(serializers.ModelSerializer):
    """Kitob yaratish uchun serializer"""
    
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'published_date']


class AuthorWithBooksCreateSerializer(serializers.ModelSerializer):
    """Author bilan birga kitoblarni yaratish"""
    books = BookCreateSerializer(many=True)  # <-- read_only=True yo'q!
    
    class Meta:
        model = Author
        fields = ['name', 'email', 'bio', 'books']
    
    def create(self, validated_data):
        """Author va uning kitoblarini yaratish"""
        books_data = validated_data.pop('books')  # <-- Kitoblar ma'lumotlarini ajratib olamiz
        author = Author.objects.create(**validated_data)  # <-- Author yaratamiz
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)  # <-- Har bir kitobni yaratamiz
        
        return author


"""
POST Request:
{
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "Django expert",
    "books": [
        {
            "title": "Django Guide",
            "isbn": "978-1111111111",
            "price": "29.99",
            "published_date": "2024-01-15"
        },
        {
            "title": "Advanced Django",
            "isbn": "978-2222222222",
            "price": "39.99",
            "published_date": "2024-03-20"
        }
    ]
}

Response: Author va 2 ta kitob yaratiladi
"""


# ==================== 2. UPDATE NESTED ====================

class AuthorUpdateSerializer(serializers.ModelSerializer):
    """Author va kitoblarni yangilash"""
    books = BookCreateSerializer(many=True)
    
    class Meta:
        model = Author
        fields = ['name', 'email', 'bio', 'books']
    
    def update(self, instance, validated_data):
        """Author va kitoblarni yangilash"""
        books_data = validated_data.pop('books', None)
        
        # Author ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        
        # Kitoblarni yangilash
        if books_data is not None:
            # Eski kitoblarni o'chirish
            instance.books.all().delete()
            
            # Yangi kitoblarni yaratish
            for book_data in books_data:
                Book.objects.create(author=instance, **book_data)
        
        return instance


"""
PUT /api/authors/1/ Request:
{
    "name": "John Doe Updated",
    "email": "john.new@example.com",
    "bio": "Senior Django expert",
    "books": [
        {
            "title": "Django Mastery",
            "isbn": "978-3333333333",
            "price": "49.99",
            "published_date": "2024-06-01"
        }
    ]
}

Natija:
- Author ma'lumotlari yangilandi
- Eski kitoblar o'chirildi
- Yangi kitob yaratildi
"""


# ==================== 3. TRANSACTION BILAN ====================

class AuthorTransactionSerializer(serializers.ModelSerializer):
    """Transaction bilan xavfsiz yaratish"""
    books = BookCreateSerializer(many=True)
    
    class Meta:
        model = Author
        fields = ['name', 'email', 'bio', 'books']
    
    @transaction.atomic  # <-- Agar xatolik bo'lsa, hamma o'zgarishlar bekor qilinadi
    def create(self, validated_data):
        """Transaction ichida yaratish"""
        books_data = validated_data.pop('books')
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        
        return author


"""
Agar kitob yaratishda xatolik bo'lsa:
- Transaction rollback bo'ladi
- Author ham yaratilmaydi
- Database tutarliliği saqlanadi
"""


# ==================== 4. PARTIAL UPDATE ====================

class BookUpdateSerializer(serializers.ModelSerializer):
    """Kitobni yangilash serializer"""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'price', 'published_date']
        read_only_fields = ['id']


class AuthorPartialUpdateSerializer(serializers.ModelSerializer):
    """Qisman yangilash - mavjud kitoblarni o'zgartirish"""
    books = BookUpdateSerializer(many=True)
    
    class Meta:
        model = Author
        fields = ['name', 'email', 'bio', 'books']
    
    def update(self, instance, validated_data):
        """Qisman yangilash"""
        books_data = validated_data.pop('books', None)
        
        # Author ni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Kitoblarni yangilash (o'chirmasdan)
        if books_data:
            for book_data in books_data:
                book_id = book_data.get('id')
                if book_id:
                    # Mavjud kitobni yangilash
                    Book.objects.filter(id=book_id, author=instance).update(**book_data)
                else:
                    # Yangi kitob yaratish
                    Book.objects.create(author=instance, **book_data)
        
        return instance


"""
PATCH /api/authors/1/ Request:
{
    "books": [
        {
            "id": 1,
            "price": "34.99"  // Faqat narxni yangilash
        },
        {
            "title": "New Book",
            "isbn": "978-4444444444",
            "price": "24.99",
            "published_date": "2024-07-01"
        }
    ]
}

Natija:
- ID=1 kitobning narxi yangilandi
- Yangi kitob qo'shildi
- Boshqa kitoblar o'zgarmadi
"""


# ==================== 5. VALIDATION BILAN ====================

class ValidatedBookSerializer(serializers.ModelSerializer):
    """Validation bilan kitob serializer"""
    
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'published_date']
    
    def validate_isbn(self, value):
        """ISBN validatsiyasi"""
        if len(value) != 13:
            raise serializers.ValidationError("ISBN 13 ta belgidan iborat bo'lishi kerak")
        if not value.startswith('978'):
            raise serializers.ValidationError("ISBN 978 bilan boshlanishi kerak")
        return value
    
    def validate_price(self, value):
        """Narx validatsiyasi"""
        if value <= 0:
            raise serializers.ValidationError("Narx musbat son bo'lishi kerak")
        if value > 1000:
            raise serializers.ValidationError("Narx 1000 dan oshmasligi kerak")
        return value


class AuthorValidatedSerializer(serializers.ModelSerializer):
    """Validation bilan author serializer"""
    books = ValidatedBookSerializer(many=True)
    
    class Meta:
        model = Author
        fields = ['name', 'email', 'bio', 'books']
    
    def validate_books(self, value):
        """Kitoblar ro'yxati validatsiyasi"""
        if len(value) > 10:
            raise serializers.ValidationError("Bir marta 10 tadan ko'p kitob qo'shib bo'lmaydi")
        
        # ISBN takrorlanmasligi kerak
        isbns = [book['isbn'] for book in value]
        if len(isbns) != len(set(isbns)):
            raise serializers.ValidationError("ISBN'lar takrorlanmasligi kerak")
        
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        books_data = validated_data.pop('books')
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        
        return author


"""
POST Request (xato):
{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "bio": "Author",
    "books": [
        {
            "title": "Book 1",
            "isbn": "123",  // <-- Xato: 13 ta belgidan kam
            "price": "-10",  // <-- Xato: manfiy narx
            "published_date": "2024-01-15"
        }
    ]
}

Response (400 Bad Request):
{
    "books": [
        {
            "isbn": ["ISBN 13 ta belgidan iborat bo'lishi kerak"],
            "price": ["Narx musbat son bo'lishi kerak"]
        }
    ]
}
"""


# ==================== 6. EXISTING OBJECT BILAN ====================

class BookLinkSerializer(serializers.Serializer):
    """Mavjud kitobni bog'lash yoki yangi yaratish"""
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=200)
    isbn = serializers.CharField(max_length=13)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    published_date = serializers.DateField()


class AuthorFlexibleSerializer(serializers.ModelSerializer):
    """Mavjud kitoblarni bog'lash yoki yangi yaratish"""
    books = BookLinkSerializer(many=True)
    
    class Meta:
        model = Author
        fields = ['name', 'email', 'bio', 'books']
    
    @transaction.atomic
    def create(self, validated_data):
        books_data = validated_data.pop('books')
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            book_id = book_data.pop('id', None)
            
            if book_id:
                # Mavjud kitobni bog'lash
                try:
                    book = Book.objects.get(id=book_id)
                    book.author = author
                    book.save()
                except Book.DoesNotExist:
                    raise serializers.ValidationError(f"Book with id {book_id} not found")
            else:
                # Yangi kitob yaratish
                Book.objects.create(author=author, **book_data)
        
        return author


"""
POST Request:
{
    "name": "Mike Johnson",
    "email": "mike@example.com",
    "bio": "Tech writer",
    "books": [
        {
            "id": 5  // <-- Mavjud kitobni bog'lash
        },
        {
            "title": "New Book",  // <-- Yangi kitob yaratish
            "isbn": "978-5555555555",
            "price": "27.99",
            "published_date": "2024-08-01"
        }
    ]
}

Natija:
- ID=5 kitobning author'i o'zgartirildi
- Yangi kitob yaratildi
"""


# ==================== VIEWS ====================

from rest_framework import generics


class AuthorCreateView(generics.CreateAPIView):
    """Author va kitoblarni yaratish"""
    queryset = Author.objects.all()
    serializer_class = AuthorValidatedSerializer


class AuthorUpdateView(generics.UpdateAPIView):
    """Author va kitoblarni yangilash"""
    queryset = Author.objects.all()
    serializer_class = AuthorUpdateSerializer


class AuthorPartialUpdateView(generics.UpdateAPIView):
    """Author va kitoblarni qisman yangilash"""
    queryset = Author.objects.all()
    serializer_class = AuthorPartialUpdateSerializer


# ==================== BEST PRACTICES ====================

"""
1. TRANSACTION ISHLATISH:
   - @transaction.atomic decorator
   - Xatolik bo'lsa rollback
   - Database tutarliligi

2. VALIDATION:
   - Har bir nested serializer validate qilinadi
   - validate_<field> metodlari
   - Custom validation logic

3. PERFORMANCE:
   - Bulk create ishlatish (if needed)
   - select_related / prefetch_related
   - Minimal queries

4. ERROR HANDLING:
   - Try/except bloklar
   - ValidationError raise qilish
   - User-friendly error messages

5. UPDATE STRATEGIES:
   - Replace all: eski o'chirish, yangi yaratish
   - Partial update: faqat o'zgarganlarni yangilash
   - Link existing: mavjud objectlarni bog'lash

6. TESTING:
   - Success cases
   - Validation errors
   - Transaction rollback
   - Edge cases
"""


# ==================== SUMMARY ====================

"""
╔═══════════════════════╦═══════════════════════════════════════════╗
║ Operation             ║ Method                                    ║
╠═══════════════════════╬═══════════════════════════════════════════╣
║ Create nested         ║ Override create(), pop nested data        ║
║ Update nested         ║ Override update(), handle nested data     ║
║ Delete old, add new   ║ instance.books.all().delete() + create    ║
║ Partial update        ║ Update existing by ID, create new ones    ║
║ Link existing         ║ Get by ID, update foreign key            ║
║ Safe operations       ║ @transaction.atomic                       ║
║ Validation            ║ validate_<field>, validate()              ║
╚═══════════════════════╩═══════════════════════════════════════════╝

Eng muhim:
1. Transaction ishlatish (rollback uchun)
2. Validation qo'shish (xavfsizlik uchun)
3. Performance optimize qilish (N+1 yo'q)
4. Clear error messages (debug uchun)
"""