# Lesson 04: Homework - ListAPIView

## Topshiriq 1: Authors API yarating
Books app ichida Author modelini yarating va uning uchun ListAPIView yozing.

**Talablar:**
- Author modeli: name, bio, birth_date
- AuthorSerializer yarating
- AuthorListView (ListAPIView) yarating
- `/api/authors/` endpoint qo'shing

## Topshiriq 2: Filtering qo'shing
BookListView ga qidiruv funksiyasini qo'shing.

**Talablar:**
- Kitobni title bo'yicha qidirish
- URL parameter: `/api/books/?search=Django`
- DRF'ning `filter_backends` ishlatish

## Topshiriq 3: Pagination
Kitoblar ro'yxatiga pagination qo'shing.

**Talablar:**
- PageNumberPagination ishlatish
- Har bir sahifada 5 ta kitob
- Response da next/previous linklar

## Topshiriq 4: Testing
API uchun testlar yozing.

**Talablar:**
- Test 1: Bo'sh ro'yxat qaytarish
- Test 2: 3 ta kitob yaratib, API orqali olish
- Test 3: Response format to'g'riligini tekshirish

## Bonus topshiriq 🌟
Book va Author o'rtasida ManyToMany relationship yarating (bir kitobning bir necha mualliflari bo'lishi mumkin).

**Talablar:**
- Book modeliga authors field qo'shing
- BookSerializer da author ma'lumotlarini ham ko'rsating
- Nested serialization ishlatish

## Topshiriqni topshirish
1. Yangi branch yarating: `homework-04-your-name`
2. Barcha topshiriqlarni bajaring
3. Commit va push qiling
4. Pull Request yarating

Omad! 🚀