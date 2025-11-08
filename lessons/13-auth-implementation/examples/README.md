# Authentication Examples

Bu papkada authentication bilan bog'liq misollar joylashgan.

## Fayllar

1. **token_auth_example.py** - Token Authentication asoslari
2. **custom_permissions_example.py** - Custom permission class'lar
3. **jwt_auth_example.py** - JWT Authentication misoli

## Ishlatish

Har bir fayl mustaqil example bo'lib, uni o'rganish va test qilish mumkin.
```bash
# Virtual muhitni ishga tushiring
pipenv shell

# Django shell ochish
python manage.py shell

# Example kodni run qilish
exec(open('examples/token_auth_example.py').read())
```

## Eslatma

Bu fayllar faqat o'rganish uchun. Real loyihada `accounts/views.py` va `books/views.py` ishlatiladi.