from rest_framework.throttling import SimpleRateThrottle, BaseThrottle
from django.core.cache import cache
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MembershipThrottle(SimpleRateThrottle):
    """
    Foydalanuvchi membership darajasiga qarab throttling
    """
    # Default scope qo'shamiz
    scope = 'membership'
    
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        
        return f'membership_throttle_{request.user.pk}'
    
    def allow_request(self, request, view):
        """
        Bu yerda request mavjud bo'ladi
        """
        # Request ni saqlaymiz
        self.request = request
        
        # Rate ni olish
        self.rate = self.get_rate()
        if self.rate is None:
            return True  # Throttle yo'q (admin uchun)
        
        # Parent method ni chaqirish
        return super().allow_request(request, view)
    
    def get_rate(self):
        """
        Membership darajasiga qarab limit
        """
        # Agar request hali yo'q bo'lsa (initialization paytida)
        if not hasattr(self, 'request'):
            return '100/hour'  # Default
        
        user = self.request.user
        
        if not user.is_authenticated:
            return None
        
        # Admin - cheksiz
        if user.is_staff:
            return None
        
        # Premium member (Books app uses books_profile related_name)
        books_profile = getattr(user, 'books_profile', None)
        if books_profile and getattr(books_profile, 'is_premium', False):
            return '1000/hour'
        
        # Oddiy user
        return '100/hour'


class BorrowThrottle(SimpleRateThrottle):
    """
    Kitob olish uchun maxsus throttle
    Kuniga 5 tadan ko'p kitob olib bo'lmaydi
    """
    scope = 'borrow'
    
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        
        # Kunlik limit uchun
        today = datetime.now().strftime('%Y-%m-%d')
        return f'borrow_throttle_{request.user.pk}_{today}'
    
    def get_rate(self):
        return '5/day'


class MonitoredBookThrottle(SimpleRateThrottle):
    """
    Kitoblar uchun monitoring bilan throttle
    """
    scope = 'monitored_books'
    
    def get_cache_key(self, request, view):
        # User authenticated bo'lsa - user ID
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            # Aks holda - IP address
            ident = self.get_ident(request)
        
        return f'throttle_monitored_books_{ident}'
    
    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        
        if not allowed:
            # Log yozish
            logger.warning(
                f'Book throttled: user={request.user}, '
                f'path={request.path}, '
                f'method={request.method}'
            )
            
            # Metrics
            cache_key = f'book_throttle_violations_{datetime.now().date()}'
            violations = cache.get(cache_key, 0)
            cache.set(cache_key, violations + 1, 86400)
        
        return allowed
    
    def get_rate(self):
        return '100/hour'


class SearchThrottle(SimpleRateThrottle):
    """
    Qidiruv uchun alohida throttle
    """
    scope = 'search'
    
    def get_cache_key(self, request, view):
        # IP bo'yicha (anonim va user uchun)
        ident = self.get_ident(request)
        return f'search_throttle_{ident}'