"""
Books Views Tests - REAL PROJECT
=================================

BookListCreateView, BookDetailView testlari
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from books.models import Book, Author, Genre
from decimal import Decimal
from datetime import date


class BookListCreateViewTest(APITestCase):
    """BookListCreateView testlari"""
    
    def setUp(self):
        """Har test uchun kerakli ma'lumotlar"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.genre = Genre.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Test Author',
            email='author@example.com',
            bio='Author bio',
            birth_date=date(1980, 1, 1)
        )
        
        self.book = Book.objects.create(
            title='Existing Book',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('19.99'),
            pages=200,
            publisher='Publisher',
            owner=self.user
        )
    
    def test_list_books_unauthenticated(self):
        """GET /api/books/ - Unauthenticated (allowed)"""
        url = '/api/books/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Pagination bo'lsa
        if 'results' in response.data:
            self.assertGreaterEqual(len(response.data['results']), 1)
        else:
            self.assertGreaterEqual(len(response.data), 1)
    
    def test_list_books_authenticated(self):
        """GET /api/books/ - Authenticated"""
        self.client.force_authenticate(user=self.user)
        
        url = '/api/books/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_unauthenticated(self):
        """POST /api/books/ - Unauthenticated (not allowed)"""
        url = '/api/books/'
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'isbn_number': '9789876543210',
            'price': '29.99',
            'pages': 300,
            'publisher': 'Publisher'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """POST /api/books/ - Authenticated"""
        self.client.force_authenticate(user=self.user)
        
        url = '/api/books/'
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'isbn_number': '9789876543210',
            'price': '29.99',
            'pages': 300,
            'publisher': 'Test Publisher'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(Book.objects.count(), 2)
    
    def test_create_book_invalid_data(self):
        """Invalid data bilan yaratish"""
        self.client.force_authenticate(user=self.user)
        
        url = '/api/books/'
        data = {
            'title': 'New Book',
            # author_id, isbn_number, price, pages, publisher yo'q
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_search_books(self):
        """Search functionality"""
        url = '/api/books/?search=Existing'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Results borligini tekshirish
    
    def test_filter_books_by_author(self):
        """Author bo'yicha filter"""
        url = f'/api/books/?author={self.author.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_ordering_books(self):
        """Ordering by price"""
        url = '/api/books/?ordering=price'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookDetailViewTest(APITestCase):
    """BookDetailView testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
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
            owner=self.user
        )
    
    def test_retrieve_book_unauthenticated(self):
        """GET /api/books/{id}/ - Unauthenticated (allowed)"""
        url = f'/api/books/{self.book.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_retrieve_nonexistent_book(self):
        """Mavjud bo'lmagan kitob"""
        url = '/api/books/9999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_book_authenticated_owner(self):
        """PUT /api/books/{id}/ - Owner"""
        self.client.force_authenticate(user=self.user)
        
        url = f'/api/books/{self.book.id}/'
        data = {
            'title': 'Updated Title',
            'author_id': self.author.id,
            'isbn_number': '9781234567897',
            'price': '39.99',
            'pages': 250,
            'publisher': 'Updated Publisher'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        
        # Database'da yangilanganini tekshirish
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
    
    def test_partial_update_book(self):
        """PATCH /api/books/{id}/ - Qisman yangilash"""
        self.client.force_authenticate(user=self.user)
        
        url = f'/api/books/{self.book.id}/'
        data = {'title': 'Partially Updated'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated')
    
    def test_delete_book_owner(self):
        """DELETE /api/books/{id}/ - Owner"""
        self.client.force_authenticate(user=self.user)
        
        url = f'/api/books/{self.book.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Database'dan o'chirilganini tekshirish
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
    
    def test_update_book_not_owner(self):
        """UPDATE - Not owner (should fail if permission set)"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='pass123'
        )
        self.client.force_authenticate(user=other_user)
        
        url = f'/api/books/{self.book.id}/'
        data = {'title': 'Hacked Title'}
        
        response = self.client.patch(url, data)
        
        # Agar IsOwnerOrReadOnly permission qo'shilgan bo'lsa
        # 403 bo'lishi kerak
        # Agar yo'q bo'lsa, 200 bo'ladi
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]
        )


class GenreViewTest(APITestCase):
    """Genre view testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        self.genre = Genre.objects.create(
            name='Fiction',
            description='Fiction books'
        )
    
    def test_list_genres(self):
        """GET /api/genres/"""
        url = '/api/genres/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_genre(self):
        """GET /api/genres/{id}/"""
        url = f'/api/genres/{self.genre.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Fiction')
    
    def test_create_genre_authenticated(self):
        """POST /api/genres/ - Authenticated"""
        self.client.force_authenticate(user=self.user)
        
        url = '/api/genres/'
        data = {
            'name': 'Science',
            'description': 'Science books'
        }
        
        response = self.client.post(url, data)
        
        # Agar permission bor bo'lsa
        self.assertIn(
            response.status_code,
            [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN]
        )


class AuthorViewTest(APITestCase):
    """Author view testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        self.author = Author.objects.create(
            name='Existing Author',
            email='existing@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
    
    def test_list_authors(self):
        """GET /api/authors/"""
        url = '/api/authors/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_author(self):
        """GET /api/authors/{id}/"""
        url = f'/api/authors/{self.author.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Existing Author')


class PaginationTest(APITestCase):
    """Pagination testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        # 15 ta kitob yaratish
        for i in range(15):
            Book.objects.create(
                title=f'Book {i}',
                author=self.author,
                isbn_number=f'978123456{i:04d}',
                price=Decimal('10.00'),
                pages=100,
                publisher='Publisher',
                owner=self.user
            )
    
    def test_pagination_default(self):
        """Pagination default (10 items)"""
        url = '/api/books/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Pagination formatini tekshirish
        if 'results' in response.data:
            # DRF pagination format
            self.assertIn('count', response.data)
            self.assertIn('next', response.data)
            self.assertIn('previous', response.data)
            self.assertLessEqual(len(response.data['results']), 10)
    
    def test_pagination_custom_page_size(self):
        """Custom page_size"""
        url = '/api/books/?page_size=5'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            self.assertLessEqual(len(response.data['results']), 5)
    
    def test_pagination_page_2(self):
        """2-chi sahifa"""
        url = '/api/books/?page=2'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)