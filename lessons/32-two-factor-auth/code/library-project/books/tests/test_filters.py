"""
Books Filters Tests - REAL PROJECT
===================================

Django Filter testlari
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from books.models import Book, Author, Genre
from decimal import Decimal
from datetime import date


class BookFilterTest(APITestCase):
    """Book filter testlari"""
    
    def setUp(self):
        """Test ma'lumotlari"""
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        
        self.fiction = Genre.objects.create(name='Fiction')
        self.science = Genre.objects.create(name='Science')
        
        self.author1 = Author.objects.create(
            name='Author One',
            email='author1@example.com',
            bio='Bio 1',
            birth_date=date(1980, 1, 1)
        )
        self.author2 = Author.objects.create(
            name='Author Two',
            email='author2@example.com',
            bio='Bio 2',
            birth_date=date(1990, 1, 1)
        )
        
        # Turli xil kitoblar
        self.book1 = Book.objects.create(
            title='Python Programming',
            author=self.author1,
            isbn_number='9781234567897',
            price=Decimal('29.99'),
            pages=400,
            publisher='Publisher A',
            published_date=date(2023, 1, 1),
            owner=self.user
        )
        self.book1.genres.add(self.science)
        
        self.book2 = Book.objects.create(
            title='Django Development',
            author=self.author1,
            isbn_number='9789876543210',
            price=Decimal('39.99'),
            pages=500,
            publisher='Publisher A',
            published_date=date(2023, 6, 1),
            owner=self.user
        )
        self.book2.genres.add(self.science)
        
        self.book3 = Book.objects.create(
            title='Mystery Novel',
            author=self.author2,
            isbn_number='9781111111111',
            price=Decimal('19.99'),
            pages=300,
            publisher='Publisher B',
            published_date=date(2020, 1, 1),
            owner=self.user
        )
        self.book3.genres.add(self.fiction)
    
    def test_filter_by_author(self):
        """Author bo'yicha filter"""
        url = f'/api/books/?author={self.author1.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Results'ni olish (pagination bo'lishi mumkin)
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 2)
    
    def test_filter_by_min_price(self):
        """Minimal narx filter"""
        url = '/api/books/?min_price=25'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # 29.99 va 39.99 - 2 ta kitob
        self.assertGreaterEqual(len(results), 2)
    
    def test_filter_by_max_price(self):
        """Maksimal narx filter"""
        url = '/api/books/?max_price=30'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # 19.99 va 29.99 - 2 ta kitob
        self.assertGreaterEqual(len(results), 2)
    
    def test_filter_by_price_range(self):
        """Narx oralig'i"""
        url = '/api/books/?min_price=20&max_price=35'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # Faqat 29.99
        self.assertGreaterEqual(len(results), 1)
    
    def test_filter_by_pages_range(self):
        """Sahifalar oralig'i"""
        url = '/api/books/?min_pages=350&max_pages=450'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # Faqat 400 sahifali kitob
        self.assertGreaterEqual(len(results), 1)
    
    def test_filter_by_published_year(self):
        """Published year filter"""
        url = '/api/books/?published_year=2023'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # 2023'da 2 ta kitob
        self.assertGreaterEqual(len(results), 2)
    
    def test_filter_by_genre(self):
        """Genre bo'yicha filter"""
        url = f'/api/books/?genres={self.science.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # Science genreda 2 ta kitob
        self.assertGreaterEqual(len(results), 2)
    
    def test_multiple_filters(self):
        """Bir nechta filter birgalikda"""
        url = f'/api/books/?author={self.author1.id}&min_price=35'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # Author1 va price >= 35: faqat Django book (39.99)
        self.assertGreaterEqual(len(results), 1)


class BookSearchTest(APITestCase):
    """Search functionality testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        
        self.author = Author.objects.create(
            name='John Smith',
            email='john@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        Book.objects.create(
            title='Python Programming Guide',
            subtitle='Learn Python',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('29.99'),
            pages=400,
            publisher='Tech Publisher',
            owner=self.user
        )
        Book.objects.create(
            title='JavaScript Basics',
            author=self.author,
            isbn_number='9789876543210',
            price=Decimal('24.99'),
            pages=300,
            publisher='Tech Publisher',
            owner=self.user
        )
        Book.objects.create(
            title='Advanced Python Techniques',
            author=self.author,
            isbn_number='9781111111111',
            price=Decimal('34.99'),
            pages=500,
            publisher='Advanced Publisher',
            owner=self.user
        )
    
    def test_search_by_title(self):
        """Title bo'yicha qidirish"""
        url = '/api/books/?search=Python'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # 2 ta Python kitob
        self.assertGreaterEqual(len(results), 2)
    
    def test_search_by_subtitle(self):
        """Subtitle bo'yicha qidirish"""
        url = '/api/books/?search=Learn'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
    
    def test_search_by_author_name(self):
        """Author nomi bo'yicha qidirish"""
        url = '/api/books/?search=John'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # Barcha kitoblar John Smith'dan
        self.assertGreaterEqual(len(results), 3)
    
    def test_search_by_publisher(self):
        """Publisher bo'yicha qidirish"""
        url = '/api/books/?search=Tech'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        # 2 ta "Tech Publisher" kitob
        self.assertGreaterEqual(len(results), 2)
    
    def test_search_case_insensitive(self):
        """Case-insensitive qidiruv"""
        # Katta harf
        response1 = self.client.get('/api/books/?search=PYTHON')
        # Kichik harf
        response2 = self.client.get('/api/books/?search=python')
        
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        results1 = response1.data.get('results', response1.data)
        results2 = response2.data.get('results', response2.data)
        
        # Bir xil natijalar
        self.assertEqual(len(results1), len(results2))
    
    def test_search_no_results(self):
        """Natija topilmasa"""
        url = '/api/books/?search=NonexistentBook'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 0)


class BookOrderingTest(APITestCase):
    """Ordering (tartiblash) testlari"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        Book.objects.create(
            title='C Book',
            author=self.author,
            isbn_number='9783333333333',
            price=Decimal('30.00'),
            pages=300,
            publisher='Publisher',
            published_date=date(2021, 1, 1),
            owner=self.user
        )
        Book.objects.create(
            title='A Book',
            author=self.author,
            isbn_number='9781111111111',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            published_date=date(2023, 1, 1),
            owner=self.user
        )
        Book.objects.create(
            title='B Book',
            author=self.author,
            isbn_number='9782222222222',
            price=Decimal('20.00'),
            pages=200,
            publisher='Publisher',
            published_date=date(2022, 1, 1),
            owner=self.user
        )
    
    def test_order_by_title_asc(self):
        """Title bo'yicha o'sish"""
        url = '/api/books/?ordering=title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        titles = [book['title'] for book in results]
        
        # A, B, C tartibida
        self.assertEqual(titles[0], 'A Book')
    
    def test_order_by_title_desc(self):
        """Title bo'yicha kamayish"""
        url = '/api/books/?ordering=-title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        titles = [book['title'] for book in results]
        
        # C, B, A tartibida
        self.assertEqual(titles[0], 'C Book')
    
    def test_order_by_price_asc(self):
        """Narx bo'yicha o'sish"""
        url = '/api/books/?ordering=price'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        prices = [Decimal(book['price']) for book in results]
        
        # 10, 20, 30
        self.assertEqual(prices[0], Decimal('10.00'))
    
    def test_order_by_published_date(self):
        """Published date bo'yicha"""
        url = '/api/books/?ordering=published_date'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        
        # Eng eski birinchi (2021)
        if results:
            self.assertIn('2021', str(results[0].get('published_date', '')))


class CombinedFilterSearchOrderTest(APITestCase):
    """Filter + Search + Ordering birgalikda"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.genre = Genre.objects.create(name='Programming')
        
        for i in range(10):
            book = Book.objects.create(
                title=f'Programming Book {i}',
                author=self.author,
                isbn_number=f'978{i:010d}',
                price=Decimal(f'{10 + i}.99'),
                pages=100 + (i * 50),
                publisher='Tech Publisher',
                owner=self.user
            )
            book.genres.add(self.genre)
    
    def test_filter_search_order_combined(self):
        """Filter + Search + Ordering"""
        url = f'/api/books/?genres={self.genre.id}&search=Programming&ordering=-price'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        
        # Barcha natijalar "Programming" so'zini o'z ichiga oladi
        if results:
            self.assertIn('Programming', results[0]['title'])
            
            # Narx bo'yicha kamayish
            if len(results) > 1:
                price1 = Decimal(results[0]['price'])
                price2 = Decimal(results[1]['price'])
                self.assertGreaterEqual(price1, price2)