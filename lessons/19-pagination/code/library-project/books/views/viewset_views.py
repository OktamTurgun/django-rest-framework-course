from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from books.models import Book
from books.serializers import BookSerializer
from books.permissions import IsOwnerOrReadOnly, IsPublishedOrOwner, IsOwnerOrAdmin


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def published(self, request):
        books = Book.objects.filter(published=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Book.objects.count()
        published = Book.objects.filter(published=True).count()
        return Response({
            "total": total,
            "published": published,
            "unpublished": total - published
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_books(self, request):
        books = Book.objects.filter(owner=request.user)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def publish(self, request, pk=None):
        book = self.get_object()
        book.published = True
        book.save()
        return Response(self.get_serializer(book).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def unpublish(self, request, pk=None):
        book = self.get_object()
        book.published = False
        book.save()
        return Response(self.get_serializer(book).data)
