# Uyga vazifa: Autentifikatsiya

## 1-topshiriq: Books CRUD'ga autentifikatsiya qo'shish

`books/views.py` faylidagi barcha CRUD operatsiyalariga to'g'ri permission'lar qo'shing:

- **BookListAPIView**: Hamma ko'rishi mumkin (autentifikatsiya shart emas)
- **BookDetailAPIView**: Hamma ko'rishi mumkin
- **BookCreateAPIView**: Faqat autentifikatsiya qilingan foydalanuvchilar
- **BookUpdateAPIView**: Faqat autentifikatsiya qilingan foydalanuvchilar
- **BookDeleteAPIView**: Faqat autentifikatsiya qilingan foydalanuvchilar

**Maslahat:** `IsAuthenticatedOrReadOnly` va `IsAuthenticated` permission'laridan foydalaning.

## 2-topshiriq: Token bilan test qilish

1. Postman yoki cURL yordamida login qiling
2. Olingan token bilan kitob yaratishni sinab ko'ring
3. Token'siz kitob yaratishga harakat qiling (xato berishi kerak)
4. Token bilan kitobni o'zgartiring
5. Logout qiling va token ishlamasligini tekshiring

## 3-topshiriq: Qo'shimcha endpoint

`accounts/views.py` ga yangi endpoint qo'shing:

- **ChangePasswordView**: Foydalanuvchi parolini o'zgartirish
  - Faqat autentifikatsiya qilingan foydalanuvchilar
  - Eski parolni tekshirish
  - Yangi parolni saqlash

## Topshirish

Branch yarating: `lesson-12-homework`
GitHub'ga push qiling va Pull Request oching.

## Qo'shimcha ball

Token expiration (muddati tugashi) mexanizmini qo'shib ko'ring!