# Lesson 29: Email Notifications - Examples

Ushbu papkada Django email notifications bilan ishlashning turli xil misollari mavjud.

## Examples ro'yxati

### 1. Basic SMTP
- `01-smtp-basic.py` - Basic email sending with Django's send_mail

### 2. HTML Templates
- `02-html-templates.py` - HTML email templates with attachments

### 3. SendGrid Integration
- `03-sendgrid-integration.py` - SendGrid API integration

### 4. Async with Celery
- `04-async-celery.py` - Async email sending using Celery tasks

### 5. Email Service
- `05-email-service.py` - Complete email service class

## Har bir example faylida

```python
"""
Example: Description
- What it demonstrates
- Use cases
- Best practices
- Common pitfalls
"""

# Code with detailed comments
# Expected output
# Testing instructions
```

## Qanday ishlatish

1. Har bir example'ni alohida o'qing
2. Kodlarni o'zingiz yozing (copy-paste emas!)
3. Test qiling (console backend yoki MailHog)
4. Output'ni tahlil qiling
5. O'z loyihangizga qo'llang

## Testing Setup

### Option 1: Console Backend (Recommended for learning)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Option 2: MailHog (Recommended for testing)
```bash
# Install MailHog
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

# Configure Django
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Web UI: http://localhost:8025
```

### Option 3: Gmail SMTP (Production-like)
```python
# settings.py
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Get from Google
```

## Eslatma

Examples faqat demo maqsadida. Production kodda:
- Environment variables ishlatish
- Error handling qo'shish
- Logging qo'shish
- Rate limiting qo'shish
- Testing yozish
- Async sending ishlatish (Celery)