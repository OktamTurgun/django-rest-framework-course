# ReDoc - Complete Guide

## 📋 Mundarija

1. [ReDoc nima?](#1-redoc-nima)
2. [ReDoc sozlash](#2-redoc-sozlash)
3. [ReDoc vs Swagger UI](#3-redoc-vs-swagger-ui)
4. [Customization](#4-customization)
5. [Advanced features](#5-advanced-features)

---

## 1. ReDoc nima?

### 🎨 Professional API dokumentatsiya

**ReDoc** - Chiroyli va responsive API dokumentatsiya tool.

**Swagger UI vs ReDoc:**

| Feature | Swagger UI | ReDoc |
|---------|------------|-------|
| **Dizayn** | ⚠️ Oddiy | ✅ Chiroyli |
| **Testing** | ✅ "Try it out" | ❌ Yo'q |
| **Navigation** | ⚠️ Oddiy | ✅ Advanced |
| **Responsive** | ⚠️ Yaxshi | ✅ A'lo |
| **Search** | ⚠️ Oddiy | ✅ Advanced |
| **Print-friendly** | ❌ Yo'q | ✅ Ha |
| **Customization** | ⚠️ Cheklangan | ✅ Ko'p |

---

### 🤔 Qachon ReDoc ishlatish?

**Swagger UI ishlatish:**
- ✅ Development jarayonida
- ✅ Internal API (team uchun)
- ✅ Testing kerak bo'lsa

**ReDoc ishlatish:**
- ✅ Public API dokumentatsiya
- ✅ Client/Partner'larga ko'rsatish
- ✅ Documentation website
- ✅ Professional ko'rinish kerak bo'lsa

**Ideal:** Ikkalasini ham qo'ying! 🎯

---

### 📊 ReDoc'ning afzalliklari

1. **🎨 Chiroyli dizayn** - Zamonaviy va professional
2. **📱 Responsive** - Mobile, tablet, desktop
3. **🔍 Advanced search** - Tez qidirish
4. **📑 Navigation** - Sidebar bilan oson navigatsiya
5. **🖨️ Print-friendly** - PDF chiqarish mumkin
6. **⚡ Tez** - Katta API'lar uchun ham tez
7. **🎨 Theme** - Dark/Light mode
8. **🌍 Multi-language** - Ko'p til support

---

## 2. ReDoc sozlash

### ✅ drf-spectacular bilan (Already done!)

Agar swagger-guide.md'ni bajarsangiz, ReDoc allaqachon ishlaydi! 🎉

**URLs (swagger-guide.md'da qo'shgan edik):**
```python
# library_project/urls.py

from drf_spectacular.views import SpectacularRedocView

urlpatterns = [
    # ...
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

---

### 🌐 ReDoc ochish

```
http://localhost:8000/api/schema/redoc/
```

**Ko'rinishi:**

```
┌────────────────────────────────────────────────────────┐
│  📚 Library API                              v1.0.0    │
│  REST API for Library Management System                │
├────────────────────────────────────────────────────────┤
│  SIDEBAR                │  CONTENT                     │
│  ┌───────────────────┐  │  ┌─────────────────────────┐│
│  │ 📚 Books          │  │  │ GET /books/             ││
│  │   • List Books    │  │  │ List all books          ││
│  │   • Create Book   │  │  │                         ││
│  │   • Get Book      │  │  │ Query Parameters:       ││
│  │   • Update Book   │  │  │ - search (string)       ││
│  │   • Delete Book   │  │  │ - ordering (string)     ││
│  │                   │  │  │ - page (integer)        ││
│  │ 🔍 Search         │  │  │                         ││
│  │ 📖 Schemas        │  │  │ Responses:              ││
│  └───────────────────┘  │  │ 200: Success            ││
│                         │  └─────────────────────────┘│
└────────────────────────────────────────────────────────┘
```

**Features:**
- ✅ Sidebar navigation
- ✅ Search box
- ✅ Code samples
- ✅ Dark mode toggle
- ✅ Expand/Collapse

---

## 3. ReDoc vs Swagger UI

### 📸 Visual taqqoslash

#### Swagger UI:
```
┌─────────────────────────────────────┐
│ Library API                   v1.0.0│
├─────────────────────────────────────┤
│ GET /books/  [Try it out]           │
│   Responses                          │
│   200: Success                       │
│ POST /books/  [Try it out]          │
│   Request body                       │
│   {"title": "..."}                   │
└─────────────────────────────────────┘
```

**Afzalliklari:**
- ✅ Interactive testing
- ✅ "Try it out" tugmasi
- ⚠️ Oddiy dizayn

---

#### ReDoc:
```
┌──────────────────────────────────────────────┐
│ 📚 Library API                       v1.0.0  │
│ REST API for Library Management System       │
├──────────────────────────────────────────────┤
│ SIDEBAR         │  CONTENT                   │
│ 📚 Books        │  GET /books/               │
│  • List Books   │  ━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Create Book  │  List all books with       │
│  • Get Book     │  pagination and filtering  │
│                 │                            │
│ 🔍 Filters      │  QUERY PARAMETERS          │
│  • Available    │  search     string         │
│  • Expensive    │  ordering   string         │
│                 │  page       integer        │
│ 📖 Schemas      │                            │
│  • Book         │  RESPONSES                 │
│  • PaginatedList│  200   Success            │
└─────────────────┴────────────────────────────┘
```

**Afzalliklari:**
- ✅ Professional dizayn
- ✅ Sidebar navigation
- ✅ Advanced search
- ⚠️ Testing yo'q

---

### 🎯 Qaysi birini ishlatish?

**Development:**
```
Swagger UI ← Daily testing
```

**Documentation:**
```
ReDoc ← Public API docs
```

**Best practice:**
```
Ikkalasini ham qo'ying!
- /api/schema/swagger-ui/  ← Testing
- /api/schema/redoc/        ← Documentation
```

---

## 4. Customization

### 🎨 Theme sozlash

```python
# library_project/urls.py

from drf_spectacular.views import SpectacularRedocView

urlpatterns = [
    path('api/schema/redoc/', 
         SpectacularRedocView.as_view(
             url_name='schema',
             template_name='redoc.html'  # ← Custom template
         ), 
         name='redoc'
    ),
]
```

---

### 📄 Custom template yaratish

```bash
# Template papkasini yaratish
mkdir -p templates
```

```html
<!-- templates/redoc.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Library API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
</head>
<body>
    <redoc 
        spec-url='{% url "schema" %}'
        
        <!-- Theme options -->
        theme='{
            "colors": {
                "primary": {
                    "main": "#2196F3"
                }
            },
            "typography": {
                "fontSize": "16px",
                "fontFamily": "Roboto, sans-serif",
                "headings": {
                    "fontFamily": "Montserrat, sans-serif"
                }
            }
        }'
        
        <!-- UI options -->
        hide-download-button
        expand-responses="200,201"
        required-props-first
        sort-props-alphabetically
    ></redoc>
    
    <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

---

### 🎨 Color customization

```javascript
theme='{
    "colors": {
        "primary": {
            "main": "#2196F3"        // Primary color
        },
        "success": {
            "main": "#4CAF50"        // Success color (200, 201)
        },
        "error": {
            "main": "#F44336"        // Error color (400, 500)
        },
        "text": {
            "primary": "#263238"     // Text color
        },
        "http": {
            "get": "#61affe",        // GET color
            "post": "#49cc90",       // POST color
            "put": "#fca130",        // PUT color
            "delete": "#f93e3e"      // DELETE color
        }
    }
}'
```

---

### 🔤 Typography customization

```javascript
theme='{
    "typography": {
        "fontSize": "16px",
        "lineHeight": "1.6",
        "fontWeightLight": "300",
        "fontWeightRegular": "400",
        "fontWeightBold": "700",
        "fontFamily": "Roboto, sans-serif",
        "headings": {
            "fontFamily": "Montserrat, sans-serif",
            "fontWeight": "700"
        },
        "code": {
            "fontSize": "14px",
            "fontFamily": "Courier, monospace"
        }
    }
}'
```

---

### ⚙️ ReDoc options

```html
<redoc 
    spec-url='{% url "schema" %}'
    
    <!-- Layout -->
    hide-download-button          <!-- Schema yuklab olish tugmasini yashirish -->
    hide-hostname                 <!-- Hostname'ni yashirish -->
    hide-loading                  <!-- Loading indicator'ni yashirish -->
    
    <!-- Behavior -->
    expand-responses="200,201"    <!-- Default ochiq response'lar -->
    expand-single-schema-field    <!-- Single field schema'ni ochish -->
    json-sample-expand-level="2"  <!-- JSON example expand level -->
    
    <!-- Display -->
    required-props-first          <!-- Required field'lar birinchi -->
    sort-props-alphabetically     <!-- Field'larni alfabetik tartiblash -->
    no-auto-auth                  <!-- Auto-auth'ni o'chirish -->
    
    <!-- Menu -->
    scroll-y-offset="50"          <!-- Scroll offset -->
    menu-toggle                   <!-- Menu toggle qo'shish -->
></redoc>
```

---

## 5. Advanced Features

### 🔍 Search functionality

ReDoc'da search avtomatik ishlaydi!

**Features:**
- ✅ Endpoint name'da qidirish
- ✅ Description'da qidirish
- ✅ Tag'larda qidirish
- ✅ Schema name'da qidirish

**Keyboard shortcuts:**
```
/  - Search'ni ochish
Esc - Search'ni yopish
```

---

### 📱 Responsive design

ReDoc avtomatik responsive:

**Desktop (> 1200px):**
```
┌─────────────────────────────────┐
│ SIDEBAR  │  CONTENT             │
│          │                      │
│          │                      │
└─────────────────────────────────┘
```

**Tablet (768px - 1200px):**
```
┌─────────────────────────────┐
│ ☰ MENU  │  CONTENT         │
│         │                  │
└─────────────────────────────┘
```

**Mobile (< 768px):**
```
┌────────────────┐
│ ☰ MENU         │
│                │
│ CONTENT        │
│                │
└────────────────┘
```

---

### 🖨️ Print-friendly

ReDoc PDF export uchun optimallashtirilgan:

**Brauzerda:**
```
File → Print → Save as PDF
```

**Features:**
- ✅ Clean layout
- ✅ Page breaks
- ✅ TOC (Table of Contents)
- ✅ Code highlighting

---

### 🌙 Dark mode

```html
<redoc 
    spec-url='{% url "schema" %}'
    theme='{
        "colors": {
            "primary": {
                "main": "#BB86FC"
            },
            "text": {
                "primary": "#E1E1E1"
            },
            "background": {
                "main": "#121212"
            }
        }
    }'
></redoc>
```

---

### 🔗 Deep linking

ReDoc avtomatik URL hash yaratadi:

```
http://localhost:8000/api/schema/redoc/#operation/books_list
http://localhost:8000/api/schema/redoc/#operation/books_create
http://localhost:8000/api/schema/redoc/#tag/Books
http://localhost:8000/api/schema/redoc/#section/Authentication
```

**Foyda:** Link ulashing, to'g'ri joyga o'tadi!

---

### 📦 Schema caching

```python
# library_project/settings.py

SPECTACULAR_SETTINGS = {
    # Cache schema (production uchun)
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Custom cache
    'SCHEMA_CACHE_TIMEOUT': 3600,  # 1 soat
}
```

---

### 🌍 Custom branding

```html
<!-- templates/redoc.html -->
<!DOCTYPE html>
<html>
<head>
    <title>My Company - API Documentation</title>
    <link rel="icon" href="/static/favicon.ico">
    
    <style>
        body {
            margin: 0;
            padding: 0;
        }
        
        /* Custom header */
        .custom-header {
            background: #2196F3;
            color: white;
            padding: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <!-- Custom header -->
    <div class="custom-header">
        <img src="/static/logo.png" alt="Logo" height="40">
        <h1>My Company API</h1>
        <p>Version 1.0.0</p>
    </div>
    
    <!-- ReDoc -->
    <redoc spec-url='{% url "schema" %}'></redoc>
    
    <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

---

### 📊 Multiple versions

```python
# library_project/urls.py

from drf_spectacular.views import SpectacularRedocView

urlpatterns = [
    # V1
    path('api/v1/schema/redoc/', 
         SpectacularRedocView.as_view(url_name='schema-v1'), 
         name='redoc-v1'
    ),
    
    # V2
    path('api/v2/schema/redoc/', 
         SpectacularRedocView.as_view(url_name='schema-v2'), 
         name='redoc-v2'
    ),
]
```

---

### 🔐 Password protection

```python
# views.py

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from drf_spectacular.views import SpectacularRedocView

@method_decorator(login_required, name='dispatch')
class ProtectedRedocView(SpectacularRedocView):
    """
    ReDoc faqat login qilgan user'lar uchun
    """
    pass

# urls.py
urlpatterns = [
    path('api/schema/redoc/', ProtectedRedocView.as_view(url_name='schema'), name='redoc'),
]
```

---

### 📥 Self-hosted version

Default: CDN'dan yuklanadi
```html
<script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
```

Self-hosted (Offline):
```bash
# ReDoc yuklab olish
npm install redoc
# yoki
curl -o redoc.standalone.js https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js
```

```html
<script src="{% static 'js/redoc.standalone.js' %}"></script>
```

---

## ✅ Real Example - Complete Setup

### 1. settings.py

```python
# library_project/settings.py

INSTALLED_APPS = [
    # ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Library API',
    'DESCRIPTION': 'Complete REST API for Library Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # ReDoc settings
    'REDOC_DIST': 'SIDECAR',  # Offline mode
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← Custom templates
        # ...
    },
]
```

---

### 2. urls.py

```python
# library_project/urls.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    
    # Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI (Testing)
    path('api/docs/', 
         SpectacularSwaggerView.as_view(url_name='schema'), 
         name='swagger-ui'
    ),
    
    # ReDoc (Documentation)
    path('api/documentation/', 
         SpectacularRedocView.as_view(
             url_name='schema',
             template_name='redoc.html'
         ), 
         name='redoc'
    ),
]
```

---

### 3. templates/redoc.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Library API - Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }
        
        .custom-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .custom-header h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 700;
        }
        
        .custom-header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <!-- Custom header -->
    <div class="custom-header">
        <h1>📚 Library API Documentation</h1>
        <p>Complete REST API for Library Management System</p>
        <p style="font-size: 14px; margin-top: 15px;">
            Version 1.0.0 | 
            <a href="{% url 'swagger-ui' %}" style="color: white;">Swagger UI</a> | 
            <a href="{% url 'schema' %}" style="color: white;">OpenAPI Schema</a>
        </p>
    </div>
    
    <!-- ReDoc -->
    <redoc 
        spec-url='{% url "schema" %}'
        theme='{
            "colors": {
                "primary": {
                    "main": "#667eea"
                },
                "success": {
                    "main": "#10b981"
                }
            },
            "typography": {
                "fontSize": "16px",
                "lineHeight": "1.6",
                "fontFamily": "Inter, sans-serif",
                "headings": {
                    "fontFamily": "Inter, sans-serif",
                    "fontWeight": "700"
                }
            }
        }'
        hide-download-button
        expand-responses="200,201"
        required-props-first
        sort-props-alphabetically
    ></redoc>
    
    <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

---

## ✅ Xulosa

### Siz nimalarni o'rgandingiz:

1. ✅ **ReDoc nima** - Professional API dokumentatsiya tool
2. ✅ **Setup** - drf-spectacular bilan sozlash
3. ✅ **ReDoc vs Swagger** - Farqlar va qachon ishlatish
4. ✅ **Customization** - Theme, colors, typography
5. ✅ **Options** - Layout va behavior sozlamalari
6. ✅ **Advanced** - Search, responsive, print, deep linking
7. ✅ **Branding** - Custom header va logo

---

### 🎯 Best Practices

1. ✅ **Ikkalasini ham qo'ying:**
   - Swagger UI - Testing uchun
   - ReDoc - Documentation uchun

2. ✅ **Custom template yarating:**
   - Branding qo'shing
   - Company colors
   - Logo va header

3. ✅ **URL naming:**
   - `/api/docs/` - Swagger UI
   - `/api/documentation/` - ReDoc
   - `/api/schema/` - Raw schema

4. ✅ **Production:**
   - Cache'ni yoqing
   - Schema'ni optimize qiling
   - Password protection (internal API)

5. ✅ **Mobile:**
   - Responsive dizayn (default)
   - Test qiling mobile'da

---

### Keyingi qadamlar

1. ✅ Library project'ga ReDoc qo'shing
2. ✅ Custom template yarating
3. ✅ Theme customize qiling
4. ✅ Swagger UI va ReDoc'ni taqqoslang
5. ✅ `homework.md`'ni o'qing

---

**Keyingi:** [homework.md](homework.md) - Uyga vazifa

Happy documenting! 