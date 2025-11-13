"""
03 - Custom Actions misoli
@action dekorator bilan qo'shimcha endpoint'lar
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Book  
from .serializers import BookSerializer, RatingSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # 1. List-level action (detail=False)
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        URL: /api/books/recent/
        So'nggi 10 ta kitobni qaytaradi
        """
        recent_books = Book.objects.all()[:10]
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)
    
    # 2. Detail-level action (detail=True)
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        URL: /api/books/{id}/publish/
        Bitta kitobni publish qiladi
        """
        book = self.get_object()
        book.published = True
        book.save()
        return Response({'status': 'book published'})
    
    # 3. Multiple HTTP methods
    @action(detail=True, methods=['get', 'post', 'delete'])
    def bookmark(self, request, pk=None):
        """
        URL: /api/books/{id}/bookmark/
        GET - bookmark bormi tekshirish
        POST - bookmark qo'shish
        DELETE - bookmark o'chirish
        """
        book = self.get_object()
        
        if request.method == 'GET':
            is_bookmarked = request.user in book.bookmarks.all()
            return Response({'bookmarked': is_bookmarked})
        
        elif request.method == 'POST':
            book.bookmarks.add(request.user)
            return Response({'status': 'bookmarked'})
        
        elif request.method == 'DELETE':
            book.bookmarks.remove(request.user)
            return Response({'status': 'bookmark removed'})
    
    # 4. Custom permission
    @action(detail=False, 
            methods=['get'], 
            permission_classes=[IsAdminUser])
    def admin_statistics(self, request):
        """
        URL: /api/books/admin_statistics/
        Faqat admin ko'ra oladi
        """
        stats = {
            'total': Book.objects.count(),
            'published': Book.objects.filter(published=True).count(),
        }
        return Response(stats)
    
    # 5. Custom URL path
    @action(detail=False, 
            methods=['get'],
            url_path='by-author/(?P<author_name>[^/.]+)')
    def by_author(self, request, author_name=None):
        """
        URL: /api/books/by-author/John/
        Muallif nomi bo'yicha qidirish
        """
        books = Book.objects.filter(author__icontains=author_name)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    # 6. Serializer bilan validation
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """
        URL: /api/books/{id}/rate/
        Kitobni baholash
        """
        book = self.get_object()
        serializer = RatingSerializer(data=request.data)
        
        if serializer.is_valid():
            rating = serializer.validated_data['rating']
            book.rating = rating
            book.save()
            return Response({'status': 'rating saved'})
        
        return Response(serializer.errors, 
                       status=status.HTTP_400_BAD_REQUEST)


# Router avtomatik yaratadigan URL'lar:
"""
Standard endpoints:
- GET    /api/books/              -> list
- POST   /api/books/              -> create
- GET    /api/books/{id}/         -> retrieve
- PUT    /api/books/{id}/         -> update
- DELETE /api/books/{id}/         -> destroy

Custom endpoints:
- GET    /api/books/recent/               -> recent action
- GET    /api/books/admin_statistics/     -> admin_statistics action
- GET    /api/books/by-author/{name}/     -> by_author action
- POST   /api/books/{id}/publish/         -> publish action
- GET    /api/books/{id}/bookmark/        -> bookmark GET
- POST   /api/books/{id}/bookmark/        -> bookmark POST
- DELETE /api/books/{id}/bookmark/        -> bookmark DELETE
- POST   /api/books/{id}/rate/            -> rate action
"""