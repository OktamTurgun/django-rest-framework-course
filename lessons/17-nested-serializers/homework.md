# Homework: Nested Serializers & Relations

## Maqsad

Ushbu vazifada siz **nested serializers** va **serializer relations** bilan amaliy ishlashni o'rganasiz. Library projectimizga yangi modellar qo'shib, ularni API orqali boshqarasiz.

---

## Vazifa 1: Author va Book Modellarini Yaratish


### Topshiriq

1. `books/models.py` faylida **Author** modelini yarating:
   - `name` - CharField (max_length=100)
   - `bio` - TextField
   - `birth_date` - DateField
   - `email` - EmailField (unique=True)

2. `Book` modeliga **author** maydonini qo'shing:
   - `author` - ForeignKey to Author (related_name='books')

3. Migratsiya yarating va qo'llang:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Admin panelda Author va Book'ni ro'yxatdan o'tkazing

### Kutilgan natija

- Author modeli to'g'ri yaratilgan
- Book modelida author bog'lanishi mavjud
- Admin panelda har ikkalasi ko'rinadi

---

## Vazifa 2: Basic Nested Serializer

### Topshiriq

1. `books/serializers.py` da **AuthorSerializer** yarating
2. **BookSerializer**ni yangilang va `author` maydonini nested qiling
3. Har ikkala serializerni test qiling

### Misol kod:

```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date', 'email']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'subtitle', 'author', 'isbn', 'price', 'published_date']
```

### Test

GET `/api/books/1/` so'rovida author ma'lumotlari to'liq ko'rinishi kerak:

```json
{
    "id": 1,
    "title": "Django Guide",
    "subtitle": "Complete Tutorial",
    "author": {
        "id": 1,
        "name": "John Doe",
        "bio": "Django expert",
        "birth_date": "1985-05-15",
        "email": "john@example.com"
    },
    "isbn": "978-1234567890",
    "price": "29.99",
    "published_date": "2024-01-15"
}
```

---

## Vazifa 3: Many-to-Many Relationship

### Topshiriq

1. **Genre** modelini yarating:
   - `name` - CharField (max_length=50, unique=True)
   - `description` - TextField (blank=True)

2. `Book` modeliga **genres** ManyToMany maydonini qo'shing:
```python
genres = models.ManyToManyField(Genre, related_name='books', blank=True)
```

3. **GenreSerializer** yarating

4. **BookSerializer**ni yangilang:
```python
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'subtitle', 'author', 'genres', 'isbn', 'price', 'published_date']
```

### Test

GET `/api/books/1/` so'rovida genres ham ko'rinishi kerak:

```json
{
    "id": 1,
    "title": "Django Guide",
    "author": {...},
    "genres": [
        {"id": 1, "name": "Programming", "description": "Computer programming books"},
        {"id": 2, "name": "Web Development", "description": "Web development tutorials"}
    ],
    "isbn": "978-1234567890",
    "price": "29.99"
}
```

---

## Vazifa 4: Writable Nested Serializer

### Topshiriq

Author yaratish bilan birga uning kitoblarini ham yaratish imkoniyatini qo'shing.

1. **AuthorCreateSerializer** yarating:

```python
class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'subtitle', 'isbn', 'price', 'published_date']

class AuthorCreateSerializer(serializers.ModelSerializer):
    books = BookCreateSerializer(many=True, required=False)
    
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date', 'email', 'books']
    
    def create(self, validated_data):
        books_data = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        
        return author
```

2. **AuthorViewSet** yaratib, `create` actionni qo'shing

### Test

POST `/api/authors/` so'rovi:

```json
{
    "name": "Jane Smith",
    "bio": "Python developer and author",
    "birth_date": "1990-03-20",
    "email": "jane@example.com",
    "books": [
        {
            "title": "Python Basics",
            "subtitle": "Learn Python from scratch",
            "isbn": "978-1111111111",
            "price": "19.99",
            "published_date": "2024-06-01"
        },
        {
            "title": "Advanced Python",
            "subtitle": "Master Python programming",
            "isbn": "978-2222222222",
            "price": "34.99",
            "published_date": "2024-09-15"
        }
    ]
}
```

Javobda author va uning barcha kitoblari yaratilgan bo'lishi kerak.

---

## Bonus Vazifa

### Topshiriq

1. **AuthorDetailSerializer** yarating:
   - Author ma'lumotlari
   - Uning barcha kitoblari
   - Jami kitoblar soni
   - O'rtacha kitob narxi

```python
class AuthorDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    total_books = serializers.SerializerMethodField()
    average_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date', 'email', 'books', 'total_books', 'average_price']
    
    def get_total_books(self, obj):
        return obj.books.count()
    
    def get_average_price(self, obj):
        from django.db.models import Avg
        result = obj.books.aggregate(Avg('price'))
        return result['price__avg']
```

2. Author detail viewda ushbu serializerni ishlating

---

## Topshirish

1. Barcha kodingizni Git'ga commit qiling:
```bash
git add .
git commit -m "feat: add nested serializers and relations"
git push origin lesson-17
```

2. Pull Request yarating:
   - Title: `Lesson 17: Nested Serializers & Relations`
   - Description: Qanday o'zgarishlar kiritganingizni yozing

3. **screenshots** papkasiga quyidagi rasmlarni qo'shing:
   - Admin paneldagi Author va Book ro'yxati
   - Postman'da nested serializer response
   - Many-to-many genres response
   - Writable nested POST so'rovi va natijasi
   - 
---

## Muhim Eslatmalar

- Barcha migratsiyalarni to'g'ri qo'llang
- Admin panelni unutmang
- Har bir serializer uchun test yozing
- Code style'ga e'tibor bering (PEP 8)
- Git commit messagelarini to'g'ri yozing

---

## Yordam Kerak Bo'lsa

- [DRF Relations Docs](https://www.django-rest-framework.org/api-guide/relations/)
- [Nested Serializers Guide](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects)
- `examples` papkasidagi kod misollarni ko'ring

**Omad!**