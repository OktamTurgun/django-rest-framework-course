"""
Example 1: Basic SMTP Email Sending

Demonstrates:
- Django's send_mail() function
- send_mass_mail() for bulk emails
- EmailMessage for advanced features
- Basic error handling
- Console backend for testing

Use cases:
- Simple notifications
- Password reset emails
- Contact form emails
- Basic alerts
"""

from django.core.exceptions import ValidationError

from django.core.mail import (
    send_mail,
    send_mass_mail,
    EmailMessage,
    EmailMultiAlternatives
)
from django.conf import settings

# ============================================================================
# BASIC EMAIL SENDING
# ============================================================================

def example_1_simple_email():
    """
    Simplest way to send email in Django
    
    send_mail() parameters:
    - subject: Email subject line
    - message: Plain text message body
    - from_email: Sender email (uses DEFAULT_FROM_EMAIL if None)
    - recipient_list: List of recipient emails
    - fail_silently: If False, raises exception on error
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Email")
    print("="*60)
    
    try:
        send_mail(
            subject='Welcome to Library System',
            message='Thank you for registering. Start browsing books now!',
            from_email='noreply@library.com',
            recipient_list=['user@example.com'],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
        
    except Exception as e:
        print(f"❌ Email failed: {e}")


def example_2_multiple_recipients():
    """
    Send same email to multiple recipients
    
    Note: All recipients will see each other's emails in 'To' field
    For individual emails, use loop or send_mass_mail()
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Recipients")
    print("="*60)
    
    recipients = [
        'user1@example.com',
        'user2@example.com',
        'user3@example.com',
    ]
    
    send_mail(
        subject='New Book Available',
        message='Check out our latest book: Python Programming',
        from_email='noreply@library.com',
        recipient_list=recipients,
    )
    
    print(f"✅ Email sent to {len(recipients)} recipients")


def example_3_with_auth_user():
    """
    Send email with auth_user and auth_password
    
    Useful when you want to override default SMTP credentials
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 3: With Auth Credentials")
    print("="*60)
    
    send_mail(
        subject='Test Email',
        message='Testing custom SMTP credentials',
        from_email='custom@example.com',
        recipient_list=['user@example.com'],
        auth_user='custom@example.com',  # Override EMAIL_HOST_USER
        auth_password='custom-password',  # Override EMAIL_HOST_PASSWORD
    )
    
    print("✅ Email sent with custom credentials")


# ============================================================================
# BULK EMAILS
# ============================================================================

def example_4_mass_mail():
    """
    Send different emails to different recipients efficiently
    
    send_mass_mail() sends all emails in one SMTP connection
    Much faster than calling send_mail() in a loop
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 4: Mass Mail")
    print("="*60)
    
    # Each tuple: (subject, message, from_email, recipient_list)
    messages = (
        (
            'Welcome User 1',
            'Hi User 1, welcome to Library System!',
            'noreply@library.com',
            ['user1@example.com']
        ),
        (
            'Welcome User 2',
            'Hi User 2, welcome to Library System!',
            'noreply@library.com',
            ['user2@example.com']
        ),
        (
            'Welcome User 3',
            'Hi User 3, welcome to Library System!',
            'noreply@library.com',
            ['user3@example.com']
        ),
    )
    
    # Send all emails in one connection
    num_sent = send_mass_mail(messages, fail_silently=False)
    
    print(f"✅ {num_sent} emails sent via mass mail")


# ============================================================================
# EMAIL MESSAGE CLASS
# ============================================================================

def example_5_email_message_basic():
    """
    EmailMessage class for more control
    
    Advantages over send_mail():
    - Can add attachments
    - Can add CC, BCC
    - Can add custom headers
    - More flexible
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 5: EmailMessage Basic")
    print("="*60)
    
    email = EmailMessage(
        subject='Order Confirmation',
        body='Your order #12345 has been confirmed.',
        from_email='orders@library.com',
        to=['customer@example.com'],
        bcc=['admin@library.com'],  # Blind carbon copy
        cc=['manager@library.com'],  # Carbon copy
        reply_to=['support@library.com'],  # Reply-to address
    )
    
    email.send()
    
    print("✅ Email sent with CC and BCC")


def example_6_email_with_attachment():
    """
    Send email with file attachment
    
    Use cases:
    - Send invoice PDF
    - Send report CSV
    - Send document
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 6: Email with Attachment")
    print("="*60)
    
    email = EmailMessage(
        subject='Your Invoice',
        body='Please find attached your invoice.',
        from_email='billing@library.com',
        to=['customer@example.com'],
    )
    
    # Attach file from path
    # email.attach_file('/path/to/invoice.pdf')
    
    # Or attach from content
    invoice_content = b'PDF content here...'
    email.attach(
        filename='invoice.pdf',
        content=invoice_content,
        mimetype='application/pdf'
    )
    
    email.send()
    
    print("✅ Email sent with attachment")


def example_7_custom_headers():
    """
    Add custom email headers
    
    Use cases:
    - Message-ID for tracking
    - X-Custom headers for metadata
    - List-Unsubscribe for newsletters
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 7: Custom Headers")
    print("="*60)
    
    email = EmailMessage(
        subject='Newsletter',
        body='Check out this month\'s updates!',
        from_email='newsletter@library.com',
        to=['subscriber@example.com'],
    )
    
    # Add custom headers
    email.extra_headers = {
        'X-Campaign-ID': '12345',
        'X-Newsletter': 'Monthly',
        'List-Unsubscribe': '<mailto:unsubscribe@library.com>',
    }
    
    email.send()
    
    print("✅ Email sent with custom headers")


# ============================================================================
# HTML EMAILS
# ============================================================================

def example_8_html_email():
    """
    Send HTML email with plain text alternative
    
    Best practice: Always provide both HTML and plain text versions
    Some email clients don't support HTML
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 8: HTML Email")
    print("="*60)
    
    # Plain text version
    text_content = 'Welcome to Library System! Start browsing books now.'
    
    # HTML version
    html_content = '''
    <html>
    <head></head>
    <body>
        <h1 style="color: #4CAF50;">Welcome to Library System! 📚</h1>
        <p>Thank you for registering.</p>
        <p>
            <a href="https://library.com/books" 
               style="background: #4CAF50; color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 5px;">
                Start Browsing Books
            </a>
        </p>
    </body>
    </html>
    '''
    
    email = EmailMultiAlternatives(
        subject='Welcome!',
        body=text_content,  # Plain text version
        from_email='noreply@library.com',
        to=['user@example.com']
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    email.send()
    
    print("✅ HTML email sent with plain text fallback")


# ============================================================================
# ERROR HANDLING
# ============================================================================

def example_9_error_handling():
    """
    Proper error handling for email sending
    
    Common errors:
    - SMTPAuthenticationError: Wrong username/password
    - SMTPConnectError: Can't connect to SMTP server
    - SMTPException: General SMTP error
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 9: Error Handling")
    print("="*60)
    
    from smtplib import SMTPException
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        send_mail(
            subject='Test Email',
            message='Testing error handling',
            from_email='noreply@library.com',
            recipient_list=['user@example.com'],
            fail_silently=False,  # Raise exception on error
        )
        
        print("✅ Email sent successfully")
        logger.info("Email sent to user@example.com")
        
    except SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        logger.error(f"SMTP error: {e}")
        # Handle SMTP-specific errors
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.exception("Unexpected email error")
        # Handle other errors


def example_10_validation():
    """
    Validate email addresses before sending
    
    Django's email validator checks format
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 10: Email Validation")
    print("="*60)
    
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    
    test_emails = [
        'valid@example.com',      # ✅ Valid
        'invalid-email',          # ❌ Invalid
        'test@domain',            # ❌ Invalid
        'user@example.co.uk',     # ✅ Valid
    ]
    
    for email in test_emails:
        try:
            validate_email(email)
            print(f"✅ Valid: {email}")
        except ValidationError:
            print(f"❌ Invalid: {email}")


# ============================================================================
# BEST PRACTICES
# ============================================================================

def example_11_best_practices():
    """
    Email sending best practices
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 11: Best Practices")
    print("="*60)
    
    # ✅ GOOD: Use try-except
    try:
        send_mail(
            subject='Important',
            message='This is important.',
            from_email='noreply@library.com',
            recipient_list=['user@example.com'],
            fail_silently=False,  # Raise on error
        )
    except Exception as e:
        # Log error, notify admins, etc.
        print(f"Error: {e}")
    
    # ✅ GOOD: Validate email before sending
    from django.core.validators import validate_email
    email = 'user@example.com'
    try:
        validate_email(email)
        # send_mail(...)
    except ValidationError:
        print(f"Invalid email: {email}")
    
    # ✅ GOOD: Use mass mail for bulk
    # Instead of loop, use send_mass_mail()
    
    # ✅ GOOD: Provide plain text + HTML
    # Use EmailMultiAlternatives
    
    # ✅ GOOD: Use descriptive from_email
    # 'Library System <noreply@library.com>' instead of just email
    
    print("✅ Best practices demonstrated")


# ============================================================================
# TESTING
# ============================================================================

def example_12_console_backend():
    """
    Use console backend for testing
    
    In settings.py:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    Emails will be printed to console instead of sent
    Perfect for development!
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 12: Console Backend Testing")
    print("="*60)
    
    send_mail(
        subject='Test Email',
        message='This email is printed to console, not sent.',
        from_email='noreply@library.com',
        recipient_list=['user@example.com'],
    )
    
    print("✅ Check console output above for email content")


# ============================================================================
# DEMO RUNNER
# ============================================================================

def run_all_examples():
    """Run all examples"""
    
    print("\n" + "="*70)
    print("DJANGO EMAIL EXAMPLES - BASIC SMTP")
    print("="*70)
    
    example_1_simple_email()
    example_2_multiple_recipients()
    # example_3_with_auth_user()  # Skip - needs real credentials
    example_4_mass_mail()
    example_5_email_message_basic()
    example_6_email_with_attachment()
    example_7_custom_headers()
    example_8_html_email()
    example_9_error_handling()
    example_10_validation()
    example_11_best_practices()
    example_12_console_backend()
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)
    print("\n💡 TIP: Use console backend in development:")
    print("   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'")


# ============================================================================
# COMMON PITFALLS TO AVOID
# ============================================================================

"""
❌ DON'T:

1. Block request thread with email sending
   # Bad
   def register_view(request):
       user = create_user(...)
       send_mail(...)  # Blocks for 2-3 seconds!
       return response
   
   # Good
   def register_view(request):
       user = create_user(...)
       send_welcome_email.delay(user.id)  # Celery task
       return response

2. Send emails in loops without bulk methods
   # Bad
   for user in users:
       send_mail(...)  # New SMTP connection each time
   
   # Good
   send_mass_mail(messages)  # One connection

3. Forget error handling
   # Bad
   send_mail(...)  # What if it fails?
   
   # Good
   try:
       send_mail(...)
   except Exception as e:
       logger.error(f"Email failed: {e}")

4. Hard-code email addresses
   # Bad
   send_mail(..., from_email='admin@library.com', ...)
   
   # Good
   send_mail(..., from_email=settings.DEFAULT_FROM_EMAIL, ...)

5. Send HTML without plain text alternative
   # Bad
   email = EmailMessage(body='<html>...</html>')
   
   # Good
   email = EmailMultiAlternatives(body='Plain text...')
   email.attach_alternative('<html>...</html>', "text/html")

✅ DO:

1. Use async sending (Celery) for non-critical emails
2. Use send_mass_mail() for bulk emails
3. Always handle exceptions
4. Use console backend in development
5. Validate email addresses
6. Provide both HTML and plain text
7. Use environment variables for credentials
8. Test emails before deploying
9. Monitor email sending (logs, Sentry)
10. Respect user preferences (unsubscribe)
"""


# ============================================================================
# USAGE
# ============================================================================

if __name__ == '__main__':
    """
    Run examples in Django shell:
    
    python manage.py shell
    >>> from examples.01_smtp_basic import run_all_examples
    >>> run_all_examples()
    
    Or run specific example:
    >>> from examples.01_smtp_basic import example_1_simple_email
    >>> example_1_simple_email()
    """
    
    run_all_examples()