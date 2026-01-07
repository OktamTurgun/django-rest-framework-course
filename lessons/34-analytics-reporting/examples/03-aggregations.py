"""
Django ORM Aggregations
Bu misolda:
- Count, Sum, Avg, Min, Max
- Group By with annotate()
- Filter + Aggregate
- Complex aggregations
- Performance optimization

NOTE: Bu faylni Django shell'da ishga tushiring:
cd code/library-project
python manage.py shell < ../../examples/03-aggregations.py
"""

from django.db.models import Count, Sum, Avg, Min, Max, F, Q, Value
from django.db.models.functions import Coalesce
from books.models import Book, Author, Genre

print("=" * 70)
print("DJANGO ORM AGGREGATION QUERIES")
print("=" * 70)

# ============================================================================
# EXAMPLE 1: Basic Aggregations (aggregate)
# ============================================================================
print("\n📊 EXAMPLE 1: Basic Aggregations")
print("-" * 70)

# aggregate() returns a dictionary with aggregate values
stats = Book.objects.aggregate(
    total_books=Count('id'),
    avg_price=Avg('price'),
    min_price=Min('price'),
    max_price=Max('price'),
    total_stock=Sum('stock'),
)

print("Overall Statistics:")
print(f"  Total Books: {stats['total_books']}")
print(f"  Average Price: ${stats['avg_price']:.2f}")
print(f"  Min Price: ${stats['min_price']:.2f}")
print(f"  Max Price: ${stats['max_price']:.2f}")
print(f"  Total Stock: {stats['total_stock']} items")

# Calculate total stock value
total_value = Book.objects.aggregate(
    total_value=Sum(F('price') * F('stock'))
)
print(f"  Total Stock Value: ${total_value['total_value']:.2f}")

print("\n✅ Basic aggregations completed")

# ============================================================================
# EXAMPLE 2: Group By with annotate()
# ============================================================================
print("\n📈 EXAMPLE 2: Group By - Books per Author")
print("-" * 70)

# annotate() adds calculated field to each object
authors_stats = Author.objects.annotate(
    book_count=Count('books'),
    avg_book_price=Avg('books__price'),
    total_stock=Sum('books__stock'),
).order_by('-book_count')

print("Top Authors by Book Count:")
for idx, author in enumerate(authors_stats[:10], 1):
    print(f"  {idx}. {author.name}")
    print(f"     Books: {author.book_count}")
    print(f"     Avg Price: ${author.avg_book_price:.2f}" if author.avg_book_price else "     Avg Price: N/A")
    print(f"     Total Stock: {author.total_stock or 0}")

print("\n✅ Group by author completed")

# ============================================================================
# EXAMPLE 3: Group By Genre
# ============================================================================
print("\n📚 EXAMPLE 3: Group By - Books per Genre")
print("-" * 70)

genres_stats = Genre.objects.annotate(
    book_count=Count('books'),
    avg_price=Avg('books__price'),
    total_stock=Sum('books__stock'),
    min_price=Min('books__price'),
    max_price=Max('books__price'),
).order_by('-book_count')

print("Genre Statistics:")
for genre in genres_stats[:10]:
    print(f"\n  Genre: {genre.name}")
    print(f"    Books: {genre.book_count}")
    if genre.avg_price:
        print(f"    Avg Price: ${genre.avg_price:.2f}")
        print(f"    Price Range: ${genre.min_price:.2f} - ${genre.max_price:.2f}")
    print(f"    Total Stock: {genre.total_stock or 0}")

print("\n✅ Group by genre completed")

# ============================================================================
# EXAMPLE 4: Filtering + Aggregation
# ============================================================================
print("\n🔍 EXAMPLE 4: Filtered Aggregations")
print("-" * 70)

# Books above average price
avg_price_value = Book.objects.aggregate(avg=Avg('price'))['avg']

expensive_books = Book.objects.filter(
    price__gt=avg_price_value
).aggregate(
    count=Count('id'),
    avg_price=Avg('price'),
    total_stock=Sum('stock'),
)

print(f"Books Above Average Price (${avg_price_value:.2f}):")
print(f"  Count: {expensive_books['count']}")
print(f"  Avg Price: ${expensive_books['avg_price']:.2f}")
print(f"  Total Stock: {expensive_books['total_stock']}")

# Low stock books
low_stock = Book.objects.filter(stock__lt=5).aggregate(
    count=Count('id'),
    authors=Count('author', distinct=True),
)

print(f"\nLow Stock Books (< 5):")
print(f"  Count: {low_stock['count']}")
print(f"  Unique Authors: {low_stock['authors']}")

print("\n✅ Filtered aggregations completed")

# ============================================================================
# EXAMPLE 5: Complex Aggregations with Q objects
# ============================================================================
print("\n🎯 EXAMPLE 5: Complex Aggregations")
print("-" * 70)

# Count books by price category
price_categories = Book.objects.aggregate(
    cheap=Count('id', filter=Q(price__lt=30)),
    moderate=Count('id', filter=Q(price__gte=30, price__lt=50)),
    expensive=Count('id', filter=Q(price__gte=50)),
)

print("Books by Price Category:")
print(f"  Cheap (< $30): {price_categories['cheap']}")
print(f"  Moderate ($30-$50): {price_categories['moderate']}")
print(f"  Expensive (≥ $50): {price_categories['expensive']}")

# Stock status
stock_status = Book.objects.aggregate(
    out_of_stock=Count('id', filter=Q(stock=0)),
    low_stock=Count('id', filter=Q(stock__gt=0, stock__lt=5)),
    in_stock=Count('id', filter=Q(stock__gte=5)),
)

print("\nBooks by Stock Status:")
print(f"  Out of Stock: {stock_status['out_of_stock']}")
print(f"  Low Stock (1-4): {stock_status['low_stock']}")
print(f"  In Stock (≥ 5): {stock_status['in_stock']}")

print("\n✅ Complex aggregations completed")

# ============================================================================
# EXAMPLE 6: Annotate with Calculated Fields
# ============================================================================
print("\n🧮 EXAMPLE 6: Calculated Fields")
print("-" * 70)

# Add calculated field to each book
books_with_value = Book.objects.annotate(
    stock_value=F('price') * F('stock')
).order_by('-stock_value')[:10]

print("Top 10 Books by Stock Value:")
for idx, book in enumerate(books_with_value, 1):
    print(f"  {idx}. {book.title}")
    print(f"     Price: ${book.price} × Stock: {book.stock}")
    print(f"     Total Value: ${book.stock_value:.2f}")

print("\n✅ Calculated fields completed")

# ============================================================================
# EXAMPLE 7: Authors with Most Books
# ============================================================================
print("\n👥 EXAMPLE 7: Most Productive Authors")
print("-" * 70)

productive_authors = Author.objects.annotate(
    total_books=Count('books'),
    total_pages=Sum('books__pages'),
    avg_pages=Avg('books__pages'),
).filter(
    total_books__gt=0
).order_by('-total_books')[:10]

print("Top 10 Most Productive Authors:")
for idx, author in enumerate(productive_authors, 1):
    print(f"  {idx}. {author.name}")
    print(f"     Books: {author.total_books}")
    print(f"     Total Pages: {author.total_pages or 0}")
    print(f"     Avg Pages: {author.avg_pages:.0f}" if author.avg_pages else "     Avg Pages: N/A")

print("\n✅ Productive authors analysis completed")

# ============================================================================
# EXAMPLE 8: Coalesce for NULL handling
# ============================================================================
print("\n🔄 EXAMPLE 8: Handling NULL values")
print("-" * 70)

# Use Coalesce to provide default values for NULL
authors_safe = Author.objects.annotate(
    book_count=Count('books'),
    avg_price=Coalesce(Avg('books__price'), Value(0.0)),
    total_stock=Coalesce(Sum('books__stock'), Value(0)),
).order_by('-book_count')[:5]

print("Authors with Safe NULL Handling:")
for author in authors_safe:
    print(f"  {author.name}")
    print(f"    Books: {author.book_count}")
    print(f"    Avg Price: ${author.avg_price:.2f}")
    print(f"    Total Stock: {author.total_stock}")

print("\n✅ NULL handling completed")

# ============================================================================
# EXAMPLE 9: Performance Comparison
# ============================================================================
print("\n⚡ EXAMPLE 9: Performance Optimization")
print("-" * 70)

import time

# BAD: Python loop (slow for large datasets)
start = time.time()
total_python = 0
for book in Book.objects.all():
    total_python += book.price * book.stock
time_python = time.time() - start

# GOOD: Database aggregation (fast)
start = time.time()
total_db = Book.objects.aggregate(
    total=Sum(F('price') * F('stock'))
)['total']
time_db = time.time() - start

print("Calculating Total Stock Value:")
print(f"  Python Loop: ${total_python:.2f} (took {time_python*1000:.2f}ms)")
print(f"  DB Aggregation: ${total_db:.2f} (took {time_db*1000:.2f}ms)")
print(f"  Speedup: {time_python/time_db:.1f}x faster")

print("\n✅ Performance comparison completed")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("📊 AGGREGATION QUERIES SUMMARY")
print("=" * 70)
print("Completed Examples:")
print("  ✅ Basic aggregations (Count, Sum, Avg, Min, Max)")
print("  ✅ Group By with annotate()")
print("  ✅ Filtered aggregations")
print("  ✅ Complex aggregations with Q objects")
print("  ✅ Calculated fields with F expressions")
print("  ✅ NULL handling with Coalesce")
print("  ✅ Performance optimization")
print("\nKey Takeaways:")
print("  • Use aggregate() for single results")
print("  • Use annotate() for per-object calculations")
print("  • Use F() for database-level calculations")
print("  • Use Q() for complex filtering")
print("  • Database aggregations are much faster than Python loops")
print("=" * 70)