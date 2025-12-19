"""
Books app signals - Uses accounts.Profile instead of books.UserProfile
"""

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from .models import Book, Author, BookLog, BorrowHistory

# Import Profile from accounts app
from accounts.models import Profile


# ============================================================================
# CUSTOM SIGNALS
# ============================================================================

book_borrowed = Signal()
book_returned = Signal()
books_bulk_imported = Signal()


# ============================================================================
# USER PROFILE SIGNALS
# ============================================================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """User yaratilganda avtomatik profile yaratish"""
    if created:
        Profile.objects.get_or_create(user=instance)
        print(f"✅ Profile created for user: {instance.username}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User save bo'lganda profile ham save qilish"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
        print(f"✅ Profile saved for user: {instance.username}")


# ============================================================================
# BOOK LOGGING SIGNALS
# ============================================================================

@receiver(post_save, sender=Book)
def log_book_save(sender, instance, created, **kwargs):
    """Book create/update ni log qilish"""
    action = 'created' if created else 'updated'
    details = {}
    
    if created:
        details = {
            'stock': instance.stock,
            'price': str(instance.price),
            'is_available': instance.is_available,
        }
    else:
        details = {
            'updated_at': timezone.now().isoformat(),
        }
    
    BookLog.objects.create(
        book_title=instance.title,
        book_id=instance.id,
        action=action,
        user=None,
        details=details
    )
    
    print(f"📋 Book {action}: {instance.title}")


@receiver(pre_delete, sender=Book)
def log_book_delete(sender, instance, **kwargs):
    """Book delete ni log qilish"""
    BookLog.objects.create(
        book_title=instance.title,
        book_id=instance.id,
        action='deleted',
        user=None,
        details={
            'stock': instance.stock,
            'price': str(instance.price),
            'deleted_at': timezone.now().isoformat(),
        }
    )
    
    print(f"🗑️ Book deletion logged: {instance.title}")


# ============================================================================
# AUTHOR STATISTICS SIGNALS
# ============================================================================

@receiver(post_save, sender=Book)
def update_author_stats_on_save(sender, instance, created, **kwargs):
    """Book yaratilganda yoki o'zgarganda author statistikasini yangilash"""
    if not instance.author:
        return
        
    author = instance.author
    
    # Total books count
    author.total_books = Book.objects.filter(author=author).count()
    
    # Available books count
    author.available_books = Book.objects.filter(
        author=author,
        is_available=True
    ).count()
    
    author.save()
    
    print(f"📊 Author stats updated: {author.name} - Total: {author.total_books}, Available: {author.available_books}")


@receiver(post_delete, sender=Book)
def update_author_stats_on_delete(sender, instance, **kwargs):
    """Book o'chirilganda author statistikasini yangilash"""
    if not instance.author:
        return
        
    author = instance.author
    
    # Total books count
    author.total_books = Book.objects.filter(author=author).count()
    
    # Available books count
    author.available_books = Book.objects.filter(
        author=author,
        is_available=True
    ).count()
    
    author.save()
    
    print(f"📊 Author stats updated after deletion: {author.name}")


# ============================================================================
# CUSTOM SIGNAL FUNCTIONS
# ============================================================================

def borrow_book(book_id, user, days=14):
    """Book borrow qilish va signal yuborish"""
    try:
        book = Book.objects.get(id=book_id)
        
        # Validation
        if not book.is_available:
            raise ValueError(f"Book '{book.title}' is not available")
        
        if book.stock < 1:
            raise ValueError(f"Book '{book.title}' is out of stock")
        
        # Update book
        book.is_available = False
        book.stock -= 1
        book.save()
        
        # Create history
        due_date = timezone.now() + timezone.timedelta(days=days)
        history = BorrowHistory.objects.create(
            book=book,
            user=user,
            due_date=due_date
        )
        
        # Send signal
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
    """Book return qilish va signal yuborish"""
    try:
        book = Book.objects.get(id=book_id)
        
        # Find active borrow history
        history = BorrowHistory.objects.filter(
            book=book,
            user=user,
            returned_at__isnull=True
        ).first()
        
        if not history:
            raise ValueError(f"Book '{book.title}' is not borrowed by {user.username}")
        
        # Update book
        book.is_available = True
        book.stock += 1
        book.save()
        
        # Update history
        return_date = timezone.now()
        history.returned_at = return_date
        history.save()
        
        # Send signal
        book_returned.send(
            sender=Book,
            book=book,
            user=user,
            return_date=return_date
        )
        
        print(f"✅ Book '{book.title}' returned by {user.username}")
        return history
        
    except Book.DoesNotExist:
        raise ValueError(f"Book with ID {book_id} not found")


# ============================================================================
# BOOK BORROW/RETURN SIGNAL RECEIVERS
# ============================================================================

@receiver(book_borrowed)
def on_book_borrowed(sender, book, user, due_date, **kwargs):
    """Book borrow qilinganda"""
    # Update user profile (from accounts app)
    profile = user.profile
    profile.books_borrowed += 1
    profile.save()
    
    # Create log
    BookLog.objects.create(
        book_title=book.title,
        book_id=book.id,
        action='borrowed',
        user=user,
        details={
            'due_date': due_date.isoformat(),
            'borrowed_at': timezone.now().isoformat(),
        }
    )
    
    print(f"📚 Book borrowed:")
    print(f"   Book: {book.title}")
    print(f"   User: {user.username}")
    print(f"   Due: {due_date.strftime('%Y-%m-%d')}")


@receiver(book_returned)
def on_book_returned(sender, book, user, return_date, **kwargs):
    """Book return qilinganda"""
    # Update user profile (from accounts app)
    profile = user.profile
    profile.books_returned += 1
    profile.save()
    
    # Create log
    BookLog.objects.create(
        book_title=book.title,
        book_id=book.id,
        action='returned',
        user=user,
        details={
            'returned_at': return_date.isoformat(),
        }
    )
    
    print(f"📚 Book returned:")
    print(f"   Book: {book.title}")
    print(f"   User: {user.username}")
    print(f"   Returned: {return_date.strftime('%Y-%m-%d %H:%M')}")


# ============================================================================
# BULK IMPORT SIGNAL RECEIVERS
# ============================================================================

@receiver(books_bulk_imported)
def on_books_imported(sender, count, user, **kwargs):
    """Bulk import qilinganda"""
    print(f"📦 Bulk Import Completed:")
    print(f"   Count: {count} books")
    print(f"   User: {user.username}")
    print(f"   Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")