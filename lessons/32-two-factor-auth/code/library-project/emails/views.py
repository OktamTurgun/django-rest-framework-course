"""
Email Test and Management Views
Provides API endpoints for testing and managing email functionality
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

from .services import EmailService
from books.models import Book


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_test_email(request):
    """
    Send test welcome email to authenticated user.
    
    POST /api/emails/test/
    
    Response:
        200: Email sent successfully
        400: User has no email
        500: Email sending failed
    """
    try:
        user = request.user
        
        # Check if user has email
        if not user.email:
            return Response(
                {
                    'error': 'User email not found',
                    'detail': 'Please add an email address to your profile'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Send test welcome email
        success = EmailService.send_welcome_email(user)
        
        if success:
            return Response({
                'message': 'Test email sent successfully',
                'email': user.email,
                'username': user.username,
                'timestamp': datetime.now().isoformat()
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    'error': 'Failed to send email',
                    'detail': 'Check server logs for more information'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        return Response(
            {
                'error': 'Internal server error',
                'detail': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_book_borrow_email(request, book_id):
    """
    Send test book borrowed email.
    
    POST /api/emails/test-borrow/{book_id}/
    
    Args:
        book_id: ID of the book to test with
        
    Response:
        200: Email sent successfully
        404: Book not found
        400: User has no email
    """
    try:
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        
        if not user.email:
            return Response(
                {'error': 'User email not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create test dates
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)
        
        # Send test email
        success = EmailService.send_book_borrowed_email(
            user=user,
            book=book,
            borrow_date=borrow_date,
            due_date=due_date
        )
        
        if success:
            return Response({
                'message': 'Test book borrow email sent',
                'email': user.email,
                'book': {
                    'id': book.id,
                    'title': book.title,
                    'author': book.author.name,
                },
                'borrow_date': borrow_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
            })
        else:
            return Response(
                {'error': 'Failed to send email'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_book_reminder_email(request, book_id):
    """
    Send test book reminder email.
    
    POST /api/emails/test-reminder/{book_id}/
    
    Query Parameters:
        is_overdue (bool): Whether to test overdue scenario
        days (int): Days until due or overdue
        
    Response:
        200: Email sent successfully
    """
    try:
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        
        if not user.email:
            return Response(
                {'error': 'User email not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get query parameters
        is_overdue = request.query_params.get('is_overdue', 'false').lower() == 'true'
        days = int(request.query_params.get('days', 3))
        
        # Calculate dates and fees
        if is_overdue:
            due_date = datetime.now() - timedelta(days=days)
            days_overdue = days
            days_until_due = 0
            late_fee = days * 1.0  # $1 per day
        else:
            due_date = datetime.now() + timedelta(days=days)
            days_overdue = 0
            days_until_due = days
            late_fee = 0
        
        # Send test reminder
        success = EmailService.send_book_reminder_email(
            user=user,
            book=book,
            due_date=due_date,
            days_until_due=days_until_due,
            is_overdue=is_overdue,
            days_overdue=days_overdue,
            late_fee=late_fee
        )
        
        if success:
            return Response({
                'message': 'Test reminder email sent',
                'email': user.email,
                'book_title': book.title,
                'scenario': 'overdue' if is_overdue else 'reminder',
                'days': days,
                'late_fee': late_fee if is_overdue else None,
            })
        else:
            return Response(
                {'error': 'Failed to send email'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def email_status(request):
    """
    Get email configuration status.
    
    GET /api/emails/status/
    
    Response:
        200: Email configuration details
    """
    from django.conf import settings
    
    return Response({
        'email_backend': settings.EMAIL_BACKEND,
        'default_from_email': settings.DEFAULT_FROM_EMAIL,
        'user_email': request.user.email or 'Not set',
        'user_has_email': bool(request.user.email),
        'site_url': getattr(settings, 'SITE_URL', 'Not configured'),
    })