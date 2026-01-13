"""
Notifications Signals
=====================

Avtomatik notification yuborish uchun signals.

Triggers:
- User ro'yxatdan o'tganda
- Yangi kitob qo'shilganda
- Device token yaratilganda
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import DeviceToken, UserPreferences, NotificationLog
from .services import notification_manager

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Yangi user yaratilganda preferences yaratish
    
    Signal: post_save(User)
    """
    if created:
        UserPreferences.objects.get_or_create(user=instance)
        logger.info(f"✓ UserPreferences created for: {instance.username}")


@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance, created, **kwargs):
    """
    Yangi user'ga xush kelibsiz notification yuborish
    
    Signal: post_save(User)
    """
    if created:
        try:
            # Push notification
            notification_manager.send_push(
                user=instance,
                title="Xush kelibsiz! 🎉",
                body=f"Assalomu alaykum {instance.username}! Bizning platformamizga xush kelibsiz.",
                data={
                    'type': 'welcome',
                    'user_id': instance.id
                }
            )
            
            logger.info(f"✓ Welcome notification sent to: {instance.username}")
        
        except Exception as e:
            logger.error(f"✗ Failed to send welcome notification: {e}")


@receiver(post_save, sender=DeviceToken)
def notify_new_device(sender, instance, created, **kwargs):
    """
    Yangi qurilma qo'shilganda notification yuborish
    
    Signal: post_save(DeviceToken)
    """
    if created:
        try:
            # SMS notification
            notification_manager.send_sms(
                user=instance.user,
                message=f"Yangi qurilma qo'shildi: {instance.device_type} - {instance.device_name or 'Unknown'}",
                phone_number=None,  # User profile'dan olinadi
                metadata={
                    'type': 'security',
                    'device_id': instance.id,
                    'device_type': instance.device_type
                }
            )
            
            logger.info(f"✓ New device notification sent to: {instance.user.username}")
        
        except Exception as e:
            logger.error(f"✗ Failed to send new device notification: {e}")


# ============================================
# BOOKS APP SIGNALS (agar books app bo'lsa)
# ============================================

try:
    from books.models import Book
    
    @receiver(post_save, sender=Book)
    def notify_new_book(sender, instance, created, **kwargs):
        """
        Yangi kitob qo'shilganda barcha foydalanuvchilarga xabar berish
        
        Signal: post_save(Book)
        """
        if created:
            try:
                # Faqat notification_preferences.new_book_notifications=True bo'lgan userlar
                users = User.objects.filter(
                    notification_preferences__new_book_notifications=True,
                    notification_preferences__push_enabled=True,
                    is_active=True
                )
                
                for user in users:
                    notification_manager.send_push(
                        user=user,
                        title="Yangi kitob qo'shildi! 📚",
                        body=f"{instance.title} - {instance.author}",
                        data={
                            'type': 'new_book',
                            'book_id': instance.id,
                            'book_title': instance.title
                        }
                    )
                
                logger.info(f"✓ New book notification sent to {users.count()} users: {instance.title}")
            
            except Exception as e:
                logger.error(f"✗ Failed to send new book notification: {e}")

except ImportError:
    logger.info("Books app not found - new book signals disabled")


# ============================================
# BORROWING SIGNALS (agar borrowing app bo'lsa)
# ============================================

try:
    from books.models import Borrowing
    
    @receiver(post_save, sender=Borrowing)
    def notify_borrowing_created(sender, instance, created, **kwargs):
        """
        Kitob olish/ijaraga olish yaratilganda notification
        
        Signal: post_save(Borrowing)
        """
        if created:
            try:
                notification_manager.send_push(
                    user=instance.user,
                    title="Kitob ijaraga berildi ✅",
                    body=f"{instance.book.title} - Qaytarish sanasi: {instance.return_date.strftime('%d.%m.%Y')}",
                    data={
                        'type': 'borrowing_created',
                        'borrowing_id': instance.id,
                        'book_id': instance.book.id
                    }
                )
                
                # SMS ham yuborish
                notification_manager.send_sms(
                    user=instance.user,
                    message=f"Kitob: {instance.book.title}\nQaytarish: {instance.return_date.strftime('%d.%m.%Y')}",
                    metadata={
                        'type': 'borrowing_created',
                        'borrowing_id': instance.id
                    }
                )
                
                logger.info(f"✓ Borrowing created notification sent to: {instance.user.username}")
            
            except Exception as e:
                logger.error(f"✗ Failed to send borrowing notification: {e}")
    
    
    @receiver(post_save, sender=Borrowing)
    def notify_borrowing_returned(sender, instance, created, **kwargs):
        """
        Kitob qaytarilganda notification
        
        Signal: post_save(Borrowing)
        """
        if not created and instance.returned:
            try:
                notification_manager.send_push(
                    user=instance.user,
                    title="Kitob qaytarildi ✅",
                    body=f"{instance.book.title} muvaffaqiyatli qaytarildi. Rahmat!",
                    data={
                        'type': 'borrowing_returned',
                        'borrowing_id': instance.id,
                        'book_id': instance.book.id
                    }
                )
                
                logger.info(f"✓ Borrowing returned notification sent to: {instance.user.username}")
            
            except Exception as e:
                logger.error(f"✗ Failed to send return notification: {e}")

except ImportError:
    logger.info("Borrowing model not found - borrowing signals disabled")


# ============================================
# OVERDUE REMINDER (Celery Task bilan ishlaydi)
# ============================================

def send_overdue_reminders():
    """
    Muddati o'tgan kitoblar uchun eslatma yuborish
    
    Bu funksiyani Celery task sifatida ishlatish mumkin:
    @shared_task
    def send_overdue_reminders_task():
        send_overdue_reminders()
    """
    try:
        from books.models import Borrowing
        from django.utils import timezone
        
        # Muddati o'tgan borrowings
        overdue = Borrowing.objects.filter(
            returned=False,
            return_date__lt=timezone.now().date()
        ).select_related('user', 'book')
        
        for borrowing in overdue:
            # Faqat overdue_notifications yoqilgan userlarga
            prefs = UserPreferences.objects.filter(
                user=borrowing.user,
                overdue_notifications=True
            ).first()
            
            if prefs:
                # Push notification
                notification_manager.send_push(
                    user=borrowing.user,
                    title="Kitobni qaytarish muddati o'tgan! ⚠️",
                    body=f"{borrowing.book.title} - Qaytarish kerak edi: {borrowing.return_date.strftime('%d.%m.%Y')}",
                    data={
                        'type': 'overdue',
                        'borrowing_id': borrowing.id,
                        'book_id': borrowing.book.id
                    }
                )
                
                # SMS ham yuborish
                notification_manager.send_sms(
                    user=borrowing.user,
                    message=f"⚠️ Muddati o'tgan: {borrowing.book.title}\nIltimos tezroq qaytaring!",
                    metadata={
                        'type': 'overdue',
                        'borrowing_id': borrowing.id
                    }
                )
        
        logger.info(f"✓ Overdue reminders sent to {overdue.count()} users")
        return overdue.count()
    
    except ImportError:
        logger.warning("Borrowing model not found")
        return 0
    except Exception as e:
        logger.error(f"✗ Failed to send overdue reminders: {e}")
        return 0


def send_due_date_reminders(days_before=3):
    """
    Qaytarish muddati yaqinlashganda eslatma yuborish
    
    Args:
        days_before: Necha kun oldin eslatma yuborish (default: 3)
    
    Bu funksiyani Celery task sifatida ishlatish mumkin
    """
    try:
        from books.models import Borrowing
        from django.utils import timezone
        from datetime import timedelta
        
        # Yaqinda qaytarish kerak bo'lgan borrowings
        target_date = timezone.now().date() + timedelta(days=days_before)
        
        upcoming = Borrowing.objects.filter(
            returned=False,
            return_date=target_date
        ).select_related('user', 'book')
        
        for borrowing in upcoming:
            # Faqat due_date_reminders yoqilgan userlarga
            prefs = UserPreferences.objects.filter(
                user=borrowing.user,
                due_date_reminders=True
            ).first()
            
            if prefs:
                # Push notification
                notification_manager.send_push(
                    user=borrowing.user,
                    title="Kitobni qaytarish muddati yaqinlashmoqda 📅",
                    body=f"{borrowing.book.title} - {days_before} kundan keyin qaytarish kerak",
                    data={
                        'type': 'due_reminder',
                        'borrowing_id': borrowing.id,
                        'book_id': borrowing.book.id,
                        'days_remaining': days_before
                    }
                )
        
        logger.info(f"✓ Due date reminders sent to {upcoming.count()} users")
        return upcoming.count()
    
    except ImportError:
        logger.warning("Borrowing model not found")
        return 0
    except Exception as e:
        logger.error(f"✗ Failed to send due date reminders: {e}")
        return 0


# ============================================
# SYSTEM NOTIFICATIONS
# ============================================

def send_system_notification(title, message, notification_type='system', user_ids=None, all_users=False):
    """
    Tizim notification yuborish
    
    Args:
        title: Sarlavha
        message: Xabar
        notification_type: Notification turi
        user_ids: Foydalanuvchi ID'lari (list)
        all_users: Barcha foydalanuvchilarga yuborish (bool)
    
    Returns:
        dict: Natija
    
    Example:
        send_system_notification(
            title="Tizim yangilanmoqda",
            message="Bugun kechqurun 22:00 da tizim texnik ishlar uchun to'xtatiladi",
            all_users=True
        )
    """
    try:
        if all_users:
            users = User.objects.filter(
                notification_preferences__system_notifications=True,
                notification_preferences__push_enabled=True,
                is_active=True
            )
        elif user_ids:
            users = User.objects.filter(
                id__in=user_ids,
                notification_preferences__system_notifications=True,
                notification_preferences__push_enabled=True,
                is_active=True
            )
        else:
            return {'success': False, 'error': 'No recipients'}
        
        success_count = 0
        for user in users:
            result = notification_manager.send_push(
                user=user,
                title=title,
                body=message,
                data={
                    'type': notification_type,
                    'system': True
                }
            )
            if result.get('success'):
                success_count += 1
        
        logger.info(f"✓ System notification sent to {success_count}/{users.count()} users")
        
        return {
            'success': True,
            'sent': success_count,
            'total': users.count()
        }
    
    except Exception as e:
        logger.error(f"✗ Failed to send system notification: {e}")
        return {'success': False, 'error': str(e)}