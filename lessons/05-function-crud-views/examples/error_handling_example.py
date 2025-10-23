"""
Error Handling Examples - Function-based Views
=============================================

Bu faylda turli xil xatolarni boshqarish usullari ko'rsatilgan.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import datetime


# ==================== BASIC ERROR HANDLING ====================

@api_view(['GET'])
def basic_error_handling(request, pk):
    """
    Try-except bilan oddiy xato boshqarish
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    except Book.DoesNotExist:
        return Response(
            {'error': 'Kitob topilmadi'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        return Response(
            {'error': 'Kutilmagan xato', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== get_object_or_404 ====================

@api_view(['GET'])
def using_get_object_or_404(request, pk):
    """
    get_object_or_404 - avtomatik 404 qaytaradi
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    # Bu avtomatik 404 xatosi qaytaradi agar topilmasa
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)
    
    return Response(serializer.data)


# ==================== MULTIPLE EXCEPTION HANDLING ====================

@api_view(['POST'])
def multiple_exceptions(request):
    """
    Bir nechta xato turlarini boshqarish
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    try:
        serializer = BookSerializer(data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        book = serializer.save()
        
        return Response(
            BookSerializer(book).data,
            status=status.HTTP_201_CREATED
        )
    
    except ValidationError as e:
        return Response(
            {
                'error': 'Validatsiya xatosi',
                'details': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except IntegrityError as e:
        return Response(
            {
                'error': 'Ma\'lumotlar bazasi xatosi',
                'details': 'Bu ma\'lumot allaqachon mavjud (ISBN yoki boshqa unique maydon)'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except Exception as e:
        return Response(
            {
                'error': 'Server xatosi',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== CUSTOM ERROR MESSAGES ====================

@api_view(['DELETE'])
def delete_with_custom_errors(request, pk):
    """
    Custom xato xabarlari bilan o'chirish
    """
    from code.models import Book
    
    try:
        book = Book.objects.get(pk=pk)
        
        # Biznes logika - mavjud kitoblarni o'chirib bo'lmaydi
        if book.is_available:
            return Response(
                {
                    'error': 'Mavjud kitoblarni o\'chirib bo\'lmaydi',
                    'suggestion': 'Avval is_available=false qiling'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book_title = book.title
        book.delete()
        
        return Response(
            {
                'success': True,
                'message': f'"{book_title}" kitobi o\'chirildi',
                'deleted_id': pk
            },
            status=status.HTTP_200_OK
        )
    
    except Book.DoesNotExist:
        return Response(
            {
                'error': 'Kitob topilmadi',
                'searched_id': pk,
                'suggestion': 'ID to\'g\'ri ekanligini tekshiring'
            },
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== LOGGING ERRORS ====================

import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_with_logging(request):
    """
    Xatolarni log qilish bilan
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    try:
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        
        logger.info(f'Yangi kitob yaratildi: {book.title}')
        
        return Response(
            BookSerializer(book).data,
            status=status.HTTP_201_CREATED
        )
    
    except ValidationError as e:
        logger.warning(f'Validatsiya xatosi: {e}')
        return Response(
            {'error': 'Validatsiya xatosi', 'details': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except Exception as e:
        logger.error(f'Kutilmagan xato: {e}', exc_info=True)
        return Response(
            {'error': 'Server xatosi'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== DETAILED ERROR RESPONSE ====================

@api_view(['PUT'])
def update_with_detailed_errors(request, pk):
    """
    Batafsil xato ma'lumotlari bilan
    """
    from code.models import Book
    from code.serializers import BookSerializer
    import traceback
    
    try:
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'error': 'Validatsiya xatosi',
                    'errors': serializer.errors,
                    'timestamp': datetime.now().isoformat()
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        
        return Response(
            {
                'success': True,
                'message': 'Kitob yangilandi',
                'data': serializer.data
            }
        )
    
    except Exception as e:
        # Batafsil xato ma'lumotlari (faqat development uchun!)
        return Response(
            {
                'success': False,
                'error': 'Server xatosi',
                'message': str(e),
                'type': type(e).__name__,
                'traceback': traceback.format_exc() if request.user.is_staff else None
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== VALIDATION ERROR FORMATTING ====================

@api_view(['POST'])
def formatted_validation_errors(request):
    """
    Validatsiya xatolarini formatlash
    """
    from code.serializers import BookSerializer
    
    serializer = BookSerializer(data=request.data)
    
    if not serializer.is_valid():
        # Xatolarni user-friendly formatda
        errors = []
        
        for field, field_errors in serializer.errors.items():
            for error in field_errors:
                errors.append({
                    'field': field,
                    'message': str(error),
                    'value': request.data.get(field, None)
                })
        
        return Response(
            {
                'success': False,
                'message': 'Ma\'lumotlar noto\'g\'ri',
                'errors': errors,
                'total_errors': len(errors)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Success response
    return Response({'success': True})


# ==================== GRACEFUL DEGRADATION ====================

@api_view(['GET'])
def graceful_degradation(request):
    """
    Xato bo'lsa ham qisman ma'lumot qaytarish
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    response_data = {
        'success': True,
        'books': [],
        'stats': {},
        'errors': []
    }
    
    # 1. Kitoblarni olish (xato bo'lsa ham davom etadi)
    try:
        books = Book.objects.all()
        response_data['books'] = BookSerializer(books, many=True).data
    except Exception as e:
        response_data['errors'].append({
            'section': 'books',
            'error': str(e)
        })
        response_data['success'] = False
    
    # 2. Statistikani hisoblash (xato bo'lsa ham davom etadi)
    try:
        from django.db.models import Count, Avg
        response_data['stats'] = {
            'total': Book.objects.count(),
            'avg_price': Book.objects.aggregate(Avg('price'))['price__avg']
        }
    except Exception as e:
        response_data['errors'].append({
            'section': 'stats',
            'error': str(e)
        })
        response_data['success'] = False
    
    # Agar birorta section ishlasa ham, 200 qaytaramiz
    if response_data['books'] or response_data['stats']:
        return Response(response_data, status=status.HTTP_200_OK)
    
    # Agar hech narsa ishlamasa, 500
    return Response(
        {
            'success': False,
            'message': 'Hech qanday ma\'lumot olinmadi',
            'errors': response_data['errors']
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


# ==================== TRANSACTION WITH ROLLBACK ====================

from django.db import transaction

@api_view(['POST'])
def create_with_transaction(request):
    """
    Transaction bilan - xato bo'lsa rollback
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    try:
        with transaction.atomic():
            # Bir nechta kitoblarni yaratish
            books_data = request.data.get('books', [])
            
            if not books_data:
                raise ValidationError('Kamida bitta kitob ma\'lumoti kerak')
            
            created_books = []
            
            for book_data in books_data:
                serializer = BookSerializer(data=book_data)
                
                if not serializer.is_valid():
                    # Xato bo'lsa - barcha o'zgarishlar bekor qilinadi
                    raise ValidationError(serializer.errors)
                
                book = serializer.save()
                created_books.append(book)
            
            return Response(
                {
                    'success': True,
                    'message': f'{len(created_books)} ta kitob yaratildi',
                    'books': BookSerializer(created_books, many=True).data
                },
                status=status.HTTP_201_CREATED
            )
    
    except ValidationError as e:
        return Response(
            {
                'success': False,
                'error': 'Validatsiya xatosi',
                'details': str(e),
                'message': 'Hech qanday kitob yaratilmadi (rollback)'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except Exception as e:
        return Response(
            {
                'success': False,
                'error': 'Server xatosi',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== CUSTOM EXCEPTION CLASS ====================

class BookNotAvailableError(Exception):
    """Custom exception - kitob mavjud emas"""
    pass


class InsufficientStockError(Exception):
    """Custom exception - kitob yetarli emas"""
    pass


@api_view(['POST'])
def purchase_book(request, pk):
    """
    Custom exception'lar bilan
    """
    from code.models import Book
    
    try:
        book = get_object_or_404(Book, pk=pk)
        quantity = int(request.data.get('quantity', 1))
        
        # Custom exception'larni qo'llash
        if not book.is_available:
            raise BookNotAvailableError(f'{book.title} kitob mavjud emas')
        
        # Biznes logika (misol uchun)
        # if book.stock < quantity:
        #     raise InsufficientStockError(f'Faqat {book.stock} ta qolgan')
        
        return Response({
            'success': True,
            'message': f'{quantity} ta "{book.title}" sotib olindi'
        })
    
    except BookNotAvailableError as e:
        return Response(
            {
                'error': 'Kitob mavjud emas',
                'details': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except InsufficientStockError as e:
        return Response(
            {
                'error': 'Yetarli miqdorda yo\'q',
                'details': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except ValueError:
        return Response(
            {'error': 'Quantity raqam bo\'lishi kerak'},
            status=status.HTTP_400_BAD_REQUEST
        )


# ==================== RETRY MECHANISM ====================

import time

@api_view(['POST'])
def create_with_retry(request, max_retries=3):
    """
    Xato bo'lsa qayta urinish
    """
    from code.models import Book
    from code.serializers import BookSerializer
    
    for attempt in range(max_retries):
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            book = serializer.save()
            
            return Response(
                {
                    'success': True,
                    'data': BookSerializer(book).data,
                    'attempts': attempt + 1
                },
                status=status.HTTP_201_CREATED
            )
        
        except IntegrityError as e:
            if attempt < max_retries - 1:
                # Kutib turish va qayta urinish
                time.sleep(0.5)
                logger.warning(f'Retry attempt {attempt + 1}/{max_retries}')
                continue
            else:
                # Oxirgi urinish ham muvaffaqiyatsiz
                return Response(
                    {
                        'success': False,
                        'error': 'Ma\'lumot saqlanmadi',
                        'attempts': max_retries,
                        'details': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except Exception as e:
            # Boshqa xatolar uchun qayta urinmaymiz
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ==================== ERROR RESPONSE HELPER ====================

def error_response(message, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Standart xato response yaratuvchi helper funksiya
    """
    from datetime import datetime
    
    response_data = {
        'success': False,
        'error': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if details:
        response_data['details'] = details
    
    return Response(response_data, status=status_code)


@api_view(['POST'])
def using_error_helper(request):
    """
    Error helper funksiyasini ishlatish
    """
    from code.serializers import BookSerializer
    
    serializer = BookSerializer(data=request.data)
    
    if not serializer.is_valid():
        return error_response(
            'Validatsiya xatosi',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        book = serializer.save()
        return Response(
            {
                'success': True,
                'data': BookSerializer(book).data
            },
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return error_response('Saqlashda xato', details=str(e))