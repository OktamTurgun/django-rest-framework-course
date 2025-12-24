"""
Firebase Push Notification Service
===================================

Real Firebase Cloud Messaging (FCM) implementation.
Bu service haqiqiy push notifications yuboradi.

MOCK MODE: Development uchun mock mode qo'llab-quvvatlanadi.
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


class FirebasePushService:
    """
    Firebase Cloud Messaging Service
    
    Real push notifications yuboradi:
    - Single device
    - Multiple devices
    - Topics
    
    Mock mode: Development/testing uchun
    """
    
    def __init__(self):
        """Firebase'ni ishga tushirish"""
        self.enabled = settings.NOTIFICATION_SETTINGS.get('PUSH_ENABLED', True)
        self.mock_mode = settings.NOTIFICATION_SETTINGS.get('MOCK_MODE', False)
        
        if self.mock_mode:
            logger.info("📱 Push Service initialized (MOCK MODE)")
            return
        
        # Real Firebase initialization
        import firebase_admin
        from firebase_admin import credentials
        
        # Firebase allaqachon initialize qilinganmi?
        if not firebase_admin._apps:
            try:
                cred_path = settings.FIREBASE_CREDENTIALS_PATH
                cred = credentials.Certificate(str(cred_path))
                firebase_admin.initialize_app(cred)
                logger.info("🔥 Firebase initialized successfully")
            except Exception as e:
                logger.error(f"Firebase initialization failed: {str(e)}")
                self.enabled = False
        else:
            logger.info("🔥 Firebase already initialized")
    
    def send_push(
        self, 
        token: str, 
        title: str, 
        body: str, 
        data: Dict = None
    ) -> Dict:
        """
        Bitta qurilmaga push yuborish
        
        Args:
            token: FCM device token
            title: Notification sarlavhasi
            body: Notification matni
            data: Qo'shimcha ma'lumotlar
            
        Returns:
            dict: {
                'success': bool,
                'message_id': str,
                'error': str | None
            }
        """
        
        if not self.enabled:
            logger.warning("Push notifications disabled")
            return {
                'success': False,
                'message_id': None,
                'error': 'Push notifications are disabled'
            }
        
        # MOCK MODE
        if self.mock_mode:
            return self._mock_send(token, title, body, data)
        
        # Real Firebase send
        try:
            from firebase_admin import messaging
            
            # Message yaratish
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=token
            )
            
            # Yuborish
            response = messaging.send(message)
            
            logger.info(f"Push sent successfully: {response}")
            
            return {
                'success': True,
                'message_id': response,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Push send failed: {str(e)}")
            return {
                'success': False,
                'message_id': None,
                'error': str(e)
            }
    
    def _mock_send(self, token: str, title: str, body: str, data: Dict = None) -> Dict:
        """Mock push notification yuborish"""
        message_id = f"MOCK_PUSH_{datetime.now().timestamp()}"
        
        # Console'ga chop etish
        border = "━" * 50
        print(f"\n{border}")
        print(f"🔔 PUSH NOTIFICATION MOCK (Development Mode)")
        print(f"{border}")
        print(f"Token:   {token[:30]}...")
        print(f"Title:   {title}")
        print(f"Body:    {body}")
        print(f"Data:    {data}")
        print(f"ID:      {message_id}")
        print(f"Time:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Status:  ✓ Sent (MOCK)")
        print(f"{border}\n")
        
        logger.info(f"Mock Push sent: {title}")
        
        return {
            'success': True,
            'message_id': message_id,
            'error': None
        }
    
    def send_to_multiple(
        self, 
        tokens: List[str], 
        title: str, 
        body: str, 
        data: Dict = None
    ) -> Dict:
        """
        Ko'p qurilmalarga push yuborish
        
        Args:
            tokens: FCM token ro'yxati
            title: Notification sarlavhasi
            body: Notification matni
            data: Qo'shimcha ma'lumotlar
            
        Returns:
            dict: {
                'success_count': int,
                'failure_count': int,
                'failed_tokens': list
            }
        """
        
        if not self.enabled:
            return {
                'success_count': 0,
                'failure_count': len(tokens),
                'failed_tokens': tokens
            }
        
        # MOCK MODE
        if self.mock_mode:
            message_id = f"MOCK_PUSH_MULTI_{datetime.now().timestamp()}"
            border = "━" * 50
            print(f"\n{border}")
            print(f"🔔 MULTICAST PUSH MOCK (Development Mode)")
            print(f"{border}")
            print(f"Tokens:  {len(tokens)} devices")
            print(f"Title:   {title}")
            print(f"Body:    {body}")
            print(f"Data:    {data}")
            print(f"ID:      {message_id}")
            print(f"Status:  ✓ All Sent (MOCK)")
            print(f"{border}\n")
            
            return {
                'success': True,
                'success_count': len(tokens),
                'failure_count': 0,
                'failed_tokens': [],
                'message_id': message_id
            }
        
        try:
            from firebase_admin import messaging
            
            # Multicast message
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                tokens=tokens
            )
            
            # Yuborish
            response = messaging.send_multicast(message)
            
            # Failed tokenlarni aniqlash
            failed_tokens = []
            if response.failure_count > 0:
                for idx, resp in enumerate(response.responses):
                    if not resp.success:
                        failed_tokens.append(tokens[idx])
            
            logger.info(
                f"Multicast: {response.success_count} success, "
                f"{response.failure_count} failed"
            )
            
            return {
                'success': True,
                'success_count': response.success_count,
                'failure_count': response.failure_count,
                'failed_tokens': failed_tokens
            }
            
        except Exception as e:
            logger.error(f"Multicast send failed: {str(e)}")
            return {
                'success': False,
                'success_count': 0,
                'failure_count': len(tokens),
                'failed_tokens': tokens
            }
    
    def send_to_topic(
        self, 
        topic: str, 
        title: str, 
        body: str, 
        data: Dict = None
    ) -> Dict:
        """
        Mavzuga push yuborish
        
        Args:
            topic: Mavzu nomi
            title: Notification sarlavhasi
            body: Notification matni
            data: Qo'shimcha ma'lumotlar
        """
        
        if not self.enabled:
            return {
                'success': False,
                'message_id': None,
                'error': 'Push notifications are disabled'
            }
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                topic=topic
            )
            
            response = messaging.send(message)
            
            logger.info(f"Topic message sent: {response}")
            
            return {
                'success': True,
                'message_id': response,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Topic send failed: {str(e)}")
            return {
                'success': False,
                'message_id': None,
                'error': str(e)
            }


# Service instance yaratish
push_service = FirebasePushService()