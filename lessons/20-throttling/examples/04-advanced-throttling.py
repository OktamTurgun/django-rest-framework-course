# examples/04-advanced-throttling.py
"""
Advanced throttling: monitoring, custom responses, va best practices
"""

from rest_framework.throttling import SimpleRateThrottle, BaseThrottle
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import Throttled
from django.core.cache import cache
from django.utils import timezone
import logging
from datetime import datetime, timedelta


# Logger sozlash
logger = logging.getLogger(__name__)


# =============================================================================
# 1. Monitoring bilan throttle
# =============================================================================

class MonitoredThrottle(SimpleRateThrottle):
    """
    Barcha throttle eventlarini log qiluvchi throttle
    """
    scope = 'monitored'
    
    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        
        # Logging
        user = request.user if request.user.is_authenticated else 'anonymous'
        ip = self.get_ident(request)
        
        if not allowed:
            logger.warning(
                f'Throttled request: user={user}, ip={ip}, '
                f'view={view.__class__.__name__}, '
                f'path={request.path}'
            )
            
            # Metrics uchun cache ga yozish
            cache_key = f'throttle_violations_{datetime.now().date()}'
            violations = cache.get(cache_key, 0)
            cache.set(cache_key, violations + 1, 86400)  # 24 soat
        
        return allowed
    
    def wait(self):
        wait_time = super().wait()
        logger.info(f'Client must wait {wait_time} seconds')
        return wait_time


class MonitoredView(APIView):
    throttle_classes = [MonitoredThrottle]
    
    def get(self, request):
        return Response({'message': 'Monitoring bilan throttle'})


# =============================================================================
# 2. Custom Throttled Response
# =============================================================================

def custom_throttle_handler(exc, context):
    """
    Throttle exception uchun custom response
    """
    response = exception_handler(exc, context)
    
    if isinstance(exc, Throttled):
        wait_time = exc.wait
        
        custom_data = {
            'error': 'rate_limit_exceeded',
            'message': f'Juda ko\'p so\'rov. Iltimos {wait_time} soniya kuting.',
            'detail': {
                'retry_after': wait_time,
                'retry_at': (
                    timezone.now() + timedelta(seconds=wait_time)
                ).isoformat(),
                'current_time': timezone.now().isoformat(),
            },
            'tips': [
                'So\'rovlar orasida pauza qo\'ying',
                'Batch operatsiyalardan foydalaning',
                'Premium rejaga o\'ting'
            ]
        }
        
        response.data = custom_data
        
        # Custom headers
        response['X-RateLimit-Reset'] = int(
            (timezone.now() + timedelta(seconds=wait_time)).timestamp()
        )
        response['X-RateLimit-Remaining'] = '0'
    
    return response


# Settings.py da:
# REST_FRAMEWORK = {
#     'EXCEPTION_HANDLER': 'myapp.throttling.custom_throttle_handler'
# }


# =============================================================================
# 3. Dynamic rate limiting
# =============================================================================

class DynamicRateThrottle(SimpleRateThrottle):
    """
    Vaqt va yuklanishga qarab rate ni o'zgartiruvchi throttle
    """
    
    def get_rate(self):
        # Hozirgi soat
        current_hour = datetime.now().hour
        
        # Kun vaqti bo'yicha
        if 9 <= current_hour < 18:
            # Kunduzgi ish vaqti - yuqori yuklama
            base_rate = '100/hour'
        else:
            # Tun va dam olish kunlari - past yuklama
            base_rate = '500/hour'
        
        # Server yuklanishini tekshirish
        server_load = self.get_server_load()
        
        if server_load > 80:  # 80% dan yuqori
            return '50/hour'   # Keskin cheklash
        elif server_load > 60:
            return '100/hour'  # O'rtacha cheklash
        
        return base_rate
    
    def get_server_load(self):
        """
        Server yuklanishini olish (0-100)
        Real loyihada CPU, memory, va boshqa metrikalar tekshiriladi
        """
        # Bu yerda oddiy mock
        return cache.get('server_load', 30)
    
    def get_cache_key(self, request, view):
        user = request.user
        ident = user.pk if user.is_authenticated else self.get_ident(request)
        return f'dynamic_throttle_{ident}'


# =============================================================================
# 4. Quota-based throttling
# =============================================================================

class QuotaThrottle(BaseThrottle):
    """
    Oylik quota asosida throttling
    Har bir foydalanuvchi oyiga belgilangan miqdorda so'rov yuborishi mumkin
    """
    
    def allow_request(self, request, view):
        if not request.user.is_authenticated:
            return True  # Anonim foydalanuvchilar uchun boshqa throttle
        
        # Foydalanuvchi quota sini olish
        user = request.user
        monthly_quota = self.get_user_quota(user)
        
        # Shu oyda yuborilgan so'rovlar soni
        cache_key = self.get_cache_key(user)
        current_usage = cache.get(cache_key, 0)
        
        if current_usage >= monthly_quota:
            return False
        
        # So'rovlar sonini oshirish
        # Oyning oxirigacha saqlash
        days_until_month_end = self.days_until_month_end()
        timeout = days_until_month_end * 86400
        
        cache.set(cache_key, current_usage + 1, timeout)
        
        return True
    
    def get_cache_key(self, user):
        current_month = datetime.now().strftime('%Y-%m')
        return f'quota_{user.pk}_{current_month}'
    
    def get_user_quota(self, user):
        """
        Foydalanuvchi quota sini aniqlash
        """
        if user.is_staff:
            return 1000000  # Admin - cheksiz deyarli
        
        if hasattr(user, 'subscription'):
            subscription = user.subscription
            return subscription.monthly_quota
        
        return 1000  # Default - 1000 ta oyiga
    
    def days_until_month_end(self):
        now = datetime.now()
        next_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1)
        return (next_month - now).days
    
    def wait(self):
        # Keyingi oyning boshigacha kutish
        return self.days_until_month_end() * 86400


class QuotaView(APIView):
    throttle_classes = [QuotaThrottle]
    
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            cache_key = f'quota_{user.pk}_{datetime.now().strftime("%Y-%m")}'
            usage = cache.get(cache_key, 0)
            quota = QuotaThrottle().get_user_quota(user)
            
            return Response({
                'quota': {
                    'used': usage,
                    'total': quota,
                    'remaining': quota - usage,
                    'percentage': round((usage / quota) * 100, 2)
                }
            })
        
        return Response({'error': 'Authentication required'})


# =============================================================================
# 5. Throttle with warnings
# =============================================================================

class WarningThrottle(SimpleRateThrottle):
    """
    Limitga yaqinlashganda ogohlantirish beruvchi throttle
    """
    scope = 'warning'
    
    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        
        # Qolgan so'rovlar sonini hisoblash
        if hasattr(self, 'history'):
            total_requests = int(self.rate.split('/')[0])
            used_requests = len(self.history)
            remaining = total_requests - used_requests
            
            # Response ga header qo'shish
            request.META['X-RateLimit-Remaining'] = str(remaining)
            request.META['X-RateLimit-Limit'] = str(total_requests)
            
            # 80% dan oshsa ogohlantirish
            if remaining <= total_requests * 0.2:
                request.META['X-RateLimit-Warning'] = (
                    f'Limitingizning {remaining} ta so\'rovi qoldi'
                )
        
        return allowed


class WarningView(APIView):
    throttle_classes = [WarningThrottle]
    
    def get(self, request):
        response_data = {'message': 'OK'}
        
        # Warning headerlarini response ga qo'shish
        response = Response(response_data)
        
        if 'X-RateLimit-Remaining' in request.META:
            response['X-RateLimit-Remaining'] = request.META['X-RateLimit-Remaining']
            response['X-RateLimit-Limit'] = request.META['X-RateLimit-Limit']
        
        if 'X-RateLimit-Warning' in request.META:
            response['X-RateLimit-Warning'] = request.META['X-RateLimit-Warning']
            response_data['warning'] = request.META['X-RateLimit-Warning']
        
        return response


# =============================================================================
# 6. Graceful degradation throttle
# =============================================================================

class GracefulThrottle(BaseThrottle):
    """
    Cache ishlamasa ham xatolik bermaydigan throttle
    """
    
    def allow_request(self, request, view):
        try:
            # Oddiy throttle logikasi
            return self.check_throttle(request, view)
        except Exception as e:
            # Cache xatosi yoki boshqa muammo
            logger.error(f'Throttle error: {e}')
            
            # Xatolik bo'lsa, ruxsat berish (graceful degradation)
            return True
    
    def check_throttle(self, request, view):
        # Bu yerda oddiy throttle logikasi
        cache_key = self.get_cache_key(request)
        history = cache.get(cache_key, [])
        
        now = timezone.now().timestamp()
        
        # Eski so'rovlarni tozalash
        history = [h for h in history if h > now - 3600]  # 1 soat
        
        if len(history) >= 100:  # 100 ta so'rov/soat
            return False
        
        history.append(now)
        cache.set(cache_key, history, 3600)
        
        return True
    
    def get_cache_key(self, request):
        if request.user.is_authenticated:
            return f'graceful_throttle_{request.user.pk}'
        return f'graceful_throttle_{self.get_ident(request)}'
    
    def get_ident(self, request):
        return request.META.get('REMOTE_ADDR')
    
    def wait(self):
        return 3600


# =============================================================================
# 7. A/B Testing throttle
# =============================================================================

class ABTestingThrottle(SimpleRateThrottle):
    """
    A/B testing uchun throttle
    Foydalanuvchilarni guruhlarga bo'lib, turli limitlar qo'llash
    """
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            user_id = request.user.pk
            
            # Foydalanuvchini guruhga ajratish (A yoki B)
            group = 'A' if user_id % 2 == 0 else 'B'
            
            return f'ab_test_{group}_{user_id}'
        
        return None
    
    def get_rate(self):
        if not hasattr(self, 'request'):
            return '100/hour'
        
        user = self.request.user
        if not user.is_authenticated:
            return '100/hour'
        
        # Guruhga qarab rate
        group = 'A' if user.pk % 2 == 0 else 'B'
        
        if group == 'A':
            return '100/hour'  # Control group
        else:
            return '200/hour'  # Test group - yuqoriroq limit


# =============================================================================
# 8. Batch operation throttle
# =============================================================================

class BatchThrottle(BaseThrottle):
    """
    Batch operatsiyalar uchun maxsus throttle
    Ko'p elementli so'rovlar uchun ko'proq quota sarflaydi
    """
    
    def allow_request(self, request, view):
        # Batch hajmini aniqlash
        batch_size = self.get_batch_size(request)
        
        # Cache dan quota ni olish
        cache_key = self.get_cache_key(request)
        used_quota = cache.get(cache_key, 0)
        
        # Maksimal quota
        max_quota = 1000
        
        if used_quota + batch_size > max_quota:
            return False
        
        # Quotani yangilash
        cache.set(cache_key, used_quota + batch_size, 3600)
        
        return True
    
    def get_batch_size(self, request):
        """
        Batch hajmini aniqlash
        """
        if request.method == 'POST' and request.data:
            # Agar data list bo'lsa
            if isinstance(request.data, list):
                return len(request.data)
            
            # Agar data dict ichida 'items' bo'lsa
            if 'items' in request.data:
                items = request.data['items']
                if isinstance(items, list):
                    return len(items)
        
        return 1  # Oddiy so'rov
    
    def get_cache_key(self, request):
        if request.user.is_authenticated:
            return f'batch_throttle_{request.user.pk}'
        return f'batch_throttle_{self.get_ident(request)}'
    
    def get_ident(self, request):
        return request.META.get('REMOTE_ADDR')
    
    def wait(self):
        return 3600


class BatchAPIView(APIView):
    throttle_classes = [BatchThrottle]
    
    def post(self, request):
        items = request.data.get('items', [])
        
        return Response({
            'message': f'{len(items)} ta element qayta ishlandi',
            'batch_size': len(items)
        })


# =============================================================================
# Settings.py
# =============================================================================

"""
# settings.py

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.throttling.custom_throttle_handler',
    'DEFAULT_THROTTLE_RATES': {
        'monitored': '100/hour',
        'warning': '100/hour',
    }
}

# Cache configuration
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

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'throttle.log',
        },
    },
    'loggers': {
        'myapp.throttling': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
"""