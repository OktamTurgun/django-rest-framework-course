# Throttling Examples - Ko'rsatmalar

Bu papkada DRF Throttling ga oid amaliy misollar joylashgan.

## Fayllar tuzilishi

### 1. `01-built-in-throttles.py`
**Mavzu:** DRF da built-in throttle klasslaridan foydalanish

**O'rganiladi:**
- `AnonRateThrottle` - Anonim foydalanuvchilar uchun
- `UserRateThrottle` - Autentifikatsiya qilingan foydalanuvchilar
- `ScopedRateThrottle` - Turli endpoint lar uchun turli limitlar
- ViewSet larda throttling
- Bir nechta throttle ni birga ishlatish

**Asosiy misollar:**
```python
# Oddiy throttle
class PublicAPIView(APIView):
    throttle_classes = [AnonRateThrottle]

# Bir nechta throttle
class MixedAPIView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

# Scoped throttle
class ContactAPIView(APIView):
    throttle_scope = 'contacts'
    throttle_classes = [ScopedRateThrottle]
```

---

### 2. `02-custom-throttles.py`
**Mavzu:** Custom throttle klasslarini yaratish

**O'rganiladi:**
- `BaseThrottle` dan meros olish
- `SimpleRateThrottle` ni kengaytirish
- IP-based throttling
- User role based throttling
- API key throttling
- Burst va sustained throttling
- Method-based throttling

**Asosiy misollar:**
```python
# Oddiy custom throttle
class RandomThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return random.choice([True, False])
    
    def wait(self):
        return 60

# Role-based throttle
class RoleBasedThrottle(SimpleRateThrottle):
    def get_rate(self):
        if user.is_staff:
            return None  # Cheksiz
        if user.is_premium:
            return '10000/day'
        return '100/day'
```

---

### 3. `03-scope-throttles.py`
**Mavzu:** ScopedRateThrottle bilan chuqur ishlash

**O'rganiladi:**
- Turli operatsiyalar uchun turli scope lar
- File operations throttling
- API operations throttling
- ViewSet da scope ishlatish
- Custom action larda scope
- Multi-scope views

**Asosiy misollar:**
```python
# File upload - past limit
class FileUploadView(APIView):
    throttle_scope = 'uploads'  # 5/hour

# File download - yuqori limit
class FileDownloadView(APIView):
    throttle_scope = 'downloads'  # 50/hour

# Dynamic scope
class DynamicScopeView(APIView):
    def get_throttles(self):
        if self.request.method == 'GET':
            self.throttle_scope = 'read_operations'
        else:
            self.throttle_scope = 'write_operations'
        return super().get_throttles()
```

---

### 4. `04-advanced-throttling.py`
**Mavzu:** Advanced throttling strategiyalari

**O'rganiladi:**
- Monitoring bilan throttle
- Custom throttled response
- Dynamic rate limiting
- Quota-based throttling
- Throttle with warnings
- Graceful degradation
- A/B testing throttle
- Batch operation throttle

**Asosiy misollar:**
```python
# Monitoring
class MonitoredThrottle(SimpleRateThrottle):
    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        if not allowed:
            logger.warning(f'Throttled: {request.user}')
        return allowed

# Quota-based
class QuotaThrottle(BaseThrottle):
    def allow_request(self, request, view):
        monthly_quota = self.get_user_quota(user)
        current_usage = cache.get(cache_key, 0)
        return current_usage < monthly_quota

# Dynamic rate
class DynamicRateThrottle(SimpleRateThrottle):
    def get_rate(self):
        server_load = self.get_server_load()
        if server_load > 80:
            return '50/hour'  # Qattiq cheklash
        return '500/hour'  # Normal
```

---

## Fayllarni ishlatish

### 1. Loyihangizga nusxalash
```bash
# Kerakli faylni nusxalash
cp examples/01-built-in-throttles.py myproject/myapp/throttling.py
```

### 2. Settings.py sozlash
```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        # Qo'shimcha scope lar
        'contacts': '3/day',
        'uploads': '5/hour',
        'downloads': '50/hour',
    }
}

# Cache backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### 3. URLs.py da marshrutlash
```python
# urls.py

from django.urls import path
from myapp import views

urlpatterns = [
    path('api/public/', views.PublicAPIView.as_view()),
    path('api/contact/', views.ContactFormView.as_view()),
    path('api/upload/', views.FileUploadView.as_view()),
]
```

### 4. Ishga tushirish
```bash
# Migratsiyalar
python manage.py migrate

# Server ishga tushirish
python manage.py runserver

# Test qilish
curl http://localhost:8000/api/public/
```

---

## Test qilish

### 1. Oddiy test
```bash
# 10 marta so'rov yuborish
for i in {1..10}; do
    curl http://localhost:8000/api/public/
    echo ""
done
```

### 2. Throttle limit tekshirish
```python
# test_throttling.py

from rest_framework.test import APITestCase
from rest_framework import status

class ThrottleTest(APITestCase):
    def test_anon_throttle(self):
        # 100 ta so'rov yuborish
        for i in range(100):
            response = self.client.get('/api/public/')
            if i < 99:
                self.assertEqual(response.status_code, 200)
            else:
                # 100-so'rov bloklangan
                self.assertEqual(
                    response.status_code, 
                    status.HTTP_429_TOO_MANY_REQUESTS
                )
```

### 3. Headers tekshirish
```bash
# Throttle headers ni ko'rish
curl -I http://localhost:8000/api/public/

# Output:
# X-RateLimit-Limit: 100
# X-RateLimit-Remaining: 99
# X-RateLimit-Reset: 1640000000
```

---

## Kengaytirish

### 1. Redis ishlatish (Production)
```python
# settings.py

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

### 2. Custom exception handler
```python
# throttling.py

def custom_throttle_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, Throttled):
        custom_data = {
            'error': 'Too many requests',
            'retry_after': exc.wait,
            'message': f'Iltimos {exc.wait} soniya kuting'
        }
        response.data = custom_data
    
    return response
```

### 3. Monitoring qo'shish
```python
# throttling.py

import logging

logger = logging.getLogger(__name__)

class MonitoredThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        
        if not allowed:
            logger.warning(
                f'Throttled: {request.user} - {view.__class__.__name__}'
            )
        
        return allowed
```

---

## Best Practices

### ✅ To'g'ri yondashuv

1. **Moslashuvchan limitlar:**
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/min',        # Qattiq
        'user': '100/min',       # O'rtacha
        'premium': '1000/min',   # Yuqori
    }
}
```

2. **Turli operatsiyalar uchun turli limitlar:**
```python
class APIView(APIView):
    def get_throttles(self):
        if self.action in ['create', 'update', 'destroy']:
            return [AnonRateThrottle()]  # Past limit
        return [UserRateThrottle()]      # Yuqori limit
```

3. **Graceful error handling:**
```python
def allow_request(self, request, view):
    try:
        return super().allow_request(request, view)
    except Exception as e:
        logger.error(f'Throttle error: {e}')
        return True  # Xatolik bo'lsa ruxsat berish
```

### ❌ Xatolar

1. **Cache sozlanmagan:**
```python
# ❌ Xato: Cache yo'q
# Throttling ishlamaydi

# ✅ To'g'ri:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

2. **Noto'g'ri rate format:**
```python
# ❌ Xato
'DEFAULT_THROTTLE_RATES': {
    'user': '1000'  # Format noto'g'ri
}

# ✅ To'g'ri
'DEFAULT_THROTTLE_RATES': {
    'user': '1000/day'  # To'g'ri format
}
```

3. **Throttle testing qilinmagan:**
```python
# ❌ Xato: Test yo'q

# ✅ To'g'ri: Har doim test yozing
def test_throttle_limit(self):
    for i in range(101):
        response = self.client.get('/api/endpoint/')
        if i == 100:
            self.assertEqual(response.status_code, 429)
```

---

## Savol-javoblar

### Q: Throttling ishlamayapti, nima qilish kerak?
**A:** 
1. Cache sozlanganligini tekshiring
2. Throttle class to'g'ri import qilinganligini tekshiring
3. Settings.py da rate lar to'g'ri sozlanganligini tekshiring

### Q: Turli foydalanuvchilar uchun turli limitlar qo'yish mumkinmi?
**A:** Ha! Custom throttle yarating:
```python
class CustomThrottle(SimpleRateThrottle):
    def get_rate(self):
        if request.user.is_premium:
            return '10000/day'
        return '100/day'
```

### Q: Production da qanday cache ishlatish kerak?
**A:** Redis tavsiya etiladi:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

---

## Qo'shimcha resurslar

-  [DRF Documentation](https://www.django-rest-framework.org/api-guide/throttling/)
-  [Video tutorial](https://www.youtube.com/results?search_query=drf+throttling)
-  [Blog posts](https://blog.logrocket.com/rate-limiting-django-rest-framework/)

---

**Muvaffaqiyatlar tilayman!**