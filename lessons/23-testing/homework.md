# 📝 Lesson 23: Unit Testing - Uy Vazifasi

## 🎯 Maqsad

Ushbu uy vazifasida siz Library Project uchun **to'liq test coverage** yozasiz. Barcha model, view, serializer va business logic'larni test qilishni o'rganasiz.

## 📋 Vazifalar

### ✅ Task 1: Model Tests (test_models.py)

`books/tests/test_models.py` faylida quyidagi testlarni yozing:

#### 1.1. Book Model Tests
- [ ] `test_book_creation` - Kitob yaratish
- [ ] `test_book_str_method` - `__str__` metodi
- [ ] `test_book_slug_generation` - Slug avtomatik yaratilishi
- [ ] `test_book_isbn_validation` - ISBN validation
- [ ] `test_book_default_values` - Default qiymatlar
- [ ] `test_book_price_cannot_be_negative` - Manfiy narx bo'lmasligi
- [ ] `test_book_published_date_not_in_future` - Kelajakdagi sana bo'lmasligi

#### 1.2. Author Model Tests
- [ ] `test_author_creation` - Author yaratish
- [ ] `test_author_str_method` - `__str__` metodi
- [ ] `test_author_books_relationship` - Kitoblar bilan aloqa
- [ ] `test_author_email_unique` - Email unique bo'lishi

#### 1.3. Category Model Tests
- [ ] `test_category_creation` - Category yaratish
- [ ] `test_category_str_method` - `__str__` metodi
- [ ] `test_category_slug_unique` - Slug unique bo'lishi

**Misol:**
```python
from django.test import TestCase
from books.models import Book, Author, Category
from decimal import Decimal

class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Test Author',
            email='author@example.com'
        )
    
    def test_book_creation(self):
        """Kitob yaratish va ma'lumotlarni tekshirish"""
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            category=self.category,
            isbn='1234567890123',
            price=Decimal('19.99')
        )
        
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.price, Decimal('19.99'))
        self.assertIsNotNone(book.slug)
    
    # Qolgan testlar...
```

---

### ✅ Task 2: Serializer Tests (test_serializers.py)

`books/tests/test_serializers.py` faylida quyidagi testlarni yozing:

#### 2.1. BookSerializer Tests
- [ ] `test_book_serializer_valid_data` - Valid ma'lumotlar
- [ ] `test_book_serializer_invalid_data` - Invalid ma'lumotlar
- [ ] `test_book_serializer_missing_required_fields` - Majburiy maydonlar yo'q
- [ ] `test_book_serializer_read_only_fields` - Read-only maydonlar
- [ ] `test_book_serializer_isbn_format` - ISBN format

#### 2.2. AuthorSerializer Tests
- [ ] `test_author_serializer_valid_data`
- [ ] `test_author_serializer_with_books`
- [ ] `test_author_serializer_email_validation`

**Misol:**
```python
from django.test import TestCase
from books.serializers import BookSerializer
from books.models import Category, Author

class BookSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com'
        )
        
        self.valid_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '1234567890123',
            'price': '29.99'
        }
    
    def test_book_serializer_valid_data(self):
        """Valid ma'lumotlar bilan serializer"""
        serializer = BookSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.title, 'Test Book')
    
    def test_book_serializer_invalid_isbn(self):
        """Noto'g'ri ISBN"""
        invalid_data = self.valid_data.copy()
        invalid_data['isbn'] = '123'  # Juda qisqa
        
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('isbn', serializer.errors)
```

---

### ✅ Task 3: View Tests (test_views.py)

`books/tests/test_views.py` faylida quyidagi testlarni yozing:

#### 3.1. BookViewSet Tests
- [ ] `test_list_books` - Ro'yxat olish (GET /api/books/)
- [ ] `test_retrieve_book` - Bitta kitob (GET /api/books/{id}/)
- [ ] `test_create_book_authenticated` - Yaratish (POST) - authenticated
- [ ] `test_create_book_unauthenticated` - Yaratish - unauthenticated (401)
- [ ] `test_update_book` - Yangilash (PUT)
- [ ] `test_partial_update_book` - Qisman yangilash (PATCH)
- [ ] `test_delete_book` - O'chirish (DELETE)
- [ ] `test_filter_books_by_category` - Category bo'yicha filter
- [ ] `test_search_books` - Qidirish
- [ ] `test_ordering_books` - Tartiblash

#### 3.2. Permission Tests
- [ ] `test_only_owner_can_update_book` - Faqat owner update qila oladi
- [ ] `test_only_owner_can_delete_book` - Faqat owner delete qila oladi
- [ ] `test_admin_can_update_any_book` - Admin har qanday kitobni update qila oladi

**Misol:**
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from books.models import Book, Category, Author

class BookViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com'
        )
        
        self.book = Book.objects.create(
            title='Existing Book',
            author=self.author,
            category=self.category,
            isbn='1111111111111',
            created_by=self.user
        )
    
    def test_list_books(self):
        """GET /api/books/ - Ro'yxat olish"""
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Existing Book')
    
    def test_create_book_unauthenticated(self):
        """POST /api/books/ - Unauthenticated"""
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '2222222222222'
        }
        
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """POST /api/books/ - Authenticated"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '2222222222222',
            'price': '19.99'
        }
        
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(Book.objects.count(), 2)
```

---

### ✅ Task 4: Integration Tests (test_integration.py)

`books/tests/test_integration.py` faylida quyidagi testlarni yozing:

#### 4.1. User Registration and Book Creation Flow
- [ ] `test_user_registration_login_create_book_workflow`

#### 4.2. Complete CRUD Workflow
- [ ] `test_book_crud_workflow`

#### 4.3. Order Creation Flow (agar Order model bo'lsa)
- [ ] `test_complete_order_workflow`

#### 4.4. Review System Flow
- [ ] `test_user_buys_book_and_leaves_review`

**Misol:**
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class BookIntegrationTest(APITestCase):
    def test_complete_book_workflow(self):
        """
        To'liq workflow:
        1. User registration
        2. Login
        3. Create book
        4. Update book
        5. Delete book
        """
        # Step 1: Register
        register_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass123',
            'password2': 'pass123'
        }
        register_response = self.client.post('/api/auth/register/', register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        # Step 2: Login
        # ...
        
        # Step 3: Create book
        # ...
        
        # Step 4: Update
        # ...
        
        # Step 5: Delete
        # ...
```

---

### ✅ Task 5: Factory Boy Integration (BONUS)

`books/tests/factories.py` fayli yarating va Factory'lar yozing:

```python
import factory
from factory.django import DjangoModelFactory
from books.models import Book, Author, Category
from django.contrib.auth.models import User

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Faker('word')
    description = factory.Faker('sentence')

class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
    
    name = factory.Faker('name')
    email = factory.Faker('email')
    bio = factory.Faker('text', max_nb_chars=200)

class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book
    
    title = factory.Faker('sentence', nb_words=3)
    author = factory.SubFactory(AuthorFactory)
    category = factory.SubFactory(CategoryFactory)
    isbn = factory.Faker('isbn13')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
```

Factory'lardan foydalanib testlarni qayta yozing.

---

### ✅ Task 6: Coverage Report

1. Coverage o'rnating:
```bash
pip install coverage
```

2. `.coveragerc` fayli yarating:
```ini
[run]
source = .
omit =
    */migrations/*
    */tests/*
    */__init__.py
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    def __str__
```

3. Coverage hisoblang:
```bash
coverage run --source='books' manage.py test books
coverage report
coverage html
```

4. **Maqsad: 80%+ coverage**

5. Screenshot yoki hisobotni saqlang va README'ga qo'shing

---

## 📊 Baholash Mezonlari

### Model Tests (25 ball)
- [ ] Barcha model testlari yozilgan (15 ball)
- [ ] Edge case'lar test qilingan (5 ball)
- [ ] Validation'lar test qilingan (5 ball)

### Serializer Tests (20 ball)
- [ ] Valid/Invalid data testlari (10 ball)
- [ ] Field validation testlari (10 ball)

### View Tests (30 ball)
- [ ] CRUD operations (15 ball)
- [ ] Authentication/Permission tests (10 ball)
- [ ] Filter/Search tests (5 ball)

### Integration Tests (15 ball)
- [ ] Kamida 2 ta to'liq workflow (10 ball)
- [ ] Multi-step scenario'lar (5 ball)

### Coverage (10 ball)
- [ ] 80%+ coverage (10 ball)
- [ ] 70-79% coverage (7 ball)
- [ ] 60-69% coverage (5 ball)

### BONUS: Factory Boy (10 ball)
- [ ] Factory'lar yaratilgan (5 ball)
- [ ] Testlarda ishlatilgan (5 ball)

**Maksimal ball: 100 (+ 10 bonus)**

---

## 📤 Topshirish

1. GitHub'ga push qiling
2. Pull Request yarating
3. PR'da quyidagilarni ko'rsating:
   - Coverage hisoboti screenshot
   - Test natijalarining screenshot
   - Qisqacha tavsif

---

## 💡 Maslahatlar

1. **Testlarni bosqichma-bosqich yozing:**
   - Avval model testlar
   - Keyin serializer testlar
   - Keyin view testlar
   - Oxirida integration testlar

2. **AAA pattern'ga amal qiling:**
   - Arrange (tayyorgarlik)
   - Act (harakat)
   - Assert (tekshirish)

3. **Test nomlarini to'g'ri qo'ying:**
   - `test_what_is_being_tested`
   - Misol: `test_book_creation_with_valid_data`

4. **setUp metodidan foydalaning:**
   - Qayta ishlatiladigan ma'lumotlar uchun

5. **Edge case'larni unutmang:**
   - Empty values
   - Null values
   - Invalid formats
   - Boundary values

6. **Coverage 100% bo'lishi shart emas:**
   - 80%+ yetarli
   - Muhim qismlar qoplangan bo'lsin

---

## 🆘 Yordam

Agar qiyinchiliklarga duch kelsangiz:

1. **Examples papkadagi misollarni o'rganing**
2. **Django documentation:** https://docs.djangoproject.com/en/stable/topics/testing/
3. **DRF documentation:** https://www.django-rest-framework.org/api-guide/testing/

---

## ✅ Checklist

Topshirishdan oldin tekshiring:

- [ ] Barcha testlar yozilgan
- [ ] Barcha testlar o'tadi (green)
- [ ] Coverage 80%+
- [ ] Code formatlangan (black/autopep8)
- [ ] Commit message'lar aniq
- [ ] PR tavsifi to'liq
- [ ] README.md yangilangan

---

**Omad! Yaxshi testlar yozing!**