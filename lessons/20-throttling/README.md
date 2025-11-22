# 20-dars: Throttling (So'rovlar cheklash)

## Mavzu: DRF da so'rovlarni cheklash

### Darsning maqsadi
Ushbu darsda Django REST Framework da throttling tizimini o'rganamiz - bu API ga yuborilayotgan so'rovlar sonini cheklash mexanizmi.

## Nazariy qism

### Throttling nima?

Throttling - bu API ga muayyan vaqt oralig'ida yuborilishi mumkin bo'lgan so'rovlar sonini cheklash mexanizmi. Bu quyidagi maqsadlarda ishlatiladi:

**Asosiy maqsadlar:**
1.  **DDoS hujumlaridan himoya** - zararli so'rovlarni bloklash
2.  **Resurslarni boshqarish** - server yuklamasini kamaytirish
3.  **Biznes modeli** - turli xil foydalanuvchi darajalari uchun limitlar
4.  **Adolatli foydalanish** - barcha foydalanuvchilar uchun teng imkoniyat

### DRF da built-in throttle klasslari

#### 1. AnonRateThrottle
Autentifikatsiya qilinmagan foydalanuvchilar uchun:
```python
from rest_framework.throttling import AnonRateThrottle

class MyView(APIView):
    throttle_classes = [AnonRateThrottle]
```

**Xususiyatlari:**
- IP manzil bo'yicha identifikatsiya qiladi
- Cache da ma'lumotlarni saqlaydi
- Faqat anonim foydalanuvchilar uchun

#### 2. UserRateThrottle
Autentifikatsiya qilingan foydalanuvchilar uchun:
```python
from rest_framework.throttling import UserRateThrottle

class MyView(APIView):
    throttle_classes = [UserRateThrottle]
```

**Xususiyatlari:**
- User ID bo'yicha identifikatsiya
- Har bir foydalanuvchi uchun alohida limit
- Autentifikatsiya talab qilinadi

#### 3. ScopedRateThrottle
Har xil endpoint lar uchun turli limitlar:
```python
from rest_framework.throttling import ScopedRateThrottle

class ContactView(APIView):
    throttle_scope = 'contacts'
    throttle_classes = [ScopedRateThrottle]
```

### Throttle sozlamalari

#### Settings.py da konfiguratsiya:
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',      # Anonim: 100 ta so'rov kuniga
        'user': '1000/day',     # User: 1000 ta so'rov kuniga
        'burst': '60/min',      # Burst: 60 ta so'rov minutiga
        'sustained': '1000/day' # Sustained: 1000 ta kuniga
    }
}
```

#### Rate formatlar:
- `'5/second'` - sekundiga 5 ta
- `'100/minute'` - minutiga 100 ta
- `'1000/hour'` - soatiga 1000 ta
- `'10000/day'` - kuniga 10000 ta

### Custom Throttle yaratish

```python
from rest_framework.throttling import BaseThrottle
import random

class RandomRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        # 50% ehtimollik bilan ruxsat berish
        return random.randint(1, 10) > 5
    
    def wait(self):
        # Keyingi so'rov uchun kutish vaqti (sekundlarda)
        return 60
```

### Cache backend sozlash

Throttling cache ishlatadi, shuning uchun cache sozlanishi kerak:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

**Production uchun Redis:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## Amaliy qism

### 1. View darajasida throttling

```python
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response

class PostListView(APIView):
    throttle_classes = [UserRateThrottle]
    
    def get(self, request):
        return Response({'posts': []})
```

### 2. Bir nechta throttle

```python
class ImportantView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # Ikkala throttle ham tekshiriladi
```

### 3. ViewSet da throttling

```python
from rest_framework import viewsets

class ProductViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
    
    def get_throttles(self):
        if self.action == 'create':
            # Yaratish uchun qattiqroq limit
            return [AnonRateThrottle()]
        return super().get_throttles()
```

### 4. Turli action lar uchun turli limitlar

```python
class PostViewSet(viewsets.ModelViewSet):
    throttle_scope = 'posts'
    
    def get_throttles(self):
        if self.action in ['list', 'retrieve']:
            # O'qish uchun yuqori limit
            throttle_classes = [UserRateThrottle]
        elif self.action in ['create', 'update', 'destroy']:
            # Yozish uchun past limit
            throttle_classes = [AnonRateThrottle]
        else:
            throttle_classes = []
        
        return [throttle() for throttle in throttle_classes]
```

## Throttle headers

DRF avtomatik ravishda throttle haqida ma'lumot beruvchi headerlar qo'shadi:

```http
HTTP 429 Too Many Requests
Retry-After: 86400
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000000
```

## Throttle exception handling

```python
from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, Throttled):
        custom_response_data = {
            'error': 'Too many requests',
            'message': f'Iltimos {exc.wait} soniya kuting',
            'available_in': exc.wait
        }
        response.data = custom_response_data
    
    return response
```

Settings.py da:
```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler'
}
```

## Best Practices

### 1. ✅ Moslashuvchan limitlar
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/min',        # Anonim - qattiq
        'user': '100/min',       # Oddiy user - o'rtacha
        'premium': '1000/min',   # Premium - yuqori
    }
}
```

### 2. ✅ Turli endpoint lar uchun turli limitlar
```python
class UploadView(APIView):
    throttle_scope = 'uploads'  # Past limit
    
class SearchView(APIView):
    throttle_scope = 'searches'  # Yuqori limit
```

### 3. ✅ Monitoring va logging
```python
import logging

logger = logging.getLogger(__name__)

class MonitoredThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        if not allowed:
            logger.warning(
                f'Throttled request from {request.user} '
                f'to {view.__class__.__name__}'
            )
        return allowed
```

### 4. ✅ Graceful degradation
```python
class OptionalThrottle(BaseThrottle):
    def allow_request(self, request, view):
        try:
            # Cache ishlamasa ham davom etadi
            return self.check_throttle(request, view)
        except Exception as e:
            logger.error(f'Throttle error: {e}')
            return True  # Xatolik bo'lsa ruxsat beradi
```

## Xatolar va ularni tuzatish

### ❌ Xato: Cache sozlanmagan
```python
# Xato: Cache backend yo'q
ImproperlyConfigured: Could not find config for 'default' in settings.CACHES
```

**✅ Yechim:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### ❌ Xato: Noto'g'ri rate format
```python
# Xato
'DEFAULT_THROTTLE_RATES': {
    'user': '1000'  # ❌ Noto'g'ri format
}
```

**✅ Yechim:**
```python
'DEFAULT_THROTTLE_RATES': {
    'user': '1000/day'  # ✅ To'g'ri format
}
```

## Test qilish

```python
from rest_framework.test import APITestCase
from rest_framework import status

class ThrottleTests(APITestCase):
    def test_throttle_anon_user(self):
        # 10 ta so'rov yuborish
        for i in range(10):
            response = self.client.get('/api/posts/')
            if i < 9:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
            else:
                # 10-so'rov bloklangan bo'lishi kerak
                self.assertEqual(
                    response.status_code, 
                    status.HTTP_429_TOO_MANY_REQUESTS
                )
```

## Real-world misollar

### 1. Freemium model
```python
class FreemiumThrottle(UserRateThrottle):
    def get_rate(self):
        user = self.request.user
        if user.is_premium:
            return '10000/day'
        return '100/day'
```

### 2. IP-based limiting
```python
class IPThrottle(BaseThrottle):
    def get_cache_key(self, request, view):
        return f'throttle_ip_{request.META.get("REMOTE_ADDR")}'
```

### 3. Action-based limiting
```python
class WriteThrottle(UserRateThrottle):
    scope = 'writes'
    
    def allow_request(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return super().allow_request(request, view)
        return True  # GET, OPTIONS uchun limitlar yo'q
```

## Xulosa

Throttling DRF ning muhim xususiyati bo'lib:

✅ **Afzalliklar:**
- API ni himoya qiladi
- Resurslarni tejaydi
- Biznes modeli yaratishga yordam beradi
- Oson sozlanadi

⚠️ **E'tiborli bo'lish kerak:**
- Cache to'g'ri sozlangan bo'lishi kerak
- Limitlar real yuklamaga moslangan bo'lishi kerak
- Monitoring sozlash muhim
- Test qilishni unutmang

## Keyingi dars
21-darsda **Versioning** (API versiyalash) mavzusini o'rganamiz.

## Qo'shimcha resurslar
- [DRF Throttling Documentation](https://www.django-rest-framework.org/api-guide/throttling/)
- [Rate Limiting Strategies](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)
- [Redis for Django](https://github.com/jazzband/django-redis)