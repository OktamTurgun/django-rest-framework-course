"""
SMS Service - Mock Implementation
==================================

Bu development uchun mock SMS service.
Console'ga xabar chop etadi, lekin hamma logic real.

Production'da bu kodni Twilio bilan almashtirishingiz mumkin.
"""

import logging
from typing import Optional, Dict
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


class MockSMSService:
    """
    Mock SMS Service - Development uchun
    
    Bu service real SMS yubormaydi, lekin:
    - Console'ga chop etadi
    - Log yaratadi
    - Success/error qaytaradi
    - Telefon raqamlarini validatsiya qiladi
    """
    
    def __init__(self):
        """Service'ni ishga tushirish"""
        self.backend = settings.SMS_BACKEND
        self.enabled = settings.NOTIFICATION_SETTINGS['SMS_ENABLED']
        
        if self.backend == 'mock':
            logger.info("📱 SMS Service initialized (MOCK MODE)")
        else:
            logger.warning("⚠️ SMS Backend configured but service is MOCK")
    
    def send_sms(self, phone_number: str, message: str, metadata: Dict = None) -> Dict:
        """
        SMS yuborish (MOCK)
        
        Args:
            phone_number: Qabul qiluvchi telefon raqami (+998901234567)
            message: SMS matni
            metadata: Qo'shimcha ma'lumotlar
            
        Returns:
            dict: {
                'success': bool,
                'message_id': str,
                'status': str,
                'error': str | None
            }
        """
        
        # SMS o'chirilgan bo'lsa
        if not self.enabled:
            logger.warning("SMS disabled in settings")
            return {
                'success': False,
                'message_id': None,
                'status': 'disabled',
                'error': 'SMS notifications are disabled'
            }
        
        # Telefon raqamini validatsiya qilish
        if not self._validate_phone(phone_number):
            logger.error(f"Invalid phone number: {phone_number}")
            return {
                'success': False,
                'message_id': None,
                'status': 'invalid_phone',
                'error': 'Invalid phone number format'
            }
        
        # Mock SMS ID yaratish
        message_id = f"MOCK_SMS_{datetime.now().timestamp()}"
        
        # Console'ga chop etish (Mock)
        self._print_mock_sms(phone_number, message, message_id)
        
        # Log yaratish
        logger.info(f"Mock SMS sent to {phone_number}: {message[:50]}...")
        
        # Success qaytarish
        return {
            'success': True,
            'message_id': message_id,
            'status': 'sent',
            'error': None,
            'metadata': metadata or {}
        }
    
    def _validate_phone(self, phone_number: str) -> bool:
        """
        Telefon raqamini validatsiya qilish
        
        Format: +998901234567 (E.164)
        """
        if not phone_number:
            return False
        
        # Oddiy validatsiya
        if not phone_number.startswith('+'):
            return False
        
        # Faqat raqamlar (+ dan keyin)
        digits = phone_number[1:]
        if not digits.isdigit():
            return False
        
        # Uzunlik tekshiruvi (10-15 raqam)
        if len(digits) < 10 or len(digits) > 15:
            return False
        
        return True
    
    def _print_mock_sms(self, phone_number: str, message: str, message_id: str):
        """Console'ga mock SMS chop etish"""
        
        border = "━" * 50
        
        print(f"\n{border}")
        print(f"📱 SMS MOCK (Development Mode)")
        print(f"{border}")
        print(f"To:      {phone_number}")
        print(f"Message: {message}")
        print(f"ID:      {message_id}")
        print(f"Time:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Status:  ✓ Sent (MOCK)")
        print(f"{border}\n")
    
    def get_status(self, message_id: str) -> Dict:
        """
        SMS holatini olish (MOCK)
        
        Mock mode'da har doim 'delivered' qaytaradi
        """
        return {
            'message_id': message_id,
            'status': 'delivered',
            'timestamp': datetime.now().isoformat()
        }


# Service instance yaratish
sms_service = MockSMSService()