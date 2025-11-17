# Examples: Nested Serializers & Relations

Ushbu papkada **Nested Serializers** mavzusi bo'yicha amaliy misollar keltirilgan.

---

## Fayllar

### 1. `01-basic-nested.py`
- Asosiy nested serializer misoli
- ForeignKey relation
- Read-only nested serializer

### 2. `02-serializer-relations.py`
- PrimaryKeyRelatedField
- StringRelatedField
- SlugRelatedField
- HyperlinkedRelatedField
- Har bir relationning qachon ishlatilishi

### 3. `03-many-to-many.py`
- ManyToManyField bilan ishlash
- Nested many-to-many serializer
- Through model bilan murakkab bog'lanishlar

### 4. `04-writable-nested.py`
- Writable nested serializer
- `create()` metodini override qilish
- `update()` metodini override qilish
- Nested objectlarni yaratish va yangilash

---

## Qanday ishlatish

Har bir faylda to'liq ishlaydigan kod misollari keltirilgan. Ularni o'z projectingizga copy-paste qilishingiz mumkin:

```bash
# Misol uchun:
python 01-basic-nested.py
```

Yoki kodlarni `books/serializers.py` va `books/views.py` ga qo'shishingiz mumkin.

---

## Eslatma

Bu misollar faqat o'rganish uchun mo'ljallangan. Real projectda ularni o'z ehtiyojingizga moslashtirishingiz kerak.

---

## Qo'shimcha resurslar

- [DRF Official Docs - Relations](https://www.django-rest-framework.org/api-guide/relations/)
- [Classy DRF - Serializers](https://www.cdrf.co/)