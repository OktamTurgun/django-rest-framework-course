# Library Project - Authentication

Bu loyihada autentifikatsiya tizimi qo'shilgan.

## O'rnatish
```bash
pipenv shell
pipenv install
```

## Migratsiya
```bash
python manage.py migrate
```

## Superuser yaratish
```bash
python manage.py createsuperuser
```

## Serverni ishga tushirish
```bash
python manage.py runserver
```

## Endpoints

### Authentication
- POST `/api/accounts/login/` - Login qilish
- POST `/api/accounts/logout/` - Logout qilish
- GET `/api/accounts/me/` - Foydalanuvchi ma'lumotlari

### Books
- GET `/api/books/` - Barcha kitoblar
- GET `/api/books/<id>/` - Bitta kitob
- POST `/api/books/create/` - Kitob yaratish (Auth kerak)
- PUT/PATCH `/api/books/update/<id>/` - Kitobni yangilash (Auth kerak)
- DELETE `/api/books/delete/<id>/` - Kitobni o'chirish (Auth kerak)
- GET `/api/books/protected/` - Test endpoint (Auth kerak)

## Test qilish

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Token bilan so'rov
```bash
curl -X GET http://127.0.0.1:8000/api/books/protected/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```