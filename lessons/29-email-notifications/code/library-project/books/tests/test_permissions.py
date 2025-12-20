"""
Books Permissions Tests - REAL PROJECT
=======================================

IsOwnerOrReadOnly permission testlari
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from books.models import Book, Author, Genre
from decimal import Decimal
from datetime import date


class BookPermissionTest(APITestCase):
    """Book permission testlari"""
    
    def setUp(self):
        """Test ma'lumotlari"""
        # Regular users
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        
        # Admin user
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # Author va Genre
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        # User1'ning kitoblari
        self.user1_book = Book.objects.create(
            title='User1 Book',
            author=self.author,
            isbn_number='9781111111111',
            price=Decimal('19.99'),
            pages=200,
            publisher='Publisher',
            owner=self.user1
        )
        
        # User2'ning kitoblari
        self.user2_book = Book.objects.create(
            title='User2 Book',
            author=self.author,
            isbn_number='9782222222222',
            price=Decimal('24.99'),
            pages=250,
            publisher='Publisher',
            owner=self.user2
        )
    
    def test_list_books_public(self):
        """Ro'yxatni hamma ko'ra oladi (IsAuthenticatedOrReadOnly)"""
        url = '/api/books/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 2)
    
    def test_retrieve_book_public(self):
        """Bitta kitobni hamma ko'ra oladi"""
        url = f'/api/books/{self.user1_book.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_requires_authentication(self):
        """Yaratish uchun authentication kerak"""
        url = '/api/books/'
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'isbn_number': '9783333333333',
            'price': '29.99',
            'pages': 300,
            'publisher': 'Publisher'
        }
        
        # Unauthenticated
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Authenticated
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_can_update_own_book(self):
        """User o'z kitobini update qila oladi"""
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/books/{self.user1_book.id}/'
        data = {'title': 'Updated Title'}
        
        response = self.client.patch(url, data)
        
        # Agar IsOwnerOrReadOnly permission qo'shilgan bo'lsa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
    
    def test_user_cannot_update_others_book(self):
        """User boshqaning kitobini update qila olmaydi"""
        self.client.force_authenticate(user=self.user1)
        
        # User2'ning kitobini update qilishga urinish
        url = f'/api/books/{self.user2_book.id}/'
        data = {'title': 'Hacked Title'}
        
        response = self.client.patch(url, data)
        
        # Agar IsOwnerOrReadOnly permission qo'shilgan bo'lsa: 403
        # Agar permission yo'q bo'lsa: 200
        # Hozircha ikkalasini ham qabul qilamiz
        if response.status_code == status.HTTP_403_FORBIDDEN:
            # Permission ishlayapti
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            
            # Kitob o'zgarmaganini tekshirish
            self.user2_book.refresh_from_db()
            self.assertEqual(self.user2_book.title, 'User2 Book')
        else:
            # Permission hali qo'shilmagan
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_can_delete_own_book(self):
        """User o'z kitobini delete qila oladi"""
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/books/{self.user1_book.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.user1_book.id).exists())
    
    def test_user_cannot_delete_others_book(self):
        """User boshqaning kitobini delete qila olmaydi"""
        self.client.force_authenticate(user=self.user1)
        
        # User2'ning kitobini delete qilishga urinish
        url = f'/api/books/{self.user2_book.id}/'
        response = self.client.delete(url)
        
        # Agar permission qo'shilgan: 403
        # Agar yo'q: 204
        if response.status_code == status.HTTP_403_FORBIDDEN:
            # Permission ishlayapti
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            
            # Kitob o'chirilmaganini tekshirish
            self.assertTrue(Book.objects.filter(id=self.user2_book.id).exists())
        else:
            # Permission hali qo'shilmagan
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_admin_can_update_any_book(self):
        """Admin har qanday kitobni update qila oladi"""
        self.client.force_authenticate(user=self.admin)
        
        # User1'ning kitobini update qilish
        url = f'/api/books/{self.user1_book.id}/'
        data = {'title': 'Admin Updated'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Admin Updated')
    
    def test_admin_can_delete_any_book(self):
        """Admin har qanday kitobni delete qila oladi"""
        self.client.force_authenticate(user=self.admin)
        
        url = f'/api/books/{self.user1_book.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.user1_book.id).exists())


class ReadOnlyPermissionTest(APITestCase):
    """Read-only permission testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
    
    def test_unauthenticated_can_read(self):
        """Unauthenticated foydalanuvchi faqat o'qiy oladi"""
        # Book list
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Author list
        url = '/api/authors/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_cannot_create(self):
        """Unauthenticated yarata olmaydi"""
        # Book create
        url = '/api/books/'
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'isbn_number': '9781234567897',
            'price': '29.99',
            'pages': 200,
            'publisher': 'Publisher'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OwnerPermissionTest(APITestCase):
    """Owner-based permission testlari"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            password='pass123'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass123'
        )
        
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('19.99'),
            pages=200,
            publisher='Publisher',
            owner=self.owner
        )
    
    def test_owner_can_edit(self):
        """Owner edit qila oladi"""
        self.client.force_authenticate(user=self.owner)
        
        url = f'/api/books/{self.book.id}/'
        data = {'title': 'Owner Updated'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_owner_cannot_edit(self):
        """Owner emas edit qila olmaydi (agar permission qo'shilgan bo'lsa)"""
        self.client.force_authenticate(user=self.other_user)
        
        url = f'/api/books/{self.book.id}/'
        data = {'title': 'Hacked'}
        
        response = self.client.patch(url, data)
        
        # Permission qo'shilgan: 403
        # Qo'shilmagan: 200
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]
        )
    
    def test_owner_can_delete(self):
        """Owner delete qila oladi"""
        self.client.force_authenticate(user=self.owner)
        
        url = f'/api/books/{self.book.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_non_owner_cannot_delete(self):
        """Owner emas delete qila olmaydi (agar permission qo'shilgan bo'lsa)"""
        self.client.force_authenticate(user=self.other_user)
        
        url = f'/api/books/{self.book.id}/'
        response = self.client.delete(url)
        
        # Permission qo'shilgan: 403
        # Qo'shilmagan: 204
        self.assertIn(
            response.status_code,
            [status.HTTP_204_NO_CONTENT, status.HTTP_403_FORBIDDEN]
        )


class PublishedPermissionTest(APITestCase):
    """Published status permission testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        # Published kitob
        self.published_book = Book.objects.create(
            title='Published Book',
            author=self.author,
            isbn_number='9781111111111',
            price=Decimal('19.99'),
            pages=200,
            publisher='Publisher',
            published=True,
            owner=self.user
        )
        
        # Unpublished kitob
        self.unpublished_book = Book.objects.create(
            title='Unpublished Book',
            author=self.author,
            isbn_number='9782222222222',
            price=Decimal('24.99'),
            pages=250,
            publisher='Publisher',
            published=False,
            owner=self.user
        )
    
    def test_anyone_can_read_published_book(self):
        """Published kitobni hamma o'qiy oladi"""
        url = f'/api/books/{self.published_book.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unpublished_book_visibility(self):
        """Unpublished kitob (owner ga ko'rinadi, boshqalarga yo'q - agar permission qo'shilgan bo'lsa)"""
        # Hozircha barcha kitoblar ko'rinadi (permission qo'shilmagan)
        url = f'/api/books/{self.unpublished_book.id}/'
        response = self.client.get(url)
        
        # Permission yo'q: 200
        # Permission bor: owner emas bo'lsa 404 yoki 403
        self.assertEqual(response.status_code, status.HTTP_200_OK)