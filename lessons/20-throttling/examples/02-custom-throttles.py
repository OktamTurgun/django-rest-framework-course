# examples/02-custom-throttles.py
"""
Custom throttle klasslarini yaratish
"""

from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
import random
import time
from datetime import datetime, timedelta


# =============================================================================
# 1. Oddiy custom throttle
# =============================================================================

class RandomThrottle(BaseThrottle):
    """
    Tasodifiy throttle - test uchun
    50% ehtimollik bilan ruxsat beradi
    """
    
    def allow_request(self, request, view):
        """
        True - ruxsat beriladi
        False - bloklangan
        """
        return random.choice([True, False])
    
    def wait(self):
        """
        Keyingi so'rov uchun kutish vaqti (sekundlarda)
        Faqat allow_request False qaytarganda chaqiriladi
        """
        return 60  # 1 daqiqa kutish


class RandomThrottleView(APIView):
    throttle_classes = [RandomThrottle]
    
    def get(self, request):
        return Response({'message': 'Tasodifiy throttle - omad kuning bilan!'})


# =============================================================================
# 2. Time-based throttle
# =============================================================================

class TimeBasedThrottle(BaseThrottle):
    """
    Vaqt asosida throttling - faqat ish vaqtida ruxsat beradi
    """
    
    def allow_request(self, request, view):
        # Faqat 9:00 dan 18:00 gacha ruxsat
        current_hour = datetime.now().hour
        
        if 9 <= current_hour < 18:
            return True
        
        return False
    
    def wait(self):
        # Ertasi kuni 9:00 gacha kutish
        now = datetime.now()
        tomorrow_9am = (now + timedelta(days=1)).replace(
            hour=9, minute=0, second=0, microsecond=0
        )
        return (tomorrow_9am - now).total_seconds()


class BusinessHoursView(APIView):
    throttle_classes = [TimeBasedThrottle]
    
    def get(self, request):
        return Response({
            'message': 'Ish vaqtida xizmat',
            'time': datetime.now().strftime('%H:%M')
        })


# =============================================================================
# 3. IP-based custom throttle
# =============================================================================

class IPRateThrottle(SimpleRateThrottle):
    """
    IP manzil bo'yicha throttling
    """
    scope = 'ip_limit'
    
    def get_cache_key(self, request, view):
        """
        Cache kalit yaratish - IP manzil asosida
        """
        ident = self.get_ident(request)  # IP manzilni oladi
        return f'throttle_ip_{ident}'


class IPThrottleView(APIView):
    throttle_classes = [IPRateThrottle]
    
    def get(self, request):
        return Response({
            'ip': self.request.META.get('REMOTE_ADDR'),
            'message': 'IP bo\'yicha throttling'
        })


# =============================================================================
# 4. User role based throttle
# =============================================================================

class RoleBasedThrottle(SimpleRateThrottle):
    """
    Foydalanuvchi roli bo'yicha throttling
    """
    
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None  # Throttle qo'llanmaydi
        
        return f'throttle_user_{request.user.id}'
    
    def get_rate(self):
        """
        Rol bo'yicha rate ni qaytaradi
        """
        user = self.request.user
        
        if not user.is_authenticated:
            return None
        
        # Admin - cheksiz
        if user.is_staff:
            return None
        
        # Premium foydalanuvchi
        if hasattr(user, 'is_premium') and user.is_premium:
            return '10000/day'
        
        # Oddiy foydalanuvchi
        return '100/day'


class RoleBasedView(APIView):
    throttle_classes = [RoleBasedThrottle]
    
    def get(self, request):
        user_type = 'anonymous'
        if request.user.is_authenticated:
            if request.user.is_staff:
                user_type = 'admin'
            elif hasattr(request.user, 'is_premium') and request.user.is_premium:
                user_type = 'premium'
            else:
                user_type = 'regular'
        
        return Response({
            'user': str(request.user),
            'type': user_type,
            'message': 'Rol bo\'yicha throttling'
        })


# =============================================================================
# 5. API Key based throttle
# =============================================================================

class APIKeyThrottle(SimpleRateThrottle):
    """
    API key bo'yicha throttling
    """
    scope = 'api_key'
    
    def get_cache_key(self, request, view):
        # API key ni header dan olish
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            # API key yo'q bo'lsa, IP bo'yicha
            return f'throttle_nokey_{self.get_ident(request)}'
        
        return f'throttle_key_{api_key}'
    
    def get_rate(self):
        # API key bor foydalanuvchilar uchun yuqori limit
        api_key = self.request.META.get('HTTP_X_API_KEY')
        
        if api_key:
            return '1000/hour'
        else:
            return '10/hour'


class APIKeyView(APIView):
    throttle_classes = [APIKeyThrottle]
    
    def get(self, request):
        api_key = request.META.get('HTTP_X_API_KEY', 'None')
        return Response({
            'api_key': api_key[:8] + '...' if api_key != 'None' else 'None',
            'message': 'API key bo\'yicha throttling'
        })


# =============================================================================
# 6. Burst throttle (qisqa vaqt ichida ko'p so'rov)
# =============================================================================

class BurstThrottle(SimpleRateThrottle):
    """
    Qisqa vaqt ichida ko'p so'rovni oldini oladi
    Masalan: 1 minutda 10 tadan ortiq so'rov bo'lmasligi kerak
    """
    scope = 'burst'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return f'throttle_burst_{ident}'


class SustainedThrottle(SimpleRateThrottle):
    """
    Uzoq muddatli limit
    Masalan: 1 kunda 1000 ta so'rov
    """
    scope = 'sustained'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return f'throttle_sustained_{ident}'


class CombinedThrottleView(APIView):
    """
    Burst va sustained throttle ni birga ishlatish
    """
    throttle_classes = [BurstThrottle, SustainedThrottle]
    
    def get(self, request):
        return Response({
            'message': 'Kombinatsiyalangan throttling',
            'burst': '10/min',
            'sustained': '1000/day'
        })


# =============================================================================
# 7. Request method based throttle
# =============================================================================

class MethodBasedThrottle(SimpleRateThrottle):
    """
    HTTP metod bo'yicha throttling
    """
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return f'throttle_{request.method.lower()}_{ident}'
    
    def get_rate(self):
        """
        Metod bo'yicha rate ni qaytaradi
        """
        if self.request.method == 'GET':
            return '1000/hour'  # O'qish uchun yuqori
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            return '100/hour'   # Yozish uchun past
        elif self.request.method == 'DELETE':
            return '10/hour'    # O'chirish uchun juda past
        
        return '100/hour'  # Default


class MethodThrottleView(APIView):
    throttle_classes = [MethodBasedThrottle]
    
    def get(self, request):
        return Response({'method': 'GET', 'limit': '1000/hour'})
    
    def post(self, request):
        return Response({'method': 'POST', 'limit': '100/hour'})
    
    def delete(self, request):
        return Response({'method': 'DELETE', 'limit': '10/hour'})


# =============================================================================
# Settings.py da sozlamalar
# =============================================================================

SETTINGS_EXAMPLE = """
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'ip_limit': '100/hour',
        'api_key': '10/hour',
        'burst': '10/min',
        'sustained': '1000/day',
    }
}

# Cache backend (development uchun)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Production uchun Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
"""