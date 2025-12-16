# Homework: Signals & Webhooks

## Maqsad

Library Project'ga signal va webhook functionality qo'shish.

---

## Task 1: Basic Signals (30 points)

### 1.1 User Profile Signal (10 points)

User yaratilganda avtomatik UserProfile yaratish.

**books/models.py:**
```python
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    books_borrowed = models.IntegerField(default=0)
    books_returned = models.IntegerField(default=0)
    subscribed_to_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**books/signals.py:**
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """TODO: User yaratilganda profile yaratish"""
    pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """TODO: User save bo'lganda profile ham save qilish"""
    pass
```

**Test:**
```python
# Python shell
from django.contrib.auth.models import User

user = User.objects.create_user('testuser', 'test@example.com', 'pass123')
print(user.profile)  # UserProfile object mavjud bo'lishi kerak
```

### 1.2 Book Logging Signal (10 points)

Book CRUD operatsiyalarini log qilish.

**books/models.py:**
```python
class BookLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]
    
    book_title = models.CharField(max_length=255)
    book_id = models.IntegerField(null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
```

**books/signals.py:**
```python
@receiver(post_save, sender=Book)
def log_book_save(sender, instance, created, **kwargs):
    """TODO: Book create/update ni log qilish"""
    pass

@receiver(pre_delete, sender=Book)
def log_book_delete(sender, instance, **kwargs):
    """TODO: Book delete ni log qilish"""
    pass
```

**Test endpoints:**
```bash
# POST /api/books/ - yangi book yaratish
# PUT /api/books/1/ - book update qilish
# DELETE /api/books/1/ - book o'chirish

# GET /admin/ → BookLog model'da 3 ta log ko'rinishi kerak
```

### 1.3 Author Statistics Signal (10 points)

Author'ning kitoblari soni o'zgarganda statistika yangilash.

**books/models.py:**
```python
class Author(models.Model):
    # ... existing fields ...
    total_books = models.IntegerField(default=0)
    available_books = models.IntegerField(default=0)
```

**books/signals.py:**
```python
@receiver(post_save, sender=Book)
def update_author_stats_on_save(sender, instance, created, **kwargs):
    """TODO: Book yaratilganda yoki o'zgarganda author statistikasini yangilash"""
    pass

@receiver(post_delete, sender=Book)
def update_author_stats_on_delete(sender, instance, **kwargs):
    """TODO: Book o'chirilganda author statistikasini yangilash"""
    pass
```

**Test:**
```python
# Shell
author = Author.objects.create(name="Test Author")
Book.objects.create(title="Book 1", author=author)
Book.objects.create(title="Book 2", author=author)
author.refresh_from_db()
print(author.total_books)  # 2
```

---

## Task 2: Custom Signals (25 points)

### 2.1 Book Borrow Signal (15 points)

Custom signal: book borrowed va returned.

**books/signals.py:**
```python
from django.dispatch import Signal

# Custom signals
book_borrowed = Signal()  # providing_args=['book', 'user']
book_returned = Signal()  # providing_args=['book', 'user']

# Signal senders
def borrow_book(book_id, user):
    """TODO: Book borrow qilish va signal yuborish"""
    pass

def return_book(book_id, user):
    """TODO: Book return qilish va signal yuborish"""
    pass

# Signal receivers
@receiver(book_borrowed)
def on_book_borrowed(sender, book, user, **kwargs):
    """
    TODO: Book borrow qilinganda:
    1. User profile'dagi books_borrowed ni oshirish
    2. BookLog yaratish
    3. Console'ga log chiqarish
    """
    pass

@receiver(book_returned)
def on_book_returned(sender, book, user, **kwargs):
    """
    TODO: Book return qilinganda:
    1. User profile'dagi books_returned ni oshirish
    2. BookLog yaratish
    3. Console'ga log chiqarish
    """
    pass
```

**books/views.py:**
```python
from .signals import borrow_book, return_book

class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """
        TODO: Book borrow qilish endpoint
        - Book available bo'lishini tekshirish
        - borrow_book() funksiyasini chaqirish
        - Response qaytarish
        """
        pass

class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """
        TODO: Book return qilish endpoint
        - Book borrowed bo'lishini tekshirish
        - return_book() funksiyasini chaqirish
        - Response qaytarish
        """
        pass
```

**Test:**
```bash
# POST /api/books/1/borrow/
{
    # Response: Book borrowed successfully
}

# POST /api/books/1/return/
{
    # Response: Book returned successfully
}

# Check user profile
# GET /api/users/me/
{
    "books_borrowed": 1,
    "books_returned": 1
}
```

### 2.2 Bulk Import Signal (10 points)

Ko'p kitob import qilinganda signal.

**books/signals.py:**
```python
books_bulk_imported = Signal()  # providing_args=['count', 'user']

@receiver(books_bulk_imported)
def on_books_imported(sender, count, user, **kwargs):
    """
    TODO: Bulk import qilinganda:
    1. Admin'ga notification (console log)
    2. Import statistikasini saqlash
    """
    pass
```

**books/views.py:**
```python
class BulkImportBooksView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        """
        TODO: JSON array qabul qilib, bulk create
        Request body: [{"title": "...", "author_id": 1}, ...]
        Signal yuborish
        """
        pass
```

---

## Task 3: Webhooks (30 points)

### 3.1 Webhook Model & Service (15 points)

**webhooks/models.py:**
```python
class Webhook(models.Model):
    """
    TODO: Webhook endpoint configuration
    Fields:
    - id (UUID)
    - url (URLField)
    - event (CharField with choices)
    - secret (CharField)
    - is_active (BooleanField)
    - created_at (DateTimeField)
    """
    pass

class WebhookLog(models.Model):
    """
    TODO: Webhook delivery log
    Fields:
    - webhook (ForeignKey to Webhook)
    - payload (JSONField)
    - response_status (IntegerField)
    - response_body (TextField)
    - success (BooleanField)
    - error_message (TextField)
    - created_at (DateTimeField)
    """
    pass
```

**webhooks/services.py:**
```python
import requests
import hmac
import hashlib
import json

class WebhookService:
    
    @staticmethod
    def send_webhook(event_type: str, payload: dict):
        """
        TODO: Event uchun barcha webhook'larni yuborish
        1. Active webhook'larni topish
        2. Har biriga _deliver() chaqirish
        """
        pass
    
    @staticmethod
    def _deliver(webhook, payload):
        """
        TODO: Bitta webhook yuborish
        1. Signature generate qilish (HMAC SHA256)
        2. POST request yuborish
        3. WebhookLog yaratish
        4. Success/error handle qilish
        """
        pass
    
    @staticmethod
    def generate_signature(secret: str, payload: str) -> str:
        """TODO: HMAC SHA256 signature"""
        pass
```

### 3.2 Book Webhook Integration (15 points)

**books/signals.py:**
```python
from webhooks.services import WebhookService

@receiver(post_save, sender=Book)
def send_book_webhook(sender, instance, created, **kwargs):
    """
    TODO: Book save bo'lganda webhook yuborish
    Event: book.created yoki book.updated
    Payload: {
        'event': 'book.created',
        'timestamp': '...',
        'data': {
            'id': 1,
            'title': '...',
            'author': '...',
            'isbn': '...'
        }
    }
    """
    pass

@receiver(post_delete, sender=Book)
def send_book_delete_webhook(sender, instance, **kwargs):
    """TODO: Book delete webhook"""
    pass
```

**webhooks/views.py:**
```python
class WebhookViewSet(viewsets.ModelViewSet):
    """
    TODO: Webhook CRUD endpoints
    - List webhooks
    - Create webhook
    - Update webhook
    - Delete webhook
    - Activate/Deactivate webhook
    """
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [IsAdminUser]

class WebhookLogListView(generics.ListAPIView):
    """TODO: Webhook logs ko'rish"""
    serializer_class = WebhookLogSerializer
    permission_classes = [IsAdminUser]
```

**Test:**
```bash
# 1. Create webhook
POST /api/webhooks/
{
    "url": "https://webhook.site/unique-id",
    "event": "book.created",
    "secret": "my-secret-key",
    "is_active": true
}

# 2. Create book
POST /api/books/
{
    "title": "Test Book",
    "author": 1,
    "isbn": "1234567890"
}

# 3. Check webhook.site for received request
# Request should have:
# - X-Webhook-Signature header
# - X-Event-Type: book.created
# - JSON body with book data

# 4. Check webhook logs
GET /api/webhooks/logs/
```

---

## Task 4: Signal Best Practices (15 points)

### 4.1 Transaction Safety (5 points)

**books/signals.py:**
```python
from django.db import transaction

@receiver(post_save, sender=Book)
def create_book_index(sender, instance, created, **kwargs):
    """
    TODO: Transaction commit bo'lgandan keyin search index update
    transaction.on_commit() ishlatish
    """
    pass
```

### 4.2 Prevent Signal Recursion (5 points)

**books/signals.py:**
```python
@receiver(post_save, sender=Book)
def update_book_counter(sender, instance, **kwargs):
    """
    TODO: Book save qilinganda counter yangilash
    Lekin recursion oldini olish kerak
    
    Instance'ga _updating flag qo'yish:
    if not hasattr(instance, '_updating'):
        instance._updating = True
        # ... update logic
        delattr(instance, '_updating')
    """
    pass
```

### 4.3 Signal Testing (5 points)

**books/tests/test_signals.py:**
```python
from django.test import TestCase
from unittest.mock import patch, Mock

class BookSignalTest(TestCase):
    
    def test_user_profile_created_on_user_save(self):
        """TODO: User signal test"""
        pass
    
    def test_book_log_created_on_book_save(self):
        """TODO: Book log signal test"""
        pass
    
    @patch('webhooks.services.WebhookService.send_webhook')
    def test_webhook_sent_on_book_create(self, mock_webhook):
        """TODO: Webhook signal test (mock)"""
        pass
    
    def test_custom_signal_triggered(self):
        """TODO: Custom signal test"""
        # Mock receiver
        # Connect receiver
        # Trigger signal
        # Assert receiver called
        pass
```

---

## Qo'shimcha vazifalar (Bonus)

### Bonus 1: Email Signal (10 points)

Book borrow qilinganda admin'ga email yuborish.

**books/signals.py:**
```python
@receiver(book_borrowed)
def send_borrow_notification_email(sender, book, user, **kwargs):
    """
    TODO: Email yuborish
    Subject: Book Borrowed - {book.title}
    Message: User {user.username} borrowed "{book.title}"
    To: Admin email
    """
    pass
```

### Bonus 2: Webhook Retry Mechanism (15 points)

Webhook failed bo'lsa, retry qilish.

**webhooks/services.py:**
```python
@staticmethod
def _deliver_with_retry(webhook, payload, max_retries=3):
    """
    TODO: Retry logic
    1. Try to send webhook
    2. If failed, retry up to max_retries times
    3. Exponential backoff (1s, 2s, 4s)
    4. Log each attempt
    """
    pass
```

### Bonus 3: Webhook Receiver (10 points)

External webhook qabul qilish endpoint.

**webhooks/views.py:**
```python
class WebhookReceiverView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        TODO: Webhook qabul qilish
        1. Signature verify qilish
        2. Event type bo'yicha process qilish
        3. 200 OK response
        """
        pass
```

---

## Submission

### 1. Code Push
```bash
git add .
git commit -m "feat: implement signals and webhooks (lesson 28)"
git push origin feature/lesson-28-signals-implementation
```

### 2. Testing Checklist

**Signals:**
- [ ] User yaratilganda profile yaratiladi
- [ ] Book CRUD log qilinadi
- [ ] Author statistikasi yangilanadi
- [ ] Custom signal ishlaydi (borrow/return)
- [ ] Bulk import signal ishlaydi

**Webhooks:**
- [ ] Webhook create qilish mumkin
- [ ] Book event webhook yuboradi
- [ ] Webhook signature to'g'ri
- [ ] Webhook log saqlanadi
- [ ] Failed webhook handle qilinadi

**Best Practices:**
- [ ] Transaction safety implemented
- [ ] No signal recursion
- [ ] Tests written and passing

### 3. Documentation

README.md file yarating:
```markdown
# Lesson 28: Signals & Webhooks Implementation

## Implemented Features
1. User Profile Signal
2. Book Logging Signal
3. Author Statistics Signal
4. Custom Borrow/Return Signals
5. Webhook System
6. Webhook Logs

## API Endpoints
POST /api/books/{id}/borrow/ - Book borrow qilish
POST /api/books/{id}/return/ - Book return qilish
GET/POST /api/webhooks/ - Webhook CRUD
GET /api/webhooks/logs/ - Webhook logs

## Testing
python manage.py test books.tests.test_signals
python manage.py test webhooks.tests

## Webhook Test URL
https://webhook.site/your-unique-id
```

### 4. Screenshots

1. Admin panel - UserProfile ro'yxati
2. Admin panel - BookLog entries
3. Postman - Borrow/Return requests
4. Webhook.site - Received webhook
5. Admin panel - WebhookLog

---

## Baholash mezonlari

| Task | Points | Criteria |
|------|--------|----------|
| **Task 1** | 30 | Signals ishlaydi, test o'tadi |
| **Task 2** | 25 | Custom signals to'g'ri implement qilindi |
| **Task 3** | 30 | Webhook system to'liq ishlaydi |
| **Task 4** | 15 | Best practices qo'llandi, test yozildi |
| **Bonus** | 35 | Qo'shimcha features |
| **Total** | **100+35** | Maximum 135 points |

---

## Muhim eslatmalar

1. **Signals.py import** qilishni unutmang (apps.py'da)
2. **Transaction safety** - on_commit() ishlating
3. **No recursion** - flag ishlating
4. **Async operations** - og'ir ishlarni Celery'ga o'tkazing
5. **Webhook signature** - HMAC SHA256 ishlating
6. **Error handling** - try/except qo'ying
7. **Testing** - Mock ishlatishni o'rganing

---

## Deadline

**1 hafta** - Signals & Webhooks implementation

Good luck!