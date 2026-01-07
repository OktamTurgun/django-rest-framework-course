"""
Complete Analytics Dashboard
Bu misolda:
- Overview statistics
- Books by genre
- Books by author
- Popular books
- Real-world dashboard design

NOTE: Bu faylni Django shell'da ishga tushiring:
cd code/library-project
python manage.py shell < ../../examples/04-dashboard-stats.py
"""

from django.db.models import Count, Sum, Avg, Min, Max, F, Q
from django.db.models.functions import Coalesce
from books.models import Book, Author, Genre
from datetime import datetime, timedelta

print("=" * 70)
print("ANALYTICS DASHBOARD - COMPLETE STATISTICS")
print("=" * 70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# ============================================================================
# SECTION 1: Overview Statistics
# ============================================================================
print("\n📊 OVERVIEW STATISTICS")
print("-" * 70)

# Calculate all overview stats
overview = {
    'books': Book.objects.aggregate(
        total=Count('id'),
        avg_price=Avg('price'),
        min_price=Min('price'),
        max_price=Max('price'),
        total_stock=Sum('stock'),
        total_value=Sum(F('price') * F('stock')),
    ),
    'authors': Author.objects.aggregate(
        total=Count('id'),
        with_books=Count('id', filter=Q(books__isnull=False), distinct=True),
    ),
    'genres': Genre.objects.aggregate(
        total=Count('id'),
        with_books=Count('id', filter=Q(books__isnull=False), distinct=True),
    ),
}

# Display overview
print("\n📚 BOOKS:")
print(f"  Total Books: {overview['books']['total']}")
print(f"  Average Price: ${overview['books']['avg_price']:.2f}" if overview['books']['avg_price'] else "  Average Price: N/A")
print(f"  Price Range: ${overview['books']['min_price']:.2f} - ${overview['books']['max_price']:.2f}" if overview['books']['min_price'] else "  Price Range: N/A")
print(f"  Total Stock: {overview['books']['total_stock'] or 0} items")
print(f"  Total Stock Value: ${overview['books']['total_value']:.2f}" if overview['books']['total_value'] else "  Total Stock Value: $0.00")

print("\n👥 AUTHORS:")
print(f"  Total Authors: {overview['authors']['total']}")
print(f"  Authors with Books: {overview['authors']['with_books']}")

print("\n📂 GENRES:")
print(f"  Total Genres: {overview['genres']['total']}")
print(f"  Genres with Books: {overview['genres']['with_books']}")

# ============================================================================
# SECTION 2: Books by Genre
# ============================================================================
print("\n\n📂 BOOKS BY GENRE")
print("-" * 70)

genres_analysis = Genre.objects.annotate(
    book_count=Count('books'),
    avg_price=Coalesce(Avg('books__price'), 0.0),
    total_stock=Coalesce(Sum('books__stock'), 0),
    total_value=Coalesce(Sum(F('books__price') * F('books__stock')), 0.0),
).filter(
    book_count__gt=0
).order_by('-book_count')

print("\nTop Genres by Book Count:")
print(f"{'Rank':<6} {'Genre':<25} {'Books':<8} {'Avg $':<10} {'Stock':<8} {'Value':<12}")
print("-" * 70)

for idx, genre in enumerate(genres_analysis[:10], 1):
    print(
        f"{idx:<6} "
        f"{genre.name[:24]:<25} "
        f"{genre.book_count:<8} "
        f"${genre.avg_price:<9.2f} "
        f"{genre.total_stock:<8} "
        f"${genre.total_value:<11.2f}"
    )

# Genre with highest average price
if genres_analysis:
    expensive_genre = genres_analysis.order_by('-avg_price').first()
    print(f"\n💰 Most Expensive Genre: {expensive_genre.name} (${expensive_genre.avg_price:.2f} avg)")

    # Genre with most stock
    stock_genre = genres_analysis.order_by('-total_stock').first()
    print(f"📦 Highest Stock Genre: {stock_genre.name} ({stock_genre.total_stock} items)")

# ============================================================================
# SECTION 3: Books by Author
# ============================================================================
print("\n\n👥 BOOKS BY AUTHOR")
print("-" * 70)

authors_analysis = Author.objects.annotate(
    book_count=Count('books'),
    avg_price=Coalesce(Avg('books__price'), 0.0),
    total_stock=Coalesce(Sum('books__stock'), 0),
    total_pages=Coalesce(Sum('books__pages'), 0),
    avg_pages=Coalesce(Avg('books__pages'), 0.0),
).filter(
    book_count__gt=0
).order_by('-book_count')

print("\nTop Authors by Book Count:")
print(f"{'Rank':<6} {'Author':<25} {'Books':<8} {'Avg $':<10} {'Pages':<10}")
print("-" * 70)

for idx, author in enumerate(authors_analysis[:10], 1):
    print(
        f"{idx:<6} "
        f"{author.name[:24]:<25} "
        f"{author.book_count:<8} "
        f"${author.avg_price:<9.2f} "
        f"{int(author.avg_pages):<10}"
    )

# Most productive author
if authors_analysis:
    productive = authors_analysis.first()
    print(f"\n✍️ Most Productive: {productive.name} ({productive.book_count} books)")

    # Author with most pages
    pages_author = authors_analysis.order_by('-total_pages').first()
    print(f"📖 Most Pages Written: {pages_author.name} ({pages_author.total_pages} pages)")

# ============================================================================
# SECTION 4: Price Analysis
# ============================================================================
print("\n\n💰 PRICE ANALYSIS")
print("-" * 70)

# Books by price range
price_ranges = {
    'Budget (< $30)': Book.objects.filter(price__lt=30).count(),
    'Moderate ($30-$50)': Book.objects.filter(price__gte=30, price__lt=50).count(),
    'Premium ($50-$70)': Book.objects.filter(price__gte=50, price__lt=70).count(),
    'Luxury (≥ $70)': Book.objects.filter(price__gte=70).count(),
}

print("\nBooks by Price Range:")
for category, count in price_ranges.items():
    percentage = (count / overview['books']['total'] * 100) if overview['books']['total'] > 0 else 0
    bar = '█' * int(percentage / 2)
    print(f"  {category:<20} {count:>4} books ({percentage:>5.1f}%) {bar}")

# Top 5 most expensive books
print("\nTop 5 Most Expensive Books:")
expensive_books = Book.objects.select_related('author').order_by('-price')[:5]
for idx, book in enumerate(expensive_books, 1):
    author_name = book.author.name if book.author else "Unknown"
    print(f"  {idx}. {book.title[:40]:<42} ${book.price:>6.2f} - {author_name}")

# Top 5 cheapest books
print("\nTop 5 Most Affordable Books:")
cheap_books = Book.objects.select_related('author').order_by('price')[:5]
for idx, book in enumerate(cheap_books, 1):
    author_name = book.author.name if book.author else "Unknown"
    print(f"  {idx}. {book.title[:40]:<42} ${book.price:>6.2f} - {author_name}")

# ============================================================================
# SECTION 5: Stock Analysis
# ============================================================================
print("\n\n📦 STOCK ANALYSIS")
print("-" * 70)

# Stock status
stock_analysis = {
    'Out of Stock': Book.objects.filter(stock=0).count(),
    'Critical (1-2)': Book.objects.filter(stock__gte=1, stock__lte=2).count(),
    'Low (3-5)': Book.objects.filter(stock__gte=3, stock__lte=5).count(),
    'Normal (6-10)': Book.objects.filter(stock__gte=6, stock__lte=10).count(),
    'High (> 10)': Book.objects.filter(stock__gt=10).count(),
}

print("\nStock Status Distribution:")
for status, count in stock_analysis.items():
    percentage = (count / overview['books']['total'] * 100) if overview['books']['total'] > 0 else 0
    bar = '█' * int(percentage / 2)
    print(f"  {status:<20} {count:>4} books ({percentage:>5.1f}%) {bar}")

# Books needing restock
restock_needed = Book.objects.filter(stock__lt=5).select_related('author').order_by('stock')[:10]
if restock_needed:
    print("\n⚠️ Books Needing Restock (Stock < 5):")
    for book in restock_needed:
        author_name = book.author.name if book.author else "Unknown"
        print(f"  • {book.title[:35]:<37} Stock: {book.stock} - {author_name}")

# Highest stock books
print("\nTop 5 Highest Stock Books:")
high_stock = Book.objects.select_related('author').order_by('-stock')[:5]
for idx, book in enumerate(high_stock, 1):
    author_name = book.author.name if book.author else "Unknown"
    print(f"  {idx}. {book.title[:40]:<42} Stock: {book.stock:>3} - {author_name}")

# ============================================================================
# SECTION 6: Value Analysis
# ============================================================================
print("\n\n💎 VALUE ANALYSIS")
print("-" * 70)

# Books by stock value
books_with_value = Book.objects.annotate(
    stock_value=F('price') * F('stock')
).select_related('author').order_by('-stock_value')

print("\nTop 10 Books by Total Stock Value:")
print(f"{'Rank':<6} {'Title':<35} {'Price':<10} {'Stock':<8} {'Value':<12}")
print("-" * 70)

for idx, book in enumerate(books_with_value[:10], 1):
    title = book.title[:34]
    print(
        f"{idx:<6} "
        f"{title:<35} "
        f"${book.price:<9.2f} "
        f"{book.stock:<8} "
        f"${book.stock_value:<11.2f}"
    )

# ============================================================================
# SECTION 7: Summary & Recommendations
# ============================================================================
print("\n\n🎯 SUMMARY & RECOMMENDATIONS")
print("-" * 70)

total_books = overview['books']['total']
out_of_stock = stock_analysis['Out of Stock']
low_stock = stock_analysis['Critical (1-2)'] + stock_analysis['Low (3-5)']
expensive_count = price_ranges['Luxury (≥ $70)']

print("\n📌 Key Insights:")
print(f"  • {out_of_stock} books ({out_of_stock/total_books*100:.1f}%) are out of stock" if total_books > 0 else "  • No stock data available")
print(f"  • {low_stock} books ({low_stock/total_books*100:.1f}%) have low stock" if total_books > 0 else "  • No low stock")
print(f"  • {expensive_count} luxury books (≥ $70)")
print(f"  • Average book price: ${overview['books']['avg_price']:.2f}" if overview['books']['avg_price'] else "  • No price data")
print(f"  • Total inventory value: ${overview['books']['total_value']:.2f}" if overview['books']['total_value'] else "  • No inventory value")

print("\n💡 Recommendations:")
if out_of_stock > 0:
    print(f"  ⚠️ Restock {out_of_stock} out-of-stock books")
if low_stock > 0:
    print(f"  ⚠️ Monitor {low_stock} low-stock books")

# Most profitable genre
if genres_analysis:
    top_genre = genres_analysis.order_by('-total_value').first()
    print(f"  💰 Focus on '{top_genre.name}' genre (${top_genre.total_value:.2f} value)")

# Most productive author
if authors_analysis:
    top_author = authors_analysis.first()
    print(f"  ✍️ Promote '{top_author.name}' ({top_author.book_count} books)")

# ============================================================================
# Footer
# ============================================================================
print("\n" + "=" * 70)
print("📊 DASHBOARD GENERATED SUCCESSFULLY")
print("=" * 70)
print(f"Total Books Analyzed: {total_books}")
print(f"Total Authors: {overview['authors']['total']}")
print(f"Total Genres: {overview['genres']['total']}")
print(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)