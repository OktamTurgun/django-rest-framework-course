from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from books.models import Book
from books.serializers import (
    BookHomeworkFieldValidationSerializer,
    BookHomeworkObjectValidationSerializer
)

class BookHomeworkFieldValidationView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookHomeworkFieldValidationSerializer(books, many=True)
        return Response({
            "message": "Homework: field validation",
            "count": len(serializer.data),
            "results": serializer.data
        })

    def post(self, request):
        serializer = BookHomeworkFieldValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookHomeworkObjectValidationView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookHomeworkObjectValidationSerializer(books, many=True)
        return Response({
            "message": "Homework: object validation",
            "count": len(serializer.data),
            "results": serializer.data
        })

    def post(self, request):
        serializer = BookHomeworkObjectValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProtectedView(APIView):
    """
    Test authentication types
    URL: /api/protected/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Determine authentication type
        auth_type = 'Unknown'
        
        if request.auth:
            auth_type = request.auth.__class__.__name__
        elif request.user.is_authenticated:
            auth_type = 'Session'
            
        return Response({
            'message': 'Siz muvaffaqiyatli autentifikatsiya qildingiz!',
            'user': request.user.username,
            'user_id': request.user.pk,
            'email': request.user.email,
            'auth_method': auth_type,
            'is_staff': request.user.is_staff
        })
