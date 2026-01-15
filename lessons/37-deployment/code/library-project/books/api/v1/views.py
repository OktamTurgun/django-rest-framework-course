"""
V1 API Views
"""
from rest_framework import generics
from books.models import Book, Author
from rest_framework.response import Response
from .serializers import (
    BookSerializerV1,
    BookListSerializerV1,
    AuthorSerializerV1
)
from .pagination import V1Pagination


class BookListAPIView(generics.ListCreateAPIView):
    """
    V1: Book List and Create
    GET: List all books
    POST: Create new book
    """
    queryset = Book.objects.select_related('author').all()
    pagination_class = V1Pagination
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializerV1
        return BookSerializerV1


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    V1: Book Detail, Update, Delete
    GET: Retrieve book
    PUT/PATCH: Update book
    DELETE: Delete book
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV1


class AuthorListAPIView(generics.ListCreateAPIView):
    """
    V1: Author List and Create
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializerV1
    pagination_class = V1Pagination


class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    V1: Author Detail, Update, Delete
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializerV1

    def retrieve(self, request, *args, **kwargs):
        """Add version info to response"""
        instance = self.get_object()
        serilizer = self.get_serializer(instance)
        return Response({
            'version': 'v1',
            'data': serializer.data
        })
    
class AuthorBooksAPIView(generics.ListAPIView):
    """
    V1: List all books by specific author
    """
    serializer_class = BookListSerializerV1
    pagination_class = V1Pagination
    
    def get_queryset(self):
        """Filter books by author"""
        author_id = self.kwargs['pk']
        return Book.objects.filter(author_id=author_id).select_related('author')
    
    def list(self, request, *args, **kwargs):
        """Custom response with author info"""
        author_id = self.kwargs['pk']
        
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(
                {
                    'version': 'v1',
                    'error': 'Author not found'
                },
                status=404
            )
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            # Add author info to paginated response
            response.data['author'] = author.name
            response.data['total_books'] = queryset.count()
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'version': 'v1',
            'author': author.name,
            'total_books': queryset.count(),
            'books': serializer.data
        })