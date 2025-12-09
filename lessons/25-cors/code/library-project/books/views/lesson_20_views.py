from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import (
    AnonRateThrottle, 
    UserRateThrottle, 
    ScopedRateThrottle
)
from books.throttling import (
    MembershipThrottle, 
    BorrowThrottle, 
    MonitoredBookThrottle,
    SearchThrottle
)
from books.models import Book, Author
from books.serializers import BookSerializer, AuthorSerializer
from datetime import datetime


class BookViewSet(viewsets.ModelViewSet):
    """
    Kitoblar ViewSet - turli action lar uchun turli throttle
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_throttles(self):
        """
        Action ga qarab throttle tanlash
        """
        if self.action == 'list':
            # Ro'yxat ko'rish - yuqori limit
            throttle_classes = [MonitoredBookThrottle]
            
        elif self.action == 'create':
            # Yaratish - past limit
            throttle_classes = [AnonRateThrottle]
            
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Tahrirlash/O'chirish - o'rtacha limit
            throttle_classes = [UserRateThrottle]
            
        elif self.action == 'borrow':
            # Kitob olish - maxsus throttle
            throttle_classes = [BorrowThrottle]
            
        elif self.action == 'search':
            # Qidiruv - alohida throttle
            throttle_classes = [SearchThrottle]
            
        else:
            # Default
            throttle_classes = [MembershipThrottle]
        
        return [throttle() for throttle in throttle_classes]
    
    @action(detail=True, methods=['post'], throttle_classes=[BorrowThrottle])
    def borrow(self, request, pk=None):
        """
        Kitob olish - kuniga 5 ta
        """
        book = self.get_object()
        
        # Kitob mavjudligini tekshirish
        if book.available_copies <= 0:
            return Response({
                'error': 'Kitob mavjud emas'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Kitobni berish
        book.available_copies -= 1
        book.save()
        
        return Response({
            'message': f'"{book.title}" kitobini oldingiz',
            'remaining_copies': book.available_copies
        })
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """
        Kitobni qaytarish - yuqori limit
        """
        book = self.get_object()
        
        book.available_copies += 1
        book.save()
        
        return Response({
            'message': f'"{book.title}" kitobini qaytardingiz',
            'available_copies': book.available_copies
        })
    
    @action(detail=False, methods=['get'], throttle_classes=[SearchThrottle])
    def search(self, request):
        """
        Qidiruv - minutiga 30 ta
        """
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({
                'error': 'Qidiruv so\'rovi kiritilmadi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Qidiruv
        books = Book.objects.filter(title__icontains=query)
        serializer = self.get_serializer(books, many=True)
        
        return Response({
            'query': query,
            'count': books.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def quota_status(self, request):
        """
        Foydalanuvchi quota ma'lumotlari
        """
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Bugungi borrow count
        today = datetime.now().strftime('%Y-%m-%d')
        cache_key = f'borrow_throttle_{request.user.pk}_{today}'
        
        # Cache dan history olish
        from django.core.cache import cache
        history = cache.get(cache_key, [])
        
        borrowed_today = len(history) if isinstance(history, list) else 0
        
        return Response({
            'user': request.user.username,
            'borrowed_today': borrowed_today,
            'daily_limit': 5,
            'remaining': max(0, 5 - borrowed_today)
        })


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Mualliflar ViewSet - scoped throttling
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    throttle_classes = [ScopedRateThrottle]
    
    def get_throttles(self):
        # Action bo'yicha scope
        if self.action == 'list':
            self.throttle_scope = 'authors_list'
        elif self.action == 'create':
            self.throttle_scope = 'authors_create'
        
        return super().get_throttles()
