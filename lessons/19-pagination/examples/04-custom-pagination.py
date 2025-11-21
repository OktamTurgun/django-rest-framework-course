"""
Custom Pagination Example

O'z pagination class'laringizni yaratish.
Custom response format, logic, va behavior.
"""

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict
from books.models import Book
from books.serializers import BookSerializer


# ==================== 1. CUSTOM RESPONSE FORMAT ====================

class CustomResponsePagination(PageNumberPagination):
    """
    Custom response format
    
    Standard:
    {
        "count": 100,
        "next": "...",
        "previous": "...",
        "results": [...]
    }
    
    Custom:
    {
        "pagination": {...},
        "data": [...]
    }
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('total_items', self.page.paginator.count),
                ('total_pages', self.page.paginator.num_pages),
                ('current_page', self.page.number),
                ('page_size', len(data)),
                ('has_next', self.page.has_next()),
                ('has_previous', self.page.has_previous()),
            ])),
            ('links', OrderedDict([
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])),
            ('data', data)
        ]))


"""
Response:
{
    "pagination": {
        "total_items": 100,
        "total_pages": 10,
        "current_page": 1,
        "page_size": 10,
        "has_next": true,
        "has_previous": false
    },
    "links": {
        "next": "http://localhost:8000/api/books/?page=2",
        "previous": null
    },
    "data": [...]
}
"""


# ==================== 2. METADATA PAGINATION ====================

class MetadataPagination(PageNumberPagination):
    """
    Pagination with metadata
    """
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'pagination': {
                    'page': self.page.number,
                    'pages': self.page.paginator.num_pages,
                    'count': self.page.paginator.count,
                }
            },
            'data': data
        })


"""
Response:
{
    "meta": {
        "pagination": {
            "page": 1,
            "pages": 10,
            "count": 100
        }
    },
    "data": [...]
}
"""


# ==================== 3. RANGE-BASED PAGINATION ====================

class RangePagination(LimitOffsetPagination):
    """
    Range info bilan pagination
    """
    default_limit = 10
    max_limit = 100
    
    def get_paginated_response(self, data):
        offset = self.offset
        limit = self.limit
        count = self.count
        
        return Response({
            'count': count,
            'range': {
                'from': offset + 1,  # 1-based
                'to': min(offset + limit, count),
                'showing': len(data),
                'of': count
            },
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


"""
Response:
{
    "count": 100,
    "range": {
        "from": 1,
        "to": 10,
        "showing": 10,
        "of": 100
    },
    "next": "...",
    "previous": null,
    "results": [...]
}
"""


# ==================== 4. HEADER-BASED PAGINATION ====================

class HeaderPagination(PageNumberPagination):
    """
    Pagination ma'lumotlarini header'da qaytarish
    Body'da faqat data
    """
    page_size = 10
    
    def get_paginated_response(self, data):
        response = Response(data)
        
        # Headers
        response['X-Total-Count'] = self.page.paginator.count
        response['X-Page'] = self.page.number
        response['X-Page-Size'] = len(data)
        response['X-Total-Pages'] = self.page.paginator.num_pages
        
        # Links
        if self.get_next_link():
            response['Link-Next'] = self.get_next_link()
        if self.get_previous_link():
            response['Link-Previous'] = self.get_previous_link()
        
        return response


"""
Response Headers:
X-Total-Count: 100
X-Page: 1
X-Page-Size: 10
X-Total-Pages: 10
Link-Next: http://localhost:8000/api/books/?page=2

Response Body:
[
    {...},
    {...}
]
"""


# ==================== 5. LAZY COUNT PAGINATION ====================

class LazyCountPagination(PageNumberPagination):
    """
    Count ni faqat birinchi sahifada hisoblash
    Performance optimization uchun
    """
    page_size = 10
    
    def get_paginated_response(self, data):
        # Faqat birinchi sahifada count qilish
        if self.page.number == 1:
            count = self.page.paginator.count
        else:
            count = None  # Yoki cache'dan olish
        
        return Response({
            'count': count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


"""
First page:
{
    "count": 100,
    ...
}

Other pages:
{
    "count": null,  # Not calculated
    ...
}
"""


# ==================== 6. CONDITIONAL PAGINATION ====================

class ConditionalPagination(PageNumberPagination):
    """
    User role'ga qarab turli page_size
    """
    page_size = 10
    max_page_size = 100
    
    def get_page_size(self, request):
        # Admin uchun katta page_size
        if request.user.is_staff:
            return min(
                int(request.query_params.get(self.page_size_query_param, 50)),
                200
            )
        
        # Premium user uchun
        if hasattr(request.user, 'is_premium') and request.user.is_premium:
            return min(
                int(request.query_params.get(self.page_size_query_param, 25)),
                100
            )
        
        # Regular user uchun
        return super().get_page_size(request)


# ==================== 7. AGGREGATED PAGINATION ====================

class AggregatedPagination(PageNumberPagination):
    """
    Pagination bilan aggregation
    """
    page_size = 10
    
    def get_paginated_response(self, data):
        # Aggregation qo'shish
        from django.db.models import Sum, Avg
        
        queryset = self.page.object_list.model.objects.all()
        aggregates = queryset.aggregate(
            total_price=Sum('price'),
            avg_price=Avg('price')
        )
        
        return Response({
            'count': self.page.paginator.count,
            'aggregates': {
                'total_price': float(aggregates['total_price'] or 0),
                'average_price': float(aggregates['avg_price'] or 0),
            },
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


"""
Response:
{
    "count": 100,
    "aggregates": {
        "total_price": 2999.50,
        "average_price": 29.99
    },
    "next": "...",
    "results": [...]
}
"""


# ==================== 8. GRAPHQL-STYLE PAGINATION ====================

class GraphQLStylePagination(PageNumberPagination):
    """
    GraphQL Relay-style pagination
    """
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'edges': [
                {
                    'node': item,
                    'cursor': self.encode_cursor(item)
                }
                for item in data
            ],
            'pageInfo': {
                'hasNextPage': self.page.has_next(),
                'hasPreviousPage': self.page.has_previous(),
                'startCursor': self.encode_cursor(data[0]) if data else None,
                'endCursor': self.encode_cursor(data[-1]) if data else None,
            },
            'totalCount': self.page.paginator.count
        })
    
    def encode_cursor(self, item):
        """Simple cursor encoding"""
        import base64
        cursor = f"id:{item['id']}"
        return base64.b64encode(cursor.encode()).decode()


"""
Response:
{
    "edges": [
        {
            "node": {...},
            "cursor": "aWQ6MQ=="
        }
    ],
    "pageInfo": {
        "hasNextPage": true,
        "hasPreviousPage": false,
        "startCursor": "aWQ6MQ==",
        "endCursor": "aWQ6MTA="
    },
    "totalCount": 100
}
"""


# ==================== 9. DYNAMIC PAGINATION CLASS ====================

def create_pagination_class(page_size=10, max_page_size=100, response_format='standard'):
    """
    Pagination class factory
    
    Usage:
    SmallPagination = create_pagination_class(page_size=5)
    LargePagination = create_pagination_class(page_size=100, max_page_size=500)
    """
    
    class DynamicPagination(PageNumberPagination):
        pass
    
    DynamicPagination.page_size = page_size
    DynamicPagination.page_size_query_param = 'page_size'
    DynamicPagination.max_page_size = max_page_size
    
    # Custom response format
    if response_format == 'meta':
        def get_paginated_response(self, data):
            return Response({
                'meta': {
                    'page': self.page.number,
                    'total': self.page.paginator.count
                },
                'data': data
            })
        DynamicPagination.get_paginated_response = get_paginated_response
    
    return DynamicPagination


# Usage
SmallPagination = create_pagination_class(page_size=5, max_page_size=50)
MediumPagination = create_pagination_class(page_size=25, max_page_size=100)
LargePagination = create_pagination_class(page_size=100, max_page_size=500)


# ==================== 10. CACHE-OPTIMIZED PAGINATION ====================

from django.core.cache import cache

class CachedCountPagination(PageNumberPagination):
    """
    Count'ni cache'da saqlash
    """
    page_size = 10
    cache_timeout = 300  # 5 minutes
    
    def get_paginated_response(self, data):
        # Cache key
        cache_key = f'pagination_count_{self.request.path}'
        
        # Try to get from cache
        count = cache.get(cache_key)
        
        if count is None:
            # Calculate and cache
            count = self.page.paginator.count
            cache.set(cache_key, count, self.cache_timeout)
        
        return Response({
            'count': count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


# ==================== REAL WORLD EXAMPLES ====================

class APIStandardPagination(PageNumberPagination):
    """
    Production-ready standard pagination
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('status', 'success'),
            ('pagination', OrderedDict([
                ('count', self.page.paginator.count),
                ('page', self.page.number),
                ('pages', self.page.paginator.num_pages),
                ('page_size', len(data)),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])),
            ('data', data)
        ]))


class MobileFriendlyPagination(PageNumberPagination):
    """
    Mobile app uchun optimized
    """
    page_size = 15  # Smaller for mobile
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response({
            'hasMore': self.page.has_next(),
            'total': self.page.paginator.count,
            'items': data
        })


# ==================== USAGE ====================

from rest_framework import generics

class BookListView(generics.ListAPIView):
    """
    Books with custom pagination
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomResponsePagination


class MobileBookView(generics.ListAPIView):
    """
    Books for mobile app
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = MobileFriendlyPagination


# ==================== BEST PRACTICES ====================

"""
1. CONSISTENCY:
   ✅ Use same format across API
   ✅ Document response structure
   ✅ Version your API

2. PERFORMANCE:
   ✅ Cache count queries
   ✅ Lazy load when possible
   ✅ Optimize database queries

3. FLEXIBILITY:
   ✅ Allow page_size customization
   ✅ Set reasonable limits
   ✅ Support different formats per client

4. DOCUMENTATION:
   ✅ Document custom response format
   ✅ Provide examples
   ✅ Show edge cases

5. ERROR HANDLING:
   ✅ Handle invalid pages gracefully
   ✅ Return proper HTTP status codes
   ✅ Provide clear error messages
"""


# ==================== TESTING ====================

"""
Test Custom Pagination:

1. Standard Cases:
   - First page
   - Middle page
   - Last page
   - Empty results

2. Custom Response:
   - Check response structure
   - Verify all fields present
   - Validate data types

3. Edge Cases:
   - Invalid page number
   - Page beyond last
   - Negative page
   - Non-numeric page

4. Performance:
   - Count query called correctly
   - Cache working (if implemented)
   - No N+1 queries

5. Integration:
   - Works with filters
   - Works with search
   - Works with ordering
"""


# ==================== COMMON PATTERNS ====================

"""
1. SIMPLE WRAPPER:
   {
       "data": [...],
       "meta": {...}
   }

2. NESTED:
   {
       "response": {
           "data": [...],
           "pagination": {...}
       }
   }

3. FLAT:
   {
       "items": [...],
       "total": 100,
       "page": 1
   }

4. GRAPHQL-STYLE:
   {
       "edges": [...],
       "pageInfo": {...}
   }

Choose based on:
- Client expectations
- API conventions
- Team preferences
- Existing codebase
"""