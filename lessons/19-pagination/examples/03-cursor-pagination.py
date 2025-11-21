"""
CursorPagination Example

Cursor-based pagination - katta dataset'lar uchun eng yaxshi.
Real-time feeds, infinite scroll uchun ideal.
"""

from rest_framework import generics
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import AllowAny
from books.models import Book, ActivityLog
from books.serializers import BookSerializer, BookListSerializer, ActivityLogSerializer


# ==================== 1. BASIC CURSOR PAGINATION ====================

class BookCursorPagination(CursorPagination):
    """
    Basic cursor pagination
    
    IMPORTANT: ordering field majburiy!
    """
    page_size = 10
    ordering = '-created_at'  # MUST have ordering!
    cursor_query_param = 'cursor'


class BookFeedView(generics.ListAPIView):
    """
    Book feed - cursor pagination bilan
    
    Usage:
    GET /api/books/feed/
    GET /api/books/feed/?cursor=cD0yMDI0LTAxLTE1...
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookCursorPagination


"""
Response:
{
    "next": "http://localhost:8000/api/books/feed/?cursor=cD0yMDI0...",
    "previous": null,
    "results": [
        // 10 ta kitob
    ]
}

Note: No count, no page numbers!
"""


# ==================== 2. WHY CURSOR PAGINATION? ====================

"""
PROBLEM with PageNumber/LimitOffset:

Imagine:
- GET /api/books/?page=1 -> items 1-10
- New book added at position 1
- GET /api/books/?page=2 -> items 12-21 (item 11 skipped!)

SOLUTION with Cursor:
- Cursor remembers exact position
- New items don't affect pagination
- Consistent results

PERFORMANCE:

LimitOffset with large offset:
SELECT * FROM books LIMIT 10 OFFSET 100000  -- SLOW! Scans 100000 rows

Cursor:
SELECT * FROM books WHERE id > 12345 ORDER BY id LIMIT 10  -- FAST! Uses index
"""


# ==================== 3. DIFFERENT ORDERINGS ====================

class NewestFirstPagination(CursorPagination):
    """Eng yangi birinchi - created_at descending"""
    page_size = 20
    ordering = '-created_at'


class OldestFirstPagination(CursorPagination):
    """Eng eski birinchi - created_at ascending"""
    page_size = 20
    ordering = 'created_at'


class PriceAscendingPagination(CursorPagination):
    """Arzondan qimmatga"""
    page_size = 20
    ordering = 'price'


class PriceDescendingPagination(CursorPagination):
    """Qimmatdan arzonga"""
    page_size = 20
    ordering = '-price'


# ==================== 4. MULTIPLE ORDERING FIELDS ====================

class ComplexOrderingPagination(CursorPagination):
    """
    Multiple ordering fields
    
    Format: 'field1,-field2,field3'
    """
    page_size = 15
    ordering = ('-published_date', 'title')  # Date desc, then title asc


"""
SQL equivalent:
ORDER BY published_date DESC, title ASC
"""


# ==================== 5. CUSTOM CURSOR PARAMETER ====================

class CustomCursorPagination(CursorPagination):
    """
    Custom cursor parameter name
    """
    page_size = 10
    ordering = '-created_at'
    cursor_query_param = 'c'  # ?c=cD0yMDI0...


"""
Usage:
GET /api/books/?c=cD0yMDI0LTAxLTE1...
"""


# ==================== 6. VARIABLE PAGE SIZE ====================

class VariablePageSizeCursorPagination(CursorPagination):
    """
    User can change page size
    """
    page_size = 10
    ordering = '-created_at'
    page_size_query_param = 'page_size'
    max_page_size = 100


"""
Usage:
GET /api/books/feed/?page_size=20
GET /api/books/feed/?page_size=50&cursor=...
"""


# ==================== 7. REAL-TIME FEED ====================

class RealTimeFeedPagination(CursorPagination):
    """
    Real-time feed pagination
    Ideal for: Twitter, Instagram, Facebook feeds
    """
    page_size = 20
    ordering = '-created_at'


class BookNewsFeedView(generics.ListAPIView):
    """
    Book news feed - yangi kitoblar
    
    Features:
    - Real-time updates
    - No skipped items
    - Consistent pagination
    
    Usage:
    GET /api/books/newsfeed/
    """
    serializer_class = BookListSerializer
    pagination_class = RealTimeFeedPagination
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # Faqat published kitoblar
        return Book.objects.filter(
            published=True
        ).select_related('author').prefetch_related('genres')


# ==================== 8. INFINITE SCROLL ====================

class InfiniteScrollPagination(CursorPagination):
    """
    Infinite scroll uchun
    Mobile apps, social media
    """
    page_size = 15
    ordering = '-created_at'
    
    def get_paginated_response(self, data):
        """Simplified response"""
        from rest_framework.response import Response
        
        return Response({
            'has_more': self.get_next_link() is not None,
            'next_cursor': self.get_next_link(),
            'data': data
        })


"""
Response:
{
    "has_more": true,
    "next_cursor": "http://localhost:8000/api/books/?cursor=...",
    "data": [...]
}

Frontend (React example):
const loadMore = () => {
    if (hasMore) {
        fetch(nextCursor)
    }
}
"""


# ==================== 9. BIDIRECTIONAL PAGINATION ====================

class BidirectionalPagination(CursorPagination):
    """
    Forward va backward navigation
    """
    page_size = 10
    ordering = '-created_at'


"""
Usage:
GET /api/books/               # Initial load
GET /api/books/?cursor=...    # Next page (forward)

Response includes 'previous' link:
{
    "next": "...",
    "previous": "...",  # Go back
    "results": [...]
}

User can navigate both directions!
"""


# ==================== 10. CURSOR + FILTERS ====================

from rest_framework.filters import SearchFilter, OrderingFilter

class FilteredCursorView(generics.ListAPIView):
    """
    Cursor pagination + filters
    
    NOTE: Ordering filter conflicts with cursor!
    Don't use OrderingFilter with CursorPagination!
    """
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    pagination_class = RealTimeFeedPagination
    
    # Only use filters that don't affect ordering
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author__name']


"""
Usage:
GET /api/books/?search=django
GET /api/books/?search=django&cursor=...

WARNING: Don't combine with OrderingFilter!
OrderingFilter changes ordering, cursor breaks!
"""


# ==================== 11. TIMESTAMP-BASED CURSOR ====================

class TimestampCursorPagination(CursorPagination):
    """
    Timestamp-based cursor
    Perfect for: Logs, activities, events
    """
    page_size = 50
    ordering = '-timestamp'  # Assuming 'timestamp' field exists


class ActivityLogView(generics.ListAPIView):
    """
    Activity log with cursor pagination
    
    Use Case: View logs without skipping entries
    """
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    pagination_class = TimestampCursorPagination


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    # Basic feed
    path('books/feed/', BookFeedView.as_view(), name='book-feed'),
    
    # News feed
    path('books/newsfeed/', BookNewsFeedView.as_view(), name='book-newsfeed'),
    
    # Activity log
    path('logs/activity/', ActivityLogView.as_view(), name='activity-log'),
]


# ==================== ADVANTAGES ====================

"""
✅ PERFORMANCE:
   - No OFFSET, uses WHERE clause
   - Fast even with millions of records
   - Constant query time (O(1))

✅ CONSISTENCY:
   - No skipped items
   - No duplicates
   - Works perfectly with real-time data

✅ SCALABILITY:
   - Handles large datasets efficiently
   - Database-friendly
   - Uses indexes effectively

✅ USE CASES:
   - Social media feeds
   - Real-time updates
   - Activity logs
   - Infinite scroll
   - Large datasets (millions+)
"""


# ==================== DISADVANTAGES ====================

"""
❌ NO PAGE NUMBERS:
   - Can't jump to page 5
   - Only forward/backward navigation
   - No "go to page X"

❌ ORDERING REQUIRED:
   - Must have ordering field
   - Can't change ordering dynamically
   - Conflicts with OrderingFilter

❌ NO COUNT:
   - No total count
   - Can't show "Page X of Y"
   - Can't calculate total pages

❌ COMPLEXITY:
   - Cursor is opaque (encoded)
   - Can't bookmark specific page
   - More complex to implement custom features
"""


# ==================== WHEN TO USE ====================

"""
USE CursorPagination when:
✅ Large datasets (100K+ rows)
✅ Real-time feeds
✅ Infinite scroll
✅ Data changes frequently
✅ Performance is critical
✅ Mobile apps (less data transferred)

DON'T USE when:
❌ Need page numbers
❌ Need total count
❌ Small datasets (< 10K rows)
❌ User needs to jump to specific page
❌ Need dynamic ordering
"""


# ==================== CURSOR FORMAT ====================

"""
Cursor is BASE64 encoded:

Example cursor:
cD0yMDI0LTAxLTE1KzExJTNBMzAlM0EwMC4xMjM0NTY=

Decoded:
p=2024-01-15+11%3A30%3A00.123456

Contains:
- Position (p)
- Timestamp
- Direction (forward/reverse)

IMPORTANT:
❌ Don't try to generate cursor manually!
✅ Use cursor from API response
"""


# ==================== IMPLEMENTATION DETAILS ====================

"""
How it works internally:

1. First request:
   GET /api/books/
   -> Returns first 10 items + cursor

2. Cursor contains:
   - Last item's ordering value (e.g., created_at)
   - Direction (forward/backward)

3. Next request:
   GET /api/books/?cursor=cD0yMDI0...
   -> WHERE created_at < '2024-01-15...'
   -> ORDER BY created_at DESC
   -> LIMIT 10

Pseudo-SQL:
SELECT * FROM books 
WHERE created_at < :cursor_value 
ORDER BY created_at DESC 
LIMIT 10
"""


# ==================== BEST PRACTICES ====================

"""
1. ORDERING FIELD:
   ✅ Use indexed field (created_at, id)
   ✅ Use unique or nearly unique field
   ✅ Use stable field (doesn't change)

2. PAGE SIZE:
   ✅ Reasonable size (10-50)
   ✅ Consider mobile data usage
   ✅ Balance between requests and data size

3. DATABASE:
   ✅ Add index on ordering field
   ✅ Use appropriate data types
   ✅ Monitor query performance

4. ERROR HANDLING:
   ✅ Handle invalid cursors gracefully
   ✅ Return 400 for malformed cursors
   ✅ Log cursor errors for debugging

Example:
class SafeCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'
    
    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except Exception as e:
            # Log error
            logger.error(f"Cursor pagination error: {e}")
            # Return first page
            self.cursor = None
            return super().paginate_queryset(queryset, request, view)
"""


# ==================== TESTING ====================

"""
Test Cases:

1. Initial Request:
   GET /api/books/feed/
   Expected: First 10 items, next cursor, no previous

2. Next Page:
   GET /api/books/feed/?cursor=cD0yMDI0...
   Expected: Next 10 items, both cursors

3. Previous Page:
   GET /api/books/feed/?cursor=cj0xJnA...
   Expected: Previous items, both cursors

4. Invalid Cursor:
   GET /api/books/feed/?cursor=invalid
   Expected: 400 error or first page

5. Empty Cursor:
   GET /api/books/feed/?cursor=
   Expected: First page

6. With Filters:
   GET /api/books/feed/?search=django
   Expected: Filtered results with cursor

7. Last Page:
   Expected: No next cursor

8. Ordering:
   Multiple requests should maintain consistent order
   even if new items added
"""


# ==================== REAL WORLD EXAMPLE ====================

"""
Twitter-like Feed:

class TweetFeedPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'

class TweetFeedView(generics.ListAPIView):
    serializer_class = TweetSerializer
    pagination_class = TweetFeedPagination
    
    def get_queryset(self):
        user = self.request.user
        # Following tweets + own tweets
        return Tweet.objects.filter(
            Q(author__in=user.following.all()) | Q(author=user)
        ).select_related('author').prefetch_related('likes')

Frontend (React):
const [tweets, setTweets] = useState([])
const [cursor, setCursor] = useState(null)

const loadMore = async () => {
    const url = cursor || '/api/tweets/feed/'
    const data = await fetch(url)
    setTweets([...tweets, ...data.results])
    setCursor(data.next)
}
"""