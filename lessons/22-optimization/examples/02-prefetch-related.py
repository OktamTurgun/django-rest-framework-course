"""
Example 2: prefetch_related() - ManyToMany Optimization

Bu misolda ManyToMany relationships va reverse ForeignKey uchun
prefetch_related() qanday ishlashini ko'ramiz.
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
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
from django.db.models import Prefetch


# ==================== MODELS ====================

class Author(models.Model):
    """Muallif modeli"""
    name = models.CharField(max_length=200)
    bio = models.TextField()
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    """Janr modeli"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Teg modeli"""
    name = models.CharField(max_length=50)
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Kitob modeli"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    tags = models.ManyToManyField(Tag, related_name='books')
    published_date = models.DateField()
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.title


class Review(models.Model):
    """Sharh modeli"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return f"Review for {self.book.title}"


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
        sql = query['sql']
        print(sql[:200] + '...' if len(sql) > 200 else sql)
    print(f"{'='*60}\n")


def create_test_data():
    """Test ma'lumotlarini yaratish"""
    print("Creating test data...")
    
    # Authors
    author1 = Author.objects.create(name='J.K. Rowling', bio='British author')
    author2 = Author.objects.create(name='George R.R. Martin', bio='American novelist')
    
    # Genres
    fantasy = Genre.objects.create(name='Fantasy', description='Fantasy genre', is_active=True)
    adventure = Genre.objects.create(name='Adventure', description='Adventure genre', is_active=True)
    drama = Genre.objects.create(name='Drama', description='Drama genre', is_active=True)
    thriller = Genre.objects.create(name='Thriller', description='Thriller genre', is_active=False)
    
    # Tags
    magic = Tag.objects.create(name='Magic')
    dragons = Tag.objects.create(name='Dragons')
    war = Tag.objects.create(name='War')
    medieval = Tag.objects.create(name='Medieval')
    
    # Books
    book1 = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone",
        author=author1,
        published_date='1997-06-26'
    )
    book1.genres.add(fantasy, adventure)
    book1.tags.add(magic)
    
    book2 = Book.objects.create(
        title='Harry Potter and the Chamber of Secrets',
        author=author1,
        published_date='1998-07-02'
    )
    book2.genres.add(fantasy, adventure)
    book2.tags.add(magic)
    
    book3 = Book.objects.create(
        title='A Game of Thrones',
        author=author2,
        published_date='1996-08-01'
    )
    book3.genres.add(fantasy, drama)
    book3.tags.add(dragons, war, medieval)
    
    book4 = Book.objects.create(
        title='A Clash of Kings',
        author=author2,
        published_date='1998-11-16'
    )
    book4.genres.add(fantasy, drama)
    book4.tags.add(dragons, war, medieval)
    
    # Reviews
    Review.objects.create(book=book1, rating=5, comment='Excellent!')
    Review.objects.create(book=book1, rating=4, comment='Very good')
    Review.objects.create(book=book2, rating=5, comment='Amazing!')
    Review.objects.create(book=book3, rating=5, comment='Epic!')
    Review.objects.create(book=book3, rating=4, comment='Great story')
    Review.objects.create(book=book3, rating=5, comment='Best fantasy!')
    
    print("Test data created!\n")


# ==================== EXAMPLES ====================

def example_1_without_optimization():
    """
    Misol 1: Optimizatsiyasiz - ManyToMany N+1 Problem
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: WITHOUT OPTIMIZATION (ManyToMany N+1)")
    print("="*60)
    
    reset_queries()
    start_time = time.time()
    
    # Barcha kitoblarni olish
    books = Book.objects.all()
    
    # Har bir kitob uchun janrlarni chiqarish
    for book in books:
        print(f"\n{book.title}")
        print(f"  Genres: {', '.join(g.name for g in book.genres.all())}")
        print(f"  Tags: {', '.join(t.name for t in book.tags.all())}")
    
    end_time = time.time()
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print_queries()
    
    """
    Natija:
    - 1 ta query: Barcha kitoblarni olish
    - N ta query: Har bir kitob uchun genres
    - N ta query: Har bir kitob uchun tags
    Total: 1 + N + N = 9 queries ❌
    """


def example_2_with_prefetch_related():
    """
    Misol 2: prefetch_related() bilan - Optimizatsiya qilingan
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: WITH prefetch_related() (OPTIMIZED)")
    print("="*60)
    
    reset_queries()
    start_time = time.time()
    
    # prefetch_related() bilan genres va tags'ni olish
    books = Book.objects.prefetch_related('genres', 'tags').all()
    
    # Ma'lumotlarni chiqarish
    for book in books:
        print(f"\n{book.title}")
        print(f"  Genres: {', '.join(g.name for g in book.genres.all())}")
        print(f"  Tags: {', '.join(t.name for t in book.tags.all())}")
    
    end_time = time.time()
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print_queries()
    
    """
    Natija:
    - 1 ta query: Barcha kitoblarni olish
    - 1 ta query: Barcha genres'ni olish
    - 1 ta query: Barcha tags'ni olish
    Total: 3 queries! ✅
    """


def example_3_reverse_fk_prefetch():
    """
    Misol 3: Reverse ForeignKey prefetch - Author'ning kitoblari
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: REVERSE FOREIGNKEY PREFETCH")
    print("="*60)
    
    reset_queries()
    
    # Har bir author'ning kitoblarini olish (optimized)
    authors = Author.objects.prefetch_related('books').all()
    
    for author in authors:
        print(f"\n{author.name}:")
        for book in author.books.all():
            print(f"  - {book.title}")
    
    print_queries()
    
    """
    Natija:
    - 1 ta query: Barcha authorlarni olish
    - 1 ta query: Barcha books'ni olish (WHERE author_id IN (...))
    Total: 2 queries! ✅
    """


def example_4_custom_prefetch():
    """
    Misol 4: Custom Prefetch - Faqat active genrelar
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: CUSTOM PREFETCH (Active Genres Only)")
    print("="*60)
    
    reset_queries()
    
    # Faqat active genrelarni prefetch qilish
    active_genres = Genre.objects.filter(is_active=True)
    
    books = Book.objects.prefetch_related(
        Prefetch('genres', queryset=active_genres, to_attr='active_genres')
    ).all()
    
    for book in books:
        print(f"\n{book.title}")
        print(f"  Active Genres: {', '.join(g.name for g in book.active_genres)}")
    
    print_queries()
    
    """
    Natija:
    - Custom queryset bilan filter qilish mumkin
    - to_attr bilan yangi attribute yaratish mumkin
    """


def example_5_nested_prefetch():
    """
    Misol 5: Nested Prefetch - Author -> Books -> Genres
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: NESTED PREFETCH")
    print("="*60)
    
    reset_queries()
    
    # Author -> Books -> Genres (nested prefetch)
    authors = Author.objects.prefetch_related(
        Prefetch(
            'books',
            queryset=Book.objects.prefetch_related('genres')
        )
    ).all()
    
    for author in authors:
        print(f"\n{author.name}:")
        for book in author.books.all():
            print(f"  {book.title}")
            print(f"    Genres: {', '.join(g.name for g in book.genres.all())}")
    
    print_queries()
    
    """
    Natija:
    - 1 ta query: Authors
    - 1 ta query: Books
    - 1 ta query: Genres (for all books)
    Total: 3 queries! ✅
    """


def example_6_combined_optimization():
    """
    Misol 6: select_related + prefetch_related birgalikda
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: COMBINED OPTIMIZATION")
    print("="*60)
    
    reset_queries()
    
    # select_related (ForeignKey) + prefetch_related (ManyToMany)
    books = Book.objects.select_related('author').prefetch_related(
        'genres', 
        'tags',
        'reviews'
    ).all()
    
    for book in books:
        print(f"\n{book.title}")
        print(f"  Author: {book.author.name}")
        print(f"  Genres: {', '.join(g.name for g in book.genres.all())}")
        print(f"  Tags: {', '.join(t.name for t in book.tags.all())}")
        print(f"  Reviews: {book.reviews.count()} reviews")
    
    print_queries()
    
    """
    Natija:
    - 1 ta query: Books + JOIN author
    - 1 ta query: Genres
    - 1 ta query: Tags
    - 1 ta query: Reviews
    Total: 4 queries! ✅
    """


def example_7_performance_comparison():
    """
    Misol 7: Performance Comparison
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: PERFORMANCE COMPARISON")
    print("="*60)
    
    iterations = 3
    
    # WITHOUT prefetch
    reset_queries()
    start_time = time.time()
    for _ in range(iterations):
        books = Book.objects.all()
        for book in books:
            list(book.genres.all())
            list(book.tags.all())
    without_time = time.time() - start_time
    without_queries = len(connection.queries)
    
    # WITH prefetch
    reset_queries()
    start_time = time.time()
    for _ in range(iterations):
        books = Book.objects.prefetch_related('genres', 'tags').all()
        for book in books:
            list(book.genres.all())
            list(book.tags.all())
    with_time = time.time() - start_time
    with_queries = len(connection.queries)
    
    # Results
    print("\nResults:")
    print(f"{'Method':<30} {'Queries':<15} {'Time':<15}")
    print("-" * 60)
    print(f"{'Without prefetch_related()':<30} {without_queries:<15} {without_time:.4f}s")
    print(f"{'With prefetch_related()':<30} {with_queries:<15} {with_time:.4f}s")
    print("-" * 60)
    print(f"{'Improvement:':<30} {'-'}{without_queries - with_queries} queries   {'-'}{without_time - with_time:.4f}s")
    print(f"{'Percentage:':<30} {((without_queries - with_queries) / without_queries * 100):.1f}%")


# ==================== MAIN ====================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "="*60)
    print("PREFETCH_RELATED() EXAMPLES")
    print("="*60)
    
    # Database yaratish
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    # Test ma'lumotlari yaratish
    create_test_data()
    
    # Misollar
    example_1_without_optimization()
    example_2_with_prefetch_related()
    example_3_reverse_fk_prefetch()
    example_4_custom_prefetch()
    example_5_nested_prefetch()
    example_6_combined_optimization()
    example_7_performance_comparison()
    
    print("\n" + "="*60)
    print("KEY TAKEAWAYS:")
    print("="*60)
    print("1. prefetch_related() - ManyToMany va Reverse FK uchun")
    print("2. Alohida query'lar ishlatadi (JOIN emas)")
    print("3. Python'da relationship'larni birlashtiradi")
    print("4. Prefetch() obyekti bilan custom filter mumkin")
    print("5. select_related() bilan birgalikda ishlatish mumkin")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()