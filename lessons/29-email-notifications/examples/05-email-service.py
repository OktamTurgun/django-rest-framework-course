"""
Example 5: Complete Email Service

Demonstrates:
- Complete email service architecture
- Unified interface for all email types
- Support for both sync and async sending
- Template management
- Error handling and logging
- Production-ready implementation

Use cases:
- Centralized email management
- Consistent email sending across app
- Easy switching between backends
- Testable email system
"""

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from typing import List, Dict, Optional, Union
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# ============================================================================
# EMAIL SERVICE CLASS
# ============================================================================

class EmailService:
    """
    Complete email service for Django application
    
    Features:
    - Unified interface
    - Template support
    - Async support (Celery)
    - Error handling
    - Logging
    - Testing support
    
    Usage:
        service = EmailService()
        service.send_welcome_email(user)
    """
    
    def __init__(self, async_send: bool = True):
        """
        Initialize email service
        
        Args:
            async_send: Use Celery for async sending (default: True)
        """
        self.async_send = async_send
        self.from_email = settings.DEFAULT_FROM_EMAIL
    
    # ========================================================================
    # CORE METHODS
    # ========================================================================
    
    def send_email(
        self,
        subject: str,
        to_email: Union[str, List[str]],
        template_name: str,
        context: Dict,
        from_email: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List] = None,
    ) -> bool:
        """
        Send email with template
        
        Args:
            subject: Email subject
            to_email: Recipient(s)
            template_name: Template path
            context: Template context
            from_email: Sender (optional)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
            attachments: List of attachments (optional)
        
        Returns:
            bool: Success status
        """
        try:
            # Render template
            html_content = render_to_string(template_name, context)
            plain_content = strip_tags(html_content)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_content,
                from_email=from_email or self.from_email,
                to=[to_email] if isinstance(to_email, str) else to_email,
                cc=cc,
                bcc=bcc,
            )
            
            # Attach HTML version
            email.attach_alternative(html_content, "text/html")
            
            # Add attachments
            if attachments:
                for attachment in attachments:
                    email.attach(*attachment)
            
            # Send
            if self.async_send:
                # Import here to avoid circular import
                from emails.tasks import send_email_task
                send_email_task.delay(email)
            else:
                email.send()
            
            logger.info(f"✅ Email sent: {subject} to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Email error: {e}")
            return False
    
    def send_simple_email(
        self,
        subject: str,
        message: str,
        to_email: Union[str, List[str]],
        html_message: Optional[str] = None,
    ) -> bool:
        """
        Send simple email without template
        
        Args:
            subject: Email subject
            message: Plain text message
            to_email: Recipient(s)
            html_message: HTML message (optional)
        
        Returns:
            bool: Success status
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[to_email] if isinstance(to_email, str) else to_email,
                html_message=html_message,
            )
            
            logger.info(f"✅ Simple email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Email error: {e}")
            return False
    
    # ========================================================================
    # SPECIFIC EMAIL METHODS
    # ========================================================================
    
    def send_welcome_email(self, user: User) -> bool:
        """
        Send welcome email to new user
        
        Args:
            user: User instance
        
        Returns:
            bool: Success status
        """
        context = {
            'user': user,
            'site_name': getattr(settings, 'SITE_NAME', 'Library System'),
            'site_url': getattr(settings, 'SITE_URL', 'https://library.com'),
        }
        
        return self.send_email(
            subject=f'Welcome to {context["site_name"]}!',
            to_email=user.email,
            template_name='emails/welcome_email.html',
            context=context
        )
    
    def send_password_reset_email(self, user: User, reset_token: str) -> bool:
        """
        Send password reset email
        
        Args:
            user: User instance
            reset_token: Reset token
        
        Returns:
            bool: Success status
        """
        reset_url = f"{settings.SITE_URL}/reset-password/{reset_token}/"
        
        context = {
            'user': user,
            'reset_url': reset_url,
            'expiry_hours': 24,
        }
        
        return self.send_email(
            subject='Password Reset Request',
            to_email=user.email,
            template_name='emails/password_reset.html',
            context=context
        )
    
    def send_email_verification(self, user: User, verification_token: str) -> bool:
        """
        Send email verification
        
        Args:
            user: User instance
            verification_token: Verification token
        
        Returns:
            bool: Success status
        """
        verification_url = f"{settings.SITE_URL}/verify-email/{verification_token}/"
        
        context = {
            'user': user,
            'verification_url': verification_url,
        }
        
        return self.send_email(
            subject='Verify Your Email',
            to_email=user.email,
            template_name='emails/email_verification.html',
            context=context
        )
    
    def send_book_borrowed_email(self, user: User, book, due_date) -> bool:
        """
        Send book borrow confirmation
        
        Args:
            user: User instance
            book: Book instance
            due_date: Due date
        
        Returns:
            bool: Success status
        """
        context = {
            'user': user,
            'book': book,
            'due_date': due_date,
        }
        
        return self.send_email(
            subject=f'Book Borrowed: {book.title}',
            to_email=user.email,
            template_name='emails/book_borrowed.html',
            context=context
        )
    
    def send_book_reminder_email(self, user: User, book, days_remaining: int) -> bool:
        """
        Send book return reminder
        
        Args:
            user: User instance
            book: Book instance
            days_remaining: Days until due
        
        Returns:
            bool: Success status
        """
        context = {
            'user': user,
            'book': book,
            'days_remaining': days_remaining,
            'is_overdue': days_remaining < 0,
        }
        
        subject = (
            f'OVERDUE: Return {book.title}' if days_remaining < 0
            else f'Reminder: Return {book.title} in {days_remaining} days'
        )
        
        return self.send_email(
            subject=subject,
            to_email=user.email,
            template_name='emails/book_reminder.html',
            context=context
        )
    
    def send_order_confirmation_email(self, user: User, order) -> bool:
        """
        Send order confirmation
        
        Args:
            user: User instance
            order: Order instance
        
        Returns:
            bool: Success status
        """
        context = {
            'user': user,
            'order': order,
            'items': order.items.all(),
            'total': order.total,
        }
        
        return self.send_email(
            subject=f'Order #{order.id} Confirmed',
            to_email=user.email,
            template_name='emails/order_confirmation.html',
            context=context
        )
    
    def send_newsletter(self, user: User, newsletter_data: Dict) -> bool:
        """
        Send newsletter
        
        Args:
            user: User instance
            newsletter_data: Newsletter content
        
        Returns:
            bool: Success status
        """
        context = {
            'user': user,
            **newsletter_data,
            'unsubscribe_url': f"{settings.SITE_URL}/unsubscribe/{user.id}/",
        }
        
        return self.send_email(
            subject=newsletter_data.get('subject', 'Newsletter'),
            to_email=user.email,
            template_name='emails/newsletter.html',
            context=context
        )
    
    def send_notification_email(self, user: User, notification_type: str, data: Dict) -> bool:
        """
        Send generic notification email
        
        Args:
            user: User instance
            notification_type: Type of notification
            data: Notification data
        
        Returns:
            bool: Success status
        """
        templates = {
            'new_book': 'emails/new_book_notification.html',
            'new_review': 'emails/new_review_notification.html',
            'account_update': 'emails/account_update.html',
        }
        
        template_name = templates.get(
            notification_type,
            'emails/generic_notification.html'
        )
        
        context = {
            'user': user,
            'notification_type': notification_type,
            **data,
        }
        
        return self.send_email(
            subject=data.get('subject', 'Notification'),
            to_email=user.email,
            template_name=template_name,
            context=context
        )
    
    # ========================================================================
    # BULK EMAIL METHODS
    # ========================================================================
    
    def send_bulk_email(
        self,
        subject: str,
        template_name: str,
        recipients: List[User],
        shared_context: Dict,
    ) -> Dict:
        """
        Send same email to multiple users
        
        Args:
            subject: Email subject
            template_name: Template path
            recipients: List of User instances
            shared_context: Context shared by all
        
        Returns:
            dict: Results with counts
        """
        sent_count = 0
        failed_count = 0
        
        for user in recipients:
            context = {
                **shared_context,
                'user': user,
            }
            
            success = self.send_email(
                subject=subject,
                to_email=user.email,
                template_name=template_name,
                context=context
            )
            
            if success:
                sent_count += 1
            else:
                failed_count += 1
        
        result = {
            'sent': sent_count,
            'failed': failed_count,
            'total': len(recipients),
        }
        
        logger.info(f"Bulk email: {result}")
        return result
    
    def send_personalized_bulk(
        self,
        recipients_data: List[Dict],
    ) -> Dict:
        """
        Send personalized emails to multiple users
        
        Args:
            recipients_data: List of dicts with user and context
                [
                    {'user': user1, 'subject': '...', 'template': '...', 'context': {}},
                    {'user': user2, 'subject': '...', 'template': '...', 'context': {}},
                ]
        
        Returns:
            dict: Results with counts
        """
        sent_count = 0
        failed_count = 0
        
        for data in recipients_data:
            user = data['user']
            subject = data['subject']
            template_name = data['template']
            context = {**data.get('context', {}), 'user': user}
            
            success = self.send_email(
                subject=subject,
                to_email=user.email,
                template_name=template_name,
                context=context
            )
            
            if success:
                sent_count += 1
            else:
                failed_count += 1
        
        return {'sent': sent_count, 'failed': failed_count}


# ============================================================================
# EMAIL SERVICE WITH LOGGING
# ============================================================================

class EmailServiceWithLogging(EmailService):
    """
    Email service with database logging
    
    Logs all sent emails to database for tracking
    """
    
    def send_email(self, *args, **kwargs) -> bool:
        """Override to add logging"""
        subject = kwargs.get('subject', args[0] if args else '')
        to_email = kwargs.get('to_email', args[1] if len(args) > 1 else '')
        template_name = kwargs.get('template_name', args[2] if len(args) > 2 else '')
        
        # Send email
        success = super().send_email(*args, **kwargs)
        
        # Log to database
        try:
            from emails.models import EmailLog
            
            EmailLog.objects.create(
                recipient=to_email if isinstance(to_email, str) else ','.join(to_email),
                subject=subject,
                template=template_name,
                status='sent' if success else 'failed',
                error_message='' if success else 'Unknown error',
            )
        except Exception as e:
            logger.error(f"Failed to log email: {e}")
        
        return success


# ============================================================================
# EMAIL SERVICE FACTORY
# ============================================================================

class EmailServiceFactory:
    """
    Factory for creating email service instances
    
    Supports different backends and configurations
    """
    
    @staticmethod
    def create(backend: str = 'django', **kwargs) -> EmailService:
        """
        Create email service instance
        
        Args:
            backend: Backend type ('django', 'sendgrid', 'ses')
            **kwargs: Additional configuration
        
        Returns:
            EmailService instance
        """
        if backend == 'django':
            return EmailService(**kwargs)
        elif backend == 'sendgrid':
            from emails.sendgrid_service import SendGridEmailService
            return SendGridEmailService(**kwargs)
        elif backend == 'ses':
            from emails.ses_service import SESEmailService
            return SESEmailService(**kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")
    
    @staticmethod
    def get_default() -> EmailService:
        """Get default email service"""
        backend = getattr(settings, 'EMAIL_SERVICE_BACKEND', 'django')
        async_send = getattr(settings, 'EMAIL_ASYNC_SEND', True)
        
        return EmailServiceFactory.create(
            backend=backend,
            async_send=async_send
        )


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_1_basic_usage():
    """Basic email service usage"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    service = EmailService(async_send=False)
    
    # Get user
    user = User.objects.first()
    
    # Send welcome email
    service.send_welcome_email(user)
    
    # Send custom email
    service.send_email(
        subject='Test Email',
        to_email=user.email,
        template_name='emails/test.html',
        context={'user': user, 'message': 'Hello!'}
    )
    
    print("✅ Emails sent")


def example_2_bulk_emails():
    """Send bulk emails"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Bulk Emails")
    print("="*60)
    
    service = EmailService(async_send=True)
    
    # Get users
    users = User.objects.filter(is_active=True)[:10]
    
    # Send newsletter to all
    result = service.send_bulk_email(
        subject='December Newsletter',
        template_name='emails/newsletter.html',
        recipients=users,
        shared_context={
            'month': 'December',
            'year': 2024,
        }
    )
    
    print(f"✅ Bulk email result: {result}")


def example_3_with_logging():
    """Use service with logging"""
    print("\n" + "="*60)
    print("EXAMPLE 3: With Logging")
    print("="*60)
    
    service = EmailServiceWithLogging(async_send=False)
    
    user = User.objects.first()
    service.send_welcome_email(user)
    
    # Check logs
    from emails.models import EmailLog
    logs = EmailLog.objects.filter(recipient=user.email)
    print(f"✅ Email logs: {logs.count()}")


def example_4_factory_pattern():
    """Use factory pattern"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Factory Pattern")
    print("="*60)
    
    # Get default service
    service = EmailServiceFactory.get_default()
    
    # Or specify backend
    django_service = EmailServiceFactory.create('django', async_send=False)
    # sendgrid_service = EmailServiceFactory.create('sendgrid')
    
    user = User.objects.first()
    service.send_welcome_email(user)
    
    print("✅ Factory pattern demonstrated")


def example_5_error_handling():
    """Error handling in service"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Error Handling")
    print("="*60)
    
    service = EmailService(async_send=False)
    
    # Try with invalid email
    success = service.send_simple_email(
        subject='Test',
        message='Test message',
        to_email='invalid-email'  # Invalid
    )
    
    print(f"Result: {'✅ Success' if success else '❌ Failed'}")


# ============================================================================
# INTEGRATION WITH DJANGO VIEWS
# ============================================================================

"""
# In views.py

from emails.services import EmailServiceFactory

class RegisterView(APIView):
    def post(self, request):
        # Create user
        user = User.objects.create_user(...)
        
        # Send welcome email
        email_service = EmailServiceFactory.get_default()
        email_service.send_welcome_email(user)
        
        return Response({'message': 'Registered'})


class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        
        # Generate token
        token = generate_reset_token(user)
        
        # Send reset email
        email_service = EmailServiceFactory.get_default()
        email_service.send_password_reset_email(user, token)
        
        return Response({'message': 'Email sent'})
"""

# ============================================================================
# INTEGRATION WITH SIGNALS
# ============================================================================

"""
# In signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from emails.services import EmailServiceFactory

@receiver(post_save, sender=User)
def send_welcome_on_registration(sender, instance, created, **kwargs):
    if created:
        email_service = EmailServiceFactory.get_default()
        email_service.send_welcome_email(instance)


from books.signals import book_borrowed

@receiver(book_borrowed)
def send_borrow_confirmation(sender, book, user, due_date, **kwargs):
    email_service = EmailServiceFactory.get_default()
    email_service.send_book_borrowed_email(user, book, due_date)
"""

# ============================================================================
# DEMO RUNNER
# ============================================================================

def run_all_examples():
    """Run all email service examples"""
    
    print("\n" + "="*70)
    print("COMPLETE EMAIL SERVICE EXAMPLES")
    print("="*70)
    
    example_1_basic_usage()
    example_2_bulk_emails()
    example_3_with_logging()
    example_4_factory_pattern()
    example_5_error_handling()
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)


if __name__ == '__main__':
    run_all_examples()