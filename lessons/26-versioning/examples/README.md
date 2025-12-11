# API Versioning Examples

Bu papkada API versioning'ning turli namunalari keltirilgan.

## Fayllar

1. `01-versioning-basics.md` - Versioning asoslari va tushunchalar
2. `02-url-versioning.py` - URL path versioning
3. `03-header-versioning.py` - Header-based versioning
4. `04-namespace-versioning.py` - Django namespace versioning
5. `05-migration-strategies.md` - Migration strategiyalari
6. `06-best-practices.md` - Versioning best practices

## Tartib

Fayllarni ketma-ket o'rganib chiqing:

1. **Basics** - Versioning nima va nima uchun kerak
2. **URL Versioning** - Eng ko'p ishlatiladigan usul
3. **Header Versioning** - RESTful yondashuv
4. **Namespace Versioning** - Django-specific
5. **Migration** - Version'lar o'rtasida o'tish
6. **Best Practices** - Real-world tavsiyalar

## Quick Start

```bash
# Django server
python manage.py runserver

# Test V1
curl http://localhost:8000/api/v1/books/

# Test V2
curl http://localhost:8000/api/v2/books/
```

## Key Concepts

### Breaking Changes
```python
# ❌ Breaking: Field type changed
v1: "price": 29.99
v2: "price": "29.99"

# ❌ Breaking: Field removed
v1: "author": "John"
v2: # author field yo'q!
```

### Non-Breaking Changes
```python
# ✅ Safe: New optional field
v1: {"title": "Book"}
v2: {"title": "Book", "isbn": "123"}  # optional

# ✅ Safe: New endpoint
v2: GET /api/books/statistics/  # new
```

**Happy Learning!**