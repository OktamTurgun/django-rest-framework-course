"""
Email App URL Configuration
"""

from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    # Email status
    path('status/', views.email_status, name='email-status'),
    
    # Test endpoints
    path('test/', views.send_test_email, name='test-email'),
    path('test-borrow/<int:book_id>/', views.test_book_borrow_email, name='test-borrow'),
    path('test-reminder/<int:book_id>/', views.test_book_reminder_email, name='test-reminder'),
]