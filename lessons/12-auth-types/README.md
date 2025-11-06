# 12-dars: Autentifikatsiya turlari

Bu darsda Django REST Framework'dagi autentifikatsiya turlarini o'rganamiz.

## Dars maqsadi

- Autentifikatsiya va Authorization farqini tushunish
- SessionAuthentication bilan tanishish
- BasicAuthentication'ni o'rganish
- TokenAuthentication'ni amalda qo'llash
- Login/Logout endpoint'larini yaratish

## Dars tarkibi

- `code/` - Amaliy kod
- `examples/` - Misollar
- `homework.md` - Uyga vazifa

## Ishga tushirish
```bash
cd code/library-project
pipenv shell
pipenv install
python manage.py migrate
python manage.py runserver
```

## Darsdan keyin bilishingiz kerak

- ✅ Autentifikatsiya nima
- ✅ DRF'da qanday autentifikatsiya turlari bor
- ✅ Token Authentication qanday ishlaydi
- ✅ Login/Logout qanday qilinadi