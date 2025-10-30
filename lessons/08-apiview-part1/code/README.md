# APIView Part 1 - Amaliy kod

Bu papkada APIView bilan ishlaydigan amaliy library-project joylashgan.

## Dars maqsadi

Ushbu darsda biz:
1. Mavjud GenericView'larni APIView ga o'zgartiramiz
2. Request va Response bilan to'g'ri ishlaymiz
3. Status kodlarni to'g'ri qo'llaymiz
4. Custom logika qo'shamiz

## Qadamlar

### 1. Loyihani ishga tushirish

```bash
cd library-project

# Virtual environment faollashtirish (agar kerak bo'lsa)
pipenv shell

# Serverni ishga tushirish
python manage.py runserver
```

### 2. Mavjud viewlar

Hozirda `books/views.py` da GenericView'lar mavjud:
- `BookListView` (ListAPIView)
- `BookDetailView` (RetrieveAPIView)
- `BookCreateView` (CreateAPIView)
- va h.k.

### 3. APIView ga o'zgartirish

Quyidagi qadamlarda biz bu viewlarni APIView yordamida qayta yozamiz.

## O'zgarishlar

### Before (GenericView):
```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### After (APIView):
```python
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
```

## Foydali havolalar

- [Django REST Framework APIView](https://www.django-rest-framework.org/api-guide/views/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [REST API Best Practices](https://restfulapi.net/)

## Keyingi qadam

Darsning asosiy README.md faylini o'qing va ko'rsatmalarga amal qiling.