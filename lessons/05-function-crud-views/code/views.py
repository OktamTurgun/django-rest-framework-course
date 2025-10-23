from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import (
    BookSerializer, 
    BookListSerializer, 
    BookCreateSerializer
)

# ==================== LIST & CREATE ====================

@api_view(['GET', 'POST'])
def book_list(request):
    """
    GET: Barcha kitoblarni qaytaradi
    POST: Yangi kitob yaratadi
    """
    
    if request.method == 'GET':
        # Barcha kitoblarni olish
        books = Book.objects.all()
        
        # Filterlash - query params orqali
        # Example: /api/books/?author=John&available=true
        author = request.query_params.get('author', None)
        available = request.query_params.get('available', None)
        language = request.query_params.get('language', None)
        
        if author:
            books = books.filter(author__icontains=author)
        
        if available is not None:
            is_available = available.lower() == 'true'
            books = books.filter(is_available=is_available)
        
        if language:
            books = books.filter(language__icontains=language)
        
        # Qisqa serializer ishlatamiz (list uchun)
        serializer = BookListSerializer(books, many=True)
        
        return Response({
            'count': books.count(),
            'results': serializer.data
        })
    
    elif request.method == 'POST':
        # Yangi kitob yaratish
        serializer = BookCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            book = serializer.save()
            
            # To'liq ma'lumot bilan javob qaytarish
            response_serializer = BookSerializer(book)
            
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'error': 'Ma\'lumotlar noto\'g\'ri',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# ==================== RETRIEVE, UPDATE, DELETE ====================

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def book_detail(request, pk):
    """
    GET: Bitta kitobni qaytaradi
    PUT: Kitobni to'liq yangilaydi
    PATCH: Kitobni qisman yangilaydi
    DELETE: Kitobni o'chiradi
    """
    
    # Kitobni topish (404 xato qaytaradi agar topilmasa)
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'GET':
        # Bitta kitobni qaytarish
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # To'liq yangilash - barcha maydonlar kerak
        serializer = BookSerializer(book, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            {
                'error': 'Yangilash xatosi',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    elif request.method == 'PATCH':
        # Qisman yangilash - faqat berilgan maydonlar yangilanadi
        serializer = BookSerializer(
            book, 
            data=request.data, 
            partial=True  # Bu muhim!
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            {
                'error': 'Qisman yangilash xatosi',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    elif request.method == 'DELETE':
        # Kitobni o'chirish
        book_title = book.title
        book.delete()
        
        return Response(
            {
                'message': f'"{book_title}" kitobi muvaffaqiyatli o\'chirildi',
                'deleted_id': pk
            },
            status=status.HTTP_204_NO_CONTENT
        )


# ==================== QIDIRUV ====================

@api_view(['GET'])
def book_search(request):
    """
    Kitoblarni qidirish
    Example: /api/books/search/?q=python
    """
    query = request.query_params.get('q', '')
    
    if not query:
        return Response(
            {'error': 'Qidiruv so\'zi kiritilmagan. ?q=... ishlatilsin'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Title yoki Author bo'yicha qidirish
    books = Book.objects.filter(
        title__icontains=query
    ) | Book.objects.filter(
        author__icontains=query
    )
    
    serializer = BookListSerializer(books, many=True)
    
    return Response({
        'query': query,
        'count': books.count(),
        'results': serializer.data
    })


# ==================== STATISTIKA ====================

@api_view(['GET'])
def book_stats(request):
    """
    Kitoblar statistikasi
    """
    from django.db.models import Avg, Max, Min, Count
    
    total = Book.objects.count()
    available = Book.objects.filter(is_available=True).count()
    
    # Narx statistikasi
    price_stats = Book.objects.aggregate(
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    
    # Til bo'yicha count
    languages = Book.objects.values('language').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Eng qimmat kitob
    most_expensive = Book.objects.order_by('-price').first()
    
    # Eng arzon kitob
    cheapest = Book.objects.order_by('price').first()
    
    # Oxirgi qo'shilgan
    latest = Book.objects.order_by('-created_at').first()
    
    return Response({
        'total_books': total,
        'available_books': available,
        'unavailable_books': total - available,
        'price_stats': {
            'average': round(price_stats['avg_price'], 2) if price_stats['avg_price'] else 0,
            'max': price_stats['max_price'],
            'min': price_stats['min_price'],
        },
        'languages': {item['language']: item['count'] for item in languages},
        'most_expensive': BookListSerializer(most_expensive).data if most_expensive else None,
        'cheapest': BookListSerializer(cheapest).data if cheapest else None,
        'latest_added': BookSerializer(latest).data if latest else None,
    })


# ==================== MAVJUDLIKNI O'ZGARTIRISH ====================

@api_view(['POST'])
def toggle_availability(request, pk):
    """
    Kitobning mavjudligini o'zgartirish (toggle)
    """
    book = get_object_or_404(Book, pk=pk)
    
    book.is_available = not book.is_available
    book.save()
    
    return Response({
        'id': book.id,
        'title': book.title,
        'is_available': book.is_available,
        'message': f'Kitob endi {"mavjud" if book.is_available else "mavjud emas"}'
    })