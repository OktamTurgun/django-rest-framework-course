"""
Lesson 23: Basic API Testing with APITestCase
==============================================

Bu faylda Django REST Framework'ning APITestCase klassi bilan
oddiy testlar yozishni o'rganamiz.

Mavzular:
1. APITestCase nima?
2. Test yozish asoslari
3. HTTP metodlari (GET, POST, PUT, PATCH, DELETE)
4. Autentifikatsiya
5. Assertion metodlari
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


# =============================================================================
# 1. ODDIY API TEST
# =============================================================================

class SimpleAPITest(APITestCase):
    """
    Eng oddiy API test misoli
    
    APITestCase - bu Django REST Framework'ning test klassi.
    U bizga API'ni test qilish uchun maxsus metodlar beradi.
    """
    
    def test_api_root(self):
        """
        API root endpoint'ini test qilish
        
        Bu test:
        1. Root URL'ga GET request yuboradi
        2. Response status code'ni tekshiradi
        """
        # Act - harakat (GET request yuborish)
        response = self.client.get('/api/')
        
        # Assert - tekshirish (200 OK status kutamiz)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# =============================================================================
# 2. CRUD OPERATIONS TESTING
# =============================================================================

class BookCRUDTest(APITestCase):
    """
    CRUD operatsiyalarini test qilish
    (Create, Read, Update, Delete)
    """
    
    def setUp(self):
        """
        Har bir test oldidan ishga tushadi
        Bu yerda test uchun kerakli ma'lumotlarni tayyorlaymiz
        """
        # Foydalanuvchi yaratish
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Test uchun kitob ma'lumotlari
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'published_date': '2024-01-01',
            'pages': 200,
            'language': 'English'
        }
    
    def test_create_book_without_authentication(self):
        """
        Autentifikatsiyasiz kitob yaratish (muvaffaqiyatsiz bo'lishi kerak)
        """
        # Act
        response = self.client.post('/api/books/', self.book_data)
        
        # Assert - 401 Unauthorized kutamiz
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_with_authentication(self):
        """
        Autentifikatsiya bilan kitob yaratish (muvaffaqiyatli bo'lishi kerak)
        """
        # Arrange - foydalanuvchini autentifikatsiya qilish
        self.client.force_authenticate(user=self.user)
        
        # Act - kitob yaratish
        response = self.client.post('/api/books/', self.book_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['author'], 'Test Author')
    
    def test_get_books_list(self):
        """
        Kitoblar ro'yxatini olish
        """
        # Arrange - test kitob yaratish
        self.client.force_authenticate(user=self.user)
        self.client.post('/api/books/', self.book_data)
        
        # Act - ro'yxatni olish
        response = self.client.get('/api/books/')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_book_detail(self):
        """
        Bitta kitobning ma'lumotlarini olish
        """
        # Arrange - kitob yaratish
        self.client.force_authenticate(user=self.user)
        create_response = self.client.post('/api/books/', self.book_data)
        book_id = create_response.data['id']
        
        # Act - kitob ma'lumotlarini olish
        response = self.client.get(f'/api/books/{book_id}/')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_update_book(self):
        """
        Kitobni yangilash (PUT)
        """
        # Arrange
        self.client.force_authenticate(user=self.user)
        create_response = self.client.post('/api/books/', self.book_data)
        book_id = create_response.data['id']
        
        # Act - kitobni yangilash
        updated_data = self.book_data.copy()
        updated_data['title'] = 'Updated Book Title'
        response = self.client.put(f'/api/books/{book_id}/', updated_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')
    
    def test_partial_update_book(self):
        """
        Kitobni qisman yangilash (PATCH)
        """
        # Arrange
        self.client.force_authenticate(user=self.user)
        create_response = self.client.post('/api/books/', self.book_data)
        book_id = create_response.data['id']
        
        # Act - faqat title'ni yangilash
        response = self.client.patch(
            f'/api/books/{book_id}/',
            {'title': 'Partially Updated'}
        )
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated')
        self.assertEqual(response.data['author'], 'Test Author')  # Boshqalar o'zgarmagan
    
    def test_delete_book(self):
        """
        Kitobni o'chirish
        """
        # Arrange
        self.client.force_authenticate(user=self.user)
        create_response = self.client.post('/api/books/', self.book_data)
        book_id = create_response.data['id']
        
        # Act - kitobni o'chirish
        response = self.client.delete(f'/api/books/{book_id}/')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Kitob haqiqatan o'chirilganini tekshirish
        get_response = self.client.get(f'/api/books/{book_id}/')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)


# =============================================================================
# 3. AUTHENTICATION TESTING
# =============================================================================

class AuthenticationTest(APITestCase):
    """
    Turli autentifikatsiya metodlarini test qilish
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_force_authenticate(self):
        """
        force_authenticate() metodi bilan
        Bu eng oddiy va tez usul
        """
        # Authenticate
        self.client.force_authenticate(user=self.user)
        
        # Test
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_authentication(self):
        """
        Token bilan autentifikatsiya
        """
        # Token'ni header'ga qo'shish
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Test
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_token(self):
        """
        Noto'g'ri token bilan
        """
        # Noto'g'ri token
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token_here')
        
        # Test
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_no_authentication(self):
        """
        Autentifikatsiyasiz
        """
        # Test
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# =============================================================================
# 4. ASSERTION METODLARI
# =============================================================================

class AssertionExamplesTest(APITestCase):
    """
    Turli assertion metodlari bilan tanishish
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.user)
    
    def test_status_code_assertions(self):
        """
        Status code'larni tekshirish
        """
        response = self.client.get('/api/books/')
        
        # Aniq status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Status code range
        self.assertIn(response.status_code, [200, 201])
    
    def test_response_data_assertions(self):
        """
        Response data'ni tekshirish
        """
        response = self.client.get('/api/books/')
        
        # Data mavjudligini tekshirish
        self.assertIsNotNone(response.data)
        
        # List bo'lishini tekshirish
        self.assertIsInstance(response.data, list)
        
        # List uzunligini tekshirish
        self.assertEqual(len(response.data), 0)
        self.assertGreaterEqual(len(response.data), 0)
    
    def test_response_keys_assertions(self):
        """
        Response'dagi key'larni tekshirish
        """
        # Kitob yaratish
        book_data = {
            'title': 'Test',
            'author': 'Author',
            'isbn': '1234567890123'
        }
        response = self.client.post('/api/books/', book_data)
        
        # Key'lar mavjudligini tekshirish
        self.assertIn('id', response.data)
        self.assertIn('title', response.data)
        self.assertIn('author', response.data)
        
        # Key'larning qiymatlari
        self.assertEqual(response.data['title'], 'Test')
        self.assertEqual(response.data['author'], 'Author')
    
    def test_database_assertions(self):
        """
        Database'dagi ma'lumotlarni tekshirish
        """
        # Kitob yaratish
        book_data = {
            'title': 'DB Test Book',
            'author': 'Author',
            'isbn': '1234567890123'
        }
        self.client.post('/api/books/', book_data)
        
        # Database'da mavjudligini tekshirish
        from books.models import Book
        self.assertTrue(Book.objects.filter(title='DB Test Book').exists())
        self.assertEqual(Book.objects.count(), 1)
        
        # Kitob ma'lumotlarini tekshirish
        book = Book.objects.first()
        self.assertEqual(book.title, 'DB Test Book')
        self.assertEqual(book.author, 'Author')
    
    def test_boolean_assertions(self):
        """
        Boolean qiymatlarni tekshirish
        """
        from books.models import Book
        
        # Kitob yaratish
        book = Book.objects.create(
            title='Test',
            author='Author',
            isbn='1234567890123',
            is_published=True
        )
        
        # Boolean tekshirish
        self.assertTrue(book.is_published)
        self.assertFalse(book.is_archived)
    
    def test_none_assertions(self):
        """
        None qiymatlarni tekshirish
        """
        from books.models import Book
        
        book = Book.objects.create(
            title='Test',
            author='Author',
            isbn='1234567890123'
        )
        
        # None tekshirish
        self.assertIsNone(book.description)
        self.assertIsNotNone(book.title)


# =============================================================================
# 5. VALIDATION TESTING
# =============================================================================

class ValidationTest(APITestCase):
    """
    Validation'larni test qilish
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.user)
    
    def test_create_book_with_missing_required_field(self):
        """
        Majburiy maydonlar bo'lmasa
        """
        # Title yo'q
        data = {
            'author': 'Test Author',
            'isbn': '1234567890123'
        }
        
        response = self.client.post('/api/books/', data)
        
        # 400 Bad Request kutamiz
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_book_with_invalid_isbn(self):
        """
        Noto'g'ri ISBN format
        """
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '12345'  # Juda qisqa
        }
        
        response = self.client.post('/api/books/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('isbn', response.data)
    
    def test_create_book_with_invalid_date(self):
        """
        Noto'g'ri sana format
        """
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'published_date': 'invalid-date'
        }
        
        response = self.client.post('/api/books/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# =============================================================================
# TESTLARNI ISHGA TUSHIRISH
# =============================================================================

"""
Testlarni ishga tushirish:

# Barcha testlar
python manage.py test

# Muayyan klass
python manage.py test path.to.this.file.SimpleAPITest

# Muayyan metod
python manage.py test path.to.this.file.SimpleAPITest.test_api_root

# Verbose output
python manage.py test --verbosity=2

# Parallel (tezroq)
python manage.py test --parallel


Natija:
-------
......
----------------------------------------------------------------------
Ran 6 tests in 0.123s

OK


Har bir nuqta (.) - muvaffaqiyatli test
F - muvaffaqiyatsiz test (Failed)
E - xato (Error)
"""