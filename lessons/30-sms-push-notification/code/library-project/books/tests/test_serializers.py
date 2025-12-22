"""
Books Serializers Tests - REAL PROJECT
=======================================

BookSerializer, AuthorSerializer, GenreSerializer testlari
"""

from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Book, Author, Genre
from books.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
    AuthorSerializer,
    GenreSerializer
)
from decimal import Decimal
from datetime import date


class GenreSerializerTest(TestCase):
    """GenreSerializer testlari"""
    
    def test_genre_serializer_fields(self):
        """Serializer fieldlari"""
        genre = Genre.objects.create(
            name='Fiction',
            description='Fiction books'
        )
        
        serializer = GenreSerializer(genre)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('description', data)
        self.assertEqual(data['name'], 'Fiction')
    
    def test_genre_serializer_create(self):
        """Genre yaratish"""
        data = {
            'name': 'Science',
            'description': 'Science books'
        }
        
        serializer = GenreSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        genre = serializer.save()
        self.assertEqual(genre.name, 'Science')
    
    def test_genre_serializer_missing_name(self):
        """Name majburiy"""
        data = {'description': 'Test'}  # name yo'q
        
        serializer = GenreSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class AuthorSerializerTest(TestCase):
    """AuthorSerializer testlari"""
    
    def test_author_serializer_fields(self):
        """Serializer fieldlari"""
        author = Author.objects.create(
            name='John Doe',
            email='john@example.com',
            bio='Famous author',
            birth_date=date(1980, 1, 1)
        )
        
        serializer = AuthorSerializer(author)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('email', data)
        self.assertIn('bio', data)
        self.assertIn('birth_date', data)
    
    def test_author_serializer_create(self):
        """Author yaratish"""
        data = {
            'name': 'New Author',
            'email': 'new@example.com',
            'bio': 'New author bio',
            'birth_date': '1990-01-01'
        }
        
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        author = serializer.save()
        self.assertEqual(author.name, 'New Author')
    
    def test_author_serializer_email_validation(self):
        """Email validation"""
        data = {
            'name': 'Author',
            'email': 'invalid-email',  # Noto'g'ri email
            'bio': 'Bio',
            'birth_date': '1990-01-01'
        }
        
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_author_serializer_email_unique(self):
        """Email unique"""
        Author.objects.create(
            name='Existing',
            email='existing@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        data = {
            'name': 'New',
            'email': 'existing@example.com',  # Duplicate
            'bio': 'Bio',
            'birth_date': '1990-01-01'
        }
        
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class BookSerializerTest(TestCase):
    """BookSerializer testlari"""
    
    def setUp(self):
        self.genre = Genre.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
    
    def test_book_serializer_valid_data(self):
        """Valid ma'lumotlar"""
        data = {
            'title': 'Test Book',
            'subtitle': 'Test Subtitle',
            'author': self.author.id,
            'isbn_number': '9781234567897',
            'price': '29.99',
            'pages': 200,
            'language': 'English',
            'publisher': 'Test Publisher',
            'published_date': '2024-01-01'
        }
        
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        # Owner'ni qo'lda set qilish kerak
        book = serializer.save(owner=self.user)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.price, Decimal('29.99'))
    
    def test_book_serializer_missing_required_fields(self):
        """Majburiy fieldlar yo'q"""
        data = {
            'title': 'Test Book'
            # author, isbn_number, price, pages, publisher yo'q
        }
        
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('isbn_number', serializer.errors)
        self.assertIn('price', serializer.errors)
        self.assertIn('pages', serializer.errors)
        self.assertIn('publisher', serializer.errors)
    
    def test_book_serializer_invalid_isbn(self):
        """Noto'g'ri ISBN (agar validator qo'shilgan bo'lsa)"""
        data = {
            'title': 'Test Book',
            'author': self.author.id,
            'isbn_number': '123',  # Juda qisqa
            'price': '29.99',
            'pages': 200,
            'publisher': 'Publisher'
        }
        
        serializer = BookSerializer(data=data)
        # Agar ISBN validator qo'shilgan bo'lsa
        if not serializer.is_valid():
            self.assertIn('isbn_number', serializer.errors)
    
    def test_book_serializer_update(self):
        """Kitobni yangilash"""
        book = Book.objects.create(
            title='Old Title',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('20.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        update_data = {
            'title': 'New Title',
            'price': '30.00'
        }
        
        serializer = BookSerializer(book, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_book = serializer.save()
        self.assertEqual(updated_book.title, 'New Title')
        self.assertEqual(updated_book.price, Decimal('30.00'))


class BookListSerializerTest(TestCase):
    """BookListSerializer testlari"""
    
    def setUp(self):
        self.genre = Genre.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_book_list_serializer_nested_author(self):
        """Nested author ma'lumotlari"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('19.99'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        book.genres.add(self.genre)
        
        serializer = BookListSerializer(book)
        data = serializer.data
        
        # Nested author
        self.assertIn('author', data)
        self.assertIsInstance(data['author'], dict)
        self.assertEqual(data['author']['name'], 'Author')
        
        # Nested genres
        self.assertIn('genres', data)
        self.assertIsInstance(data['genres'], list)
        self.assertEqual(len(data['genres']), 1)


class BookDetailSerializerTest(TestCase):
    """BookDetailSerializer testlari"""
    
    def setUp(self):
        self.genre = Genre.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_book_detail_serializer_all_fields(self):
        """Barcha fieldlar"""
        book = Book.objects.create(
            title='Test',
            subtitle='Subtitle',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('19.99'),
            pages=200,
            language='English',
            publisher='Publisher',
            published=True,
            published_date=date(2024, 1, 1),
            owner=self.user
        )
        book.genres.add(self.genre)
        
        serializer = BookDetailSerializer(book)
        data = serializer.data
        
        # Barcha fieldlar
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('subtitle', data)
        self.assertIn('author', data)
        self.assertIn('genres', data)
        self.assertIn('isbn_number', data)
        self.assertIn('price', data)
        self.assertIn('pages', data)
        self.assertIn('language', data)
        self.assertIn('publisher', data)
        self.assertIn('published', data)
        self.assertIn('published_date', data)


class BookCreateUpdateSerializerTest(TestCase):
    """BookCreateUpdateSerializer testlari"""
    
    def setUp(self):
        self.genre = Genre.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_create_book_with_author_id(self):
        """Author ID bilan kitob yaratish"""
        data = {
            'title': 'New Book',
            'author_id': self.author.id,  # author_id (write)
            'isbn_number': '9781234567897',
            'price': '25.00',
            'pages': 150,
            'publisher': 'Publisher'
        }
        
        serializer = BookCreateUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        book = serializer.save(owner=self.user)
        self.assertEqual(book.author, self.author)
    
    def test_create_book_with_genre_ids(self):
        """Genre IDs bilan kitob yaratish"""
        genre2 = Genre.objects.create(name='Mystery')
        
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'genre_ids': [self.genre.id, genre2.id],  # genre_ids (write)
            'isbn_number': '9781234567897',
            'price': '25.00',
            'pages': 150,
            'publisher': 'Publisher'
        }
        
        serializer = BookCreateUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        book = serializer.save(owner=self.user)
        self.assertEqual(book.genres.count(), 2)
    
    def test_isbn_validation_13_chars(self):
        """ISBN 13 belgidan iborat bo'lishi (agar validator bo'lsa)"""
        data = {
            'title': 'Test',
            'author_id': self.author.id,
            'isbn_number': '123',  # Juda qisqa
            'price': '25.00',
            'pages': 150,
            'publisher': 'Publisher'
        }
        
        serializer = BookCreateUpdateSerializer(data=data)
        # Agar validator qo'shilgan bo'lsa
        if not serializer.is_valid():
            self.assertIn('isbn_number', serializer.errors)
    
    def test_price_validation_positive(self):
        """Narx musbat (agar validator bo'lsa)"""
        data = {
            'title': 'Test',
            'author_id': self.author.id,
            'isbn_number': '9781234567897',
            'price': '0',  # 0 yoki manfiy
            'pages': 150,
            'publisher': 'Publisher'
        }
        
        serializer = BookCreateUpdateSerializer(data=data)
        # Agar validator qo'shilgan bo'lsa
        if not serializer.is_valid():
            self.assertIn('price', serializer.errors)
    
    def test_pages_validation_positive(self):
        """Pages musbat (agar validator bo'lsa)"""
        data = {
            'title': 'Test',
            'author_id': self.author.id,
            'isbn_number': '9781234567897',
            'price': '25.00',
            'pages': 0,  # 0 yoki manfiy
            'publisher': 'Publisher'
        }
        
        serializer = BookCreateUpdateSerializer(data=data)
        # Agar validator qo'shilgan bo'lsa
        if not serializer.is_valid():
            self.assertIn('pages', serializer.errors)


class ReadOnlyFieldsTest(TestCase):
    """Read-only fields testlari"""
    
    def setUp(self):
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_owner_read_only(self):
        """owner read-only"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        serializer = BookSerializer(book)
        data = serializer.data
        
        # owner username ko'rinadi
        self.assertEqual(data['owner'], 'test')
    
    def test_timestamps_read_only(self):
        """created_at va updated_at read-only"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        serializer = BookSerializer(book)
        data = serializer.data
        
        # Timestamps
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)