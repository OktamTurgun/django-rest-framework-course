# Homework: Email Notifications

## Maqsad

Library Project'ga email notification system qo'shish.

---

## Task 1: Basic Email Setup (20 points)

### 1.1 SMTP Configuration (10 points)

**settings.py:**
```python
# TODO: Configure email backend
# Use console backend for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Or use Gmail SMTP (get app password from Google)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
# DEFAULT_FROM_EMAIL = 'Library System <your-email@gmail.com>'
```

**Test:**
```python
# Python shell
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from Library System.',
    'noreply@library.com',
    ['your-email@gmail.com'],
)
```

### 1.2 Create Email Templates (10 points)

**Create template structure:**
```
templates/emails/
├── base_email.html
├── welcome_email.html
├── book_borrowed_email.html
└── book_reminder_email.html
```

**templates/emails/base_email.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
        }
        .header {
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 20px;
            background-color: #f9f9f9;
        }
        .footer {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 12px;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Library System</h1>
    </div>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
    <div class="footer">
        <p>&copy; 2024 Library System</p>
    </div>
</body>
</html>
```

**templates/emails/welcome_email.html:**
```html
{% extends 'emails/base_email.html' %}

{% block content %}
    <h2>Welcome, {{ user.username }}!</h2>
    <p>Thank you for joining Library System.</p>
    <p>You can now:</p>
    <ul>
        <li>Browse books</li>
        <li>Borrow books</li>
        <li>Write reviews</li>
    </ul>
    <p>
        <a href="{{ site_url }}" class="button">Start Browsing</a>
    </p>
{% endblock %}
```

---

## Task 2: Email Service Class (25 points)

### 2.1 Create Email Service (15 points)

**emails/services.py:**
```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class EmailService:
    """
    TODO: Implement email service
    
    Methods:
    - send_html_email(subject, template_name, context, to_email)
    - send_welcome_email(user)
    - send_book_borrowed_email(user, book, due_date)
    - send_book_reminder_email(user, book, days_remaining)
    """
    
    @staticmethod
    def send_html_email(subject, template_name, context, to_email):
        """
        TODO: Send HTML email
        
        Steps:
        1. Render HTML template with context
        2. Create plain text version (strip_tags)
        3. Create EmailMultiAlternatives
        4. Attach HTML alternative
        5. Send email
        """
        pass
    
    @staticmethod
    def send_welcome_email(user):
        """
        TODO: Send welcome email to new user
        
        Template: emails/welcome_email.html
        Context: user, site_url
        """
        pass
    
    @staticmethod
    def send_book_borrowed_email(user, book, due_date):
        """
        TODO: Send confirmation email when book borrowed
        
        Template: emails/book_borrowed_email.html
        Context: user, book, due_date
        """
        pass
```

### 2.2 Create Email Templates (10 points)

**templates/emails/book_borrowed_email.html:**
```html
{% extends 'emails/base_email.html' %}

{% block content %}
    <h2>Book Borrowed Successfully! 📚</h2>
    <p>Hi {{ user.username }},</p>
    <p>You have successfully borrowed:</p>
    <div style="background: white; padding: 15px; border-left: 4px solid #4CAF50;">
        <h3>{{ book.title }}</h3>
        <p><strong>Author:</strong> {{ book.author.name }}</p>
        <p><strong>Due Date:</strong> {{ due_date|date:"F d, Y" }}</p>
    </div>
    <p>Please return the book by the due date to avoid penalties.</p>
{% endblock %}
```

**templates/emails/book_reminder_email.html:**
```html
{% extends 'emails/base_email.html' %}

{% block content %}
    <h2>Book Return Reminder ⏰</h2>
    <p>Hi {{ user.username }},</p>
    <p>This is a reminder that the following book is due soon:</p>
    <div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">
        <h3>{{ book.title }}</h3>
        <p><strong>Due in:</strong> {{ days_remaining }} days</p>
    </div>
    <p>Please return it on time to avoid late fees.</p>
{% endblock %}
```

---

## Task 3: Integration with Signals (20 points)

### 3.1 Welcome Email on User Registration (10 points)

**accounts/signals.py:**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from emails.services import EmailService

@receiver(post_save, sender=User)
def send_welcome_email_on_registration(sender, instance, created, **kwargs):
    """
    TODO: Send welcome email when user is created
    
    Steps:
    1. Check if user is newly created (created=True)
    2. Call EmailService.send_welcome_email(instance)
    3. Handle exceptions (try/except)
    """
    pass
```

### 3.2 Borrow Confirmation Email (10 points)

**books/signals.py:**
```python
from django.dispatch import receiver
from .signals import book_borrowed
from emails.services import EmailService

@receiver(book_borrowed)
def send_borrow_confirmation(sender, book, user, due_date, **kwargs):
    """
    TODO: Send email when book is borrowed
    
    Steps:
    1. Call EmailService.send_book_borrowed_email(user, book, due_date)
    2. Handle exceptions
    3. Log email status
    """
    pass
```

---

## Task 4: Async Email with Celery (25 points)

### 4.1 Setup Celery (10 points)

**Install:**
```bash
pip install celery redis
```

**settings.py:**
```python
# TODO: Configure Celery
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
```

**library_project/celery.py:**
```python
# TODO: Create Celery app
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

app = Celery('library_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**library_project/__init__.py:**
```python
# TODO: Import celery app
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### 4.2 Create Email Tasks (15 points)

**emails/tasks.py:**
```python
from celery import shared_task
from django.contrib.auth.models import User
from books.models import Book
from .services import EmailService

@shared_task
def send_welcome_email_task(user_id):
    """
    TODO: Async task to send welcome email
    
    Steps:
    1. Get user by ID
    2. Call EmailService.send_welcome_email(user)
    3. Return success message
    4. Handle exceptions
    """
    pass

@shared_task
def send_book_borrowed_email_task(user_id, book_id, due_date_str):
    """
    TODO: Async task to send borrow confirmation
    
    Steps:
    1. Get user and book by IDs
    2. Parse due_date_str to datetime
    3. Call EmailService.send_book_borrowed_email(...)
    4. Handle exceptions
    """
    pass

@shared_task
def send_reminder_emails_task():
    """
    TODO: Periodic task to send reminders
    
    Steps:
    1. Find books due in 3 days
    2. Get BorrowHistory records (returned_at=None, due_date in 3 days)
    3. Loop through and send reminder emails
    4. Return count of sent emails
    """
    pass
```

### 4.3 Update Signals to Use Tasks (bonus)

**books/signals.py:**
```python
@receiver(book_borrowed)
def send_borrow_confirmation_async(sender, book, user, due_date, **kwargs):
    """
    TODO: Send email asynchronously
    
    Use: send_book_borrowed_email_task.delay(...)
    """
    from emails.tasks import send_book_borrowed_email_task
    
    # TODO: Call async task
    pass
```

---

## Task 5: Email Endpoints (10 points)

### 5.1 Test Email Endpoint (5 points)

**emails/views.py:**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .services import EmailService

class SendTestEmailView(APIView):
    """
    Test email sending
    
    POST /api/emails/test/
    Body: {
        "to_email": "test@example.com",
        "subject": "Test Email"
    }
    """
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        """
        TODO: Send test email
        
        Steps:
        1. Get to_email and subject from request.data
        2. Send simple email using Django's send_mail
        3. Return success response
        """
        pass
```

### 5.2 Resend Welcome Email (5 points)

**emails/views.py:**
```python
class ResendWelcomeEmailView(APIView):
    """
    Resend welcome email to user
    
    POST /api/emails/resend-welcome/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        TODO: Resend welcome email to current user
        
        Steps:
        1. Get current user (request.user)
        2. Call EmailService.send_welcome_email(user)
        3. Return success response
        """
        pass
```

---

## Task 6: Email Logging (Bonus - 10 points)

### 6.1 Email Log Model

**emails/models.py:**
```python
from django.db import models
from django.contrib.auth.models import User

class EmailLog(models.Model):
    """
    TODO: Create email log model
    
    Fields:
    - recipient (EmailField)
    - subject (CharField)
    - template (CharField)
    - status (CharField: sent, failed)
    - error_message (TextField, blank=True)
    - sent_at (DateTimeField, auto_now_add=True)
    """
    pass
```

### 6.2 Log Emails in Service

**emails/services.py:**
```python
class EmailService:
    
    @staticmethod
    def send_html_email(subject, template_name, context, to_email):
        """
        TODO: Add logging
        
        Steps:
        1. Try to send email
        2. If success: Create EmailLog (status='sent')
        3. If fail: Create EmailLog (status='failed', error_message=str(e))
        """
        pass
```

---

## Testing Checklist

### Manual Testing

**Test 1: Basic Email**
```bash
python manage.py shell

from django.core.mail import send_mail
send_mail('Test', 'Test message', 'noreply@library.com', ['your-email@gmail.com'])
```

**Expected:** Email received (or printed to console if using console backend)

**Test 2: Welcome Email**
```bash
# Create new user via API
POST /api/accounts/register/
{
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "pass123",
    "password2": "pass123"
}
```

**Expected:** 
- Welcome email sent to test2@example.com
- Check console output or inbox

**Test 3: Borrow Confirmation**
```bash
# Borrow a book
POST /api/books/1/borrow/
```

**Expected:**
- Borrow confirmation email sent
- Email contains book details and due date

**Test 4: Celery Task**
```bash
# Start Celery worker
celery -A library_project worker -l info

# In shell
from emails.tasks import send_welcome_email_task
send_welcome_email_task.delay(1)
```

**Expected:**
- Task appears in Celery logs
- Email sent asynchronously

### Automated Testing

**emails/tests.py:**
```python
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from .services import EmailService

class EmailServiceTest(TestCase):
    
    def test_send_welcome_email(self):
        """
        TODO: Test welcome email
        
        Steps:
        1. Create test user
        2. Call EmailService.send_welcome_email(user)
        3. Assert len(mail.outbox) == 1
        4. Assert mail.outbox[0].subject contains 'Welcome'
        5. Assert user.email in mail.outbox[0].to
        """
        pass
    
    def test_send_html_email(self):
        """TODO: Test HTML email sending"""
        pass
```

---

## Submission

### 1. Code Structure

```
library-project/
├── emails/
│   ├── __init__.py
│   ├── models.py          # EmailLog model
│   ├── services.py        # EmailService class
│   ├── tasks.py           # Celery tasks
│   ├── views.py           # Email endpoints
│   ├── urls.py            # Email URLs
│   └── tests.py           # Tests
├── templates/
│   └── emails/
│       ├── base_email.html
│       ├── welcome_email.html
│       ├── book_borrowed_email.html
│       └── book_reminder_email.html
├── library_project/
│   ├── celery.py          # Celery config
│   └── settings.py        # Email settings
└── requirements.txt       # Updated dependencies
```

### 2. Git Commit

```bash
git add .
git commit -m "feat: implement email notification system (lesson 29)

- Configured SMTP/console email backend
- Created email service class
- Built HTML email templates (base, welcome, borrow)
- Integrated with user registration signal
- Integrated with book borrow signal
- Setup Celery for async email sending
- Created email tasks (welcome, borrow, reminder)
- Added email endpoints (test, resend welcome)
- Created email log model
- Added comprehensive tests

Tested:
- Basic email sending
- HTML templates rendering
- Signal integration
- Async sending with Celery
- Email logging"

git push origin feature/lesson-29-email-notifications
```

### 3. Screenshots

Take screenshots of:
1. Console output showing email sent
2. Received email (welcome or borrow confirmation)
3. Celery worker logs
4. Admin panel - EmailLog entries

### 4. Documentation

**README.md:**
```markdown
# Lesson 29: Email Notifications Implementation

## Setup

1. Install dependencies:
```bash
pip install celery redis
```

2. Configure email in settings.py (see settings.py)

3. Start Redis (for Celery):
```bash
redis-server
```

4. Start Celery worker:
```bash
celery -A library_project worker -l info
```

## Features Implemented

- SMTP configuration
- HTML email templates
- Email service class
- Welcome email on registration
- Borrow confirmation email
- Async email with Celery
- Email logging

## Testing

Run tests:
```bash
python manage.py test emails
```

## Endpoints

- POST /api/emails/test/ - Send test email (admin only)
- POST /api/emails/resend-welcome/ - Resend welcome email
```

---

## Baholash Mezonlari

| Task | Points | Criteria |
|------|--------|----------|
| **Task 1** | 20 | SMTP configured, templates created |
| **Task 2** | 25 | Email service implemented, works correctly |
| **Task 3** | 20 | Signals integrated, emails sent on events |
| **Task 4** | 25 | Celery setup, async tasks working |
| **Task 5** | 10 | Email endpoints working |
| **Task 6 (Bonus)** | 10 | Email logging implemented |
| **Total** | **100+10** | Maximum 110 points |

---

## Muhim Eslatmalar

1. **Gmail SMTP:** 2-Step Verification yoqing va App Password oling
2. **Celery:** Redis server ishga tushirish kerak
3. **Templates:** HTML email templates responsive bo'lishi kerak
4. **Error Handling:** Try/except ishlatish muhim
5. **Testing:** Console backend'dan foydalaning development'da
6. **Async:** Production'da har doim async email ishlating

---

**Good luck!**