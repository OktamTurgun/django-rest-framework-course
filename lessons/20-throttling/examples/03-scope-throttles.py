# examples/03-scope-throttles.py
"""
ScopedRateThrottle - turli endpoint lar uchun turli limitlar
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import viewsets, status
from rest_framework.decorators import action


# =============================================================================
# 1. Oddiy scope throttling
# =============================================================================

class ContactFormView(APIView):
    """
    Kontakt formasi - kuniga 3 marta
    """
    throttle_scope = 'contact'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')
        
        return Response({
            'message': 'Kontakt so\'rovingiz qabul qilindi',
            'scope': 'contact',
            'limit': '3/day'
        }, status=status.HTTP_201_CREATED)


class NewsletterSubscribeView(APIView):
    """
    Newsletter obuna - kuniga 1 marta
    """
    throttle_scope = 'newsletter'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request):
        email = request.data.get('email')
        
        return Response({
            'message': 'Newsletter ga obuna bo\'ldingiz',
            'email': email,
            'scope': 'newsletter',
            'limit': '1/day'
        })


# =============================================================================
# 2. Turli HTTP metodlar uchun turli scope
# =============================================================================

class DynamicScopeView(APIView):
    """
    GET va POST uchun turli scope lar
    """
    throttle_classes = [ScopedRateThrottle]
    
    def get_throttles(self):
        # Metod bo'yicha scope o'zgartirish
        if self.request.method == 'GET':
            self.throttle_scope = 'read_operations'
        else:
            self.throttle_scope = 'write_operations'
        
        return super().get_throttles()
    
    def get(self, request):
        return Response({
            'method': 'GET',
            'scope': 'read_operations',
            'limit': '1000/hour'
        })
    
    def post(self, request):
        return Response({
            'method': 'POST',
            'scope': 'write_operations',
            'limit': '100/hour'
        })


# =============================================================================
# 3. File operation scopes
# =============================================================================

class FileUploadView(APIView):
    """
    Fayl yuklash - soatiga 5 ta
    """
    throttle_scope = 'uploads'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request):
        file = request.FILES.get('file')
        
        if not file:
            return Response({
                'error': 'Fayl topilmadi'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Fayl yuklandi',
            'filename': file.name,
            'size': file.size,
            'scope': 'uploads',
            'limit': '5/hour'
        })


class FileDownloadView(APIView):
    """
    Fayl yuklash - soatiga 50 ta
    """
    throttle_scope = 'downloads'
    throttle_classes = [ScopedRateThrottle]
    
    def get(self, request, file_id):
        return Response({
            'message': 'Fayl yuklab olish',
            'file_id': file_id,
            'scope': 'downloads',
            'limit': '50/hour'
        })


# =============================================================================
# 4. API operations scopes
# =============================================================================

class SearchAPIView(APIView):
    """
    Qidiruv API - minutiga 20 ta
    """
    throttle_scope = 'search'
    throttle_classes = [ScopedRateThrottle]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        
        return Response({
            'query': query,
            'results': [],
            'scope': 'search',
            'limit': '20/minute'
        })


class ExportAPIView(APIView):
    """
    Ma'lumotlarni eksport qilish - soatiga 2 ta
    """
    throttle_scope = 'export'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request):
        format_type = request.data.get('format', 'csv')
        
        return Response({
            'message': 'Eksport boshlandi',
            'format': format_type,
            'scope': 'export',
            'limit': '2/hour'
        })


class ImportAPIView(APIView):
    """
    Ma'lumotlarni import qilish - soatiga 1 ta
    """
    throttle_scope = 'import'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request):
        return Response({
            'message': 'Import boshlandi',
            'scope': 'import',
            'limit': '1/hour'
        })


# =============================================================================
# 5. ViewSet da scope throttling
# =============================================================================

class ArticleViewSet(viewsets.ModelViewSet):
    """
    Maqola ViewSet - turli action lar uchun turli scope
    """
    throttle_classes = [ScopedRateThrottle]
    
    def get_throttles(self):
        # Action bo'yicha scope o'rnatish
        action_scopes = {
            'list': 'article_list',
            'retrieve': 'article_detail',
            'create': 'article_create',
            'update': 'article_update',
            'destroy': 'article_delete',
        }
        
        self.throttle_scope = action_scopes.get(
            self.action, 
            'article_default'
        )
        
        return super().get_throttles()
    
    def list(self, request):
        return Response({
            'action': 'list',
            'scope': 'article_list',
            'limit': '100/minute'
        })
    
    def create(self, request):
        return Response({
            'action': 'create',
            'scope': 'article_create',
            'limit': '10/hour'
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        return Response({
            'action': 'destroy',
            'scope': 'article_delete',
            'limit': '5/hour'
        })


# =============================================================================
# 6. Custom action larda scope
# =============================================================================

class BlogViewSet(viewsets.ModelViewSet):
    """
    Blog ViewSet - custom action lar bilan
    """
    throttle_classes = [ScopedRateThrottle]
    
    @action(
        detail=True, 
        methods=['post'],
        throttle_scope='blog_like'
    )
    def like(self, request, pk=None):
        """
        Like - minutiga 10 ta
        """
        return Response({
            'message': 'Liked',
            'post_id': pk,
            'scope': 'blog_like',
            'limit': '10/minute'
        })
    
    @action(
        detail=True,
        methods=['post'],
        throttle_scope='blog_comment'
    )
    def comment(self, request, pk=None):
        """
        Komment - soatiga 20 ta
        """
        return Response({
            'message': 'Comment added',
            'post_id': pk,
            'scope': 'blog_comment',
            'limit': '20/hour'
        })
    
    @action(
        detail=True,
        methods=['post'],
        throttle_scope='blog_share'
    )
    def share(self, request, pk=None):
        """
        Ulashish - soatiga 5 ta
        """
        return Response({
            'message': 'Shared',
            'post_id': pk,
            'scope': 'blog_share',
            'limit': '5/hour'
        })
    
    @action(
        detail=True,
        methods=['get'],
        throttle_scope='blog_stats'
    )
    def stats(self, request, pk=None):
        """
        Statistika - minutiga 30 ta
        """
        return Response({
            'post_id': pk,
            'views': 1000,
            'likes': 150,
            'scope': 'blog_stats',
            'limit': '30/minute'
        })


# =============================================================================
# 7. User type va scope kombinatsiyasi
# =============================================================================

class PremiumContentView(APIView):
    """
    Premium kontent - foydalanuvchi tipiga qarab scope
    """
    throttle_classes = [ScopedRateThrottle]
    
    def get_throttles(self):
        # Foydalanuvchi tipiga qarab scope
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'is_premium') and self.request.user.is_premium:
                self.throttle_scope = 'premium_content'
            else:
                self.throttle_scope = 'regular_content'
        else:
            self.throttle_scope = 'anon_content'
        
        return super().get_throttles()
    
    def get(self, request):
        user_type = 'anonymous'
        scope = 'anon_content'
        
        if request.user.is_authenticated:
            if hasattr(request.user, 'is_premium') and request.user.is_premium:
                user_type = 'premium'
                scope = 'premium_content'
            else:
                user_type = 'regular'
                scope = 'regular_content'
        
        return Response({
            'user_type': user_type,
            'scope': scope,
            'limits': {
                'anon_content': '10/day',
                'regular_content': '100/day',
                'premium_content': '10000/day'
            }
        })


# =============================================================================
# 8. Multi-scope view
# =============================================================================

class ComplexOperationView(APIView):
    """
    Murakkab operatsiya - bir nechta scope tekshirish
    """
    
    def get_throttles(self):
        # Asosiy scope
        throttle1 = ScopedRateThrottle()
        throttle1.scope = 'complex_operation'
        
        # Qo'shimcha scope (agar POST bo'lsa)
        throttles = [throttle1]
        
        if self.request.method == 'POST':
            throttle2 = ScopedRateThrottle()
            throttle2.scope = 'write_operation'
            throttles.append(throttle2)
        
        return throttles
    
    def get(self, request):
        return Response({
            'method': 'GET',
            'scopes': ['complex_operation'],
            'limits': {
                'complex_operation': '50/hour'
            }
        })
    
    def post(self, request):
        return Response({
            'method': 'POST',
            'scopes': ['complex_operation', 'write_operation'],
            'limits': {
                'complex_operation': '50/hour',
                'write_operation': '20/hour'
            }
        })


# =============================================================================
# Settings.py da sozlamalar
# =============================================================================

"""
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        # Kontakt va newsletter
        'contact': '3/day',
        'newsletter': '1/day',
        
        # Read/Write operations
        'read_operations': '1000/hour',
        'write_operations': '100/hour',
        
        # File operations
        'uploads': '5/hour',
        'downloads': '50/hour',
        
        # API operations
        'search': '20/minute',
        'export': '2/hour',
        'import': '1/hour',
        
        # Article CRUD
        'article_list': '100/minute',
        'article_detail': '200/minute',
        'article_create': '10/hour',
        'article_update': '20/hour',
        'article_delete': '5/hour',
        'article_default': '50/hour',
        
        # Blog actions
        'blog_like': '10/minute',
        'blog_comment': '20/hour',
        'blog_share': '5/hour',
        'blog_stats': '30/minute',
        
        # User type based
        'anon_content': '10/day',
        'regular_content': '100/day',
        'premium_content': '10000/day',
        
        # Complex operations
        'complex_operation': '50/hour',
        'write_operation': '20/hour',
    }
}

# Cache backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
"""


# =============================================================================
# URLs.py
# =============================================================================

"""
# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('articles', views.ArticleViewSet, basename='article')
router.register('blogs', views.BlogViewSet, basename='blog')

urlpatterns = [
    # Contact va Newsletter
    path('contact/', views.ContactFormView.as_view()),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view()),
    
    # Dynamic scope
    path('dynamic/', views.DynamicScopeView.as_view()),
    
    # File operations
    path('upload/', views.FileUploadView.as_view()),
    path('download/<int:file_id>/', views.FileDownloadView.as_view()),
    
    # API operations
    path('search/', views.SearchAPIView.as_view()),
    path('export/', views.ExportAPIView.as_view()),
    path('import/', views.ImportAPIView.as_view()),
    
    # Premium content
    path('premium/', views.PremiumContentView.as_view()),
    
    # Complex operation
    path('complex/', views.ComplexOperationView.as_view()),
    
    # ViewSets
    path('', include(router.urls)),
]
"""