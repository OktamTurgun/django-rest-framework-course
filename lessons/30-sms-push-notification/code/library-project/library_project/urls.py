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
from accounts.views import LoginView, LogoutView, UserInfoView, ChangePasswordView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # API VERSIONING URLS
    # V1 API (Deprecated)
    path('api/v1/', include('books.api.v1.urls')),
    
    # V2 API (Active)
    path('api/v2/', include('books.api.v2.urls')),

    # API endpoints
    path('api/', include('books.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/emails/', include('emails.urls')), # New email app URLs

    # DRF browsable API login
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),

    # dj-rest-auth
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # Shortcut URLs for testing
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserInfoView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Default Django auth (HTML)
    path('auth/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Development mode configuration
if settings.DEBUG:
    import debug_toolbar

    # Debug Toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Static & Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
