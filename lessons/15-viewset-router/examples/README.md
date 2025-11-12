# Examples - ViewSet va Router Misollari

Bu papkada ViewSet va Router bilan ishlashning turli misollarini topasiz.

## Fayllar

### 01-simple-viewset.py
**Mavzu:** Oddiy ModelViewSet

**O'rganasiz:**
- Eng oddiy ViewSet yaratish
- Queryset'ni override qilish
- Serializer'ni dinamik tanlash

**Qachon ishlatiladi:**
- Standart CRUD operatsiyalar kerak bo'lganda
- Tez prototype yaratishda

---

### 02-readonly-viewset.py
**Mavzu:** ReadOnlyModelViewSet va GenericViewSet

**O'rganasiz:**
- Faqat o'qish uchun API
- Mixins bilan custom ViewSet
- Minimal ViewSet yaratish

**Qachon ishlatiladi:**
- Public API (faqat GET)
- Ma'lumotlar katalogi
- Reference data endpoints

---

### 03-custom-actions.py
**Mavzu:** Custom Actions

**O'rganasiz:**
- @action dekorator
- detail=True/False farqi
- Multiple HTTP methods
- Custom permissions
- Custom URL patterns

**Qachon ishlatiladi:**
- Standard CRUD yetmaydi
- Business logic endpoint'lari kerak
- Special operations (publish, archive, etc.)

---

### 04-router-comparison.py
**Mavzu:** Router turlari va sozlamalari

**O'rganasiz:**
- SimpleRouter vs DefaultRouter
- Multiple routers
- Custom basename
- URL prefix
- Trailing slash

**Qachon ishlatiladi:**
- API versiyalash
- Complex URL struktura
- Production vs Development sozlamalar

---

## Qanday ishlatish

### 1. Bitta misol faylini o'qing
```python
# Misol: 01-simple-viewset.py
```

### 2. Asosiy konseptlarni tushuning
- Kod commentlarini o'qing
- Har bir qism nimani qilishini tahlil qiling

### 3. O'z loyihangizda sinab ko'ring
- Misolni copy qiling
- O'z modelingizga moslang
- Test qiling

### 4. Keyingi misolga o'ting

---

## Ketma-ketlik

Agar birinchi marta o'rganayotgan bo'lsangiz:

1.  **01-simple-viewset.py** - Asoslar
2.  **02-readonly-viewset.py** - Variantlar
3.  **03-custom-actions.py** - Ilg'or funksiyalar
4.  **04-router-comparison.py** - Router sozlamalari

---

## Maslahatlar

1. **Har bir misolni alohida sinab ko'ring**
   - Copy-paste qilmang, yozing!
   - Har bir qatorni tushuning

2. **O'z misollaringizni yarating**
   - Darsda o'rgangan narsalarni qo'llang
   - Real loyihangiz uchun moslashtiring

3. **Xatolar bilan ishlashni o'rganing**
   - Xato chiqqanda debug qiling
   - Stack trace'ni o'qishni o'rganing

4. **DRF documentation'ni o'qing**
   - https://www.django-rest-framework.org/
   - Har doim eng yaxshi manba

---

## Savol-javob

**Q: Barcha misollarni ketma-ket o'rganish shartmi?**
A: Yo'q, lekin tavsiya etiladi. Har bir misol avvalgisiga asoslanadi.

**Q: Misollar production-ready?**
A: Yo'q, bu o'quv misollari. Production uchun qo'shimcha xavfsizlik va optimizatsiya kerak.

**Q: Qaysi ViewSet'ni ishlatish kerak?**
A: 
- Standart CRUD → ModelViewSet
- Faqat o'qish → ReadOnlyModelViewSet
- Custom logic → GenericViewSet + Mixins

---

## Foydali havolalar

- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [DRF Routers](https://www.django-rest-framework.org/api-guide/routers/)
- [DRF Actions](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)