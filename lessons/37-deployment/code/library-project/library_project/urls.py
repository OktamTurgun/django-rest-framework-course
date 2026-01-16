"""
Library Project URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView  # ← YANGI
from accounts.views import LoginView, LogoutView, UserInfoView, ChangePasswordView
from books.health import HealthCheckView

urlpatterns = [

     # ============================================================================
    # HEALTH CHECK - Production Monitoring
    # ============================================================================
    path('health/', HealthCheckView.as_view(), name='health-check'),  # ← YANGI
    path('api/health/', HealthCheckView.as_view(), name='api-health-check'),  # ← YANGI
    # ============================================================================
    # ADMIN PANEL
    # ============================================================================
    path('admin/', admin.site.urls),

    # ============================================================================
    # API VERSIONING
    # ============================================================================
    # V1 API (Deprecated)
    path('api/v1/', include('books.api.v1.urls')),
    
    # V2 API (Active)
    path('api/v2/', include('books.api.v2.urls')),

    # ============================================================================
    # API ENDPOINTS
    # ============================================================================
    path('api/', include('books.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/emails/', include('emails.urls')),
    path("api/notifications/", include("notifications.urls")),

    # ============================================================================
    # AUTHENTICATION - DRF Browsable API
    # ============================================================================
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),

    # ============================================================================
    # AUTHENTICATION - DJ-REST-AUTH (Standard)
    # ============================================================================
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # ============================================================================
    # AUTHENTICATION - SOCIAL AUTH (LESSON 31 - YANGI)
    # ============================================================================
    
    # Browser-based Social Auth (allauth)
    # Bu URLlar browser da redirect qiladi
    path('accounts/', include('allauth.urls')),
    
    # Bu URLs quyidagilarni beradi:
    # - /accounts/google/login/       → Google login page
    # - /accounts/google/login/callback/  → Google callback
    # - /accounts/github/login/       → GitHub login page
    # - /accounts/github/login/callback/  → GitHub callback
    # - va boshqalar...

    # ============================================================================
    # SHORTCUT URLs (for testing)
    # ============================================================================
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserInfoView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # ============================================================================
    # DEFAULT DJANGO AUTH (HTML)
    # ============================================================================
    path('auth/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),

    # ============================================================================
    # API DOCUMENTATION
    # ============================================================================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # ============================================================================
    # SOCIAL AUTH TEST PAGE (YANGI)
    # ============================================================================
    path('social-test/', TemplateView.as_view(
        template_name='social_auth_test.html'
    ), name='social_test'),

    # 2FA URLs - YANGI
    path('api/v1/users/', include('users.urls')),
]

# ============================================================================
# DEVELOPMENT MODE CONFIGURATION
# ============================================================================
if settings.DEBUG:
    import debug_toolbar

    # Debug Toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Static & Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)