"""
Example 1: select_related() - ForeignKey Optimization

Bu misolda ForeignKey relationships uchun select_related() qanday
ishlashini va N+1 problemni qanday hal qilishini ko'ramiz.
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
from django.db.models import QuerySet
import time

# Django sozlamalari
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        LOGGING={
            'version': 1,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                'django.db.backends': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                },
            },
        },
    )
    django.setup()

from django.db import models


# ==================== MODELS ====================

class Country(models.Model):
    """Mamlakat modeli"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Author(models.Model):
    """Muallif modeli"""
    name = models.CharField(max_length=200)
    bio = models.TextField()
    birth_date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='authors')
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Nashriyot modeli"""
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='publishers')
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Kitob modeli"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    pages = models.IntegerField()
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.title


# ==================== HELPER FUNCTIONS ====================

def reset_queries():
    """Query count'ni reset qilish"""
    connection.queries_log.clear()


def print_queries():
    """Barcha query'larni chiqarish"""
    print(f"\n{'='*60}")
    print(f"Total Queries: {len(connection.queries)}")
    print(f"{'='*60}")
    for i, query in enumerate(connection.queries, 1):
        print(f"\nQuery {i}:")
        print(query['sql'][:200] + '...' if len(query['sql']) > 200 else query['sql'])
    print(f"{'='*60}\n")


def create_test_data():
    """Test ma'lumotlarini yaratish"""
    print("Creating test data...")
    
    # Countries
    usa = Country.objects.create(name='USA', code='US')
    uk = Country.objects.create(name='United Kingdom', code='GB')
    france = Country.objects.create(name='France', code='FR')
    
    # Authors
    author1 = Author.objects.create(
        name='Ernest Hemingway',
        bio='American novelist',
        birth_date='1899-07-21',
        country=usa
    )
    author2 = Author.objects.create(
        name='George Orwell',
        bio='English novelist',
        birth_date='1903-06-25',
        country=uk
    )
    author3 = Author.objects.create(
        name='Victor Hugo',
        bio='French poet',
        birth_date='1802-02-26',
        country=france
    )
    
    # Publishers
    publisher1 = Publisher.objects.create(name='Scribner', country=usa)
    publisher2 = Publisher.objects.create(name='Penguin Books', country=uk)
    publisher3 = Publisher.objects.create(name='Flammarion', country=france)
    
    # Books
    Book.objects.create(
        title='The Old Man and the Sea',
        author=author1,
        publisher=publisher1,
        published_date='1952-09-01',
        pages=127
    )
    Book.objects.create(
        title='A Farewell to Arms',
        author=author1,
        publisher=publisher1,
        published_date='1929-09-27',
        pages=332
    )
    Book.objects.create(
        title='1984',
        author=author2,
        publisher=publisher2,
        published_date='1949-06-08',
        pages=328
    )
    Book.objects.create(
        title='Animal Farm',
        author=author2,
        publisher=publisher2,
        published_date='1945-08-17',
        pages=112
    )
    Book.objects.create(
        title='Les Misérables',
        author=author3,
        publisher=publisher3,
        published_date='1862-03-31',
        pages=1463
    )
    
    print("Test data created!\n")


# ==================== EXAMPLES ====================

def example_1_without_optimization():
    """
    Misol 1: Optimizatsiyasiz - N+1 Problem
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: WITHOUT OPTIMIZATION (N+1 Problem)")
    print("="*60)
    
    reset_queries()
    start_time = time.time()
    
    # Barcha kitoblarni olish
    books = Book.objects.all()
    
    # Har bir kitob uchun muallif va nashriyot ma'lumotlarini chiqarish
    for book in books:
        print(f"{book.title} by {book.author.name} ({book.publisher.name})")
    
    end_time = time.time()
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print_queries()
    
    """
    Natija:
    - 1 ta query: Barcha kitoblarni olish
    - N ta query: Har bir kitob uchun author
    - N ta query: Har bir kitob uchun publisher
    Total: 1 + N + N = 1 + 10 = 11 queries ❌
    """


def example_2_with_select_related():
    """
    Misol 2: select_related() bilan - Optimizatsiya qilingan
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: WITH select_related() (OPTIMIZED)")
    print("="*60)
    
    reset_queries()
    start_time = time.time()
    
    # select_related() bilan author va publisher'ni olish
    books = Book.objects.select_related('author', 'publisher').all()
    
    # Har bir kitob ma'lumotlarini chiqarish
    for book in books:
        print(f"{book.title} by {book.author.name} ({book.publisher.name})")
    
    end_time = time.time()
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print_queries()
    
    """
    Natija:
    - 1 ta query: Books + JOIN authors + JOIN publishers
    Total: 1 query! ✅
    """


def example_3_nested_select_related():
    """
    Misol 3: Nested select_related() - Chuqur relationships
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: NESTED select_related()")
    print("="*60)
    
    reset_queries()
    start_time = time.time()
    
    # Author'ning country'sini ham olish
    books = Book.objects.select_related(
        'author__country',  # Author va uning country'si
        'publisher__country'  # Publisher va uning country'si
    ).all()
    
    # Ma'lumotlarni chiqarish
    for book in books:
        print(f"{book.title}")
        print(f"  Author: {book.author.name} from {book.author.country.name}")
        print(f"  Publisher: {book.publisher.name} from {book.publisher.country.name}")
        print()
    
    end_time = time.time()
    
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    print_queries()
    
    """
    Natija:
    - 1 ta query: Books + JOIN authors + JOIN author countries + 
                  JOIN publishers + JOIN publisher countries
    Total: 1 query! ✅
    """


def example_4_partial_select_related():
    """
    Misol 4: Qisman select_related() - Faqat keraklisini olish
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: PARTIAL select_related()")
    print("="*60)
    
    reset_queries()
    
    # Faqat author'ni optimize qilish
    books = Book.objects.select_related('author').all()
    
    for book in books:
        # Author uchun query yo'q (optimized)
        print(f"{book.title} by {book.author.name}")
        # Publisher uchun query boradi (not optimized)
        # print(f"Publisher: {book.publisher.name}")  # Bu qo'shimcha query yaratadi
    
    print_queries()
    
    """
    Natija:
    - select_related() faqat ko'rsatilgan fieldlar uchun ishlaydi
    - Boshqa fieldlarga murojaat qilsak, qo'shimcha query bo'ladi
    """


def example_5_performance_comparison():
    """
    Misol 5: Performance Comparison - Before vs After
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: PERFORMANCE COMPARISON")
    print("="*60)
    
    iterations = 3
    
    # WITHOUT optimization
    reset_queries()
    start_time = time.time()
    for _ in range(iterations):
        books = Book.objects.all()
        list(books)  # Force evaluation
        for book in books:
            _ = book.author.name
            _ = book.publisher.name
    without_time = time.time() - start_time
    without_queries = len(connection.queries)
    
    # WITH optimization
    reset_queries()
    start_time = time.time()
    for _ in range(iterations):
        books = Book.objects.select_related('author', 'publisher').all()
        list(books)  # Force evaluation
        for book in books:
            _ = book.author.name
            _ = book.publisher.name
    with_time = time.time() - start_time
    with_queries = len(connection.queries)
    
    # Results
    print("\nResults:")
    print(f"{'Method':<30} {'Queries':<15} {'Time':<15}")
    print("-" * 60)
    print(f"{'Without select_related()':<30} {without_queries:<15} {without_time:.4f}s")
    print(f"{'With select_related()':<30} {with_queries:<15} {with_time:.4f}s")
    print("-" * 60)
    print(f"{'Improvement:':<30} {'-'}{without_queries - with_queries} queries   {'-'}{without_time - with_time:.4f}s")
    print(f"{'Percentage:':<30} {((without_queries - with_queries) / without_queries * 100):.1f}%")


# ==================== MAIN ====================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "="*60)
    print("SELECT_RELATED() EXAMPLES")
    print("="*60)
    
    # Database yaratish
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    # Test ma'lumotlari yaratish
    create_test_data()
    
    # Misollar
    example_1_without_optimization()
    example_2_with_select_related()
    example_3_nested_select_related()
    example_4_partial_select_related()
    example_5_performance_comparison()
    
    print("\n" + "="*60)
    print("KEY TAKEAWAYS:")
    print("="*60)
    print("1. select_related() - ForeignKey uchun ishlatiladi")
    print("2. SQL JOIN operatsiyasi orqali ishlaydi")
    print("3. N+1 problemni hal qiladi")
    print("4. Nested relationships ham qo'llab-quvvatlanadi")
    print("5. Performance'ni sezilarli darajada oshiradi")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()