# CORS Asoslari - Qadamma-qadam

## Maqsad
Bu file'da CORS'ni qanday ishlashini, muammolarini va yechimlarini amaliy misollar bilan o'rganamiz.

---

## 1. CORS Nima? Nima Uchun Kerak?

### Origin Nima?

**Origin** = Protokol + Domen + Port

```
https://example.com:443
   ↑        ↑         ↑
Protokol  Domen     Port
```

### Same-Origin vs Cross-Origin

**Bir xil Origin (Same-Origin):**
```javascript
// Ikkala URL ham http://example.com
https://example.com/api/users      ✅
https://example.com/api/books      ✅
https://example.com/page           ✅
```

**Turli Origin (Cross-Origin):**
```javascript
https://example.com      →  http://example.com         ❌ (protokol boshqa)
https://example.com      →  https://api.example.com    ❌ (subdomain boshqa)
https://example.com:443  →  https://example.com:8000   ❌ (port boshqa)
https://example.com      →  https://another.com        ❌ (domen boshqa)
```

---

## 2. Same-Origin Policy (SOP)

**Same-Origin Policy** - brauzer xavfsizligi uchun automatik blocking mexanizmi.

### Muammo: Frontend va Backend Turli Portta

```javascript
// Frontend: http://localhost:3000 (React)
fetch('http://localhost:8000/api/books/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

**Natija:**
```
❌ ERROR: Access to fetch at 'http://localhost:8000/api/books/' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Nima bo'ldi?**
- Frontend: `http://localhost:3000` → React Dev Server
- Backend: `http://localhost:8000` → Django
- Port turli bo'lgani uchun → Brauzer blokladi! ❌

---

## 3. CORS Qanday Ishlaydi?

### Request Turları

#### 1. Simple Request (Oddiy So'rov)

**Qachon oddiy so'rov?**
- `GET`, `HEAD`, `POST` (faqat)
- Standard headers (Content-Type: form-data, text/plain)
- Credentials yoq

**Jarayon:**
```
Frontend (localhost:3000)         Backend (localhost:8000)
        |                                |
        |  GET /api/books/              |
        |  Origin: http://localhost:3000|
        |-----------------------------→ |
        |                                |
        |  200 OK                        |
        |  Access-Control-Allow-Origin: * (yoki localhost:3000)
        |←-----------------------------|
        |                                |
       ✅ Data olinadi!
```

#### 2. Preflight Request (Tekshiruvchi So'rov)

**Qachon preflight kerak?**
- `POST`, `PUT`, `DELETE`, `PATCH`
- Custom headers (`Authorization`, `X-API-Key`)
- Content-Type: `application/json`

**Jarayon:**

```
Frontend (localhost:3000)         Backend (localhost:8000)
        |                                |
        |  OPTIONS /api/books/          |  ← PREFLIGHT
        |  Origin: localhost:3000       |
        |  Access-Control-Request-Method: POST
        |  Access-Control-Request-Headers: Content-Type
        |-----------------------------→ |
        |                                |
        |  200 OK (200 YOK 204)          |
        |  Access-Control-Allow-Origin: localhost:3000
        |  Access-Control-Allow-Methods: GET, POST, PUT, DELETE
        |  Access-Control-Allow-Headers: Content-Type, Authorization
        |  Access-Control-Max-Age: 86400
        |←-----------------------------|
        |                                |
        |  POST /api/books/              |  ← HAQIQIY SO'ROV
        |  Origin: localhost:3000       |
        |  Content-Type: application/json
        |  {"title": "Django Guide"}    |
        |-----------------------------→ |
        |                                |
        |  201 Created                   |
        |  Access-Control-Allow-Origin: localhost:3000
        |←-----------------------------|
        |                                |
       ✅ Data yuborildi!
```

### CORS Headers

```python
# Backend response'ga qo'shiladi:

# 1. Qaysi origin'larni ruxsat berish
Access-Control-Allow-Origin: http://localhost:3000

# 2. Qaysi method'larni ruxsat berish
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS

# 3. Qaysi header'larni ruxsat berish
Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key

# 4. Preflight'ni cache'lash (sekund)
Access-Control-Max-Age: 86400  # 24 soat

# 5. Credentials (cookies, auth) ruxsat berish
Access-Control-Allow-Credentials: true

# 6. Response'dan ko'rsatilishiga ruxsat berish
Access-Control-Expose-Headers: X-Total-Count, X-Page-Number
```

---

## 4. CORS Xatoliklari va Yechimi

### Xatolik 1: "Access to XMLHttpRequest blocked by CORS policy"

```javascript
// Frontend code
fetch('http://backend.com/api/books/')
```

**Xatolik:**
```
Access to fetch at 'http://backend.com/api/books/' from origin 
'http://frontend.com' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Yechim:** Django backend'da CORS'ni o'rnatish

```python
# settings.py
INSTALLED_APPS = ['corsheaders', ...]
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOWED_ORIGINS = ['http://frontend.com']
```

---

### Xatolik 2: "The CORS protocol does not allow specifying a wildcard"

```python
# ❌ XATO
CORS_ALLOWED_ORIGINS = ['*']  # String '*'!

# ✅ TO'G'RI
CORS_ALLOW_ALL_ORIGINS = True  # Yoki
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', ...]
```

**Sabab:** CORS standardi `"*"` string'i o'rniga `CORS_ALLOW_ALL_ORIGINS = True` yoki aniq origin'lar istamaydi.

---

### Xatolik 3: "Credentials mode is 'include' but 'Access-Control-Allow-Credentials' is missing"

```javascript
// Frontend code
fetch('http://backend.com/api/books/', {
  credentials: 'include',  // Cookies yubor
  method: 'GET'
})
```

**Yechim:** Backend'da credentials ruxsat berish

```python
# settings.py
CORS_ALLOWED_ORIGINS = ['http://frontend.com']
CORS_ALLOW_CREDENTIALS = True  # ← Qo'shing!
```

---

### Xatolik 4: "Authorization header is not allowed by Access-Control-Allow-Headers"

```javascript
// Frontend code
fetch('http://backend.com/api/books/', {
  headers: {
    'Authorization': 'Bearer token123'
  }
})
```

**Yechim:** Authorization header'ni ruxsat berish

```python
# settings.py
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',  # ← Qo'shing!
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

---

## 5. Amaliy Misol: React Frontend + Django Backend

### Stsenariya
```
Frontend: http://localhost:3000 (React)
Backend:  http://localhost:8000 (Django)
```

### Backend Setup

**settings.py:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'corsheaders',  # ← Qo'shing
    
    'books',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← ENG YUQORIDA!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React dev
    "http://127.0.0.1:3000",
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

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
]

CORS_ALLOW_CREDENTIALS = True
```

### Frontend Code (React)

**API Service:**
```javascript
// api.js
const API_URL = 'http://localhost:8000/api';

// GET - Oddiy so'rov
export const getBooks = async () => {
  const response = await fetch(`${API_URL}/books/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  });
  return response.json();
};

// POST - Murakkab so'rov (preflight)
export const createBook = async (bookData) => {
  const response = await fetch(`${API_URL}/books/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    credentials: 'include',  // Cookies yuborish
    body: JSON.stringify(bookData)
  });
  return response.json();
};

// DELETE
export const deleteBook = async (bookId) => {
  const response = await fetch(`${API_URL}/books/${bookId}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    credentials: 'include'
  });
  return response.json();
};
```

**React Component:**
```javascript
// BookList.js
import { useEffect, useState } from 'react';
import { getBooks, createBook, deleteBook } from './api';

export default function BookList() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    // Kitoblarni olish
    getBooks()
      .then(data => setBooks(data))
      .catch(error => console.error('CORS Error:', error));
  }, []);

  const handleCreate = async (title) => {
    try {
      const newBook = await createBook({ title });
      setBooks([...books, newBook]);
    } catch (error) {
      console.error('Create error:', error);
    }
  };

  return (
    <div>
      <h1>Kitoblar</h1>
      {books.map(book => (
        <div key={book.id}>
          <p>{book.title}</p>
          <button onClick={() => deleteBook(book.id)}>O'chirish</button>
        </div>
      ))}
    </div>
  );
}
```

---

## 6. Development vs Production

### Development

```python
# ⚠️ FAQAT DEVELOPMENT UCHUN
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False
```

**Foydasi:**
- Tez setup
- Frontend development qulay

**Kamchiligi:**
- Xavfli!
- Har qanday website kirishiga ruxsat!

### Production

```python
# ✅ PRODUCTION UCHUN
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
    "https://app.example.com",
]

CORS_ALLOW_CREDENTIALS = True  (agar auth kerak bo'lsa)

# Regex pattern - subdomainlar uchun
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.example\.com$",
]
```

**Xavfsizlik:**
- Faqat kerakli origin'lardan
- HTTPS majburiy
- Whitelisting (aniq ro'yxat)

---

## 7. Xulosa

| Tushuncha | Tavsifi |
|-----------|---------|
| **Origin** | Protokol + Domen + Port |
| **SOP** | Brauzer xavfsizligi - blokirovka |
| **CORS** | SOP'ni boshqarish mexanizmi |
| **Simple Request** | GET/HEAD/POST, standard headers |
| **Preflight** | OPTIONS so'rov, tekshiruvchi |
| **Middleware** | `corsheaders.middleware.CorsMiddleware` |
| **Settings** | `CORS_ALLOWED_ORIGINS`, `CORS_ALLOW_METHODS` |
| **Credentials** | `CORS_ALLOW_CREDENTIALS = True` |

---

## Keyingi Bosqichlar

1. **02-django-cors-setup.py** - Qadamma-qadam o'rnatish
2. **03-cors-configuration.py** - Kengaytirilgan sozlashlar
3. **04-security-best-practices.md** - Xavfsizlik
4. **05-frontend-integration.html** - React integratsiyasi

---

## Foydalanilgan Manbalar

- [Django CORS Headers Documentation](https://github.com/adamchainz/django-cors-headers)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [W3C CORS Specification](https://www.w3.org/TR/cors/)
