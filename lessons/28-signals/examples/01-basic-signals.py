"""
Example 1: Basic Django Signals

Demonstrates:
- Built-in model signals
- Signal receivers
- Signal parameters
- Common use cases

Built-in Model Signals:
- pre_save: Model save() dan oldin
- post_save: Model save() dan keyin
- pre_delete: Model delete() dan oldin
- post_delete: Model delete() dan keyin
- m2m_changed: ManyToMany relationship o'zgarganda
"""

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

# ============================================================================
# MODELS
# ============================================================================

class Book(models.Model):
    """Book model"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class BookLog(models.Model):
    """Book operation log"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]
    
    book_title = models.CharField(max_length=200)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.action.upper()}: {self.book_title}"


# ============================================================================
# SIGNAL RECEIVERS
# ============================================================================

# ========== PRE_SAVE SIGNAL ==========

@receiver(pre_save, sender=Book)
def book_pre_save(sender, instance, **kwargs):
    """
    pre_save signal: Model save() dan OLDIN ishga tushadi
    
    Use cases:
    - Data validation va preprocessing
    - Default value setting
    - Field modification before save
    - Checking if field changed
    """
    print(f"\n📝 PRE_SAVE: Book save qilinmoqda...")
    print(f"   Title: {instance.title}")
    print(f"   Price: ${instance.price}")
    
    # Example 1: Auto-set availability based on stock
    if instance.stock > 0:
        instance.is_available = True
        print("   ✅ Auto-set: is_available = True (stock > 0)")
    else:
        instance.is_available = False
        print("   ❌ Auto-set: is_available = False (stock = 0)")
    
    # Example 2: Title capitalize
    if instance.title:
        instance.title = instance.title.title()
        print(f"   ✏️ Title capitalized: {instance.title}")
    
    # Example 3: Check if this is update (not create)
    if instance.pk:  # pk exists = updating existing object
        try:
            old_instance = Book.objects.get(pk=instance.pk)
            if old_instance.price != instance.price:
                print(f"   💰 Price changed: ${old_instance.price} → ${instance.price}")
        except Book.DoesNotExist:
            pass


# ========== POST_SAVE SIGNAL ==========

@receiver(post_save, sender=Book)
def book_post_save(sender, instance, created, **kwargs):
    """
    post_save signal: Model save() dan KEYIN ishga tushadi
    
    Parameters:
    - sender: Model class (Book)
    - instance: Actual instance that was saved
    - created: Boolean - True if new object created
    - **kwargs: Additional arguments
    
    Use cases:
    - Logging
    - Sending notifications
    - Creating related objects
    - Triggering background tasks
    """
    print(f"\n💾 POST_SAVE: Book saved!")
    
    if created:
        # New book created
        print(f"   ✨ NEW BOOK CREATED: {instance.title}")
        print(f"   📚 Stock: {instance.stock}")
        print(f"   💵 Price: ${instance.price}")
        
        # Create log entry
        BookLog.objects.create(
            book_title=instance.title,
            action='created',
            details=f"New book added with {instance.stock} copies"
        )
        print("   📋 Log entry created")
        
        # Send notification (in real app, use Celery for this)
        print("   📧 Email notification sent to subscribers")
        
    else:
        # Existing book updated
        print(f"   🔄 BOOK UPDATED: {instance.title}")
        
        # Create log entry
        BookLog.objects.create(
            book_title=instance.title,
            action='updated',
            details=f"Book details updated at {timezone.now()}"
        )
        print("   📋 Update log created")


# ========== PRE_DELETE SIGNAL ==========

@receiver(pre_delete, sender=Book)
def book_pre_delete(sender, instance, **kwargs):
    """
    pre_delete signal: Model delete() dan OLDIN
    
    Use cases:
    - Data validation before deletion
    - Warning notifications
    - Creating backup
    - Checking dependencies
    """
    print(f"\n🗑️ PRE_DELETE: Book delete qilinmoqda...")
    print(f"   Title: {instance.title}")
    print(f"   Stock: {instance.stock}")
    
    # Example: Warning if book has stock
    if instance.stock > 0:
        print(f"   ⚠️ WARNING: Deleting book with {instance.stock} copies in stock!")
    
    # Example: Check if book is borrowed (in real app)
    # if instance.is_borrowed:
    #     raise ValidationError("Cannot delete borrowed book!")
    
    print("   💾 Creating backup before deletion...")


# ========== POST_DELETE SIGNAL ==========

@receiver(post_delete, sender=Book)
def book_post_delete(sender, instance, **kwargs):
    """
    post_delete signal: Model delete() dan KEYIN
    
    Use cases:
    - Cleanup operations
    - Delete related files
    - Logging
    - Cascade operations (if needed)
    """
    print(f"\n🗑️ POST_DELETE: Book deleted!")
    print(f"   Title: {instance.title}")
    
    # Create deletion log
    BookLog.objects.create(
        book_title=instance.title,
        action='deleted',
        details=f"Book deleted at {timezone.now()}"
    )
    print("   📋 Deletion log created")
    
    # Clean up related files (example)
    # if instance.cover_image:
    #     instance.cover_image.delete()
    #     print("   🖼️ Cover image deleted")
    
    print("   ✅ Cleanup completed")


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def demo_basic_signals():
    """
    Demo: Basic signal operations
    
    Run this in Django shell:
    >>> from examples.01_basic_signals import demo_basic_signals
    >>> demo_basic_signals()
    """
    
    print("=" * 60)
    print("DEMO: Basic Django Signals")
    print("=" * 60)
    
    # ========== CREATE ==========
    print("\n" + "=" * 60)
    print("TEST 1: Creating new book")
    print("=" * 60)
    
    book1 = Book.objects.create(
        title="python programming",  # lowercase intentionally
        author="John Doe",
        price=29.99,
        stock=10
    )
    # Expected output:
    # PRE_SAVE: validation, title capitalize, stock check
    # POST_SAVE: log creation, notification
    
    print(f"\n✅ Book created: {book1.title}")
    print(f"   Available: {book1.is_available}")  # Should be True (stock > 0)
    
    # ========== UPDATE ==========
    print("\n" + "=" * 60)
    print("TEST 2: Updating book")
    print("=" * 60)
    
    book1.price = 24.99
    book1.save()
    # Expected output:
    # PRE_SAVE: price change detection
    # POST_SAVE: update log
    
    # ========== STOCK TO ZERO ==========
    print("\n" + "=" * 60)
    print("TEST 3: Setting stock to zero")
    print("=" * 60)
    
    book1.stock = 0
    book1.save()
    # Expected output:
    # PRE_SAVE: is_available set to False
    # POST_SAVE: update log
    
    book1.refresh_from_db()
    print(f"\n✅ Stock updated: {book1.stock}")
    print(f"   Available: {book1.is_available}")  # Should be False
    
    # ========== DELETE ==========
    print("\n" + "=" * 60)
    print("TEST 4: Deleting book")
    print("=" * 60)
    
    book1.delete()
    # Expected output:
    # PRE_DELETE: warning if stock > 0, backup
    # POST_DELETE: deletion log, cleanup
    
    # ========== CHECK LOGS ==========
    print("\n" + "=" * 60)
    print("LOGS:")
    print("=" * 60)
    
    logs = BookLog.objects.all().order_by('timestamp')
    for log in logs:
        print(f"   {log.timestamp.strftime('%H:%M:%S')} - {log.action.upper()}: {log.book_title}")
        if log.details:
            print(f"      Details: {log.details}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED")
    print("=" * 60)


# ============================================================================
# SIGNAL CONNECTION METHODS
# ============================================================================

def alternative_signal_connection():
    """
    @receiver decorator'siz signal connection
    
    Bu method @receiver decorator bilan bir xil ishlaydi.
    Faqat syntax farq qiladi.
    """
    
    def my_callback(sender, instance, **kwargs):
        print(f"Book saved: {instance.title}")
    
    # Connect signal manually
    post_save.connect(my_callback, sender=Book)
    
    # Disconnect when needed
    # post_save.disconnect(my_callback, sender=Book)


# ============================================================================
# COMMON PATTERNS
# ============================================================================

# Pattern 1: Check if field changed
@receiver(pre_save, sender=Book)
def detect_price_change(sender, instance, **kwargs):
    """Detect specific field changes"""
    if instance.pk:
        try:
            old = Book.objects.get(pk=instance.pk)
            if old.price != instance.price:
                print(f"💰 Price change detected!")
                # Send notification, log, etc.
        except Book.DoesNotExist:
            pass


# Pattern 2: Create related object
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create related profile"""
    if created:
        # UserProfile.objects.create(user=instance)
        pass


# Pattern 3: Cleanup files
@receiver(post_delete, sender=Book)
def delete_book_files(sender, instance, **kwargs):
    """Delete related files"""
    # if instance.cover_image:
    #     instance.cover_image.delete(save=False)
    pass


# ============================================================================
# IMPORTANT NOTES
# ============================================================================

"""
⚠️ IMPORTANT PITFALLS TO AVOID:

1. Infinite loops:
   @receiver(post_save, sender=Book)
   def bad_signal(sender, instance, **kwargs):
       instance.save()  # ❌ Causes infinite loop!

2. Heavy operations:
   @receiver(post_save, sender=Book)
   def slow_signal(sender, instance, **kwargs):
       send_email()  # ❌ Blocks request!
       # Use Celery instead: send_email.delay()

3. Signal in signal:
   Signals calling other signals can cause unexpected behavior

4. Database queries in pre_save:
   Can cause N+1 queries

5. Forgetting to import signals.py:
   Add import in apps.py ready() method

✅ BEST PRACTICES:

1. Keep signals simple and fast
2. Use Celery for heavy operations
3. Be careful with transactions
4. Test signals thoroughly
5. Document signal side effects
6. Use transaction.on_commit() for critical operations
"""

# ============================================================================
# TESTING
# ============================================================================

"""
How to test signals:

from django.test import TestCase
from unittest.mock import patch

class BookSignalTest(TestCase):
    
    @patch('path.to.send_email')
    def test_book_created_sends_email(self, mock_send_email):
        book = Book.objects.create(title="Test", ...)
        mock_send_email.assert_called_once()
    
    def test_book_log_created(self):
        book = Book.objects.create(title="Test", ...)
        self.assertTrue(
            BookLog.objects.filter(
                book_title="Test",
                action='created'
            ).exists()
        )
"""