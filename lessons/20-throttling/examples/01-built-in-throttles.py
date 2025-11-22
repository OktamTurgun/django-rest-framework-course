# examples/01-built-in-throttles.py
"""
DRF da built-in throttle klasslaridan foydalanish
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
    ScopedRateThrottle
)
from rest_framework import viewsets
from rest_framework.decorators import action


# =============================================================================
# 1. AnonRateThrottle - Anonim foydalanuvchilar uchun
# =============================================================================

class PublicAPIView(APIView):
    """
    Anonim foydalanuvchilar uchun cheklangan API
    IP manzil bo'yicha identifikatsiya qiladi
    """
    throttle_classes = [AnonRateThrottle]
    
    def get(self, request):
        return Response({
            'message': 'Bu ochiq API',
            'info': 'Anonim foydalanuvchilar uchun limitlangan'
        })


# =============================================================================
# 2. UserRateThrottle - Autentifikatsiya qilingan foydalanuvchilar uchun
# =============================================================================

class UserAPIView(APIView):
    """
    Autentifikatsiya qilingan foydalanuvchilar uchun
    User ID bo'yicha identifikatsiya
    """
    throttle_classes = [UserRateThrottle]
    
    def get(self, request):
        return Response({
            'message': 'Bu himoyalangan API',
            'user': str(request.user),
            'info': 'Foydalanuvchi ID bo\'yicha limitlangan'
        })


# =============================================================================
# 3. Ikkala throttle ni birga ishlatish
# =============================================================================

class MixedAPIView(APIView):
    """
    Anonim va autentifikatsiya qilingan foydalanuvchilar uchun
    Har ikki throttle ham tekshiriladi
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get(self, request):
        throttle_info = {
            'user_type': 'authenticated' if request.user.is_authenticated else 'anonymous',
            'user': str(request.user),
        }
        return Response(throttle_info)


# =============================================================================
# 4. ScopedRateThrottle - Turli scope lar uchun
# =============================================================================

class ContactAPIView(APIView):
    """
    Kontakt so'rovlari uchun alohida limit
    """
    throttle_scope = 'contacts'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request):
        return Response({
            'message': 'Kontakt so\'rovi qabul qilindi',
            'scope': 'contacts'
        })


class UploadAPIView(APIView):
    """
    Fayl yuklash uchun alohida (past) limit
    """
    throttle_scope = 'uploads'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request):
        return Response({
            'message': 'Fayl yuklash so\'rovi',
            'scope': 'uploads'
        })


class SearchAPIView(APIView):
    """
    Qidiruv uchun alohida (yuqori) limit
    """
    throttle_scope = 'searches'
    throttle_classes = [ScopedRateThrottle]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        return Response({
            'message': 'Qidiruv natijasi',
            'query': query,
            'scope': 'searches'
        })


# =============================================================================
# 5. ViewSet da throttling
# =============================================================================

class PostViewSet(viewsets.ModelViewSet):
    """
    Post ViewSet - barcha action lar uchun throttling
    """
    throttle_classes = [UserRateThrottle]
    
    def list(self, request):
        return Response({
            'action': 'list',
            'throttle': 'UserRateThrottle'
        })
    
    def create(self, request):
        return Response({
            'action': 'create',
            'throttle': 'UserRateThrottle'
        }, status=status.HTTP_201_CREATED)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product ViewSet - turli action lar uchun turli throttle
    """
    
    def get_throttles(self):
        """
        Action ga qarab throttle tanlash
        """
        if self.action in ['create', 'update', 'destroy']:
            # Yozish operatsiyalari uchun qattiqroq limit
            throttle_classes = [AnonRateThrottle]
        else:
            # O'qish operatsiyalari uchun yumshoqroq limit
            throttle_classes = [UserRateThrottle]
        
        return [throttle() for throttle in throttle_classes]
    
    def list(self, request):
        return Response({
            'action': 'list',
            'throttle': 'UserRateThrottle (yumshoq)'
        })
    
    def create(self, request):
        return Response({
            'action': 'create',
            'throttle': 'AnonRateThrottle (qattiq)'
        }, status=status.HTTP_201_CREATED)


# =============================================================================
# 6. Custom action da throttling
# =============================================================================

class ArticleViewSet(viewsets.ModelViewSet):
    """
    Article ViewSet - custom action larda throttling
    """
    throttle_classes = [UserRateThrottle]
    
    @action(detail=True, methods=['post'], 
            throttle_classes=[AnonRateThrottle])
    def like(self, request, pk=None):
        """
        Like uchun alohida qattiq limit
        """
        return Response({
            'message': f'Article {pk} like qilindi',
            'throttle': 'AnonRateThrottle'
        })
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Statistika uchun standart limit
        """
        return Response({
            'article_id': pk,
            'views': 1000,
            'throttle': 'UserRateThrottle'
        })


# =============================================================================
# 7. Conditional throttling
# =============================================================================

class ConditionalThrottleView(APIView):
    """
    Shartli throttling - faqat muayyan sharoitlarda
    """
    throttle_classes = [UserRateThrottle]
    
    def get_throttles(self):
        # Agar development mode bo'lsa, throttle yo'q
        from django.conf import settings
        if settings.DEBUG:
            return []
        
        return super().get_throttles()
    
    def get(self, request):
        return Response({
            'message': 'Conditional throttling',
            'throttled': not self.request._request.META.get('DEBUG', False)
        })


# =============================================================================
# 8. Multiple scoped throttles
# =============================================================================

class MultiScopedView(APIView):
    """
    Bir nechta scope uchun throttling
    """
    throttle_classes = [ScopedRateThrottle]
    
    def get_throttles(self):
        # GET va POST uchun turli scope
        if self.request.method == 'GET':
            self.throttle_scope = 'read_ops'
        else:
            self.throttle_scope = 'write_ops'
        
        return super().get_throttles()
    
    def get(self, request):
        return Response({
            'method': 'GET',
            'scope': 'read_ops'
        })
    
    def post(self, request):
        return Response({
            'method': 'POST',
            'scope': 'write_ops'
        })


# =============================================================================
# Settings.py da kerakli sozlamalar:
# =============================================================================

SETTINGS_EXAMPLE = """
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        # Built-in throttle lar uchun
        'anon': '100/day',          # Anonim: 100 ta kuniga
        'user': '1000/day',         # User: 1000 ta kuniga
        
        # Scoped throttle lar uchun
        'contacts': '10/day',       # Kontakt: 10 ta kuniga
        'uploads': '5/hour',        # Upload: 5 ta soatiga
        'searches': '100/minute',   # Qidiruv: 100 ta minutiga
        'read_ops': '1000/hour',    # O'qish: 1000 ta soatiga
        'write_ops': '100/hour',    # Yozish: 100 ta soatiga
    }
}

# Cache backend (throttling uchun kerak)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
"""

# =============================================================================
# URLs.py da marshrutlar
# =============================================================================

URL_PATTERNS_EXAMPLE = """
# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')
router.register('products', views.ProductViewSet, basename='product')
router.register('articles', views.ArticleViewSet, basename='article')

urlpatterns = [
    # APIView lar
    path('public/', views.PublicAPIView.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('mixed/', views.MixedAPIView.as_view()),
    
    # Scoped throttles
    path('contact/', views.ContactAPIView.as_view()),
    path('upload/', views.UploadAPIView.as_view()),
    path('search/', views.SearchAPIView.as_view()),
    
    # Conditional
    path('conditional/', views.ConditionalThrottleView.as_view()),
    path('multi-scoped/', views.MultiScopedView.as_view()),
    
    # ViewSets
    path('', include(router.urls)),
]
"""