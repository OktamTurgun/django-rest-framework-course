"""
Notification Manager
====================

Barcha notification servislarni boshqaradi.
SMS, Push, Email notification yuborish uchun unified interface.
"""

import logging
from typing import Optional, Dict, Any, List
from django.contrib.auth.models import User
from django.utils import timezone

from .sms_service import sms_service
from .push_service import push_service
from ..models import NotificationLog, DeviceToken, UserPreferences, NotificationType

logger = logging.getLogger(__name__)


class NotificationManager:
    """
    Notification Manager
    
    Barcha notification turlarini boshqaradi:
    - SMS
    - Push
    - Email (kelajakda)
    """
    
    def __init__(self):
        self.sms = sms_service
        self.push = push_service
    
    def send_sms(
        self,
        user: User,
        message: str,
        phone_number: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        SMS yuborish
        
        Args:
            user: Foydalanuvchi
            message: SMS matni
            phone_number: Telefon raqami (agar yo'q bo'lsa user profiledan olinadi)
            metadata: Qo'shimcha ma'lumotlar
        
        Returns:
            dict: Natija
        """
        # User preferences tekshirish
        prefs = self._get_user_preferences(user)
        if not prefs.sms_enabled:
            logger.info(f"SMS disabled for user: {user.username}")
            return {'success': False, 'error': 'SMS disabled by user'}
        
        # Sokin soatlarni tekshirish
        if not prefs.should_send_now():
            logger.info(f"Quiet hours active for user: {user.username}")
            return {'success': False, 'error': 'Quiet hours active'}
        
        # Telefon raqamini olish
        if not phone_number:
            phone_number = self._get_user_phone(user)
        
        if not phone_number:
            logger.error(f"No phone number for user: {user.username}")
            return {'success': False, 'error': 'No phone number'}
        
        # SMS yuborish
        result = self.sms.send_sms(phone_number, message, metadata)
        
        # Log yaratish
        self._create_notification_log(
            user=user,
            notification_type=NotificationType.SMS,
            title='SMS Notification',
            message=message,
            recipient=phone_number,
            result=result,
            metadata=metadata
        )
        
        return result
    
    def send_push(
        self,
        user: User,
        title: str,
        body: str,
        data: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Push notification yuborish
        
        Args:
            user: Foydalanuvchi
            title: Sarlavha
            body: Matn
            data: Qo'shimcha data
        
        Returns:
            dict: Natija
        """
        # User preferences tekshirish
        prefs = self._get_user_preferences(user)
        if not prefs.push_enabled:
            logger.info(f"Push disabled for user: {user.username}")
            return {'success': False, 'error': 'Push disabled by user'}
        
        # Sokin soatlarni tekshirish
        if not prefs.should_send_now():
            logger.info(f"Quiet hours active for user: {user.username}")
            return {'success': False, 'error': 'Quiet hours active'}
        
        # Foydalanuvchi tokenlarini olish
        tokens = self._get_user_tokens(user)
        
        if not tokens:
            logger.warning(f"No device tokens for user: {user.username}")
            return {'success': False, 'error': 'No device tokens'}
        
        # Push yuborish
        if len(tokens) == 1:
            result = self.push.send_push(tokens[0], title, body, data)
            recipient = tokens[0]
        else:
            result = self.push.send_to_multiple(tokens, title, body, data)
            recipient = f"{len(tokens)} devices"
        
        # Log yaratish
        self._create_notification_log(
            user=user,
            notification_type=NotificationType.PUSH,
            title=title,
            message=body,
            recipient=recipient,
            result=result,
            metadata=data
        )
        
        return result
    
    def send_to_all_users(
        self,
        title: str,
        body: str,
        notification_type: str = 'push',
        data: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Barcha foydalanuvchilarga yuborish
        
        Args:
            title: Sarlavha
            body: Matn
            notification_type: 'sms' yoki 'push'
            data: Qo'shimcha data
        
        Returns:
            dict: Natija
        """
        users = User.objects.filter(is_active=True)
        
        success_count = 0
        failure_count = 0
        
        for user in users:
            if notification_type == 'push':
                result = self.send_push(user, title, body, data)
            elif notification_type == 'sms':
                result = self.send_sms(user, body, metadata=data)
            else:
                continue
            
            if result.get('success'):
                success_count += 1
            else:
                failure_count += 1
        
        logger.info(
            f"Broadcast sent: {notification_type} | "
            f"Success: {success_count} | Failed: {failure_count}"
        )
        
        return {
            'success': True,
            'success_count': success_count,
            'failure_count': failure_count,
            'total': users.count()
        }
    
    def _get_user_preferences(self, user: User) -> UserPreferences:
        """Foydalanuvchi sozlamalarini olish"""
        prefs, created = UserPreferences.objects.get_or_create(user=user)
        return prefs
    
    def _get_user_phone(self, user: User) -> Optional[str]:
        """Foydalanuvchi telefon raqamini olish"""
        # Agar user modelida phone_number field bo'lsa
        if hasattr(user, 'phone_number') and user.phone_number:
            return user.phone_number
        
        # Agar profile modelida bo'lsa
        if hasattr(user, 'profile') and hasattr(user.profile, 'phone_number'):
            return user.profile.phone_number
        
        return None
    
    def _get_user_tokens(self, user: User) -> List[str]:
        """Foydalanuvchi device tokenlarini olish"""
        tokens = DeviceToken.objects.filter(
            user=user,
            is_active=True
        ).values_list('token', flat=True)
        
        return list(tokens)
    
    def _create_notification_log(
        self,
        user: User,
        notification_type: str,
        title: str,
        message: str,
        recipient: str,
        result: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Notification log yaratish"""
        try:
            from ..models import NotificationStatus
            
            log = NotificationLog.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                recipient=recipient,
                status=NotificationStatus.SENT if result.get('success') else NotificationStatus.FAILED,
                error_message=result.get('error', ''),
                metadata=metadata or {}
            )
            
            if result.get('success'):
                log.mark_as_delivered()
            
            return log
        
        except Exception as e:
            logger.error(f"Failed to create notification log: {e}")
            return None


# Singleton instance
notification_manager = NotificationManager()