# Lesson 29: Email Notifications

> Django'da Email yuborish - SMTP, SendGrid, HTML Templates va Async Email Sending

## Maqsad

Ushbu darsda siz quyidagilarni o'rganasiz:
-  Django email system basics
-  SMTP configuration (Gmail, Outlook, etc.)
-  HTML email templates
-  SendGrid integration
-  Async email sending with Celery
-  Email service architecture
-  Email testing strategies
-  Production best practices

## Nazariy qism

### 1. Email nima uchun kerak?

**Real-world use cases:**
```
 User Registration → Welcome email
 Password Reset → Reset link email
 Order Confirmation → Receipt email
 New Book Added → Notification email
 Weekly Report → Summary email
 Newsletter → Marketing email
 Email Verification → Activation link
 Security Alert → Warning email
```

### 2. Email Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Email Sending Flow                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. User Action (register, order, etc.)                 │
│            ↓                                             │
│  2. Django View/Signal triggers email                   │
│            ↓                                             │
│  3. Email Service prepares message                       │
│            ↓                                             │
│  4. SMTP Server / SendGrid API                          │
│            ↓                                             │
│  5. User receives email                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 3. Email Methods Comparison

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| **Django SMTP** | Free, simple setup | Slow, blocked by some ISPs | Development, small apps |
| **Gmail SMTP** | Easy, reliable | Limited (500/day), needs app password | Testing, small projects |
| **SendGrid API** | Fast, scalable, analytics | Paid (free tier: 100/day) | Production, high volume |
| **Amazon SES** | Cheap, reliable | AWS setup needed | Enterprise, high volume |
| **Mailgun** | Developer-friendly | Paid | Production |

---

## Django Email Basics

### 1. Settings Configuration

**settings.py:**
```python
# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP Settings (Gmail example)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password

# Default sender
DEFAULT_FROM_EMAIL = 'Library System <noreply@library.com>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Admin emails (for error reports)
ADMINS = [
    ('Admin', 'admin@library.com'),
]

# ============================================================================
# EMAIL BACKEND OPTIONS
# ============================================================================

# Development - Console backend (prints to console)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development - File backend (saves to files)
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

# Production - SMTP backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

### 2. Basic Email Sending

```python
from django.core.mail import send_mail

# Simple email
send_mail(
    subject='Welcome to Library System',
    message='Thank you for registering!',
    from_email='noreply@library.com',
    recipient_list=['user@example.com'],
    fail_silently=False,
)
```

---

## SMTP Configuration

### Option 1: Gmail SMTP

**Setup Steps:**

1. **Enable 2-Step Verification:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Copy the generated 16-character password

3. **Django Settings:**
```python
# Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
DEFAULT_FROM_EMAIL = 'Library System <your-gmail@gmail.com>'
```

**Limits:**
- Free: 500 emails/day
- G Suite: 2000 emails/day

### Option 2: Outlook/Hotmail SMTP

```python
# Outlook SMTP
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Option 3: Custom SMTP (cPanel, etc.)

```python
# Custom SMTP
EMAIL_HOST = 'mail.yourdomain.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

---

## HTML Email Templates

### 1. Email Templates Structure

```
templates/emails/
├── base_email.html           # Base template
├── welcome_email.html        # Welcome email
├── password_reset_email.html # Password reset
├── order_confirmation.html   # Order confirmation
└── book_notification.html    # New book notification
```

### 2. Base Email Template

**templates/emails/base_email.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }
        .content {
            background-color: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
        }
        .footer {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 12px;
            border-radius: 0 0 5px 5px;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 0;
        }
        .button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Library System</h1>
    </div>
    
    <div class="content">
        {% block content %}{% endblock %}
    </div>
    
    <div class="footer">
        <p>&copy; 2024 Library System. All rights reserved.</p>
        <p>
            <a href="#" style="color: white;">Unsubscribe</a> | 
            <a href="#" style="color: white;">Contact Us</a>
        </p>
    </div>
</body>
</html>
```

### 3. Welcome Email Template

**templates/emails/welcome_email.html:**
```html
{% extends 'emails/base_email.html' %}

{% block content %}
    <h2>Welcome, {{ user.username }}!</h2>
    
    <p>Thank you for registering at Library System!</p>
    
    <p>Your account has been successfully created. You can now:</p>
    <ul>
        <li>Browse our collection of books</li>
        <li>Borrow and return books</li>
        <li>Write reviews</li>
        <li>Track your reading history</li>
    </ul>
    
    <p>
        <a href="{{ site_url }}" class="button">Start Browsing</a>
    </p>
    
    <p>If you have any questions, feel free to contact us.</p>
    
    <p>Best regards,<br>Library Team</p>
{% endblock %}
```

### 4. Sending HTML Email

```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user):
    """Send welcome email with HTML template"""
    
    # Context for template
    context = {
        'user': user,
        'site_url': 'https://library.com',
        'subject': 'Welcome to Library System',
    }
    
    # Render HTML
    html_message = render_to_string('emails/welcome_email.html', context)
    
    # Plain text version (fallback)
    plain_message = strip_tags(html_message)
    
    # Create email
    email = EmailMultiAlternatives(
        subject='Welcome to Library System',
        body=plain_message,
        from_email='noreply@library.com',
        to=[user.email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_message, "text/html")
    
    # Send
    email.send(fail_silently=False)
```

---

## SendGrid Integration

### 1. Setup SendGrid

**Install:**
```bash
pip install sendgrid
```

**Get API Key:**
1. Sign up: https://sendgrid.com/
2. Go to Settings → API Keys
3. Create API Key
4. Copy key

**settings.py:**
```python
# SendGrid configuration
SENDGRID_API_KEY = 'your-sendgrid-api-key'

# Use SendGrid backend
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

# Or use django-sendgrid-v5
# pip install django-sendgrid-v5
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
```

### 2. SendGrid Service Class

**emails/services.py:**
```python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from django.conf import settings
from django.template.loader import render_to_string

class SendGridService:
    """SendGrid email service"""
    
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    
    def send_email(self, to_email, subject, html_content, plain_content=None):
        """
        Send email via SendGrid
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML body
            plain_content: Plain text body (optional)
        """
        message = Mail(
            from_email=Email(settings.DEFAULT_FROM_EMAIL),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        if plain_content:
            message.content = [
                Content("text/plain", plain_content),
                Content("text/html", html_content)
            ]
        
        try:
            response = self.client.send(message)
            print(f"✅ Email sent: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False
    
    def send_template_email(self, to_email, template_name, context):
        """
        Send email using Django template
        
        Args:
            to_email: Recipient email
            template_name: Template path
            context: Template context
        """
        # Render template
        html_content = render_to_string(template_name, context)
        subject = context.get('subject', 'Notification')
        
        return self.send_email(to_email, subject, html_content)
```

### 3. Usage

```python
from emails.services import SendGridService

# Initialize service
email_service = SendGridService()

# Send email
email_service.send_template_email(
    to_email='user@example.com',
    template_name='emails/welcome_email.html',
    context={
        'user': user,
        'site_url': 'https://library.com',
        'subject': 'Welcome!',
    }
)
```

---

## Async Email Sending with Celery

### 1. Why Async?

**Problems with sync email:**
```python
# ❌ BAD: Blocks request for 2-3 seconds
def register_user(request):
    user = User.objects.create(...)
    send_welcome_email(user)  # Waits here!
    return Response({'message': 'Registered'})
```

**Solution: Async with Celery:**
```python
# ✅ GOOD: Returns immediately
def register_user(request):
    user = User.objects.create(...)
    send_welcome_email.delay(user.id)  # Background task
    return Response({'message': 'Registered'})
```

### 2. Celery Setup

**Install:**
```bash
pip install celery redis
```

**settings.py:**
```python
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

**library_project/celery.py:**
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

app = Celery('library_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**library_project/__init__.py:**
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### 3. Email Tasks

**emails/tasks.py:**
```python
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User

@shared_task
def send_welcome_email_task(user_id):
    """Async task to send welcome email"""
    try:
        user = User.objects.get(id=user_id)
        
        context = {
            'user': user,
            'site_url': 'https://library.com',
            'subject': 'Welcome to Library System',
        }
        
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        
        email = EmailMultiAlternatives(
            subject='Welcome to Library System',
            body=plain_message,
            from_email='noreply@library.com',
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        
        print(f"✅ Welcome email sent to {user.email}")
        return f"Email sent to {user.email}"
        
    except User.DoesNotExist:
        print(f"❌ User {user_id} not found")
        return f"User {user_id} not found"
    except Exception as e:
        print(f"❌ Email error: {e}")
        return f"Error: {e}"


@shared_task
def send_book_notification_task(book_id, user_ids):
    """Send new book notification to multiple users"""
    from books.models import Book
    
    try:
        book = Book.objects.get(id=book_id)
        users = User.objects.filter(
            id__in=user_ids,
            profile__subscribed_to_notifications=True
        )
        
        for user in users:
            context = {
                'user': user,
                'book': book,
                'site_url': 'https://library.com',
            }
            
            html_message = render_to_string('emails/book_notification.html', context)
            plain_message = strip_tags(html_message)
            
            email = EmailMultiAlternatives(
                subject=f'New Book: {book.title}',
                body=plain_message,
                from_email='noreply@library.com',
                to=[user.email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
        
        print(f"✅ Notification sent to {users.count()} users")
        return f"Sent to {users.count()} users"
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Error: {e}"


@shared_task
def send_password_reset_task(user_id, reset_token):
    """Send password reset email"""
    try:
        user = User.objects.get(id=user_id)
        
        reset_url = f"https://library.com/reset-password/{reset_token}/"
        
        context = {
            'user': user,
            'reset_url': reset_url,
        }
        
        html_message = render_to_string('emails/password_reset.html', context)
        plain_message = strip_tags(html_message)
        
        email = EmailMultiAlternatives(
            subject='Password Reset Request',
            body=plain_message,
            from_email='noreply@library.com',
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        
        return f"Reset email sent to {user.email}"
        
    except Exception as e:
        return f"Error: {e}"
```

### 4. Usage in Views/Signals

```python
from emails.tasks import send_welcome_email_task, send_book_notification_task

# In view
def register_user(request):
    user = User.objects.create(...)
    
    # Send email asynchronously
    send_welcome_email_task.delay(user.id)
    
    return Response({'message': 'Registered successfully'})

# In signal
@receiver(post_save, sender=Book)
def notify_new_book(sender, instance, created, **kwargs):
    if created:
        # Get subscribed users
        user_ids = User.objects.filter(
            profile__subscribed_to_notifications=True
        ).values_list('id', flat=True)
        
        # Send async notification
        send_book_notification_task.delay(instance.id, list(user_ids))
```

### 5. Run Celery Worker

```bash
# Start Celery worker
celery -A library_project worker --loglevel=info

# Start Celery beat (for periodic tasks)
celery -A library_project beat --loglevel=info
```

---

## Email Service Architecture

### 1. Email Service Class

**emails/services.py:**
```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .tasks import (
    send_welcome_email_task,
    send_book_notification_task,
    send_password_reset_task
)

class EmailService:
    """
    Centralized email service
    
    Handles all email sending with:
    - Template rendering
    - Async sending (Celery)
    - Error handling
    - Logging
    """
    
    @staticmethod
    def send_email(subject, template_name, context, to_email, async_send=True):
        """
        Generic email sender
        
        Args:
            subject: Email subject
            template_name: Template path
            context: Template context
            to_email: Recipient email(s)
            async_send: Send via Celery (default: True)
        """
        # Render template
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        if async_send:
            # TODO: Create generic async task
            pass
        else:
            # Send synchronously
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email] if isinstance(to_email, str) else to_email
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
    
    @staticmethod
    def send_welcome_email(user, async_send=True):
        """Send welcome email to new user"""
        if async_send:
            send_welcome_email_task.delay(user.id)
        else:
            context = {
                'user': user,
                'site_url': settings.SITE_URL,
            }
            EmailService.send_email(
                subject='Welcome to Library System',
                template_name='emails/welcome_email.html',
                context=context,
                to_email=user.email,
                async_send=False
            )
    
    @staticmethod
    def send_book_notification(book, user_ids, async_send=True):
        """Send new book notification"""
        if async_send:
            send_book_notification_task.delay(book.id, user_ids)
        else:
            # Sync send logic
            pass
    
    @staticmethod
    def send_password_reset(user, reset_token, async_send=True):
        """Send password reset email"""
        if async_send:
            send_password_reset_task.delay(user.id, reset_token)
        else:
            # Sync send logic
            pass
    
    @staticmethod
    def send_order_confirmation(order, async_send=True):
        """Send order confirmation email"""
        pass
```

---

## Testing Email

### 1. Console Backend (Development)

**settings.py:**
```python
# Development - Print to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Output:**
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Welcome to Library System
From: noreply@library.com
To: user@example.com
Date: Thu, 19 Dec 2024 10:00:00 -0000
Message-ID: <...>

Welcome, testuser!
Thank you for registering...
```

### 2. File Backend (Development)

**settings.py:**
```python
# Save to files
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
```

Emails saved to: `sent_emails/` directory

### 3. MailHog (Local Testing)

**Install:**
```bash
# Download from: https://github.com/mailhog/MailHog
# Or use Docker:
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

**settings.py:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
```

**Web UI:** http://localhost:8025

### 4. Mailtrap (Cloud Testing)

**Sign up:** https://mailtrap.io/

**settings.py:**
```python
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = 'your-mailtrap-user'
EMAIL_HOST_PASSWORD = 'your-mailtrap-password'
EMAIL_PORT = 2525
```

---

## Production Best Practices

### 1. Environment Variables

**.env:**
```
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=Library System <noreply@library.com>
```

**settings.py:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
```

### 2. Error Handling

```python
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def send_email_safe(subject, message, recipient_list):
    """Send email with error handling"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient_list}")
    except Exception as e:
        logger.error(f"Email failed: {e}")
        # Optional: Send to error tracking (Sentry)
```

### 3. Rate Limiting

```python
from django.core.cache import cache

def send_email_with_limit(user_email, subject, message):
    """Send email with rate limiting"""
    cache_key = f'email_sent:{user_email}'
    
    # Check if email sent in last hour
    if cache.get(cache_key):
        return False, "Email already sent. Please wait."
    
    # Send email
    send_mail(subject, message, 'noreply@library.com', [user_email])
    
    # Set cache (1 hour)
    cache.set(cache_key, True, 3600)
    
    return True, "Email sent successfully"
```

### 4. Email Logging

```python
class EmailLog(models.Model):
    """Log all sent emails"""
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    template = models.CharField(max_length=100)
    status = models.CharField(max_length=20)  # sent, failed
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
```

---

## Homework

[Homework topshiriqlar](homework.md) faylida.

## Qo'shimcha resurslar

- [Django Email Documentation](https://docs.djangoproject.com/en/stable/topics/email/)
- [SendGrid Django](https://github.com/elbuo8/sendgrid-django)
- [Celery Documentation](https://docs.celeryproject.org/)
- [HTML Email Templates](https://github.com/leemunroe/responsive-html-email-template)

## Keyingi dars

[Lesson 30: SMS & Push Notifications →](../30-sms-push-notifications/)

---

**Eslatma:** Production'da har doim async email sending ishlating!