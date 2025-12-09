# Homework 25: CORS Configuration

##  Umumiy Talablar

Library Management tizimiga CORS sozlash va frontend bilan integratsiya qilish.

---

##  Vazifa 1: django-cors-headers O'rnatish (10 ball)

### Topshiriq:
1. `django-cors-headers` paketini o'rnating
2. `INSTALLED_APPS` va `MIDDLEWARE` sozlang
3. Basic configuration qo'shing

### Kutilayotgan Kod:

```bash
# O'rnatish
pip install django-cors-headers
```

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # TOP'da!
    'django.middleware.security.SecurityMiddleware',
    # ...
]
```

### Test:
```bash
python manage.py runserver

# Boshqa terminalda
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS http://localhost:8000/api/books/
```

---

##  Vazifa 2: Development Configuration (15 ball)

### Topshiriq:
Development muhiti uchun CORS sozlash

```python
# settings.py

DEBUG = True

# Development settings
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    # Production settings (keyinroq qo'shamiz)
    pass
```

### Test:
Simple HTML file yarating va test qiling:

```html
<!-- test-cors.html -->
<!DOCTYPE html>
<html>
<head>
    <title>CORS Test</title>
</head>
<body>
    <h1>CORS Test</h1>
    <button onclick="testCORS()">Test API</button>
    <pre id="result"></pre>

    <script>
        function testCORS() {
            fetch('http://localhost:8000/api/books/')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').textContent = 
                        JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    document.getElementById('result').textContent = 
                        'Error: ' + error;
                });
        }
    </script>
</body>
</html>
```

Faylni brauzerda oching va "Test API" tugmasini bosing.

---

##  Vazifa 3: Production Configuration (20 ball)

### Topshiriq:
Production uchun xavfsiz CORS sozlash

```python
# settings.py
import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'

if DEBUG:
    # Development
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Production
    CORS_ALLOWED_ORIGINS = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "https://app.yourdomain.com",
    ]
    
    # Yoki environment variable'dan
    cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '')
    if cors_origins:
        CORS_ALLOWED_ORIGINS = cors_origins.split(',')

# Custom headers ruxsat berish
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

# Credentials support
CORS_ALLOW_CREDENTIALS = True

# Preflight cache
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours
```

### .env fayli:

```env
DEBUG=False
CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
```

---

##  Vazifa 4: Frontend Integration (React) (25 ball)

### Topshiriq:
Simple React app yarating va API bilan bog'lang

```bash
# React app yaratish
npx create-react-app library-frontend
cd library-frontend
npm install axios
```

```javascript
// src/api/books.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getBooks = async () => {
  const response = await api.get('/books/');
  return response.data;
};

export const getBook = async (id) => {
  const response = await api.get(`/books/${id}/`);
  return response.data;
};

export const createBook = async (bookData) => {
  const response = await api.post('/books/', bookData);
  return response.data;
};

export const updateBook = async (id, bookData) => {
  const response = await api.put(`/books/${id}/`, bookData);
  return response.data;
};

export const deleteBook = async (id) => {
  await api.delete(`/books/${id}/`);
};

export default api;
```

```javascript
// src/App.js
import React, { useState, useEffect } from 'react';
import { getBooks } from './api/books';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const data = await getBooks();
      setBooks(data.results || data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch books: ' + err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <div className="App">
      <h1>Library Books</h1>
      <button onClick={fetchBooks}>Refresh</button>
      
      <div className="books-list">
        {books.map(book => (
          <div key={book.id} className="book-card">
            <h3>{book.title}</h3>
            <p>Author: {book.author?.name || book.author}</p>
            <p>ISBN: {book.isbn}</p>
            <p>Price: ${book.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
```

```css
/* src/App.css */
.App {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.book-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-card h3 {
  margin-top: 0;
  color: #333;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
```

### Run:
```bash
# Django backend
python manage.py runserver

# React frontend (yangi terminal)
npm start
```

Browser'da `http://localhost:3000` oching.

---

##  Vazifa 5: CORS Error Handling (15 ball)

### Topshiriq:
CORS xatolarini to'g'ri handle qilish

```javascript
// src/api/errorHandler.js
export const handleCORSError = (error) => {
  if (error.message.includes('CORS')) {
    return {
      type: 'CORS',
      message: 'Backend server CORS sozlamalarini tekshiring',
      solution: 'Django settings.py da CORS_ALLOWED_ORIGINS ni to\'g\'rilang'
    };
  }
  
  if (error.message.includes('Network')) {
    return {
      type: 'Network',
      message: 'Backend server ishlamayapti',
      solution: 'python manage.py runserver ni ishga tushiring'
    };
  }
  
  return {
    type: 'Unknown',
    message: error.message,
    solution: 'Console loglarni tekshiring'
  };
};
```

```javascript
// src/App.js (yangilangan)
import { handleCORSError } from './api/errorHandler';

const fetchBooks = async () => {
  try {
    setLoading(true);
    const data = await getBooks();
    setBooks(data.results || data);
    setError(null);
  } catch (err) {
    const errorInfo = handleCORSError(err);
    setError(
      `${errorInfo.type} Error: ${errorInfo.message}\n` +
      `Solution: ${errorInfo.solution}`
    );
    console.error('Error details:', err);
  } finally {
    setLoading(false);
  }
};
```

---

##  Vazifa 6: Custom CORS Middleware (Bonus +10 ball)

### Topshiriq:
Custom CORS middleware yarating (advanced)

```python
# books/middleware.py
from django.utils.deprecation import MiddlewareMixin

class CustomCORSMiddleware(MiddlewareMixin):
    """
    Custom CORS middleware - logging va analytics uchun
    """
    
    def process_request(self, request):
        """CORS preflight request'ni handle qilish"""
        origin = request.META.get('HTTP_ORIGIN')
        
        if request.method == 'OPTIONS':
            # Logging
            print(f"CORS Preflight from: {origin}")
            print(f"Method: {request.META.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')}")
            print(f"Headers: {request.META.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS')}")
        
        return None
    
    def process_response(self, request, response):
        """Response'ga CORS headerlar qo'shish"""
        origin = request.META.get('HTTP_ORIGIN')
        
        if origin:
            # Custom logic: faqat ma'lum soatlarda ruxsat berish
            from datetime import datetime
            hour = datetime.now().hour
            
            if 9 <= hour <= 18:  # 9 AM - 6 PM
                response['X-CORS-Status'] = 'Allowed'
            else:
                response['X-CORS-Status'] = 'Outside business hours'
        
        return response
```

```python
# settings.py
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'books.middleware.CustomCORSMiddleware',  # Custom middleware
    # ...
]
```

---

##  Vazifa 7: CORS Testing Suite (Bonus +15 ball)

### Topshiriq:
CORS test suite yarating

```python
# books/tests/test_cors.py
from django.test import TestCase, Client
from django.conf import settings

class CORSTestCase(TestCase):
    """CORS configuration testlari"""
    
    def setUp(self):
        self.client = Client()
        self.origin = 'http://localhost:3000'
    
    def test_simple_cors_request(self):
        """Simple GET request CORS test"""
        response = self.client.get(
            '/api/books/',
            HTTP_ORIGIN=self.origin
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', response)
    
    def test_preflight_request(self):
        """Preflight OPTIONS request test"""
        response = self.client.options(
            '/api/books/',
            HTTP_ORIGIN=self.origin,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST',
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS='content-type'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access-Control-Allow-Methods', response)
        self.assertIn('Access-Control-Allow-Headers', response)
    
    def test_credentials_with_origin(self):
        """Credentials bilan request test"""
        response = self.client.get(
            '/api/books/',
            HTTP_ORIGIN=self.origin,
            HTTP_COOKIE='sessionid=test123'
        )
        
        if settings.CORS_ALLOW_CREDENTIALS:
            self.assertIn('Access-Control-Allow-Credentials', response)
    
    def test_disallowed_origin(self):
        """Ruxsat berilmagan origin test"""
        bad_origin = 'http://malicious.com'
        
        response = self.client.get(
            '/api/books/',
            HTTP_ORIGIN=bad_origin
        )
        
        if not settings.CORS_ALLOW_ALL_ORIGINS:
            # Origin ruxsat berilmagan bo'lishi kerak
            allowed_origin = response.get('Access-Control-Allow-Origin')
            if allowed_origin:
                self.assertNotEqual(allowed_origin, bad_origin)
```

### Run tests:
```bash
python manage.py test books.tests.test_cors
```

---

##  Baholash Mezonlari

| Vazifa | Ballar | Tavsif |
|--------|--------|--------|
| CORS o'rnatish | 10 | django-cors-headers setup |
| Development config | 15 | Dev muhiti sozlash |
| Production config | 20 | Prod xavfsiz sozlash |
| React integration | 25 | Frontend bilan bog'lash |
| Error handling | 15 | Xatolarni handle qilish |
| **Jami** | **85** | |
| Custom middleware | +10 | Bonus |
| Testing suite | +15 | Bonus |
| **Maksimal** | **110** | |

---

##  Topshirish Talablari

1. Barcha vazifalar bajarilgan
2. React app ishlayapti va API bilan bog'langan
3. Production sozlamalar xavfsiz
4. CORS testlari yozilgan va o'tayapti
5. README.md'da qanday ishlatish ko'rsatilgan

---

##  Qo'shimcha Topshiriqlar (Ixtiyoriy)

### 1. Vue.js Integration
React o'rniga Vue.js ishlatib ko'ring

### 2. CORS Analytics Dashboard
CORS request'larni track qiluvchi dashboard yarating

### 3. Multiple Frontend Support
React, Vue, Angular - barcha uchun sozlash

### 4. CORS Documentation
API documentation'ga CORS qo'llanmasi qo'shing

---

##  Topshirish Formati

```
homework-25-cors/
├── backend/
│   ├── library_project/
│   │   └── settings.py (CORS config)
│   └── books/
│       ├── middleware.py
│       └── tests/test_cors.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── books.js
│   │   │   └── errorHandler.js
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
└── README.md
```

---

##  Deadline

**3 kun** (72 soat)

---

##  Maslahatlar

1. Development'da `CORS_ALLOW_ALL_ORIGINS = True` ishlatish mumkin
2. Production'da HECH QACHON wildcard ishlatmang
3. Preflight request'larni understand qiling
4. Browser DevTools Network tab'da CORS headerlarni tekshiring
5. Frontend va backend bir vaqtda test qiling

**Omad!**