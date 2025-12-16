"""
Example 4: Signal Best Practices & Common Pitfalls

Demonstrates:
- Transaction safety
- Preventing infinite loops
- Performance optimization
- Error handling
- Testing strategies
- Common mistakes to avoid

This example shows real-world patterns and anti-patterns
"""

from django.db import models, transaction
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache
import time

# ============================================================================
# MODELS
# ============================================================================

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')


# ============================================================================
# PITFALL 1: INFINITE LOOP
# ============================================================================

# ❌ BAD: Causes infinite loop
@receiver(post_save, sender=Book)
def bad_update_counter(sender, instance, **kwargs):
    """
    DON'T DO THIS!
    
    Problem: Signal triggers save(), which triggers signal again → infinite loop
    """
    # instance.updated_count += 1
    # instance.save()  # ❌ Triggers signal again!
    pass


# ✅ GOOD: Multiple solutions

# Solution 1: Use flag to prevent recursion
@receiver(post_save, sender=Book)
def good_update_counter_v1(sender, instance, **kwargs):
    """
    Use flag to prevent recursion
    
    Pattern: Check if flag exists, if not - process and set flag
    """
    if not hasattr(instance, '_updating'):
        instance._updating = True
        instance.updated_count += 1
        instance.save()
        delattr(instance, '_updating')
        print(f"✅ Counter updated (with flag): {instance.updated_count}")


# Solution 2: Use update() instead of save()
@receiver(post_save, sender=Book)
def good_update_counter_v2(sender, instance, created, **kwargs):
    """
    Use update() - doesn't trigger signals
    
    Pattern: QuerySet.update() bypasses signals
    """
    if not created:
        Book.objects.filter(pk=instance.pk).update(
            updated_count=instance.updated_count + 1
        )
        print(f"✅ Counter updated (with update())")


# Solution 3: Use pre_save instead
@receiver(pre_save, sender=Book)
def good_update_counter_v3(sender, instance, **kwargs):
    """
    Use pre_save to modify before save
    
    Pattern: Modify in pre_save, no need to save again
    """
    if instance.pk:  # Only for updates
        instance.updated_count += 1
        print(f"✅ Counter updated (in pre_save): {instance.updated_count}")


# ============================================================================
# PITFALL 2: TRANSACTION ISSUES
# ============================================================================

# ❌ BAD: Sends email before transaction commits
@receiver(post_save, sender=Order)
def bad_send_confirmation(sender, instance, created, **kwargs):
    """
    DON'T DO THIS!
    
    Problem: Email sent even if transaction rolls back
    """
    # if created:
    #     send_email(instance.user.email, "Order created")  # ❌ Too early!
    pass


# ✅ GOOD: Wait for transaction commit
@receiver(post_save, sender=Order)
def good_send_confirmation(sender, instance, created, **kwargs):
    """
    Wait for transaction to commit
    
    Pattern: Use transaction.on_commit() for side effects
    """
    if created:
        def send_email_on_commit():
            # This runs ONLY after successful commit
            print(f"📧 Email sent to {instance.user.email}")
            # send_email(instance.user.email, "Order created")
        
        transaction.on_commit(send_email_on_commit)
        print("✅ Email scheduled (after commit)")


# ============================================================================
# PITFALL 3: PERFORMANCE ISSUES
# ============================================================================

# ❌ BAD: N+1 query problem
@receiver(post_save, sender=Book)
def bad_notify_users(sender, instance, created, **kwargs):
    """
    DON'T DO THIS!
    
    Problem: One query per user (N+1 problem)
    Blocks the request thread
    """
    # if created:
    #     for user in User.objects.all():  # ❌ N+1 queries
    #         send_notification(user, instance)  # ❌ Blocking operation
    pass


# ✅ GOOD: Async task with bulk operations
@receiver(post_save, sender=Book)
def good_notify_users(sender, instance, created, **kwargs):
    """
    Use async task (Celery) for heavy operations
    
    Pattern: Signal triggers Celery task, task handles bulk processing
    """
    if created:
        # Get all user IDs at once
        user_ids = list(User.objects.values_list('id', flat=True))
        
        # Schedule async task
        # notify_users_about_book.delay(instance.id, user_ids)
        print(f"✅ Notification task scheduled for {len(user_ids)} users")


# ============================================================================
# PITFALL 4: HEAVY OPERATIONS IN SIGNALS
# ============================================================================

# ❌ BAD: Heavy operation in signal
@receiver(post_save, sender=Book)
def bad_generate_thumbnail(sender, instance, **kwargs):
    """
    DON'T DO THIS!
    
    Problem: Blocks request for 5 seconds
    """
    # if instance.cover_image:
    #     time.sleep(5)  # ❌ Simulating heavy operation
    #     generate_thumbnail(instance.cover_image)  # ❌ Blocks request
    pass


# ✅ GOOD: Async processing
@receiver(post_save, sender=Book)
def good_generate_thumbnail(sender, instance, **kwargs):
    """
    Use Celery for heavy operations
    
    Pattern: Signal triggers task, task does the work
    """
    if instance.cover_image:
        # generate_thumbnail_task.delay(instance.id)
        print("✅ Thumbnail generation scheduled")


# ============================================================================
# PITFALL 5: ERROR HANDLING
# ============================================================================

# ❌ BAD: No error handling
@receiver(post_save, sender=Book)
def bad_error_handling(sender, instance, **kwargs):
    """
    DON'T DO THIS!
    
    Problem: One error breaks all receivers
    """
    # result = 10 / 0  # ❌ Crashes all other receivers
    pass


# ✅ GOOD: Proper error handling
@receiver(post_save, sender=Book)
def good_error_handling(sender, instance, **kwargs):
    """
    Wrap in try/except to prevent breaking other receivers
    
    Pattern: Log error, don't break the chain
    """
    try:
        # Risky operation
        result = 10 / 0
    except Exception as e:
        # Log error
        print(f"❌ Error in signal: {e}")
        # logger.exception("Signal error")
        # Don't raise - let other receivers run


# ============================================================================
# BEST PRACTICE 1: CACHE INVALIDATION
# ============================================================================

@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    """
    Invalidate cache when book changes
    
    Pattern: Clear cache on model changes
    """
    cache_keys = [
        f'book:{instance.id}',
        f'books:all',
        f'books:author:{instance.author}',
    ]
    
    for key in cache_keys:
        cache.delete(key)
    
    print(f"✅ Cache invalidated for book {instance.id}")


# ============================================================================
# BEST PRACTICE 2: IDEMPOTENT OPERATIONS
# ============================================================================

@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, **kwargs):
    """
    Idempotent profile creation
    
    Pattern: Use get_or_create for idempotency
    Safe to run multiple times
    """
    from django.contrib.auth.models import User
    
    # profile, created = UserProfile.objects.get_or_create(user=instance)
    # if created:
    #     print(f"✅ Profile created for {instance.username}")
    # else:
    #     print(f"✓ Profile already exists for {instance.username}")
    pass


# ============================================================================
# BEST PRACTICE 3: CONDITIONAL SIGNAL EXECUTION
# ============================================================================

@receiver(post_save, sender=Book)
def conditional_processing(sender, instance, created, **kwargs):
    """
    Run logic only when specific conditions met
    
    Pattern: Check conditions early, return if not met
    """
    # Only for newly created books
    if not created:
        return
    
    # Only for expensive books
    if instance.price < 50:
        return
    
    # Only if stock available
    if instance.stock == 0:
        return
    
    # Now do the processing
    print(f"✅ Processing premium book: {instance.title}")


# ============================================================================
# BEST PRACTICE 4: FIELD CHANGE DETECTION
# ============================================================================

@receiver(pre_save, sender=Book)
def detect_field_changes(sender, instance, **kwargs):
    """
    Detect which fields changed
    
    Pattern: Compare with old instance
    Useful for: audit logging, conditional actions
    """
    if not instance.pk:
        return  # New instance, no changes to detect
    
    try:
        old_instance = Book.objects.get(pk=instance.pk)
        
        # Check price change
        if old_instance.price != instance.price:
            print(f"💰 Price changed: ${old_instance.price} → ${instance.price}")
            # Log price change
            # Send notification if price dropped
        
        # Check stock change
        if old_instance.stock != instance.stock:
            print(f"📦 Stock changed: {old_instance.stock} → {instance.stock}")
            # Check if out of stock
            if instance.stock == 0:
                print("⚠️ Out of stock!")
        
    except Book.DoesNotExist:
        pass


# ============================================================================
# BEST PRACTICE 5: SIGNAL DISCONNECTION FOR TESTING
# ============================================================================

from contextlib import contextmanager

@contextmanager
def disconnect_signal(signal, receiver, sender):
    """
    Context manager to temporarily disconnect signal
    
    Usage:
        with disconnect_signal(post_save, my_receiver, MyModel):
            # Signal is disconnected here
            MyModel.objects.create(...)
        # Signal is reconnected here
    """
    signal.disconnect(receiver, sender=sender)
    try:
        yield
    finally:
        signal.connect(receiver, sender=sender)


def demo_signal_disconnect():
    """Demo signal disconnection"""
    
    print("\n--- With signal ---")
    book1 = Book.objects.create(title="Book 1", author="Author", price=10)
    
    print("\n--- Without signal ---")
    with disconnect_signal(post_save, good_send_confirmation, Order):
        order = Order.objects.create(user_id=1, total=99.99)
    
    print("\n--- With signal again ---")
    book2 = Book.objects.create(title="Book 2", author="Author", price=20)


# ============================================================================
# BEST PRACTICE 6: BULK OPERATIONS
# ============================================================================

@receiver(post_save, sender=Book)
def handle_bulk_operations(sender, instance, **kwargs):
    """
    Handle bulk_create and bulk_update
    
    Note: bulk_create/bulk_update don't trigger signals!
    """
    # This won't be called for bulk_create
    print(f"✅ Book saved individually: {instance.title}")


def demo_bulk_operations():
    """
    Demonstrate signal behavior with bulk operations
    """
    
    print("\n--- Individual create (triggers signal) ---")
    Book.objects.create(title="Book 1", author="Author", price=10)
    
    print("\n--- Bulk create (NO signals) ---")
    Book.objects.bulk_create([
        Book(title="Book 2", author="Author", price=20),
        Book(title="Book 3", author="Author", price=30),
    ])
    
    print("\n--- Bulk update (NO signals) ---")
    Book.objects.filter(author="Author").update(price=15)


# ============================================================================
# TESTING PATTERNS
# ============================================================================

"""
# test_signals.py

from django.test import TestCase, TransactionTestCase
from unittest.mock import patch, Mock, call
from django.db.models.signals import post_save

class SignalTestCase(TestCase):
    '''Test signals with proper mocking'''
    
    def test_signal_triggered(self):
        '''Test that signal is triggered'''
        with patch('path.to.signal.handler') as mock_handler:
            book = Book.objects.create(title="Test")
            mock_handler.assert_called_once()
    
    def test_signal_with_args(self):
        '''Test signal arguments'''
        mock_handler = Mock()
        post_save.connect(mock_handler, sender=Book)
        
        book = Book.objects.create(title="Test")
        
        call_kwargs = mock_handler.call_args[1]
        self.assertEqual(call_kwargs['sender'], Book)
        self.assertEqual(call_kwargs['instance'].title, "Test")
        self.assertTrue(call_kwargs['created'])
        
        post_save.disconnect(mock_handler, sender=Book)
    
    def test_signal_side_effects(self):
        '''Test signal side effects'''
        book = Book.objects.create(title="Test")
        
        # Check side effects
        self.assertTrue(BookLog.objects.filter(book=book).exists())
        self.assertEqual(cache.get(f'book:{book.id}'), None)

class TransactionSignalTest(TransactionTestCase):
    '''Test signals with transactions'''
    
    def test_on_commit_signal(self):
        '''Test transaction.on_commit behavior'''
        with patch('path.to.send_email') as mock_email:
            with transaction.atomic():
                order = Order.objects.create(user_id=1, total=99)
                # Email not sent yet
                mock_email.assert_not_called()
            
            # Email sent after commit
            mock_email.assert_called_once()
"""

# ============================================================================
# PERFORMANCE MONITORING
# ============================================================================

import time
from functools import wraps

def monitor_signal_performance(signal_name):
    """
    Decorator to monitor signal performance
    
    Usage:
        @monitor_signal_performance("book_saved")
        @receiver(post_save, sender=Book)
        def my_signal(sender, instance, **kwargs):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = (time.time() - start_time) * 1000
            
            if duration > 100:  # Warn if > 100ms
                print(f"⚠️ Slow signal '{signal_name}': {duration:.2f}ms")
            
            return result
        return wrapper
    return decorator


@monitor_signal_performance("book_saved")
@receiver(post_save, sender=Book)
def monitored_signal(sender, instance, **kwargs):
    """Example monitored signal"""
    # Simulate work
    time.sleep(0.05)
    print(f"✅ Book saved: {instance.title}")


# ============================================================================
# SUMMARY: DO'S AND DON'TS
# ============================================================================

"""
✅ DO:

1. Keep signals simple and fast
2. Use Celery for heavy operations
3. Use transaction.on_commit() for side effects
4. Handle errors gracefully (try/except)
5. Use update() to avoid triggering signals
6. Clear cache when models change
7. Test signals thoroughly
8. Monitor signal performance
9. Document signal side effects
10. Use idempotent operations

❌ DON'T:

1. Call save() in post_save (infinite loop)
2. Do heavy operations in signals (blocks request)
3. Send emails/notifications without on_commit
4. Ignore errors (wrap in try/except)
5. Create N+1 query problems
6. Put business logic in signals
7. Create signal chains (signal → signal)
8. Forget to import signals (apps.py ready())
9. Use signals when simple function call is better
10. Rely on bulk_create/bulk_update triggering signals

## PERFORMANCE TIPS:

1. Use select_related/prefetch_related
2. Batch database operations
3. Cache frequently accessed data
4. Use Celery for async processing
5. Monitor slow signals (> 100ms)
6. Avoid database queries in loops
7. Use bulk operations when possible
8. Implement circuit breakers for external calls

## TESTING TIPS:

1. Mock external services
2. Use TransactionTestCase for on_commit tests
3. Test both success and failure cases
4. Verify signal arguments
5. Check side effects (cache, database, etc.)
6. Test signal disconnection
7. Measure test coverage
"""