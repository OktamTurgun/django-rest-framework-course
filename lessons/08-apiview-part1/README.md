# 08 - APIView Asoslari - Part 1

## Mundarija
- [Kirish](#kirish)
- [APIView nima?](#apiview-nima)
- [GenericView vs APIView](#genericview-vs-apiview)
- [Request va Response](#request-va-response)
- [Status kodlar](#status-kodlar)
- [Amaliy misol](#amaliy-misol)
- [Xulosa](#xulosa)

---

## Darsdan kutilgan natijalar

Siz ushbu darsni tugatgandan so'ng:
- ✅ APIView nima ekanligini tushunasiz
- ✅ Request va Response obyektlari bilan ishlay olasiz
- ✅ Status kodlarni to'g'ri qo'llay olasiz
- ✅ APIView yordamida oddiy API yarata olasiz
- ✅ GenericView va APIView o'rtasidagi farqni bilasiz

---

## Kirish

Oldingi darslarimizda biz **GenericView**lar bilan ishladik (ListAPIView, RetrieveAPIView va boshqalar). Bu viewlar bizga ko'p funksiyalarni avtomatik bajarib berdi. Lekin ba'zan bizga to'liq nazorat kerak bo'ladi - aynan shu paytda **APIView** yordam beradi.

---

## APIView nima?

**APIView** - bu Django REST Framework ning eng asosiy view klassi. U bizga HTTP so'rovlari ustida to'liq nazorat beradi.

### APIView ning asosiy xususiyatlari:

1. **To'liq nazorat** - har bir HTTP metodini (GET, POST, PUT, DELETE) o'zingiz yozasiz
2. **Moslashuvchanlik** - istalgan mantiqni qo'sha olasiz
3. **DRF funksiyalari** - DRF ning barcha imkoniyatlaridan foydalanasiz

### Oddiy kod misoli:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloAPIView(APIView):
    """
    Oddiy APIView misoli
    """
    def get(self, request):
        """GET so'roviga javob"""
        data = {
            'message': 'Salom, APIView!',
            'method': 'GET'
        }
        return Response(data)
    
    def post(self, request):
        """POST so'roviga javob"""
        data = {
            'message': 'Ma\'lumot qabul qilindi',
            'received': request.data
        }
        return Response(data, status=status.HTTP_201_CREATED)
```

---

## GenericView vs APIView

### GenericView (masalan, ListAPIView)

**Afzalliklari:**
- ✅ Tez va oson
- ✅ Kod kamroq
- ✅ Standard CRUD operatsiyalar uchun ideal

**Kamchiliklari:**
- ❌ Cheklangan moslashuvchanlik
- ❌ Murakkab mantiq uchun mos emas

```python
# GenericView misoli
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Faqat 3 qator kod!
```

### APIView

**Afzalliklari:**
- ✅ To'liq nazorat
- ✅ Har qanday mantiqni amalga oshirish mumkin
- ✅ Murakkab biznes logika uchun ideal

**Kamchiliklari:**
- ❌ Ko'proq kod yozish kerak
- ❌ Barcha narsani o'zingiz qilishingiz kerak

```python
# APIView misoli
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    # Ko'proq kod, lekin ko'proq nazorat!
```

### Qachon nimani ishlatish?

| Vazifa | Tavsiya |
|--------|---------|
| Oddiy CRUD operatsiyalar | **GenericView** ishlatish |
| Murakkab biznes logika | **APIView** ishlatish |
| Maxsus filter/validation | **APIView** ishlatish |
| Standart REST API | **GenericView** ishlatish |
| Ko'p modellar bilan ishlash | **APIView** ishlatish |

---

## Request va Response

### 🔷 Request obyekti

DRF ning `Request` obyekti Django ning oddiy request obyektini kengaytiradi va ko'proq imkoniyatlar beradi.

#### Request ning asosiy xususiyatlari:

```python
class ExampleView(APIView):
    def post(self, request):
        # 1. request.data - JSON, form yoki file data
        username = request.data.get('username')
        
        # 2. request.query_params - URL parametrlari (?page=1&sort=name)
        page = request.query_params.get('page', 1)
        
        # 3. request.method - HTTP metodi (GET, POST, PUT, DELETE)
        method = request.method
        
        # 4. request.user - autentifikatsiya qilingan foydalanuvchi
        user = request.user
        
        # 5. request.auth - autentifikatsiya tokeni
        token = request.auth
        
        return Response({'status': 'success'})
```

#### Django Request vs DRF Request

| Xususiyat | Django Request | DRF Request |
|-----------|----------------|-------------|
| JSON parsing | ❌ Manual | ✅ Avtomatik |
| Form data | ✅ POST | ✅ data |
| File uploads | ✅ FILES | ✅ data |
| Query params | ✅ GET | ✅ query_params |
| Authentication | ⚠️ Cheklangan | ✅ To'liq qo'llab-quvvatlash |

### Response obyekti

DRF ning `Response` obyekti avtomatik ravishda ma'lumotlarni JSON formatiga o'giradi.

```python
from rest_framework.response import Response
from rest_framework import status

class BookDetailView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            
            # Oddiy response
            return Response(serializer.data)
            
        except Book.DoesNotExist:
            # Xato bilan response
            return Response(
                {'error': 'Kitob topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            # Muvaffaqiyatli response
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        # Validation xatolari bilan response
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
```

---

## Status kodlar

HTTP status kodlari serverning javob holatini bildiradi. DRF ularni oson ishlatish uchun konstantalar taqdim etadi.

### Muvaffaqiyatli javoblar (2xx)

```python
from rest_framework import status

# 200 OK - standart muvaffaqiyatli javob
status.HTTP_200_OK

# 201 CREATED - yangi resurs yaratildi
status.HTTP_201_CREATED

# 204 NO CONTENT - muvaffaqiyatli, lekin javob yo'q (DELETE uchun)
status.HTTP_204_NO_CONTENT
```

**Misol:**
```python
class BookCreateView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED  # 201 qaytaramiz
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Mijoz xatolari (4xx)

```python
# 400 BAD REQUEST - noto'g'ri so'rov
status.HTTP_400_BAD_REQUEST

# 401 UNAUTHORIZED - autentifikatsiya talab qilinadi
status.HTTP_401_UNAUTHORIZED

# 403 FORBIDDEN - ruxsat yo'q
status.HTTP_403_FORBIDDEN

# 404 NOT FOUND - resurs topilmadi
status.HTTP_404_NOT_FOUND

# 405 METHOD NOT ALLOWED - metod ruxsat berilmagan
status.HTTP_405_METHOD_NOT_ALLOWED
```

**Misol:**
```python
class BookDetailView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Kitob topilmadi'},
                status=status.HTTP_404_NOT_FOUND  # 404 qaytaramiz
            )
```

### Server xatolari (5xx)

```python
# 500 INTERNAL SERVER ERROR - server xatosi
status.HTTP_500_INTERNAL_SERVER_ERROR

# 503 SERVICE UNAVAILABLE - xizmat mavjud emas
status.HTTP_503_SERVICE_UNAVAILABLE
```

### Status kodlar qo'llanma jadvali

| Kod | Konstanta | Ishlatish |
|-----|-----------|-----------|
| 200 | `HTTP_200_OK` | GET, PUT - muvaffaqiyatli |
| 201 | `HTTP_201_CREATED` | POST - yaratildi |
| 204 | `HTTP_204_NO_CONTENT` | DELETE - o'chirildi |
| 400 | `HTTP_400_BAD_REQUEST` | Validation xatosi |
| 401 | `HTTP_401_UNAUTHORIZED` | Login kerak |
| 403 | `HTTP_403_FORBIDDEN` | Ruxsat yo'q |
| 404 | `HTTP_404_NOT_FOUND` | Topilmadi |
| 500 | `HTTP_500_INTERNAL_SERVER_ERROR` | Server xatosi |

---

## Amaliy misol

Keling, to'liq CRUD operatsiyalarni APIView bilan yozamiz:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(APIView):
    """
    Kitoblar ro'yxati va yangi kitob yaratish
    """
    
    def get(self, request):
        """
        Barcha kitoblarni olish
        GET /api/books/
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Yangi kitob yaratish
        POST /api/books/
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookDetailView(APIView):
    """
    Bitta kitob bilan ishlash (olish, yangilash, o'chirish)
    """
    
    def get_object(self, pk):
        """Kitobni ID orqali topish yoki 404 qaytarish"""
        return get_object_or_404(Book, pk=pk)
    
    def get(self, request, pk):
        """
        Bitta kitobni olish
        GET /api/books/1/
        """
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Kitobni to'liq yangilash
        PUT /api/books/1/
        """
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self, request, pk):
        """
        Kitobni qisman yangilash
        PATCH /api/books/1/
        """
        book = self.get_object(pk)
        serializer = BookSerializer(
            book,
            data=request.data,
            partial=True  # Qisman yangilash
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        """
        Kitobni o'chirish
        DELETE /api/books/1/
        """
        book = self.get_object(pk)
        book.delete()
        return Response(
            {'message': 'Kitob muvaffaqiyatli o\'chirildi'},
            status=status.HTTP_204_NO_CONTENT
        )
```

### URLs konfiguratsiyasi:

```python
# books/urls.py
from django.urls import path
from .views import BookListCreateView, BookDetailView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
```

---

## APIView ning asosiy printsiplari

### 1. Har bir HTTP metodi - alohida method

```python
class MyView(APIView):
    def get(self, request):      # GET so'rovlar
        pass
    
    def post(self, request):     # POST so'rovlar
        pass
    
    def put(self, request, pk):  # PUT so'rovlar
        pass
    
    def delete(self, request, pk):  # DELETE so'rovlar
        pass
```

### 2. Har doim Response qaytarish

```python
# ✅ To'g'ri
return Response(data)

# ❌ Noto'g'ri
return data  # Bu ishlamaydi!
```

### 3. Status kodlarni to'g'ri ishlatish

```python
# ✅ To'g'ri
return Response(data, status=status.HTTP_201_CREATED)

# ⚠️ Ishlaydi, lekin tavsiya etilmaydi
return Response(data, status=201)
```

### 4. Xatolarni to'g'ri qaytarish

```python
try:
    book = Book.objects.get(pk=pk)
    # ...
except Book.DoesNotExist:
    return Response(
        {'error': 'Kitob topilmadi'},
        status=status.HTTP_404_NOT_FOUND
    )
```

---

## Xulosa

### Nima o'rgandik:

1. **APIView** - DRF ning eng asosiy va moslashuvchan view klassi
2. **Request** - DRF ning kengaytirilgan request obyekti
3. **Response** - Avtomatik JSON konversiya
4. **Status kodlar** - To'g'ri HTTP javoblar
5. **CRUD** - APIView bilan to'liq CRUD operatsiyalar

### 🔄 GenericView vs APIView:

- **GenericView** → Tez va oddiy, standart vazifalar uchun
- **APIView** → To'liq nazorat, murakkab vazifalar uchun

### Keyingi darsda:

- APIView bilan murakkab misollar
- Custom permission va authentication
- Pagination va filtering
- Exception handling

---

## Qo'shimcha materiallar

- [DRF APIView Documentation](https://www.django-rest-framework.org/api-guide/views/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Best Practices](https://restfulapi.net/)