# CORS Examples

Bu papkada CORS bilan ishlashning turli namunalari keltirilgan.

## Fayllar

1. `01-cors-basics.md` - CORS asoslari va tushunchalar
2. `02-django-cors-setup.py` - Django CORS sozlash
3. `03-cors-configuration.py` - Turli CORS konfiguratsiyalari
4. `04-security-best-practices.md` - Xavfsizlik tavsiyalari
5. `05-frontend-integration.html` - Frontend bilan integratsiya

## Tartib

Fayllarni ketma-ket o'rganib chiqing:

1. **Basics** - CORS nima va qanday ishlaydi
2. **Setup** - Django'da qanday sozlash
3. **Configuration** - Turli holatlar uchun sozlash
4. **Security** - Xavfsizlik jihatlari
5. **Integration** - Frontend bilan ishlash

## Test Qilish

Har bir example'ni o'qib chiqqach, o'zingiz test qilib ko'ring!

### Quick Start

```bash
# 1. Django backend
python manage.py runserver

# 2. Simple HTML test
# 05-frontend-integration.html ni browser'da oching

# 3. CORS headerlarni ko'rish
# Browser DevTools -> Network -> Headers
```

## Foydali Buyruqlar

```bash
# CORS test qilish
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS http://localhost:8000/api/books/

# Response headerlarni ko'rish
curl -I -H "Origin: http://localhost:3000" \
     http://localhost:8000/api/books/
```

**Happy Learning!**