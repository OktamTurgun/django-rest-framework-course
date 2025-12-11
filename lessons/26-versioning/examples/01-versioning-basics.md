# API Versioning Basics

##  Versioning Nima?

**API Versioning** - bu API'ni o'zgartirganingizda eski client'lar ishlay berishini ta'minlash mexanizmi.

---

##  Nima Uchun Kerak?

### Scenario: Mobile App + API

```
2023-01: V1 API ishga tushdi
        Mobile app release qilindi
        10,000 users yuklab oldi

2023-06: Yangi feature kerak - Author as object

Problem: Mobile app'ni hamma user yangilamaydi!
        iOS App Store review - 1 hafta
        Users yangilashni kechiktiradi
        Eski versiya hali ishlatiladi
```

### Yechim: API Versioning

```
V1 API: /api/v1/books/  → Eski format (eski app'lar uchun)
V2 API: /api/v2/books/  → Yangi format (yangi app'lar uchun)

Natija: Ikkala app ham ishlaydi! ✅
```

---

##  Breaking vs Non-Breaking Changes

### ✅ Non-Breaking Changes (Xavfsiz)

```json
// ✅ 1. Yangi optional field
// V1
{
    "id": 1,
    "title": "Django Book",
    "author": "John Doe"
}

// V1.1 (yangi field, lekin optional)
{
    "id": 1,
    "title": "Django Book",
    "author": "John Doe",
    "isbn": "1234567890"  // YANGI, lekin optional
}
```

```json
// ✅ 2. Response'ga qo'shimcha ma'lumot
// V1
{
    "results": [...]
}

// V1.1
{
    "results": [...],
    "meta": {  // YANGI metadata
        "total": 100,
        "page": 1
    }
}
```

```python
# ✅ 3. Yangi endpoint
GET /api/books/           # Mavjud
GET /api/books/popular/   # YANGI endpoint
```

```json
// ✅ 4. Yangi default value
// POST /api/books/
{
    "title": "Book",
    "status": "draft"  // Default qiymat bilan
}
```

### ❌ Breaking Changes (Versioning Kerak)

```json
// ❌ 1. Field type o'zgarishi
// V1
{
    "price": 29.99  // number
}

// V2
{
    "price": "29.99"  // string ❌ BREAK!
}
```

```json
// ❌ 2. Field nomini o'zgartirish
// V1
{
    "author": "John Doe"
}

// V2
{
    "author_name": "John Doe"  // ❌ BREAK!
}
```

```json
// ❌ 3. Field strukturasini o'zgartirish
// V1
{
    "author": "John Doe"  // string
}

// V2
{
    "author": {  // object ❌ BREAK!
        "id": 1,
        "name": "John Doe"
    }
}
```

```json
// ❌ 4. Field o'chirish
// V1
{
    "id": 1,
    "title": "Book",
    "author": "John"
}

// V2
{
    "id": 1,
    "title": "Book"
    // author yo'q! ❌ BREAK!
}
```

```json
// ❌ 5. Yangi required field
// V1 POST
{
    "title": "Book"
}

// V2 POST
{
    "title": "Book",
    "isbn": "123"  // ❌ REQUIRED! BREAK!
}
```

```python
# ❌ 6. Endpoint o'chirish
GET /api/books/  # V1'da mavjud
GET /api/books/  # V2'da 404 ❌ BREAK!
```

```json
// ❌ 7. Status code o'zgarishi
// V1
POST /api/books/ → 200 OK

// V2
POST /api/books/ → 201 Created  // ❌ BREAK!
```

---

##  Semantic Versioning

Format: **MAJOR.MINOR.PATCH**

```
v2.1.3
│ │ │
│ │ └─ PATCH: Bug fixes (backward compatible)
│ └─── MINOR: New features (backward compatible)
└───── MAJOR: Breaking changes (NOT backward compatible)
```

### Misollar:

| Change | Old | New | Tavsif |
|--------|-----|-----|--------|
| Bug fix | v1.0.0 | v1.0.1 | Price calculation fix |
| New feature | v1.0.1 | v1.1.0 | Book reviews endpoint |
| Breaking | v1.1.0 | v2.0.0 | Author as object |

### API Versioning'da:

Ko'pincha faqat **MAJOR** version ishlatiladi:

```
v1, v2, v3, v4...
```

Sabab:
- API client'lar faqat major breaking changes bilan qiziqadi
- Minor/Patch o'zgarishlar backward compatible
- URL sodda qoladi

---

##  Version Lifecycle

### Typical Timeline:

```
┌─────────────────────────────────────────────────┐
│  v1.0 Release                                   │
│  2023-01-01                                     │
└─────────────────────────────────────────────────┘
           │
           │ (6 months development)
           ▼
┌─────────────────────────────────────────────────┐
│  v2.0 Release (Beta)                            │
│  2023-06-01                                     │
│  v1 still active                                │
└─────────────────────────────────────────────────┘
           │
           │ (1 month beta testing)
           ▼
┌─────────────────────────────────────────────────┐
│  v2.0 Stable                                    │
│  2023-07-01                                     │
│  v1 DEPRECATED (Warning added)                  │
└─────────────────────────────────────────────────┘
           │
           │ (6 months deprecation period)
           ▼
┌─────────────────────────────────────────────────┐
│  v1 SUNSET                                      │
│  2024-01-01                                     │
│  v1 returns 410 Gone                            │
│  v2 active                                      │
└─────────────────────────────────────────────────┘
```

### Support Policy:

```
Active Support:     2 years
Deprecation Period: 6-12 months
Total Lifetime:     2.5-3 years
```

---

##  Versioning Strategies

### 1. URL Path Versioning (Most Popular)

```
GET /api/v1/books/
GET /api/v2/books/
```

**Used by:** Twitter, Stripe, GitHub

**✅ Pros:**
- Ko'rinadi va aniq
- Browser'da test qilish oson
- Documentation'da aniq
- Cache friendly

**❌ Cons:**
- URL o'zgaradi
- Routing murakkab bo'lishi mumkin

---

### 2. Query Parameter

```
GET /api/books/?version=1
GET /api/books/?version=2
```

**Used by:** Google APIs (ba'zi)

**✅ Pros:**
- URL path o'zgarishsiz
- Ixtiyoriy (optional)

**❌ Cons:**
- Oson unutiladi
- Default version kerak
- Cache muammolari

---

### 3. Accept Header

```http
GET /api/books/
Accept: application/vnd.myapp.v1+json

GET /api/books/
Accept: application/vnd.myapp.v2+json
```

**Used by:** GitHub API

**✅ Pros:**
- RESTful
- URL clean
- HTTP standard

**❌ Cons:**
- Ko'rinmas (hidden)
- Browser test qiyin
- Documentation murakkab

---

### 4. Custom Header

```http
GET /api/books/
API-Version: 1

GET /api/books/
API-Version: 2
```

**Used by:** Microsoft APIs

**✅ Pros:**
- Sodda
- Explicit

**❌ Cons:**
- Non-standard
- Har safar header qo'shish kerak

---

### 5. Subdomain

```
https://api-v1.example.com/books/
https://api-v2.example.com/books/
```

**Used by:** AWS (ba'zi xizmatlari)

**✅ Pros:**
- Version'lar to'liq alohida
- Load balancing oson
- Monitoring sodda

**❌ Cons:**
- DNS configuration
- SSL certificates
- Infrastructure murakkab

---

##  Qaysi Strategiyani Tanlash?

### Recommendation Matrix:

| Project Type | Recommended | Why |
|--------------|-------------|-----|
| Public API | URL Path | Clear, standard, easy |
| Internal API | URL Path or Header | Team preference |
| REST Purist | Accept Header | RESTful standard |
| Simple API | URL Path | Easiest to implement |
| Enterprise | Subdomain | Separate infrastructure |

### Most Common: URL Path Versioning

```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

---

##  Real-World Examples

### Twitter API
```
https://api.twitter.com/2/tweets
                        ↑
                    Version 2
```

### Stripe API
```
https://api.stripe.com/v1/customers
```

### GitHub API
```
GET https://api.github.com/repos/owner/repo
Accept: application/vnd.github.v3+json
```

### AWS EC2
```
https://ec2.amazonaws.com/?Version=2016-11-15
```

---

##  Anti-Patterns (Qilmang!)

### ❌ Date-Based Versioning
```
/api/2023-01-15/books/
/api/2023-06-01/books/
```

**Muammo:** Ma'no yo'q, chalkash

---

### ❌ Juda Ko'p Version'lar
```
/api/v1/books/
/api/v1.1/books/
/api/v1.2/books/
/api/v2/books/
/api/v2.1/books/
```

**Muammo:** Support qiyin, client'lar chalkashadi

---

### ❌ Version'siz API
```
/api/books/  // Version yo'q!
```

**Muammo:** Breaking change qilish imkonsiz

---

## ✅ Best Practices

### 1. Start with Versioning

```python
# ✅ Birinchi kundan versioning
/api/v1/books/

# ❌ Keyin qo'shish qiyin
/api/books/  → /api/v2/books/ ???
```

### 2. Document Everything

```markdown
# API Changelog

## v2.0.0 (2023-07-01)
### Breaking Changes
- `author` is now object (was string)
- `isbn` is now required

### New Features
- Book reviews endpoint
- Pagination improvements
```

### 3. Clear Deprecation

```http
HTTP/1.1 200 OK
Warning: 299 - "API v1 deprecated. Migrate to v2 by 2024-12-31"
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
```

### 4. Long Deprecation Period

```
Minimum: 6 months
Recommended: 12 months
Enterprise: 24 months
```

### 5. Clear Migration Guide

```markdown
# Migration: V1 → V2

## Author Field
**Before (V1):**
```json
{"author": "John Doe"}
```

**After (V2):**
```json
{"author": {"id": 1, "name": "John Doe"}}
```

**Code Change:**
```javascript
// V1
const name = book.author;

// V2
const name = book.author.name;
```
```

---

##  Key Takeaways

1. **Versioning** - client'larni breaking changes'dan himoya qilish
2. **Breaking changes** - yangi version talab qiladi
3. **Non-breaking** - mavjud version'ga qo'shish mumkin
4. **URL path** - eng ko'p ishlatiladigan
5. **Deprecation** - 6-12 oy oldin warning
6. **Documentation** - har bir o'zgarishni yozish
7. **Migration guide** - client'larga yordam

---

##  Next Steps

Keyingi example'larga o'ting:
- `02-url-versioning.py` - URL versioning implementation
- `03-header-versioning.py` - Header-based versioning
- `04-namespace-versioning.py` - Django namespaces
- `05-migration-strategies.md` - Migration best practices
- `06-best-practices.md` - Production tips