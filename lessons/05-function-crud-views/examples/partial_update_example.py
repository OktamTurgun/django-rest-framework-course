"""
Filterlash va Qidiruv - Function-based Views
===========================================

Bu faylda turli xil filterlash va qidiruv usullari ko'rsatilgan.

MUHIM: Bu namuna kod - to'g'ridan-to'g'ri ishlamaydi!
O'z loyihangizga moslashtiring va kerakli import'larni qo'shing.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


# ==================== ODDIY FILTERLASH ====================

# @api_view(['GET'])
def simple_filter(request):
    """
    Oddiy filterlash - bitta maydon bo'yicha
    
    Example: /api/books/filter/?author=John
    
    ISHLATISH:
    from .models import Book
    from .serializers import BookSerializer
    from rest_framework.decorators import api_view
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    author = request.query_params.get('author', None)
    
    if author:
        books = Book.objects.filter(author__icontains=author)
    else:
        books = Book.objects.all()
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# ==================== KO'P MAYDONLI FILTERLASH ====================

@api_view(['GET'])
def multiple_filters(request):
    """
    Ko'p maydonli filterlash
    
    Example: /api/books/filter/?author=John&language=English&available=true
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    books = Book.objects.all()
    
    # Author filtri
    author = request.query_params.get('author', None)
    if author:
        books = books.filter(author__icontains=author)
    
    # Language filtri
    language = request.query_params.get('language', None)
    if language:
        books = books.filter(language__icontains=language)
    
    # Available filtri
    available = request.query_params.get('available', None)
    if available is not None:
        is_available = available.lower() == 'true'
        books = books.filter(is_available=is_available)
    
    # Price range filtri
    min_price = request.query_params.get('min_price', None)
    max_price = request.query_params.get('max_price', None)
    
    if min_price:
        books = books.filter(price__gte=float(min_price))
    if max_price:
        books = books.filter(price__lte=float(max_price))
    
    serializer = BookSerializer(books, many=True)
    
    return Response({
        'count': books.count(),
        'filters': {
            'author': author,
            'language': language,
            'available': available,
            'price_range': f"{min_price or 'N/A'} - {max_price or 'N/A'}"
        },
        'results': serializer.data
    })


# ==================== Q OBJECT BILAN QIDIRUV ====================

@api_view(['GET'])
def advanced_search(request):
    """
    Q object yordamida murakkab qidiruv
    
    Example: /api/books/search/?q=python
    Title YOKI Author'da qidiradi
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    query = request.query_params.get('q', '')
    
    if not query:
        return Response(
            {'error': 'Qidiruv so\'zi kiritilmagan'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Q object - OR condition
    books = Book.objects.filter(
        Q(title__icontains=query) | 
        Q(author__icontains=query) |
        Q(isbn__icontains=query)
    )
    
    serializer = BookSerializer(books, many=True)
    
    return Response({
        'query': query,
        'count': books.count(),
        'results': serializer.data
    })


# ==================== SORTING (Tartiblash) ====================

@api_view(['GET'])
def sorted_list(request):
    """
    Tartiblash bilan ro'yxat
    
    Example: 
    /api/books/sorted/?order_by=price          # Arzondan qimmatga
    /api/books/sorted/?order_by=-price         # Qimmatdan arzonga
    /api/books/sorted/?order_by=title          # Alifbo tartibida
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    order_by = request.query_params.get('order_by', '-created_at')
    
    # Allowed fields for ordering
    allowed_fields = ['title', '-title', 'author', '-author', 
                     'price', '-price', 'created_at', '-created_at']
    
    if order_by not in allowed_fields:
        return Response(
            {
                'error': 'Noto\'g\'ri tartiblash maydoni',
                'allowed_fields': allowed_fields
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    books = Book.objects.all().order_by(order_by)
    serializer = BookSerializer(books, many=True)
    
    return Response({
        'ordered_by': order_by,
        'count': books.count(),
        'results': serializer.data
    })


# ==================== PAGINATION (Sahifalash) ====================

@api_view(['GET'])
def paginated_list(request):
    """
    Qo'lda sahifalash
    
    Example: /api/books/paginated/?page=2&page_size=10
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    # Query params
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    
    # Offset va limit hisoblash
    start = (page - 1) * page_size
    end = start + page_size
    
    # Barcha kitoblar
    all_books = Book.objects.all()
    total = all_books.count()
    
    # Sahifalangan kitoblar
    books = all_books[start:end]
    
    serializer = BookSerializer(books, many=True)
    
    # Keyingi/Oldingi sahifa bormi?
    has_next = end < total
    has_previous = page > 1
    
    return Response({
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'has_next': has_next,
        'has_previous': has_previous,
        'results': serializer.data
    })


# ==================== DATE RANGE FILTER ====================

@api_view(['GET'])
def date_range_filter(request):
    """
    Sana oralig'i bo'yicha filterlash
    
    Example: /api/books/date-range/?start=2024-01-01&end=2024-12-31
    """
    from code.models import Book
    from code.serializers import BookSerializer
    from datetime import datetime
    
    start_date = request.query_params.get('start', None)
    end_date = request.query_params.get('end', None)
    
    books = Book.objects.all()
    
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            books = books.filter(published_date__gte=start)
        except ValueError:
            return Response(
                {'error': 'Noto\'g\'ri start sana formati (YYYY-MM-DD)'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            books = books.filter(published_date__lte=end)
        except ValueError:
            return Response(
                {'error': 'Noto\'g\'ri end sana formati (YYYY-MM-DD)'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    serializer = BookSerializer(books, many=True)
    
    return Response({
        'date_range': {
            'start': start_date,
            'end': end_date
        },
        'count': books.count(),
        'results': serializer.data
    })


# ==================== COMPLEX FILTER ====================

@api_view(['GET'])
def complex_filter(request):
    """
    Murakkab filterlash - bir nechta shartlar bilan
    
    Example: /api/books/complex/?min_price=20&max_price=50&language=English&available=true&order_by=-price
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    books = Book.objects.all()
    
    # Price range
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    
    if min_price:
        books = books.filter(price__gte=float(min_price))
    if max_price:
        books = books.filter(price__lte=float(max_price))
    
    # Language
    language = request.query_params.get('language')
    if language:
        books = books.filter(language__icontains=language)
    
    # Availability
    available = request.query_params.get('available')
    if available:
        is_available = available.lower() == 'true'
        books = books.filter(is_available=is_available)
    
    # Search in title/author
    search = request.query_params.get('search')
    if search:
        books = books.filter(
            Q(title__icontains=search) | 
            Q(author__icontains=search)
        )
    
    # Ordering
    order_by = request.query_params.get('order_by', '-created_at')
    books = books.order_by(order_by)
    
    serializer = BookSerializer(books, many=True)
    
    return Response({
        'filters_applied': {
            'min_price': min_price,
            'max_price': max_price,
            'language': language,
            'available': available,
            'search': search,
            'order_by': order_by
        },
        'count': books.count(),
        'results': serializer.data
    })