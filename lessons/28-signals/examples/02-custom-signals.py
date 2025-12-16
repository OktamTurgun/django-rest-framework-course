"""
Example 2: Custom Django Signals

Demonstrates:
- Creating custom signals
- Sending custom signals with arguments
- Multiple receivers for one signal
- Signal dispatching patterns
- Real-world use cases

Custom signals are useful when:
- You need app-specific events
- Built-in signals are not enough
- You want decoupled architecture
- You need to notify multiple listeners
"""

from django.dispatch import Signal, receiver
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# ============================================================================
# CUSTOM SIGNALS DEFINITION
# ============================================================================

# Signal 1: Book borrowed/returned
book_borrowed = Signal()  # providing_args=['book', 'user', 'due_date']
book_returned = Signal()  # providing_args=['book', 'user', 'return_date']

# Signal 2: Order processing
order_created = Signal()  # providing_args=['order']
order_paid = Signal()     # providing_args=['order', 'payment_method']
order_shipped = Signal()  # providing_args=['order', 'tracking_number']
order_cancelled = Signal()  # providing_args=['order', 'reason']

# Signal 3: User activity
user_login_attempt = Signal()  # providing_args=['username', 'success', 'ip']
user_password_changed = Signal()  # providing_args=['user']

# Signal 4: Inventory
low_stock_alert = Signal()  # providing_args=['product', 'current_stock']
out_of_stock_alert = Signal()  # providing_args=['product']


# ============================================================================
# MODELS
# ============================================================================

class Book(models.Model):
    title = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    borrowed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    is_borrowed = models.BooleanField(default=False)


class BorrowHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# ============================================================================
# BOOK BORROW/RETURN SIGNALS
# ============================================================================

def borrow_book(book_id, user, days=14):
    """
    Book borrow qilish va signal yuborish
    
    Args:
        book_id: Book ID
        user: User instance
        days: Borrow duration in days
    
    Returns:
        BorrowHistory instance
    """
    try:
        book = Book.objects.get(id=book_id)
        
        # Validation
        if book.is_borrowed:
            raise ValueError(f"Book '{book.title}' is already borrowed")
        
        if book.stock < 1:
            raise ValueError(f"Book '{book.title}' is out of stock")
        
        # Update book
        book.is_borrowed = True
        book.borrowed_by = user
        book.stock -= 1
        book.save()
        
        # Create history
        due_date = timezone.now() + timezone.timedelta(days=days)
        history = BorrowHistory.objects.create(
            book=book,
            user=user,
            due_date=due_date
        )
        
        # 🔥 SEND SIGNAL
        book_borrowed.send(
            sender=Book,
            book=book,
            user=user,
            due_date=due_date
        )
        
        print(f"✅ Book '{book.title}' borrowed by {user.username}")
        return history
        
    except Book.DoesNotExist:
        raise ValueError(f"Book with ID {book_id} not found")


def return_book(book_id, user):
    """
    Book return qilish va signal yuborish
    
    Args:
        book_id: Book ID
        user: User instance
    
    Returns:
        BorrowHistory instance
    """
    try:
        book = Book.objects.get(id=book_id)
        
        # Validation
        if not book.is_borrowed:
            raise ValueError(f"Book '{book.title}' is not borrowed")
        
        if book.borrowed_by != user:
            raise ValueError(f"Book not borrowed by {user.username}")
        
        # Update book
        book.is_borrowed = False
        book.borrowed_by = None
        book.stock += 1
        book.save()
        
        # Update history
        history = BorrowHistory.objects.filter(
            book=book,
            user=user,
            returned_at__isnull=True
        ).first()
        
        if history:
            history.returned_at = timezone.now()
            history.save()
        
        # 🔥 SEND SIGNAL
        book_returned.send(
            sender=Book,
            book=book,
            user=user,
            return_date=timezone.now()
        )
        
        print(f"✅ Book '{book.title}' returned by {user.username}")
        return history
        
    except Book.DoesNotExist:
        raise ValueError(f"Book with ID {book_id} not found")


# ============================================================================
# SIGNAL RECEIVERS - BOOK BORROW/RETURN
# ============================================================================

@receiver(book_borrowed)
def log_book_borrowed(sender, book, user, due_date, **kwargs):
    """Log borrow event"""
    print(f"\n📋 [LOG] Book borrowed:")
    print(f"   Book: {book.title}")
    print(f"   User: {user.username}")
    print(f"   Due: {due_date.strftime('%Y-%m-%d')}")


@receiver(book_borrowed)
def send_borrow_confirmation(sender, book, user, due_date, **kwargs):
    """Send email confirmation"""
    print(f"\n📧 [EMAIL] Sending borrow confirmation to {user.email}")
    print(f"   Subject: Book Borrowed - {book.title}")
    print(f"   Message: Please return by {due_date.strftime('%Y-%m-%d')}")
    # In real app: send_mail.delay(...)


@receiver(book_borrowed)
def update_user_statistics(sender, book, user, **kwargs):
    """Update user profile statistics"""
    print(f"\n📊 [STATS] Updating user statistics")
    # profile = user.profile
    # profile.books_borrowed += 1
    # profile.save()


@receiver(book_borrowed)
def check_low_stock(sender, book, **kwargs):
    """Check if stock is low"""
    if book.stock < 3:
        print(f"\n⚠️ [ALERT] Low stock warning for '{book.title}'")
        # Send signal for low stock
        low_stock_alert.send(
            sender=Book,
            product=book,
            current_stock=book.stock
        )


@receiver(book_returned)
def log_book_returned(sender, book, user, return_date, **kwargs):
    """Log return event"""
    print(f"\n📋 [LOG] Book returned:")
    print(f"   Book: {book.title}")
    print(f"   User: {user.username}")
    print(f"   Returned: {return_date.strftime('%Y-%m-%d %H:%M')}")


@receiver(book_returned)
def check_late_return(sender, book, user, return_date, **kwargs):
    """Check if return is late"""
    history = BorrowHistory.objects.filter(
        book=book,
        user=user,
        returned_at=return_date
    ).first()
    
    if history and history.due_date < return_date:
        days_late = (return_date - history.due_date).days
        print(f"\n⏰ [LATE] Book returned {days_late} days late!")
        # Calculate fine, send notification, etc.


# ============================================================================
# ORDER PROCESSING SIGNALS
# ============================================================================

def create_order(user, total):
    """Create order and trigger signals"""
    order = Order.objects.create(user=user, total=total)
    
    # 🔥 SEND SIGNAL
    order_created.send(
        sender=Order,
        order=order
    )
    
    return order


def process_payment(order_id, payment_method='card'):
    """Process payment and trigger signals"""
    order = Order.objects.get(id=order_id)
    order.status = 'paid'
    order.save()
    
    # 🔥 SEND SIGNAL
    order_paid.send(
        sender=Order,
        order=order,
        payment_method=payment_method
    )
    
    return order


def ship_order(order_id, tracking_number):
    """Ship order and trigger signals"""
    order = Order.objects.get(id=order_id)
    order.status = 'shipped'
    order.tracking_number = tracking_number
    order.save()
    
    # 🔥 SEND SIGNAL
    order_shipped.send(
        sender=Order,
        order=order,
        tracking_number=tracking_number
    )
    
    return order


# ============================================================================
# SIGNAL RECEIVERS - ORDER PROCESSING
# ============================================================================

@receiver(order_created)
def send_order_confirmation(sender, order, **kwargs):
    """Send order confirmation email"""
    print(f"\n📧 [EMAIL] Order confirmation sent")
    print(f"   Order ID: {order.id}")
    print(f"   Total: ${order.total}")


@receiver(order_created)
def create_invoice(sender, order, **kwargs):
    """Generate invoice"""
    print(f"\n📄 [INVOICE] Invoice generated for order #{order.id}")


@receiver(order_paid)
def notify_payment_success(sender, order, payment_method, **kwargs):
    """Notify user about successful payment"""
    print(f"\n💳 [PAYMENT] Payment successful")
    print(f"   Order: #{order.id}")
    print(f"   Method: {payment_method}")
    print(f"   Amount: ${order.total}")


@receiver(order_paid)
def update_inventory(sender, order, **kwargs):
    """Update inventory after payment"""
    print(f"\n📦 [INVENTORY] Updating inventory for order #{order.id}")


@receiver(order_shipped)
def send_shipping_notification(sender, order, tracking_number, **kwargs):
    """Send shipping notification with tracking"""
    print(f"\n🚚 [SHIPPING] Order shipped")
    print(f"   Order: #{order.id}")
    print(f"   Tracking: {tracking_number}")


# ============================================================================
# MULTIPLE RECEIVERS EXAMPLE
# ============================================================================

@receiver(low_stock_alert)
def notify_admin_low_stock(sender, product, current_stock, **kwargs):
    """Notify admin about low stock"""
    print(f"\n👨‍💼 [ADMIN] Low stock alert")
    print(f"   Product: {product.title}")
    print(f"   Current stock: {current_stock}")


@receiver(low_stock_alert)
def auto_reorder(sender, product, current_stock, **kwargs):
    """Automatically create reorder request"""
    if current_stock < 2:
        print(f"\n🔄 [AUTO-REORDER] Creating reorder request for {product.title}")


@receiver(low_stock_alert)
def log_low_stock(sender, product, current_stock, **kwargs):
    """Log low stock event"""
    print(f"\n📝 [LOG] Low stock logged: {product.title} ({current_stock})")


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_custom_signals():
    """
    Demo custom signals
    
    Run in Django shell:
    >>> from examples.02_custom_signals import demo_custom_signals
    >>> demo_custom_signals()
    """
    
    print("=" * 70)
    print("DEMO: Custom Signals")
    print("=" * 70)
    
    # Setup
    user = User.objects.create_user('testuser', 'test@example.com', 'pass123')
    book = Book.objects.create(title="Python Guide", stock=5)
    
    # ========== BORROW BOOK ==========
    print("\n" + "=" * 70)
    print("TEST 1: Borrow Book Signal")
    print("=" * 70)
    
    borrow_book(book.id, user, days=7)
    # Expected: Multiple receivers triggered
    # - log_book_borrowed
    # - send_borrow_confirmation
    # - update_user_statistics
    # - check_low_stock (if stock < 3)
    
    # ========== RETURN BOOK ==========
    print("\n" + "=" * 70)
    print("TEST 2: Return Book Signal")
    print("=" * 70)
    
    return_book(book.id, user)
    # Expected: Return receivers triggered
    # - log_book_returned
    # - check_late_return
    
    # ========== ORDER WORKFLOW ==========
    print("\n" + "=" * 70)
    print("TEST 3: Order Processing Signals")
    print("=" * 70)
    
    # Create order
    print("\n--- Creating Order ---")
    order = create_order(user, Decimal('99.99'))
    
    # Process payment
    print("\n--- Processing Payment ---")
    process_payment(order.id, 'card')
    
    # Ship order
    print("\n--- Shipping Order ---")
    ship_order(order.id, 'TRACK123456')
    
    # ========== LOW STOCK ALERT ==========
    print("\n" + "=" * 70)
    print("TEST 4: Low Stock Alert (Multiple Receivers)")
    print("=" * 70)
    
    book2 = Book.objects.create(title="JavaScript Book", stock=1)
    borrow_book(book2.id, user)
    # Expected: low_stock_alert signal triggers 3 receivers
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETED")
    print("=" * 70)


# ============================================================================
# ADVANCED: CONDITIONAL SIGNAL RECEIVERS
# ============================================================================

@receiver(book_borrowed)
def premium_user_bonus(sender, book, user, **kwargs):
    """Give bonus only to premium users"""
    # if user.profile.is_premium:
    #     print(f"\n🌟 [BONUS] Premium user bonus applied!")
    pass


@receiver(order_paid)
def large_order_discount(sender, order, **kwargs):
    """Apply discount for large orders"""
    if order.total > 100:
        print(f"\n🎉 [DISCOUNT] Large order discount applied!")


# ============================================================================
# SIGNAL DISCONNECTION EXAMPLE
# ============================================================================

def demo_signal_disconnect():
    """
    Demo: How to disconnect signals
    
    Useful for:
    - Testing
    - Temporary disable
    - Conditional behavior
    """
    
    print("\n" + "=" * 70)
    print("DEMO: Signal Disconnection")
    print("=" * 70)
    
    user = User.objects.create_user('user2', 'user2@example.com', 'pass')
    book = Book.objects.create(title="Test Book", stock=10)
    
    # Normal borrow (all signals active)
    print("\n--- Borrow 1: All signals active ---")
    borrow_book(book.id, user)
    
    # Disconnect email signal
    print("\n--- Disconnecting email signal ---")
    book_borrowed.disconnect(send_borrow_confirmation)
    
    # Return and borrow again (no email)
    return_book(book.id, user)
    print("\n--- Borrow 2: Email signal disconnected ---")
    borrow_book(book.id, user)
    
    # Reconnect
    print("\n--- Reconnecting email signal ---")
    book_borrowed.connect(send_borrow_confirmation)
    
    return_book(book.id, user)
    print("\n--- Borrow 3: All signals active again ---")
    borrow_book(book.id, user)


# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
✅ CUSTOM SIGNALS BEST PRACTICES:

1. Clear naming:
   - Use descriptive names: user_registered, order_paid
   - Follow pattern: entity_action

2. Document arguments:
   # Signal: book_borrowed
   # Args: book, user, due_date

3. Keep receivers focused:
   - Each receiver = one responsibility
   - Don't put business logic in receivers

4. Use kwargs:
   - Always accept **kwargs for future compatibility
   - @receiver(my_signal)
     def handler(sender, arg1, arg2, **kwargs):

5. Error handling:
   - Wrap receiver logic in try/except
   - Log errors, don't let one receiver break others

6. Testing:
   - Test signal sending
   - Test each receiver separately
   - Mock heavy operations

7. Performance:
   - Keep receivers fast
   - Use Celery for heavy tasks
   - Avoid database queries in loops

8. Documentation:
   - Document when signal is sent
   - Document expected arguments
   - List all receivers

❌ AVOID:

1. Too many signals
   - Don't create signal for every action
   - Use signals for important events only

2. Signal chains
   - Receiver triggering another signal
   - Can cause unexpected behavior

3. Modifying sender in receiver
   - Don't change the object that triggered signal
   - Can cause infinite loops

4. Business logic in signals
   - Signals for notification/logging only
   - Keep business logic in views/services
"""

# ============================================================================
# TESTING CUSTOM SIGNALS
# ============================================================================

"""
from django.test import TestCase
from unittest.mock import patch, Mock

class CustomSignalTest(TestCase):
    
    def test_book_borrowed_signal_sent(self):
        '''Test signal is sent when book borrowed'''
        # Mock receiver
        mock_receiver = Mock()
        book_borrowed.connect(mock_receiver)
        
        # Trigger action
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        book = Book.objects.create(title="Test", stock=5)
        borrow_book(book.id, user)
        
        # Assert signal was sent
        self.assertTrue(mock_receiver.called)
        call_kwargs = mock_receiver.call_args[1]
        self.assertEqual(call_kwargs['book'], book)
        self.assertEqual(call_kwargs['user'], user)
        
        # Cleanup
        book_borrowed.disconnect(mock_receiver)
    
    def test_multiple_receivers_called(self):
        '''Test all receivers are triggered'''
        receivers = [Mock(), Mock(), Mock()]
        
        for receiver in receivers:
            book_borrowed.connect(receiver)
        
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        book = Book.objects.create(title="Test", stock=5)
        borrow_book(book.id, user)
        
        for receiver in receivers:
            self.assertTrue(receiver.called)
        
        # Cleanup
        for receiver in receivers:
            book_borrowed.disconnect(receiver)
"""