"""
Email Service Module
Handles all email sending functionality for the library system.
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Centralized email service for sending various types of emails.
    Supports both HTML and plain text formats.
    """
    
    @staticmethod
    def send_html_email(
        subject: str,
        template_name: str,
        context: Dict,
        recipient_list: List[str],
        from_email: Optional[str] = None
    ) -> bool:
        """
        Send HTML email using template.
        
        Args:
            subject (str): Email subject line
            template_name (str): Template file name in emails/ directory
            context (dict): Context data for template rendering
            recipient_list (list): List of recipient email addresses
            from_email (str, optional): Sender email address
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Use default from email if not provided
            if from_email is None:
                from_email = settings.DEFAULT_FROM_EMAIL
            
            # Render HTML content from template
            html_content = render_to_string(
                f'emails/{template_name}',
                context
            )
            
            # Create plain text version by stripping HTML tags
            text_content = strip_tags(html_content)
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=recipient_list
            )
            
            # Attach HTML version
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send(fail_silently=False)
            
            logger.info(
                f"Email sent successfully: '{subject}' to {recipient_list}"
            )
            return True
            
        except Exception as e:
            logger.error(
                f"Failed to send email: '{subject}' to {recipient_list}. "
                f"Error: {str(e)}"
            )
            return False
    
    @staticmethod
    def send_welcome_email(user) -> bool:
        """
        Send welcome email to newly registered user.
        
        Args:
            user: User instance
            
        Returns:
            bool: True if sent successfully
        """
        if not user.email:
            logger.warning(f"User {user.username} has no email address")
            return False
        
        context = {
            'user': user,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        return EmailService.send_html_email(
            subject='Welcome to Library System! 📚',
            template_name='welcome_email.html',
            context=context,
            recipient_list=[user.email]
        )
    
    @staticmethod
    def send_book_borrowed_email(user, book, borrow_date, due_date) -> bool:
        """
        Send email notification when user borrows a book.
        
        Args:
            user: User instance
            book: Book instance
            borrow_date: Date when book was borrowed
            due_date: Date when book should be returned
            
        Returns:
            bool: True if sent successfully
        """
        if not user.email:
            logger.warning(f"User {user.username} has no email address")
            return False
        
        context = {
            'user': user,
            'book': book,
            'borrow_date': borrow_date,
            'due_date': due_date,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        return EmailService.send_html_email(
            subject=f'Book Borrowed: {book.title}',
            template_name='book_borrowed_email.html',
            context=context,
            recipient_list=[user.email]
        )
    
    @staticmethod
    def send_book_reminder_email(
        user, 
        book, 
        due_date, 
        days_until_due=0,
        is_overdue=False,
        days_overdue=0,
        late_fee=0
    ) -> bool:
        """
        Send reminder email for book return.
        
        Args:
            user: User instance
            book: Book instance
            due_date: Book due date
            days_until_due: Days remaining until due date
            is_overdue: Whether book is overdue
            days_overdue: Number of days overdue
            late_fee: Late fee amount
            
        Returns:
            bool: True if sent successfully
        """
        if not user.email:
            logger.warning(f"User {user.username} has no email address")
            return False
        
        context = {
            'user': user,
            'book': book,
            'due_date': due_date,
            'days_until_due': days_until_due,
            'is_overdue': is_overdue,
            'days_overdue': days_overdue,
            'late_fee': late_fee,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        if is_overdue:
            subject = f'⚠️ Overdue Book: {book.title}'
        else:
            subject = f'Reminder: {book.title} Due Soon'
        
        return EmailService.send_html_email(
            subject=subject,
            template_name='book_reminder_email.html',
            context=context,
            recipient_list=[user.email]
        )
    
    @staticmethod
    def send_bulk_emails(
        subject: str,
        template_name: str,
        recipient_data: List[Dict]
    ) -> Dict[str, int]:
        """
        Send bulk emails to multiple recipients with personalized content.
        
        Args:
            subject: Email subject
            template_name: Template file name
            recipient_data: List of dicts with 'email' and 'context' keys
            
        Returns:
            dict: Statistics with 'sent' and 'failed' counts
        """
        stats = {'sent': 0, 'failed': 0}
        
        for data in recipient_data:
            email = data.get('email')
            context = data.get('context', {})
            
            if email:
                success = EmailService.send_html_email(
                    subject=subject,
                    template_name=template_name,
                    context=context,
                    recipient_list=[email]
                )
                
                if success:
                    stats['sent'] += 1
                else:
                    stats['failed'] += 1
        
        logger.info(
            f"Bulk email completed: {stats['sent']} sent, "
            f"{stats['failed']} failed"
        )
        
        return stats