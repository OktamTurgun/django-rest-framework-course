# 17 - Nested Serializers & Relations

## Maqsad

Ushbu darsda biz Django REST Framework'da **nested serializers** va **serializer relations**ni o'rganamiz. Real loyihalarda ko'pincha modellar o'rtasida murakkab bog'liqliklar bo'ladi va ularni API orqali to'g'ri chiqarish muhimdir.

---

## Nested Serializers nima?

**Nested serializer** - bu bir serializerning ichida boshqa serializer ishlatilishi. Bu bog'langan ob'ektlarni bitta API response ichida qaytarish imkonini beradi.

### Misol: Muallif va Kitoblar

```python
# models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    
    def __str__(self):
        return self.title
```

**Oddiy serializer** (nested bo'lmagan):

```python
# serializers.py
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']
```

**Response:**
```json
{
    "id": 1,
    "title": "Django for Beginners",
    "author": 1,  // Faqat ID
    "published_date": "2024-01-15"
}
```

---

**Nested serializer** yordamida:

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'published_date']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'books']
```

**Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "bio": "Django expert",
    "books": [
        {
            "id": 1,
            "title": "Django for Beginners",
            "published_date": "2024-01-15"
        },
        {
            "id": 2,
            "title": "Advanced Django",
            "published_date": "2024-03-20"
        }
    ]
}
```

---

## Serializer Relations

DRF da turli xil relation fieldlari mavjud:

### 1. **PrimaryKeyRelatedField**

Faqat bog'langan ob'ektning ID sini qaytaradi:

```python
class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
```

**Response:**
```json
{
    "id": 1,
    "title": "Django Guide",
    "author": 1
}
```

---

### 2. **StringRelatedField**

`__str__` metodini chaqiradi:

```python
class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
```

**Response:**
```json
{
    "id": 1,
    "title": "Django Guide",
    "author": "John Doe"
}
```

---

### 3. **SlugRelatedField**

Biror bir maydonni qaytaradi:

```python
class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Author.objects.all()
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
```

**Response:**
```json
{
    "id": 1,
    "title": "Django Guide",
    "author": "John Doe"
}
```

---

### 4. **HyperlinkedRelatedField**

Bog'langan ob'ektga URL qaytaradi:

```python
class BookSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail',
        queryset=Author.objects.all()
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
```

**Response:**
```json
{
    "id": 1,
    "title": "Django Guide",
    "author": "http://localhost:8000/api/authors/1/"
}
```

---

## Many-to-Many Relationships

### Misol: Kitob va Janrlar

```python
# models.py
class Genre(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='books')
```

**Serializer:**

```python
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'genres']
```

**Response:**
```json
{
    "id": 1,
    "title": "Django Mastery",
    "genres": [
        {"id": 1, "name": "Programming"},
        {"id": 2, "name": "Web Development"}
    ]
}
```

---

## Writable Nested Serializers

Nested serializerlarni faqat o'qish uchun emas, balki **yozish** uchun ham ishlatish mumkin.

### Misol: Author bilan birga Kitob yaratish

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'published_date']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'books']
    
    def create(self, validated_data):
        books_data = validated_data.pop('books')
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        
        return author
```

**POST request:**
```json
{
    "name": "Jane Smith",
    "bio": "Python developer",
    "books": [
        {
            "title": "Python Basics",
            "published_date": "2024-05-10"
        },
        {
            "title": "Advanced Python",
            "published_date": "2024-08-20"
        }
    ]
}
```

---

## Real Misol: Library Project

Library projectimizda **Author** va **Book** modellarini qo'shamiz va nested serializerlar bilan ishlaymiz.

### Qadamlar:

1. **Models yaratish** (`books/models.py`)
2. **Serializers yozish** (`books/serializers.py`)
3. **Views yaratish** (`books/views.py`)
4. **URLs sozlash** (`books/urls.py`)
5. **Testlash** (Postman yoki Swagger orqali)

---

## Xulosa

- **Nested serializers** - bog'langan ma'lumotlarni bitta responseda qaytarish
- **Relations** - turli xil bog'lanishlarni boshqarish
- **Many-to-Many** - ko'p-ko'p bog'lanishlar
- **Writable nested** - murakkab ma'lumotlarni yaratish va yangilash

---

## Keyingi Dars

18-darsda biz **Filtering & Searching** mavzusini o'rganamiz va API'da ma'lumotlarni saralash va qidirish funksiyalarini qo'shamiz.

---

## Resurslar

- [DRF Serializer Relations](https://www.django-rest-framework.org/api-guide/relations/)
- [Nested Serializers Documentation](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects)