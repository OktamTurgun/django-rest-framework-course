"""
Example 3: SendGrid Integration

Demonstrates:
- SendGrid API setup
- Sending emails via SendGrid
- Dynamic templates
- Tracking and analytics
- Webhooks for email events
- Best practices for production

Use cases:
- High-volume email sending
- Transactional emails
- Marketing campaigns
- Email analytics
- Deliverability monitoring

Prerequisites:
- pip install sendgrid
- SendGrid account and API key
- https://sendgrid.com/
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Email, To, Content, 
    Personalization, Attachment, 
    FileContent, FileName, FileType, Disposition
)
from django.conf import settings
from django.template.loader import render_to_string
import base64

# ============================================================================
# BASIC SENDGRID USAGE
# ============================================================================

def example_1_simple_email():
    """
    Send simple email via SendGrid
    
    Setup:
    1. Sign up at https://sendgrid.com/
    2. Get API key from Settings → API Keys
    3. Add to settings: SENDGRID_API_KEY
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple SendGrid Email")
    print("="*60)
    
    message = Mail(
        from_email='noreply@library.com',
        to_emails='user@example.com',
        subject='Welcome to Library System',
        plain_text_content='Thank you for registering!',
        html_content='<strong>Thank you for registering!</strong>'
    )
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        
        print(f"✅ Email sent via SendGrid")
        print(f"   Status Code: {response.status_code}")
        print(f"   Body: {response.body}")
        print(f"   Headers: {response.headers}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_2_with_multiple_recipients():
    """
    Send email to multiple recipients
    
    Note: Each recipient gets individual email (not CC)
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Recipients")
    print("="*60)
    
    message = Mail(
        from_email='noreply@library.com',
        to_emails=[
            'user1@example.com',
            'user2@example.com',
            'user3@example.com',
        ],
        subject='New Book Available',
        html_content='<h1>Check out our new book!</h1>'
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent to multiple recipients")
        print(f"   Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================================
# ADVANCED FEATURES
# ============================================================================

def example_3_personalization():
    """
    Send personalized emails to multiple users
    
    Each user gets customized content
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 3: Personalized Emails")
    print("="*60)
    
    message = Mail(
        from_email='noreply@library.com'
    )
    
    # Set subject
    message.subject = 'Welcome to Library System'
    
    # User 1 personalization
    personalization_1 = Personalization()
    personalization_1.add_to(Email('user1@example.com'))
    personalization_1.dynamic_template_data = {
        'username': 'John',
        'book_count': 5,
    }
    message.add_personalization(personalization_1)
    
    # User 2 personalization
    personalization_2 = Personalization()
    personalization_2.add_to(Email('user2@example.com'))
    personalization_2.dynamic_template_data = {
        'username': 'Jane',
        'book_count': 12,
    }
    message.add_personalization(personalization_2)
    
    # Set content
    message.add_content(Content(
        "text/html",
        "<h1>Welcome {{username}}!</h1><p>You have {{book_count}} books.</p>"
    ))
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print("✅ Personalized emails sent")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_with_attachment():
    """
    Send email with file attachment
    
    Useful for:
    - PDF invoices
    - CSV reports
    - Documents
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 4: Email with Attachment")
    print("="*60)
    
    message = Mail(
        from_email='billing@library.com',
        to_emails='customer@example.com',
        subject='Your Invoice',
        html_content='<p>Please find attached your invoice.</p>'
    )
    
    # Read file and encode
    with open('invoice.pdf', 'rb') as f:
        file_data = f.read()
    
    encoded_file = base64.b64encode(file_data).decode()
    
    # Create attachment
    attachment = Attachment()
    attachment.file_content = FileContent(encoded_file)
    attachment.file_type = FileType('application/pdf')
    attachment.file_name = FileName('invoice.pdf')
    attachment.disposition = Disposition('attachment')
    
    message.add_attachment(attachment)
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print("✅ Email with attachment sent")
        
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================================
# SENDGRID TEMPLATES
# ============================================================================

def example_5_dynamic_template():
    """
    Use SendGrid dynamic templates
    
    Steps:
    1. Create template in SendGrid dashboard
    2. Get template ID
    3. Send email with template data
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 5: Dynamic Template")
    print("="*60)
    
    message = Mail(
        from_email='noreply@library.com',
        to_emails='user@example.com'
    )
    
    # Set dynamic template
    message.template_id = 'd-1234567890abcdef'  # Your template ID
    
    # Template data
    message.dynamic_template_data = {
        'username': 'John Doe',
        'book_title': 'Python Programming',
        'due_date': '2024-12-31',
        'site_url': 'https://library.com',
    }
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print("✅ Dynamic template email sent")
        
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================================
# SENDGRID SERVICE CLASS
# ============================================================================

class SendGridService:
    """
    SendGrid email service wrapper
    
    Provides:
    - Simple interface
    - Error handling
    - Logging
    - Template support
    """
    
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = settings.DEFAULT_FROM_EMAIL
    
    def send_simple_email(self, to_email, subject, html_content, plain_content=None):
        """
        Send simple HTML email
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML body
            plain_content: Plain text body (optional)
        
        Returns:
            bool: Success status
        """
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            if plain_content:
                message.add_content(Content("text/plain", plain_content))
            
            response = self.client.send(message)
            
            print(f"✅ Email sent: {response.status_code}")
            return response.status_code == 202
            
        except Exception as e:
            print(f"❌ SendGrid error: {e}")
            return False
    
    def send_template_email(self, to_email, template_id, template_data):
        """
        Send email using SendGrid template
        
        Args:
            to_email: Recipient email
            template_id: SendGrid template ID
            template_data: Dict of template variables
        
        Returns:
            bool: Success status
        """
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email
            )
            
            message.template_id = template_id
            message.dynamic_template_data = template_data
            
            response = self.client.send(message)
            return response.status_code == 202
            
        except Exception as e:
            print(f"❌ Template email error: {e}")
            return False
    
    def send_bulk_personalized(self, recipients_data):
        """
        Send personalized emails to multiple recipients
        
        Args:
            recipients_data: List of dicts with 'email' and 'data' keys
        
        Example:
            recipients_data = [
                {'email': 'user1@example.com', 'data': {'name': 'John'}},
                {'email': 'user2@example.com', 'data': {'name': 'Jane'}},
            ]
        """
        try:
            message = Mail(from_email=self.from_email)
            
            for recipient in recipients_data:
                personalization = Personalization()
                personalization.add_to(Email(recipient['email']))
                personalization.dynamic_template_data = recipient['data']
                message.add_personalization(personalization)
            
            response = self.client.send(message)
            return response.status_code == 202
            
        except Exception as e:
            print(f"❌ Bulk email error: {e}")
            return False


def example_6_service_class():
    """
    Use SendGrid service class
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 6: SendGrid Service Class")
    print("="*60)
    
    service = SendGridService()
    
    # Simple email
    service.send_simple_email(
        to_email='user@example.com',
        subject='Test Email',
        html_content='<h1>Hello from SendGrid Service!</h1>'
    )
    
    # Template email
    service.send_template_email(
        to_email='user@example.com',
        template_id='d-1234567890abcdef',
        template_data={'username': 'John', 'book_count': 5}
    )
    
    # Bulk personalized
    service.send_bulk_personalized([
        {'email': 'user1@example.com', 'data': {'name': 'John'}},
        {'email': 'user2@example.com', 'data': {'name': 'Jane'}},
    ])
    
    print("✅ Service class examples completed")


# ============================================================================
# SENDGRID WEBHOOKS
# ============================================================================

def example_7_webhook_handler():
    """
    Handle SendGrid webhooks for email events
    
    Events:
    - delivered
    - opened
    - clicked
    - bounced
    - dropped
    - spam report
    
    Setup:
    1. Go to SendGrid → Settings → Mail Settings → Event Webhook
    2. Set your webhook URL
    3. Select events to track
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 7: Webhook Handler")
    print("="*60)
    
    # Example Django view for webhook
    from django.views.decorators.csrf import csrf_exempt
    from django.http import JsonResponse
    import json
    
    @csrf_exempt
    def sendgrid_webhook(request):
        """
        Handle SendGrid webhook events
        
        POST /api/webhooks/sendgrid/
        """
        if request.method == 'POST':
            events = json.loads(request.body)
            
            for event in events:
                event_type = event.get('event')
                email = event.get('email')
                timestamp = event.get('timestamp')
                
                print(f"Event: {event_type}")
                print(f"Email: {email}")
                print(f"Time: {timestamp}")
                
                # Handle different events
                if event_type == 'delivered':
                    # Update database
                    pass
                elif event_type == 'opened':
                    # Track open rate
                    pass
                elif event_type == 'clicked':
                    # Track click rate
                    pass
                elif event_type == 'bounced':
                    # Mark email as invalid
                    pass
            
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    print("✅ Webhook handler example shown")


# ============================================================================
# ANALYTICS & TRACKING
# ============================================================================

def example_8_tracking():
    """
    Enable click and open tracking
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 8: Email Tracking")
    print("="*60)
    
    from sendgrid.helpers.mail import TrackingSettings, ClickTracking, OpenTracking
    
    message = Mail(
        from_email='noreply@library.com',
        to_emails='user@example.com',
        subject='Tracked Email',
        html_content='<p>Click <a href="https://library.com">here</a></p>'
    )
    
    # Enable tracking
    tracking_settings = TrackingSettings()
    
    # Click tracking
    tracking_settings.click_tracking = ClickTracking(
        enable=True,
        enable_text=True  # Track plain text links too
    )
    
    # Open tracking
    tracking_settings.open_tracking = OpenTracking(enable=True)
    
    message.tracking_settings = tracking_settings
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print("✅ Email sent with tracking enabled")
        
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================================
# PRODUCTION BEST PRACTICES
# ============================================================================

def example_9_production_setup():
    """
    Production-ready SendGrid configuration
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 9: Production Setup")
    print("="*60)
    
    print("""
    Production Best Practices:
    
    1. Environment Variables:
       SENDGRID_API_KEY=your-api-key
       DEFAULT_FROM_EMAIL=noreply@yourdomain.com
    
    2. Domain Authentication:
       - Verify domain in SendGrid
       - Setup SPF, DKIM, DMARC records
       - Improves deliverability
    
    3. IP Warmup:
       - Gradually increase email volume
       - Start with engaged users
       - Monitor reputation
    
    4. Suppression Lists:
       - Respect unsubscribes
       - Maintain bounce list
       - Remove invalid emails
    
    5. Rate Limiting:
       - Respect SendGrid limits
       - Implement retry logic
       - Use queues (Celery)
    
    6. Error Handling:
       - Log all errors
       - Retry on transient failures
       - Alert on persistent failures
    
    7. Testing:
       - Use sandbox mode for dev
       - Test templates thoroughly
       - Monitor deliverability
    
    8. Analytics:
       - Setup webhooks
       - Track open/click rates
       - Monitor bounce rates
    """)


def example_10_error_handling():
    """
    Comprehensive error handling for SendGrid
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 10: Error Handling")
    print("="*60)
    
    from sendgrid.helpers.mail import Mail
    import logging
    
    logger = logging.getLogger(__name__)
    
    def send_email_safe(to_email, subject, content):
        """
        Send email with comprehensive error handling
        """
        try:
            message = Mail(
                from_email='noreply@library.com',
                to_emails=to_email,
                subject=subject,
                html_content=content
            )
            
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"Email sent to {to_email}")
                return True, "Email sent successfully"
            else:
                logger.warning(f"Unexpected status: {response.status_code}")
                return False, f"Status: {response.status_code}"
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"SendGrid error: {error_msg}")
            
            # Handle specific errors
            if "Unauthorized" in error_msg:
                return False, "Invalid API key"
            elif "Invalid email" in error_msg:
                return False, "Invalid recipient email"
            else:
                return False, f"Error: {error_msg}"
    
    # Test error handling
    success, message = send_email_safe(
        'test@example.com',
        'Test',
        '<p>Test email</p>'
    )
    
    print(f"{'✅' if success else '❌'} {message}")


# ============================================================================
# DEMO RUNNER
# ============================================================================

def run_all_examples():
    """Run all SendGrid examples"""
    
    print("\n" + "="*70)
    print("SENDGRID INTEGRATION EXAMPLES")
    print("="*70)
    
    print("\n⚠️  Note: These examples require:")
    print("   1. SendGrid account")
    print("   2. API key in environment")
    print("   3. pip install sendgrid")
    
    # Uncomment to run (requires valid API key)
    # example_1_simple_email()
    # example_2_with_multiple_recipients()
    # example_3_personalization()
    # example_4_with_attachment()
    # example_5_dynamic_template()
    example_6_service_class()
    example_7_webhook_handler()
    example_8_tracking()
    example_9_production_setup()
    example_10_error_handling()
    
    print("\n" + "="*70)
    print("SENDGRID EXAMPLES COMPLETED")
    print("="*70)


if __name__ == '__main__':
    run_all_examples()