"""
Example 4: Database Indexes - Performance Optimization

Bu misolda database indexlar qanday ishlashi va performance'ga
qanday ta'sir qilishini ko'ramiz.
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
import time
import random
from datetime import datetime, timedelta

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
    )
    django.setup()

from django.db import models


# ==================== MODELS ====================

class BookWithoutIndex(models.Model):
    """Index'siz kitob modeli - Comparison uchun"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    
    class Meta:
        app_label = 'example'
        db_table = 'books_without_index'


class BookWithIndex(models.Model):
    """Index'li kitob modeli - Optimized"""
    title = models.CharField(max_length=200, db_index=True)
    author = models.CharField(max_length=200, db_index=True)
    isbn = models.CharField(max_length=13, unique=True)  # Unique auto-creates index
    published_date = models.DateField(db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(db_index=True)
    
    class Meta:
        app_label = 'example'
        db_table = 'books_with_index'
        indexes = [
            # Single field indexes
            models.Index(fields=['price'], name='idx_price'),
            
            # Composite indexes
            models.Index(fields=['author', 'published_date'], name='idx_author_date'),
            models.Index(fields=['title', 'author'], name='idx_title_author'),
            
            # Descending index for ordering
            models.Index(fields=['-published_date'], name='idx_date_desc'),
        ]


# ==================== HELPER FUNCTIONS ====================

def create_test_data(count=1000):
    """
    Ko'p miqdorda test ma'lumotlari yaratish
    """
    print(f"Creating {count} test records...")
    
    authors = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams', 'Charlie Brown']
    
    # Without index
    books_without = []
    for i in range(count):
        books_without.append(BookWithoutIndex(
            title=f'Book Title {i}',
            author=random.choice(authors),
            isbn=f'978{i:010d}',
            published_date=datetime.now().date() - timedelta(days=random.randint(0, 3650)),
            price=random.uniform(10, 100),
            stock=random.randint(0, 100)
        ))
    BookWithoutIndex.objects.bulk_create(books_without)
    
    # With index
    books_with = []
    for i in range(count):
        books_with.append(BookWithIndex(
            title=f'Book Title {i}',
            author=random.choice(authors),
            isbn=f'979{i:010d}',
            published_date=datetime.now().date() - timedelta(days=random.randint(0, 3650)),
            price=random.uniform(10, 100),
            stock=random.randint(0, 100)
        ))
    BookWithIndex.objects.bulk_create(books_with)
    
    print(f"✓ Created {count} records for each model\n")


def measure_query_time(query_func, label):
    """Query vaqtini o'lchash"""
    connection.queries_log.clear()
    start_time = time.time()
    result = query_func()
    elapsed = time.time() - start_time
    
    print(f"{label:<50} {elapsed*1000:.2f} ms")
    return elapsed, result


# ==================== EXAMPLES ====================

def example_1_filter_performance():
    """
    Misol 1: Filter performance - Indexed vs Non-indexed
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: FILTER PERFORMANCE COMPARISON")
    print("="*70)
    print("\nFiltering by author (frequently filtered field):\n")
    
    author = 'John Doe'
    
    # Without index
    time_without, _ = measure_query_time(
        lambda: list(BookWithoutIndex.objects.filter(author=author)),
        "WITHOUT index (full table scan):"
    )
    
    # With index
    time_with, _ = measure_query_time(
        lambda: list(BookWithIndex.objects.filter(author=author)),
        "WITH index (index lookup):"
    )
    
    improvement = ((time_without - time_with) / time_without) * 100
    print(f"\n💡 Performance improvement: {improvement:.1f}% faster with index!")


def example_2_ordering_performance():
    """
    Misol 2: Ordering performance
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: ORDERING PERFORMANCE")
    print("="*70)
    print("\nOrdering by published_date (indexed field):\n")
    
    # Without index
    time_without, _ = measure_query_time(
        lambda: list(BookWithoutIndex.objects.order_by('-published_date')[:100]),
        "WITHOUT index on published_date:"
    )
    
    # With index
    time_with, _ = measure_query_time(
        lambda: list(BookWithIndex.objects.order_by('-published_date')[:100]),
        "WITH index on published_date:"
    )
    
    improvement = ((time_without - time_with) / time_without) * 100
    print(f"\n💡 Ordering improvement: {improvement:.1f}% faster with index!")


def example_3_unique_lookup():
    """
    Misol 3: Unique field lookup (ISBN)
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: UNIQUE FIELD LOOKUP (ISBN)")
    print("="*70)
    print("\nLooking up by unique ISBN field:\n")
    
    # Without unique index
    time_without, _ = measure_query_time(
        lambda: BookWithoutIndex.objects.get(isbn='9780000000500'),
        "WITHOUT unique index:"
    )
    
    # With unique index
    time_with, _ = measure_query_time(
        lambda: BookWithIndex.objects.get(isbn='9790000000500'),
        "WITH unique index:"
    )
    
    print(f"\n💡 Unique constraint automatically creates index!")


def example_4_composite_index():
    """
    Misol 4: Composite index (multi-column)
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: COMPOSITE INDEX (MULTI-COLUMN)")
    print("="*70)
    print("\nFiltering by author AND published_date:\n")
    
    author = 'Jane Smith'
    date = datetime.now().date() - timedelta(days=365)
    
    # Without composite index
    time_without, _ = measure_query_time(
        lambda: list(BookWithoutIndex.objects.filter(
            author=author,
            published_date__gte=date
        )),
        "WITHOUT composite index:"
    )
    
    # With composite index
    time_with, _ = measure_query_time(
        lambda: list(BookWithIndex.objects.filter(
            author=author,
            published_date__gte=date
        )),
        "WITH composite index (author, published_date):"
    )
    
    print(f"\n💡 Composite indexes help when filtering multiple fields together!")


def example_5_range_queries():
    """
    Misol 5: Range queries bilan indexlar
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: RANGE QUERIES WITH INDEXES")
    print("="*70)
    print("\nRange query on stock field:\n")
    
    # Without index
    time_without, _ = measure_query_time(
        lambda: list(BookWithoutIndex.objects.filter(stock__gte=50, stock__lte=100)),
        "WITHOUT index on stock:"
    )
    
    # With index
    time_with, _ = measure_query_time(
        lambda: list(BookWithIndex.objects.filter(stock__gte=50, stock__lte=100)),
        "WITH index on stock:"
    )
    
    print(f"\n💡 Indexes significantly speed up range queries!")


def example_6_when_indexes_help():
    """
    Misol 6: Qachon indexlar yordam beradi
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: WHEN DO INDEXES HELP?")
    print("="*70)
    
    print("\n✅ Indexes are beneficial for:\n")
    
    # 1. WHERE clauses
    print("1. WHERE clauses (filter):")
    _, result = measure_query_time(
        lambda: list(BookWithIndex.objects.filter(author='John Doe')),
        "   SELECT * WHERE author = 'John Doe'"
    )
    
    # 2. ORDER BY
    print("\n2. ORDER BY clauses (ordering):")
    _, result = measure_query_time(
        lambda: list(BookWithIndex.objects.order_by('published_date')[:10]),
        "   SELECT * ORDER BY published_date"
    )
    
    # 3. JOIN operations (FK are auto-indexed)
    print("\n3. JOIN operations (ForeignKey relationships)")
    print("   ForeignKey fields are automatically indexed")
    
    # 4. UNIQUE constraints
    print("\n4. UNIQUE constraints:")
    print("   Unique fields automatically get indexes")
    
    print("\n\n❌ Indexes DON'T help much for:\n")
    print("1. Small tables (< 1000 rows)")
    print("2. Fields with low cardinality (few unique values)")
    print("3. Fields that are rarely queried")
    print("4. Write-heavy tables (indexes slow down INSERTs)")


def example_7_index_overhead():
    """
    Misol 7: Index overhead - Write operations
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: INDEX OVERHEAD ON WRITES")
    print("="*70)
    print("\nComparing INSERT performance:\n")
    
    # Bulk create without indexes
    books_without = [
        BookWithoutIndex(
            title=f'New Book {i}',
            author='Test Author',
            isbn=f'000{i:010d}',
            published_date=datetime.now().date(),
            price=50.00,
            stock=10
        ) for i in range(100)
    ]
    
    time_without, _ = measure_query_time(
        lambda: BookWithoutIndex.objects.bulk_create(books_without),
        "INSERT 100 rows WITHOUT indexes:"
    )
    
    # Bulk create with indexes
    books_with = [
        BookWithIndex(
            title=f'New Book {i}',
            author='Test Author',
            isbn=f'999{i:010d}',
            published_date=datetime.now().date(),
            price=50.00,
            stock=10
        ) for i in range(100)
    ]
    
    time_with, _ = measure_query_time(
        lambda: BookWithIndex.objects.bulk_create(books_with),
        "INSERT 100 rows WITH indexes:"
    )
    
    overhead = ((time_with - time_without) / time_without) * 100
    print(f"\n⚠️  Index overhead on writes: {overhead:.1f}% slower")
    print("💡 Trade-off: Faster reads vs slower writes")


def example_8_index_best_practices():
    """
    Misol 8: Index best practices
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: INDEX BEST PRACTICES")
    print("="*70)
    
    print("""
✅ DO:

1. Index frequently filtered fields:
   class Book(models.Model):
       title = models.CharField(max_length=200, db_index=True)
       published_date = models.DateField(db_index=True)

2. Index fields used in ORDER BY:
   class Meta:
       indexes = [
           models.Index(fields=['-created_at']),
       ]

3. Use composite indexes for multiple field queries:
   class Meta:
       indexes = [
           models.Index(fields=['author', 'published_date']),
       ]

4. Index ForeignKey fields (automatic):
   author = models.ForeignKey(Author, on_delete=models.CASCADE)

5. Use unique=True when appropriate:
   isbn = models.CharField(max_length=13, unique=True)


❌ DON'T:

1. Don't index everything:
   - More indexes = slower writes
   - More storage space needed

2. Don't index low-cardinality fields:
   - Boolean fields (only 2 values)
   - Status fields with few options

3. Don't index rarely queried fields:
   - Internal fields
   - Fields only used in admin

4. Don't index small tables:
   - < 1000 rows won't benefit much

5. Don't forget to remove unused indexes:
   - Monitor query patterns
   - Drop indexes that aren't used


📊 Monitoring Indexes:

1. Check query performance:
   python manage.py shell
   >>> from django.db import connection
   >>> print(connection.queries)

2. Use EXPLAIN:
   >>> Book.objects.filter(author='John').explain()

3. Use Django Debug Toolbar:
   - Shows which indexes are used
   - Highlights missing indexes

4. Database-specific tools:
   - PostgreSQL: EXPLAIN ANALYZE
   - MySQL: SHOW INDEX FROM table_name
   - SQLite: .indexes table_name
""")


def example_9_creating_indexes():
    """
    Misol 9: Index'lar yaratish va migration
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: CREATING INDEXES IN DJANGO")
    print("="*70)
    
    print("""
Method 1: db_index parameter
─────────────────────────────
class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    published_date = models.DateField(db_index=True)


Method 2: Meta.indexes
──────────────────────
class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['published_date'], name='idx_pub_date'),
            models.Index(fields=['-published_date']),  # Descending
            models.Index(fields=['author', 'published_date'], name='idx_author_date'),
        ]


Method 3: unique=True
─────────────────────
class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    # Automatically creates unique index


Migration Process:
──────────────────
1. Add index to model
2. Run: python manage.py makemigrations
3. Run: python manage.py migrate

Example migration:
─────────────────
class Migration(migrations.Migration):
    operations = [
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['published_date'], name='idx_pub_date'),
        ),
    ]


Removing Indexes:
────────────────
1. Remove index from model
2. Run: python manage.py makemigrations
3. Run: python manage.py migrate

Or manually:
migrations.RemoveIndex(
    model_name='book',
    name='idx_pub_date',
),
""")


# ==================== MAIN ====================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "="*70)
    print("DATABASE INDEXES - PERFORMANCE OPTIMIZATION")
    print("="*70)
    
    # Database yaratish
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    # Test ma'lumotlari yaratish
    create_test_data(count=1000)
    
    # Misollar
    example_1_filter_performance()
    example_2_ordering_performance()
    example_3_unique_lookup()
    example_4_composite_index()
    example_5_range_queries()
    example_6_when_indexes_help()
    example_7_index_overhead()
    example_8_index_best_practices()
    example_9_creating_indexes()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS:")
    print("="*70)
    print("1. Indexes dramatically speed up SELECT queries")
    print("2. Index fields used in WHERE, ORDER BY, and JOIN")
    print("3. Composite indexes for multi-field queries")
    print("4. Trade-off: Faster reads vs slower writes")
    print("5. Don't over-index - monitor and optimize")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()