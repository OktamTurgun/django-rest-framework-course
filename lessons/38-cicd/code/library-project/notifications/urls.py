"""
Notifications URLs
==================

API routing for notifications app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    NotificationLogViewSet,
    DeviceTokenViewSet,
    UserPreferencesViewSet,
    SendNotificationView,
    SendSMSView,
    SendPushView,
    TestNotificationView,
)

app_name = 'notifications'

# Router
router = DefaultRouter()
router.register(r'logs', NotificationLogViewSet, basename='notification-log')
router.register(r'tokens', DeviceTokenViewSet, basename='device-token')
router.register(r'preferences', UserPreferencesViewSet, basename='preferences')

# URL patterns
urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Send notification endpoints
    path('send/', SendNotificationView.as_view(), name='send-notification'),
    path('send-sms/', SendSMSView.as_view(), name='send-sms'),
    path('send-push/', SendPushView.as_view(), name='send-push'),
    
    # Test endpoint
    path('test/', TestNotificationView.as_view(), name='test-notification'),
]