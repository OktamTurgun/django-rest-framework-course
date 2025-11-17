"""
Serializer Relations Example

DRF da turli xil relation fieldlarini qanday ishlatish.
"""

from rest_framework import serializers
from django.db import models

# ==================== MODELS ====================

class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.title


# ==================== 1. PrimaryKeyRelatedField ====================

class BookPKSerializer(serializers.ModelSerializer):
    """Faqat author ID sini qaytaradi va qabul qiladi"""
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


"""
GET Response:
{
    "id": 1,
    "title": "Django Guide",
    "author": 1,  # <-- Faqat ID
    "price": "29.99"
}

POST Request:
{
    "title": "New Book",
    "author": 1,  # <-- ID bilan yaratish
    "price": "19.99"
}

Qachon ishlatish:
- Eng tez va sodda
- Frontend'da author ID mavjud bo'lsa
- Relationship o'zgarishlarida
"""


# ==================== 2. StringRelatedField ====================

class BookStringSerializer(serializers.ModelSerializer):
    """__str__ metodini chaqiradi"""
    author = serializers.StringRelatedField()  # <-- Read-only!
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


"""
GET Response:
{
    "id": 1,
    "title": "Django Guide",
    "author": "John Doe",  # <-- __str__ natijasi
    "price": "29.99"
}

Qachon ishlatish:
- Faqat o'qish uchun
- User-friendly ko'rinish kerak bo'lsa
- Oddiy ma'lumot yetarli bo'lsa

Kamchilik:
- Faqat read-only (yaratish/yangilash yo'q)
"""


# ==================== 3. SlugRelatedField ====================

class BookSlugSerializer(serializers.ModelSerializer):
    """Muayyan maydonni qaytaradi va qabul qiladi"""
    author = serializers.SlugRelatedField(
        slug_field='slug',  # <-- Qaysi maydon
        queryset=Author.objects.all()
    )
    
    # Faqat o'qish uchun:
    author_name = serializers.SlugRelatedField(
        source='author',
        slug_field='name',
        read_only=True
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'price']


"""
GET Response:
{
    "id": 1,
    "title": "Django Guide",
    "author": "john-doe",  # <-- slug maydoni
    "author_name": "John Doe",  # <-- name maydoni
    "price": "29.99"
}

POST Request:
{
    "title": "New Book",
    "author": "john-doe",  # <-- slug bilan yaratish
    "price": "19.99"
}

Qachon ishlatish:
- Unique slug mavjud bo'lsa
- Human-readable identifier kerak bo'lsa
- SEO-friendly URL lar uchun
"""


# ==================== 4. HyperlinkedRelatedField ====================

class BookHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    """URL link qaytaradi"""
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail',  # <-- URL name
        queryset=Author.objects.all()
    )
    
    class Meta:
        model = Book
        fields = ['url', 'title', 'author', 'price']


"""
GET Response:
{
    "url": "http://localhost:8000/api/books/1/",
    "title": "Django Guide",
    "author": "http://localhost:8000/api/authors/1/",  # <-- URL!
    "price": "29.99"
}

POST Request:
{
    "title": "New Book",
    "author": "http://localhost:8000/api/authors/1/",  # <-- URL bilan
    "price": "19.99"
}

Qachon ishlatish:
- RESTful API best practice
- Frontend navigation uchun
- HATEOAS principle
"""


# ==================== 5. CUSTOM FIELD ====================

class AuthorNameField(serializers.RelatedField):
    """Custom relation field"""
    
    def to_representation(self, value):
        """Read uchun: Object -> JSON"""
        return f"{value.name} ({value.email})"
    
    def to_internal_value(self, data):
        """Write uchun: JSON -> Object"""
        try:
            return Author.objects.get(pk=data)
        except Author.DoesNotExist:
            raise serializers.ValidationError('Author not found')


class BookCustomSerializer(serializers.ModelSerializer):
    """Custom field bilan"""
    author = AuthorNameField(queryset=Author.objects.all())
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


"""
GET Response:
{
    "id": 1,
    "title": "Django Guide",
    "author": "John Doe (john@example.com)",  # <-- Custom format!
    "price": "29.99"
}

POST Request:
{
    "title": "New Book",
    "author": 1,  # <-- ID bilan
    "price": "19.99"
}

Qachon ishlatish:
- Maxsus format kerak bo'lsa
- Murakkab logic bor bo'lsa
"""


# ==================== QIYOSLASH ====================

"""
╔════════════════════════╦══════════╦═══════════╦═══════════════════════╗
║ Field Type             ║ Read     ║ Write     ║ Use Case              ║
╠════════════════════════╬══════════╬═══════════╬═══════════════════════╣
║ PrimaryKeyRelated      ║ ID       ║ ID        ║ Eng tez, sodda        ║
║ StringRelated          ║ __str__  ║ ✗         ║ Display only          ║
║ SlugRelated            ║ slug     ║ slug      ║ SEO-friendly          ║
║ HyperlinkedRelated     ║ URL      ║ URL       ║ RESTful, navigation   ║
║ Nested Serializer      ║ Object   ║ Complex   ║ To'liq ma'lumot       ║
║ Custom Field           ║ Custom   ║ Custom    ║ Maxsus logic          ║
╚════════════════════════╩══════════╩═══════════╩═══════════════════════╝
"""


# ==================== MUHIM MASLAHATLAR ====================

"""
1. PERFORMANCE:
   - PrimaryKeyRelatedField eng tez
   - Nested serializer eng sekin
   - select_related() ishlatishni unutmang

2. USE CASE:
   - API list -> PrimaryKey yoki String
   - API detail -> Nested serializer
   - API create/update -> PrimaryKey yoki Slug

3. READ vs WRITE:
   - Read va Write uchun turli field'lar ishlatish mumkin
   - source parametri bilan bitta modelda turli field'lar

4. VALIDATION:
   - queryset parametri validation uchun kerak
   - read_only=True bo'lsa queryset kerak emas
"""


# ==================== REAL MISOL ====================

class BookFlexibleSerializer(serializers.ModelSerializer):
    """Flexible serializer - read va write uchun turli field'lar"""
    
    # Read uchun: Nested serializer (to'liq ma'lumot)
    author_detail = serializers.SerializerMethodField()
    
    # Write uchun: PrimaryKey (tez va sodda)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_detail', 'price']
    
    def get_author_detail(self, obj):
        """Read uchun to'liq author ma'lumotlari"""
        return {
            'id': obj.author.id,
            'name': obj.author.name,
            'email': obj.author.email
        }


"""
GET Response:
{
    "id": 1,
    "title": "Django Guide",
    "author_detail": {        # <-- Read: To'liq ma'lumot
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "price": "29.99"
}

POST Request:
{
    "title": "New Book",
    "author": 1,              # <-- Write: Faqat ID
    "price": "19.99"
}

Bu eng yaxshi amaliyot!
"""