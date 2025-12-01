"""
Lesson 21: File Upload Views
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from books.models import Book, UserProfile
from books.serializers import BookCoverSerializer, UserProfileSerializer


class BookFileUploadViewSet(viewsets.ModelViewSet):
    """
    Book ViewSet - cover image upload bilan
    """
    queryset = Book.objects.all()
    serializer_class = BookCoverSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_cover(self, request, pk=None):
        """
        Book cover yuklash
        
        POST /api/books/{id}/upload_cover/
        Body (form-data):
            - cover: [image file]
        """
        book = self.get_object()
        
        cover = request.FILES.get('cover')
        if not cover:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eski cover ni o'chirish
        if book.cover_image:
            book.cover_image.delete(save=False)
        if book.cover_thumbnail:
            book.cover_thumbnail.delete(save=False)
        
        # Yangi cover
        book.cover_image = cover
        book.cover_thumbnail = None  # Reset thumbnail
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete_cover(self, request, pk=None):
        """
        Book cover ni o'chirish
        
        DELETE /api/books/{id}/delete_cover/
        """
        book = self.get_object()
        
        if not book.cover_image:
            return Response(
                {'error': 'Book has no cover image'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete files
        if book.cover_image:
            book.cover_image.delete(save=False)
        if book.cover_thumbnail:
            book.cover_thumbnail.delete(save=False)
        
        book.cover_image = None
        book.cover_thumbnail = None
        book.save()
        
        return Response({'message': 'Cover deleted successfully'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    User Profile ViewSet - avatar bilan
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Faqat o'z profilini ko'rish
        """
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """
        O'z profilini olish va yangilash
        
        GET /api/profile/me/
        PUT /api/profile/me/
        PATCH /api/profile/me/
        """
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(
                profile,
                data=request.data,
                partial=(request.method == 'PATCH')
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def upload_avatar(self, request):
        """
        Avatar yuklash
        
        POST /api/profile/upload_avatar/
        Body (form-data):
            - avatar: [image file]
        """
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        avatar = request.FILES.get('avatar')
        if not avatar:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eski avatar ni o'chirish
        if profile.avatar:
            profile.avatar.delete(save=False)
        if profile.avatar_thumbnail:
            profile.avatar_thumbnail.delete(save=False)
        
        # Yangi avatar
        profile.avatar = avatar
        profile.avatar_thumbnail = None  # Reset thumbnail
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def delete_avatar(self, request):
        """
        Avatar ni o'chirish
        
        DELETE /api/profile/delete_avatar/
        """
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not profile.avatar:
            return Response(
                {'error': 'No avatar to delete'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete
        if profile.avatar:
            profile.avatar.delete(save=False)
        if profile.avatar_thumbnail:
            profile.avatar_thumbnail.delete(save=False)
        
        profile.avatar = None
        profile.avatar_thumbnail = None
        profile.save()
        
        return Response({'message': 'Avatar deleted successfully'})