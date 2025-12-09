# Lesson 25: CORS (Cross-Origin Resource Sharing)

##  Dars Maqsadi
Django REST Framework'da CORS'ni tushunish, sozlash va xavfsiz tarzda ishlatishni o'rganish.

##  Mavzular

### 1. CORS Asoslari
- CORS nima va nima uchun kerak?
- Same-Origin Policy (SOP)
- Cross-Origin requests
- Preflight requests
- CORS headers

### 2. CORS Muammosi
- Browser security model
- Origin restriction
- Common CORS errors
- Real-world scenarios

### 3. django-cors-headers
- Installation va setup
- Basic configuration
- Advanced settings
- Middleware ordering

### 4. CORS Configuration
- CORS_ALLOWED_ORIGINS
- CORS_ALLOW_ALL_ORIGINS
- CORS_ALLOWED_ORIGIN_REGEXES
- CORS_ALLOW_METHODS
- CORS_ALLOW_HEADERS
- CORS_EXPOSE_HEADERS
- CORS_ALLOW_CREDENTIALS

### 5. Security Best Practices
- Production vs Development
- Whitelist vs Blacklist
- Credentials handling
- Common vulnerabilities

---

##  CORS Nima?

**CORS (Cross-Origin Resource Sharing)** - bu brauzerlar uchun xavfsizlik mexanizmi bo'lib, bir origin (domen)'dan boshqa origin'ga HTTP so'rovlar yuborishni nazorat qiladi.

### Origin Nima?

**Origin** = Protocol + Domain + Port

```
https://example.com:443
  ↑        ↑         ↑
Protocol Domain    Port
```

**Bir xil Origin (Same-Origin):**
```
https://example.com/api/users
https://example.com/api/books
✅ Same origin
```

**Turli Origin (Cross-Origin):**
```
https://example.com      → http://example.com       ❌ (protocol)
https://example.com      → https://api.example.com  ❌ (subdomain)
https://example.com:443  → https://example.com:8000 ❌ (port)
https://example.com      → https://another.com      ❌ (domain)
```

---

##  Same-Origin Policy (SOP)

Brauzerlar default holatda **Same-Origin Policy** qo'llaydi - bu xavfsizlik uchun:

```javascript
// Frontend: http://localhost:3000
fetch('http://localhost:8000/api/books/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// ❌ ERROR:
// Access to fetch at 'http://localhost:8000/api/books/' 
// from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Sabab:**
- Frontend: `http://localhost:3000` (React, Vue, Angular)
- Backend: `http://localhost:8000` (Django)
- Port har xil → Cross-Origin → Blocked! ❌

---

## ✅ CORS Qanday Ishlaydi?

### Simple Request (Oddiy So'rov)

```
Client (localhost:3000)          Server (localhost:8000)
        |                                |
        |  GET /api/books/               |
        |  Origin: http://localhost:3000 |
        |------------------------------->|
        |                                |
        |  200 OK                        |
        |  Access-Control-Allow-Origin:  |
        |    http://localhost:3000       |
        |<-------------------------------|
        |                                |
```

### Preflight Request (Murakkab So'rov)

```
Client                          Server
   |                               |
   |  OPTIONS /api/books/          |  ← Preflight
   |  Origin: localhost:3000       |
   |  Access-Control-Request-Method: POST
   |  Access-Control-Request-Headers: Content-Type
   |----------------------------->|
   |                               |
   |  200 OK                       |
   |  Access-Control-Allow-Origin: localhost:3000
   |  Access-Control-Allow-Methods: GET, POST, PUT
   |  Access-Control-Allow-Headers: Content-Type
   |<-----------------------------|
   |                               |
   |  POST /api/books/             |  ← Actual Request
   |  Origin: localhost:3000       |
   |----------------------------->|
   |                               |
   |  201 Created                  |
   |<-----------------------------|
```

**Preflight kerak bo'ladigan holatlar:**
- POST, PUT, DELETE, PATCH (GET/HEAD emas)
- Custom headers (Authorization, X-Custom-Header)
- Content-Type: application/json

---

##  django-cors-headers O'rnatish

### 1. Installation

```bash
pip install django-cors-headers
```

### 2. Settings.py Configuration

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',  # ← CORS header support
    
    # Local apps
    'books',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← TOP'ga qo'ying!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**MUHIM:** `CorsMiddleware` eng yuqorida bo'lishi kerak!

---

##  CORS Configuration Variants

### Variant 1: Development (Barcha origin'larni ruxsat berish)

```python
# ⚠️ FAQAT DEVELOPMENT UCHUN!
CORS_ALLOW_ALL_ORIGINS = True
```

**Foydasi:**
- Tez sozlash
- Development'da qulay

**Kamchiligi:**
- ⚠️ Xavfli!
- Production'da HECH QACHON ishlatmang!

---

### Variant 2: Specific Origins (Tavsiya etiladi)

```python
# ✅ PRODUCTION UCHUN
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",       # React dev
    "http://localhost:5173",       # Vite dev
    "http://127.0.0.1:3000",
    "https://example.com",         # Production frontend
    "https://www.example.com",
    "https://app.example.com",
]
```

---

### Variant 3: Regex Pattern

```python
# Subdomain pattern
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.example\.com$",  # *.example.com
    r"^http://localhost:\d+$",        # localhost:any_port
]
```

**Misol:**
```
✅ https://api.example.com
✅ https://app.example.com
✅ http://localhost:3000
✅ http://localhost:5173
❌ https://malicious.com
```

---

## 🔧 CORS Settings (To'liq)

### 1. Allowed Origins

```python
# Aniq origin'lar
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://example.com",
]

# YO'Q: Barcha origin'larni ruxsat berish (development only!)
CORS_ALLOW_ALL_ORIGINS = False  # Production'da False

# Regex pattern
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.example\.com$",
]
```

### 2. Allowed Methods

```python
# Default: GET, POST, PUT, PATCH, DELETE, OPTIONS
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

### 3. Allowed Headers

```python
# Request'da qo'shish mumkin bo'lgan headerlar
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    
    # Custom headers
    'x-api-key',
    'x-custom-header',
]
```

### 4. Expose Headers

```python
# Frontend'ga ko'rinadigan response headerlar
CORS_EXPOSE_HEADERS = [
    'Content-Length',
    'X-Total-Count',
    'X-Page-Number',
]
```

### 5. Credentials

```python
# Cookies, Authorization headers
CORS_ALLOW_CREDENTIALS = True

# ⚠️ Agar True bo'lsa, CORS_ALLOW_ALL_ORIGINS True bo'lmasligi kerak!
```

### 6. Preflight Cache

```python
# Preflight response cache vaqti (soniyalarda)
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 soat
```

---

##  Security Best Practices

### 1. Never Use CORS_ALLOW_ALL_ORIGINS in Production

```python
# ❌ XATO
CORS_ALLOW_ALL_ORIGINS = True

# ✅ TO'G'RI
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

### 2. Use Environment Variables

```python
# settings.py
import os

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# .env
CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
```

### 3. Different Settings for Dev/Prod

```python
# settings.py
DEBUG = os.getenv('DEBUG', 'False') == 'True'

if DEBUG:
    # Development
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Production
    CORS_ALLOWED_ORIGINS = [
        "https://example.com",
        "https://www.example.com",
    ]
```

### 4. Credentials Handling

```python
# Agar cookies ishlatmoqchi bo'lsangiz
CORS_ALLOW_CREDENTIALS = True

# Frontend'da ham (JavaScript)
fetch('http://localhost:8000/api/books/', {
    credentials: 'include'  # cookies jo'natish
})
```

### 5. Wildcard Subdomain Security

```python
# ❌ Juda keng (xavfli)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.example\.com$",  # har qanday subdomain
]

# ✅ Aniqroq
CORS_ALLOWED_ORIGINS = [
    "https://app.example.com",
    "https://api.example.com",
]
```

---

##  CORS Testing

### 1. Simple GET Request

```javascript
// Frontend (React/Vue/Angular)
fetch('http://localhost:8000/api/books/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('CORS error:', error));
```

### 2. POST with JSON

```javascript
fetch('http://localhost:8000/api/books/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'New Book',
    author: 1,
    isbn: '1234567890123'
  })
})
.then(response => response.json())
.then(data => console.log('Created:', data))
.catch(error => console.error('Error:', error));
```

### 3. With Authorization

```javascript
fetch('http://localhost:8000/api/books/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
  },
})
.then(response => response.json())
.then(data => console.log(data));
```

### 4. Using Axios

```javascript
import axios from 'axios';

axios.get('http://localhost:8000/api/books/')
  .then(response => console.log(response.data))
  .catch(error => console.error(error));

// With Authorization
axios.defaults.headers.common['Authorization'] = 'Bearer token';
```

---

##  Common CORS Errors

### Error 1: No 'Access-Control-Allow-Origin' header

```
Access to fetch at 'http://localhost:8000/api/books/' 
from origin 'http://localhost:3000' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Yechim:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Error 2: Credentials + Wildcard

```
The value of the 'Access-Control-Allow-Origin' header must not be '*' 
when the request's credentials mode is 'include'.
```

**Yechim:**
```python
# ❌
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ✅
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True
```

### Error 3: Preflight Request Failed

```
Response to preflight request doesn't pass access control check
```

**Yechim:**
```python
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    # qo'shimcha headerlar
]
```

---

##  CORS Headers Reference

### Request Headers

```
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

### Response Headers

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
Access-Control-Expose-Headers: X-Total-Count
```

---

##  Real-World Example

### Frontend (React)

```javascript
// src/api/books.js
const API_URL = 'http://localhost:8000/api';

export const getBooks = async () => {
  const response = await fetch(`${API_URL}/books/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch books');
  }
  
  return response.json();
};

export const createBook = async (bookData) => {
  const response = await fetch(`${API_URL}/books/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify(bookData),
  });
  
  return response.json();
};
```

### Backend (Django)

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://localhost:5173",  # Vite
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
]
```

---

##  Foydali Linklar

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [django-cors-headers GitHub](https://github.com/adamchainz/django-cors-headers)
- [CORS Test Tool](https://www.test-cors.org/)

---

##  Xulosa

1. **CORS** - brauzer xavfsizlik mexanizmi
2. **django-cors-headers** - Django uchun CORS middleware
3. **Production'da** - faqat kerakli origin'larni ruxsat bering
4. **Development'da** - `CORS_ALLOW_ALL_ORIGINS = True` ishlatish mumkin
5. **Credentials** bilan ishlashda ehtiyot bo'ling
6. **Preflight** requests'ni tushunish muhim

---

##  Keyingi Darslar

- Lesson 26: API Versioning
- Lesson 27: Error Handling
- Lesson 28: Signals & Webhooks