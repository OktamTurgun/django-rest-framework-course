# Lesson 28: Signals & Webhooks

> Django Signals va Webhooks bilan ishlash - Event-driven architecture asoslari

## Maqsad

Ushbu darsda siz quyidagilarni o'rganasiz:
- Django signals nima va qachon ishlatiladi
- Built-in signals (pre_save, post_save, pre_delete, post_delete)
- Custom signals yaratish
- Signal receiver yozish
- Webhooks nima va qanday ishlaydi
- Webhook integration (payment, notification)
- Celery bilan async signal processing
- Signal best practices va pitfalls

## Nazariy qism

### 1. Django Signals nima?

**Signal** - bu Django'da event-driven programming uchun mexanizm. Bir joyda biror narsa sodir bo'lganda (event), boshqa joylar (receivers) bu haqida xabar oladi.

**Real-world analogy:**
```
Fire Alarm System = Signal System
- Smoke detector (sender) → Signal
- Alarm bells (receivers) → Actions
- When smoke detected → All receivers activated
```

### 2. Signals ishlatish sabablari

**Do'st (Qiling):**
```python
# Decoupled code - apps mustaqil
# User yaratilganda email yuborish
# Model o'zgarganda cache tozalash
# File upload bo'lganda thumbnail yaratish
# Payment muvaffaqiyatli bo'lganda order statusni yangilash
```

**Don'ts (Qilmang):**
```python
# Signal ichida og'ir operatsiyalar (use Celery)
# Circular signals (A→B→A)
# Business logicni signal'ga ko'chirish
# Signals o'rniga oddiy function yetarli bo'lsa
```

### 3. Signal Lifecycle

```
┌─────────────────────────────────────────┐
│          Django Signal Flow             │
├─────────────────────────────────────────┤
│                                         │
│  1. Event occurs (model save)           │
│            ↓                            │
│  2. Signal sent                         │
│            ↓                            │
│  3. Receivers notified                  │
│            ↓                            │
│  4. Receiver functions execute          │
│            ↓                            │
│  5. Original operation continues        │
│                                         │
└─────────────────────────────────────────┘
```

## Built-in Signals

### Model Signals

| Signal | Qachon ishga tushadi | Use case |
|--------|---------------------|----------|
| `pre_save` | save() dan oldin | Data validation, preprocessing |
| `post_save` | save() dan keyin | Notification, logging |
| `pre_delete` | delete() dan oldin | Cleanup check |
| `post_delete` | delete() dan keyin | File deletion, logging |
| `m2m_changed` | ManyToMany o'zgarganda | Relationship tracking |

### Request/Response Signals

| Signal | Description |
|--------|-------------|
| `request_started` | HTTP request boshlanishi |
| `request_finished` | HTTP request tugashi |
| `got_request_exception` | Exception yuz berganda |

### Management Signals

| Signal | Description |
|--------|-------------|
| `pre_migrate` | Migration oldidan |
| `post_migrate` | Migration keyin |

## Amaliy qism

### 1. Basic Signal Usage

**books/signals.py:**
```python
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Book, UserProfile

# ===== USER SIGNALS =====

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """User yaratilganda avtomatik profile yaratish"""
    if created:
        UserProfile.objects.create(user=instance)
        print(f"✅ Profile created for {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User save bo'lganda profile ham save qilish"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

# ===== BOOK SIGNALS =====

@receiver(post_save, sender=Book)
def book_saved_notification(sender, instance, created, **kwargs):
    """Book save bo'lganda notification"""
    if created:
        print(f"📚 New book added: {instance.title}")
        # Email yuborish logikasi
        # send_email_to_subscribers(instance)
    else:
        print(f"📝 Book updated: {instance.title}")

@receiver(pre_delete, sender=Book)
def book_deletion_check(sender, instance, **kwargs):
    """Book delete qilishdan oldin check"""
    if instance.is_borrowed:
        print(f"⚠️ Warning: Deleting borrowed book - {instance.title}")
        # Admin'ga notification
```

**books/apps.py:**
```python
from django.apps import AppConfig

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

    def ready(self):
        import books.signals  # Signals import qilish
```

### 2. Custom Signal

**books/signals.py:**
```python
from django.dispatch import Signal, receiver

# Custom signal yaratish
book_borrowed = Signal()  # providing_args=['book', 'user']
book_returned = Signal()

# Signal sender
def borrow_book(book, user):
    """Book borrow qilish funksiyasi"""
    # Business logic
    book.is_borrowed = True
    book.borrowed_by = user
    book.save()
    
    # Signal yuborish
    book_borrowed.send(
        sender=book.__class__,
        book=book,
        user=user
    )

# Signal receivers
@receiver(book_borrowed)
def notify_book_borrowed(sender, book, user, **kwargs):
    """Book borrow bo'lganda notification"""
    print(f"📧 Email: {user.username} borrowed '{book.title}'")

@receiver(book_borrowed)
def update_user_stats(sender, book, user, **kwargs):
    """User statistikasini yangilash"""
    profile = user.profile
    profile.books_borrowed += 1
    profile.save()

@receiver(book_borrowed)
def log_borrowing(sender, book, user, **kwargs):
    """Borrowing history saqlash"""
    BorrowHistory.objects.create(
        book=book,
        user=user,
        action='borrowed'
    )
```

### 3. Webhook Implementation

**webhooks/models.py:**
```python
from django.db import models
import uuid

class Webhook(models.Model):
    """Webhook endpoint configuration"""
    
    EVENTS = [
        ('book.created', 'Book Created'),
        ('book.updated', 'Book Updated'),
        ('book.deleted', 'Book Deleted'),
        ('user.registered', 'User Registered'),
        ('order.completed', 'Order Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    url = models.URLField(help_text="Webhook endpoint URL")
    event = models.CharField(max_length=50, choices=EVENTS)
    secret = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['url', 'event']
    
    def __str__(self):
        return f"{self.event} → {self.url}"

class WebhookLog(models.Model):
    """Webhook delivery log"""
    
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE)
    payload = models.JSONField()
    response_status = models.IntegerField(null=True)
    response_body = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**webhooks/services.py:**
```python
import requests
import hashlib
import hmac
import json
from django.conf import settings
from .models import Webhook, WebhookLog

class WebhookService:
    """Webhook yuborish xizmati"""
    
    @staticmethod
    def send_webhook(event_type: str, payload: dict):
        """Event uchun barcha webhook'larni yuborish"""
        webhooks = Webhook.objects.filter(
            event=event_type,
            is_active=True
        )
        
        for webhook in webhooks:
            WebhookService._deliver(webhook, payload)
    
    @staticmethod
    def _deliver(webhook: Webhook, payload: dict):
        """Bitta webhook yuborish"""
        try:
            # Payload preparation
            data = json.dumps(payload)
            
            # Signature generation (HMAC)
            signature = hmac.new(
                webhook.secret.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # HTTP request
            response = requests.post(
                webhook.url,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'X-Webhook-Signature': signature,
                    'X-Event-Type': webhook.event,
                },
                timeout=10
            )
            
            # Log success
            WebhookLog.objects.create(
                webhook=webhook,
                payload=payload,
                response_status=response.status_code,
                response_body=response.text[:1000],
                success=response.status_code == 200
            )
            
            return response.status_code == 200
            
        except Exception as e:
            # Log error
            WebhookLog.objects.create(
                webhook=webhook,
                payload=payload,
                success=False,
                error_message=str(e)
            )
            return False
```

**books/signals.py (with webhooks):**
```python
from webhooks.services import WebhookService

@receiver(post_save, sender=Book)
def send_book_webhook(sender, instance, created, **kwargs):
    """Book signals webhook yuboradi"""
    event = 'book.created' if created else 'book.updated'
    
    payload = {
        'event': event,
        'timestamp': timezone.now().isoformat(),
        'data': {
            'id': instance.id,
            'title': instance.title,
            'author': instance.author.name,
            'isbn': instance.isbn,
            'price': str(instance.price),
        }
    }
    
    # Webhook yuborish (async tavsiya etiladi)
    WebhookService.send_webhook(event, payload)
```

### 4. Async Signal Processing with Celery

**books/tasks.py:**
```python
from celery import shared_task
from django.core.mail import send_mail
from .models import Book

@shared_task
def send_book_notification_email(book_id, user_email):
    """Async email notification"""
    try:
        book = Book.objects.get(id=book_id)
        send_mail(
            subject=f'New Book: {book.title}',
            message=f'Check out the new book: {book.title}',
            from_email='noreply@library.com',
            recipient_list=[user_email],
        )
        return f"Email sent to {user_email}"
    except Exception as e:
        return f"Error: {str(e)}"

@shared_task
def process_webhook_async(webhook_id, payload):
    """Async webhook processing"""
    from webhooks.services import WebhookService
    webhook = Webhook.objects.get(id=webhook_id)
    return WebhookService._deliver(webhook, payload)
```

**books/signals.py (with Celery):**
```python
from .tasks import send_book_notification_email

@receiver(post_save, sender=Book)
def book_created_async_notification(sender, instance, created, **kwargs):
    """Async notification qo'llash"""
    if created:
        # Get all subscribers
        subscribers = User.objects.filter(
            profile__subscribed_to_notifications=True
        )
        
        # Send async email to each
        for user in subscribers:
            send_book_notification_email.delay(
                instance.id,
                user.email
            )
```

### 5. Signal Best Practices

**books/signals.py:**
```python
from django.db import transaction

# ✅ GOOD: Transaction-safe signal
@receiver(post_save, sender=Book)
def create_book_index(sender, instance, created, **kwargs):
    """Search index yaratish - transaction safe"""
    if created:
        transaction.on_commit(lambda: update_search_index(instance))

# ✅ GOOD: Idempotent signal
@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, **kwargs):
    """Profile mavjud emas bo'lsa yaratish"""
    UserProfile.objects.get_or_create(user=instance)

# ❌ BAD: Heavy operation in signal
@receiver(post_save, sender=Book)
def bad_signal(sender, instance, created, **kwargs):
    # Don't do this!
    for user in User.objects.all():  # N+1 problem
        send_mail(...)  # Blocking operation
        time.sleep(5)  # Never sleep in signals!

# ✅ GOOD: Use Celery instead
@receiver(post_save, sender=Book)
def good_signal(sender, instance, created, **kwargs):
    if created:
        notify_users_about_book.delay(instance.id)  # Async task
```

### 6. Webhook Security

**webhooks/security.py:**
```python
import hmac
import hashlib

def verify_webhook_signature(request, secret):
    """Webhook signature verification"""
    received_signature = request.headers.get('X-Webhook-Signature')
    
    if not received_signature:
        return False
    
    # Calculate expected signature
    body = request.body
    expected_signature = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    # Constant-time comparison
    return hmac.compare_digest(received_signature, expected_signature)

# View'da ishlatish
class WebhookReceiver(APIView):
    """External webhook'larni qabul qilish"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Get webhook config
        webhook = Webhook.objects.filter(
            url=request.path,
            is_active=True
        ).first()
        
        if not webhook:
            return Response({'error': 'Webhook not found'}, 
                          status=404)
        
        # Verify signature
        if not verify_webhook_signature(request, webhook.secret):
            return Response({'error': 'Invalid signature'}, 
                          status=401)
        
        # Process webhook
        event_type = request.headers.get('X-Event-Type')
        process_webhook_event(event_type, request.data)
        
        return Response({'status': 'received'})
```

### 7. Testing Signals

**books/tests/test_signals.py:**
```python
from django.test import TestCase
from django.db.models.signals import post_save
from unittest.mock import patch, Mock
from books.models import Book
from books.signals import book_saved_notification

class BookSignalTest(TestCase):
    
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': self.author,
            'isbn': '1234567890',
        }
    
    @patch('books.signals.send_email_to_subscribers')
    def test_new_book_sends_email(self, mock_send_email):
        """New book signal email yuborishini test qilish"""
        book = Book.objects.create(**self.book_data)
        
        # Check email function called
        mock_send_email.assert_called_once_with(book)
    
    def test_signal_creates_profile(self):
        """User signal profile yaratishini test"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Profile avtomatik yaratilganini tekshirish
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)
    
    def test_custom_signal_triggered(self):
        """Custom signal ishga tushishini test"""
        # Mock receiver
        mock_receiver = Mock()
        book_borrowed.connect(mock_receiver)
        
        # Trigger signal
        book = Book.objects.create(**self.book_data)
        user = User.objects.create_user('borrower', 'pass')
        borrow_book(book, user)
        
        # Check receiver called
        self.assertTrue(mock_receiver.called)
        
        # Cleanup
        book_borrowed.disconnect(mock_receiver)
```

## Signal vs Direct Call

### Qachon Signal ishlatish kerak?

**✅ Signals ishlatish:**
```python
# 1. Decoupled functionality
# User app → Email app (loosely coupled)

# 2. Multiple receivers
# Book created → Email + Logging + Analytics

# 3. Plugin architecture
# Third-party apps can hook into your signals

# 4. Cross-app communication
# Orders app → Inventory app → Notification app
```

**✅ Direct call ishlatish:**
```python
# 1. Same app functionality
def create_order(data):
    order = Order.objects.create(**data)
    process_payment(order)  # Direct call
    
# 2. Critical business logic
# Don't hide important logic in signals

# 3. Explicit control flow
# When you need predictable execution order

# 4. Testing simplicity
# Easier to test and debug
```

## Common Pitfalls

### 1. Signal Recursion
```python
# ❌ BAD: Infinite loop
@receiver(post_save, sender=Book)
def update_book(sender, instance, **kwargs):
    instance.updated_count += 1
    instance.save()  # Triggers same signal again!

# ✅ GOOD: Prevent recursion
@receiver(post_save, sender=Book)
def update_book(sender, instance, **kwargs):
    if not hasattr(instance, '_updating'):
        instance._updating = True
        instance.updated_count += 1
        instance.save()
        delattr(instance, '_updating')
```

### 2. Transaction Issues
```python
# ❌ BAD: Signal before transaction commit
@receiver(post_save, sender=Order)
def send_confirmation(sender, instance, created, **kwargs):
    if created:
        send_email(instance.user.email)  # May send before DB commit

# ✅ GOOD: Wait for transaction
@receiver(post_save, sender=Order)
def send_confirmation(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: send_email(instance.user.email)
        )
```

### 3. Performance Issues
```python
# ❌ BAD: N+1 queries in signal
@receiver(post_save, sender=Book)
def notify_users(sender, instance, created, **kwargs):
    for user in User.objects.all():  # Bad!
        notify(user, instance)

# ✅ GOOD: Bulk operations
@receiver(post_save, sender=Book)
def notify_users(sender, instance, created, **kwargs):
    user_ids = User.objects.values_list('id', flat=True)
    bulk_notify.delay(list(user_ids), instance.id)  # Async + bulk
```

## Real-world Examples

### Example 1: E-commerce Order System
```python
# Order signals
@receiver(post_save, sender=Order)
def order_created_workflow(sender, instance, created, **kwargs):
    """Order yaratilganda workflow"""
    if created and instance.status == 'pending':
        # 1. Inventory check
        check_inventory.delay(instance.id)
        
        # 2. Payment processing
        process_payment.delay(instance.id)
        
        # 3. Send confirmation email
        send_order_confirmation.delay(instance.id)
        
        # 4. Notify warehouse
        notify_warehouse_webhook(instance)

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    """Order status o'zgarganda"""
    if instance.tracker.has_changed('status'):
        old_status = instance.tracker.previous('status')
        new_status = instance.status
        
        # Status-based actions
        if new_status == 'paid':
            start_shipping.delay(instance.id)
        elif new_status == 'shipped':
            send_tracking_info.delay(instance.id)
        elif new_status == 'delivered':
            request_review.delay(instance.id)
```

### Example 2: Social Media Platform
```python
@receiver(post_save, sender=Post)
def post_created_actions(sender, instance, created, **kwargs):
    """Post yaratilganda"""
    if created:
        # 1. Notify followers
        notify_followers.delay(
            instance.author.id,
            instance.id
        )
        
        # 2. Process hashtags
        extract_and_save_hashtags.delay(instance.id)
        
        # 3. Generate thumbnail
        if instance.image:
            generate_thumbnail.delay(instance.id)
        
        # 4. Analytics webhook
        WebhookService.send_webhook(
            'post.created',
            {'post_id': instance.id, 'author': instance.author.username}
        )

@receiver(m2m_changed, sender=Post.likes.through)
def post_liked(sender, instance, action, pk_set, **kwargs):
    """Post like qilinganda"""
    if action == 'post_add':
        # Notify author
        for user_id in pk_set:
            notify_post_liked.delay(
                post_id=instance.id,
                liker_id=user_id
            )
```

## Homework

[Homework topshiriqlar](homework.md) faylida.

## Qo'shimcha resurslar

- [Django Signals Documentation](https://docs.djangoproject.com/en/stable/topics/signals/)
- [Webhook Best Practices](https://webhooks.fyi/)
- [Celery Documentation](https://docs.celeryproject.org/)

## Keyingi dars

[Lesson 29: Email Notifications →](../29-email-notifications/)

---

**Eslatma:** Signals - qudratli asbob, lekin ortiqcha ishlatmang. Ko'p hollarda oddiy function yaxshiroqdir!