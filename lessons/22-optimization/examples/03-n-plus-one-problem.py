"""
Example 3: N+1 Problem - Detection and Solution

Bu misolda N+1 problem nima, qanday aniqlash va hal qilishni ko'ramiz.
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection, reset_queries
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

class Category(models.Model):
    """Kategoriya modeli"""
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Author(models.Model):
    """Muallif modeli"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Kitob modeli"""
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        app_label = 'example'
    
    def __str__(self):
        return self.title


# ==================== HELPER FUNCTIONS ====================

def clear_queries():
    """Query log'ni tozalash"""
    connection.queries_log.clear()


def print_query_summary():
    """Query summary chiqarish"""
    query_count = len(connection.queries)
    print(f"\n{'='*60}")
    print(f"Total Queries Executed: {query_count}")
    print(f"{'='*60}")
    
    # Duplicate query'larni aniqlash
    query_patterns = {}
    for query in connection.queries:
        sql = query['sql'].split('WHERE')[0] if 'WHERE' in query['sql'] else query['sql']
        query_patterns[sql] = query_patterns.get(sql, 0) + 1
    
    duplicates = {k: v for k, v in query_patterns.items() if v > 1}
    
    if duplicates:
        print("\n⚠️  DUPLICATE QUERIES DETECTED (N+1 Problem!):")
        for pattern, count in duplicates.items():
            print(f"\n  Executed {count} times:")
            print(f"  {pattern[:100]}...")
    
    print(f"{'='*60}\n")
    return query_count


def create_test_data():
    """Test ma'lumotlarini yaratish"""
    print("Creating test data...")
    
    # Categories
    fiction = Category.objects.create(name='Fiction')
    non_fiction = Category.objects.create(name='Non-Fiction')
    science = Category.objects.create(name='Science')
    
    # Authors
    authors = [
        Author.objects.create(name=f'Author {i}', email=f'author{i}@example.com')
        for i in range(1, 11)
    ]
    
    # Books
    categories = [fiction, non_fiction, science]
    for i in range(1, 21):
        Book.objects.create(
            title=f'Book {i}',
            category=categories[i % 3],
            author=authors[i % 10],
            price=10.00 + i
        )
    
    print(f"Created {Category.objects.count()} categories")
    print(f"Created {Author.objects.count()} authors")
    print(f"Created {Book.objects.count()} books\n")


# ==================== EXAMPLES ====================

def example_1_classic_n_plus_one():
    """
    Misol 1: Klassik N+1 Problem
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: CLASSIC N+1 PROBLEM")
    print("="*70)
    print("\nSituation: Barcha kitoblar va ularning mualliflari ro'yxati\n")
    
    clear_queries()
    start_time = time.time()
    
    # Step 1: Barcha kitoblarni olish (1 query)
    books = Book.objects.all()
    print("✓ Fetched all books (1 query)")
    
    # Step 2: Har bir kitob uchun author olish (N query)
    print("\nAccessing author for each book:")
    for i, book in enumerate(books, 1):
        author_name = book.author.name  # Bu yerda N ta query!
        print(f"  {i}. {book.title} by {author_name}")
    
    elapsed = time.time() - start_time
    query_count = print_query_summary()
    
    print(f"⏱️  Time taken: {elapsed:.4f} seconds")
    print(f"📊 Formula: 1 (books) + {len(books)} (authors) = {query_count} queries")
    print(f"❌ This is N+1 Problem! {query_count} queries for {len(books)} books!")


def example_2_solution_select_related():
    """
    Misol 2: N+1 Problem yechimi - select_related()
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: SOLUTION WITH select_related()")
    print("="*70)
    print("\nUsing select_related() to JOIN authors\n")
    
    clear_queries()
    start_time = time.time()
    
    # select_related() bilan author'ni olish (1 query with JOIN)
    books = Book.objects.select_related('author').all()
    print("✓ Fetched all books WITH authors (1 query with JOIN)")
    
    print("\nAccessing author for each book:")
    for i, book in enumerate(books, 1):
        author_name = book.author.name  # Qo'shimcha query yo'q!
        print(f"  {i}. {book.title} by {author_name}")
    
    elapsed = time.time() - start_time
    query_count = print_query_summary()
    
    print(f"⏱️  Time taken: {elapsed:.4f} seconds")
    print(f"📊 Only 1 query with JOIN!")
    print(f"✅ Problem solved! {query_count} query instead of 21!")


def example_3_multiple_relationships():
    """
    Misol 3: Ko'p relationships - N+M problem
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: MULTIPLE RELATIONSHIPS (N+M Problem)")
    print("="*70)
    print("\nAccessing both author AND category\n")
    
    clear_queries()
    start_time = time.time()
    
    # Optimizatsiyasiz
    books = Book.objects.all()
    
    print("Accessing multiple relationships:")
    for i, book in enumerate(books, 1):
        author = book.author.name  # N queries
        category = book.category.name  # M queries
        print(f"  {i}. {book.title} - {author} ({category})")
    
    elapsed = time.time() - start_time
    query_count = print_query_summary()
    
    print(f"⏱️  Time taken: {elapsed:.4f} seconds")
    print(f"📊 Formula: 1 + N + M = {query_count} queries")
    print(f"❌ Even worse! Multiple N+1 problems combined!")


def example_4_solution_multiple_select():
    """
    Misol 4: Ko'p relationships yechimi
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: SOLUTION FOR MULTIPLE RELATIONSHIPS")
    print("="*70)
    print("\nUsing select_related() for multiple ForeignKeys\n")
    
    clear_queries()
    start_time = time.time()
    
    # Ko'p select_related()
    books = Book.objects.select_related('author', 'category').all()
    
    print("Accessing multiple relationships:")
    for i, book in enumerate(books, 1):
        author = book.author.name
        category = book.category.name
        print(f"  {i}. {book.title} - {author} ({category})")
    
    elapsed = time.time() - start_time
    query_count = print_query_summary()
    
    print(f"⏱️  Time taken: {elapsed:.4f} seconds")
    print(f"📊 Only {query_count} query with multiple JOINs!")
    print(f"✅ All relationships fetched in one go!")


def example_5_hidden_n_plus_one():
    """
    Misol 5: Yashirin N+1 - Serializer'da
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: HIDDEN N+1 IN COMPUTED PROPERTIES")
    print("="*70)
    print("\nN+1 can hide in computed properties!\n")
    
    # Book modeliga method qo'shamiz (simulation)
    def get_author_email(book):
        return book.author.email
    
    clear_queries()
    
    books = Book.objects.all()
    
    print("Getting computed values:")
    for i, book in enumerate(books, 1):
        email = get_author_email(book)  # Hidden N+1!
        print(f"  {i}. {book.title} - Contact: {email}")
    
    query_count = print_query_summary()
    
    print(f"⚠️  Computed properties can cause hidden N+1!")
    print(f"❌ {query_count} queries for {len(books)} books!")


def example_6_detecting_n_plus_one():
    """
    Misol 6: N+1 ni qanday aniqlash
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: HOW TO DETECT N+1 PROBLEM")
    print("="*70)
    
    print("\n📋 Detection Methods:\n")
    
    print("1. Django Debug Toolbar:")
    print("   - Install: pip install django-debug-toolbar")
    print("   - Look for 'Similar queries' or 'Duplicate queries'")
    print("   - Check query count on list pages\n")
    
    print("2. Query Logging:")
    print("   - Enable SQL logging in settings.py")
    print("   - Look for repeated similar queries")
    print("   - Count queries in loops\n")
    
    print("3. Manual Inspection:")
    clear_queries()
    books = Book.objects.all()[:5]
    for book in books:
        _ = book.author.name
    count = len(connection.queries)
    
    print(f"   - Got {len(list(books))} books")
    print(f"   - Made {count} queries")
    print(f"   - If queries ≈ objects + 1, you have N+1!\n")
    
    print("4. Performance Testing:")
    print("   - Measure query count with different data sizes")
    print("   - If queries grow linearly with data → N+1 problem")


def example_7_best_practices():
    """
    Misol 7: Best Practices
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: BEST PRACTICES TO AVOID N+1")
    print("="*70)
    
    print("\n✅ DO:\n")
    
    # 1. Use select_related for FK
    clear_queries()
    books = Book.objects.select_related('author', 'category').all()
    for book in books[:3]:
        print(f"✓ {book.title} by {book.author.name}")
    count1 = len(connection.queries)
    
    print(f"\n  1. Use select_related() for ForeignKey ({count1} query)\n")
    
    # 2. Use prefetch_related for M2M
    print("  2. Use prefetch_related() for ManyToMany")
    print("  3. Profile queries regularly")
    print("  4. Use Django Debug Toolbar in development")
    print("  5. Write tests to catch N+1 problems\n")
    
    print("❌ DON'T:\n")
    print("  1. Access related objects in loops without optimization")
    print("  2. Ignore duplicate queries in Debug Toolbar")
    print("  3. Assume small data sets won't cause problems")
    print("  4. Use .all() without select/prefetch_related\n")


def example_8_performance_comparison():
    """
    Misol 8: Real-world performance comparison
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: REAL-WORLD PERFORMANCE COMPARISON")
    print("="*70)
    
    # Test with different sizes
    sizes = [10, 20, 50]
    
    print("\nTesting with different data sizes:\n")
    print(f"{'Size':<10} {'Without Optimization':<30} {'With Optimization':<30}")
    print("-" * 70)
    
    for size in sizes:
        # Without optimization
        clear_queries()
        start = time.time()
        books = list(Book.objects.all()[:size])
        for book in books:
            _ = book.author.name
            _ = book.category.name
        time_without = time.time() - start
        queries_without = len(connection.queries)
        
        # With optimization
        clear_queries()
        start = time.time()
        books = list(Book.objects.select_related('author', 'category').all()[:size])
        for book in books:
            _ = book.author.name
            _ = book.category.name
        time_with = time.time() - start
        queries_with = len(connection.queries)
        
        print(f"{size:<10} {queries_without} queries ({time_without:.4f}s){' '*8} "
              f"{queries_with} query ({time_with:.4f}s)")
    
    print("\n💡 Notice: Query count grows linearly without optimization!")


# ==================== MAIN ====================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "="*70)
    print("N+1 PROBLEM: DETECTION AND SOLUTION")
    print("="*70)
    
    # Database yaratish
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    # Test ma'lumotlari yaratish
    create_test_data()
    
    # Misollar
    example_1_classic_n_plus_one()
    example_2_solution_select_related()
    example_3_multiple_relationships()
    example_4_solution_multiple_select()
    example_5_hidden_n_plus_one()
    example_6_detecting_n_plus_one()
    example_7_best_practices()
    example_8_performance_comparison()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS:")
    print("="*70)
    print("1. N+1 Problem - eng keng tarqalgan performance issue")
    print("2. Har bir loop'da related object access = potential N+1")
    print("3. select_related() - ForeignKey uchun yechim")
    print("4. Debug Toolbar - aniqlash uchun eng yaxshi vosita")
    print("5. Doim query count monitoring qiling!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()