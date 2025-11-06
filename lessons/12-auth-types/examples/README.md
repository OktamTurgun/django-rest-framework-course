# Authentication Examples

Bu papkada autentifikatsiya turlari bo'yicha misollar joylashgan.

## Fayllar

### 1. authentication_comparison.py
Barcha autentifikatsiya turlarini taqqoslash va afzalliklari/kamchiliklarini ko'rsatish.

**Ishlatish:**
```bash
python authentication_comparison.py
```

### 2. token_example.py
Token Authentication'ni amalda ko'rsatish. Login, protected endpoint'ga murojaat va logout jarayonlarini namoyish etadi.

**Talablar:**
```bash
pip install requests
```

**Ishlatish:**
```bash
# Avval server ishga tushiring
cd ../code/library-project
python manage.py runserver

# Keyin yangi terminal'da
cd examples
python token_example.py
```

### 3. session_example.py
Session Authentication'ni Django admin orqali ko'rsatish.

**Talablar:**
```bash
pip install requests
```

**Ishlatish:**
```bash
# Avval server ishga tushiring
cd ../code/library-project
python manage.py runserver

# Keyin yangi terminal'da
cd examples
python session_example.py
```

## O'rganish uchun ketma-ketlik

1. **authentication_comparison.py** - Nazariy tushuncha olish
2. **token_example.py** - Token qanday ishlashini ko'rish
3. **session_example.py** - Session qanday ishlashini ko'rish

## Eslatma

Bu misollar faqat o'rganish uchun. Real loyihalarda:
- HTTPS ishlatilishi kerak
- Environment variables'da secret ma'lumotlar
- Token expiration mexanizmi
- Rate limiting
- Proper error handling