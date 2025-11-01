# Django REST Framework — View’lar bo‘yicha to‘liq qo‘llanma

## Django REST Framework nima?

**Django REST Framework (DRF)** — bu Django framework’ining kengaytmasi bo‘lib, RESTful API’larni yaratishni soddalashtiradi.  
U serializerlar, view’lar, autentifikatsiya, ruxsatlar (permissions) va routing kabi ko‘plab kuchli imkoniyatlarni taqdim etadi.

### Nima uchun o‘rganish kerak?
- Web ilovalar endi **frontend + backend** tarzida bo‘linadi. DRF backend uchun REST API yaratadi.  
- **Mobile app**, **React/Vue frontend**, yoki **tashqi API’lar** DRF orqali backend bilan aloqa qiladi.  
- Kod **modulli, xavfsiz va testlash oson** bo‘ladi.  
- Django’ning qulay ORM tizimi bilan integratsiyalangan.

---

## Django’da View nima?

**View** — bu foydalanuvchidan (yoki API so‘rovdan) kelgan ma’lumotni qabul qilib, unga javob qaytaruvchi qismdir.  
U Django arxitekturasida `MVT` (Model–View–Template) yoki `MVC` (Model–View–Controller) tizimining "View" qismiga to‘g‘ri keladi.

DRF’da View’lar API’lar uchun ishlaydi, ya’ni JSON (yoki XML) formatda javob beradi.

---

## DRF View’lar — turlari va darajalari

| **Daraja** | **Turi** | **Qisqacha tavsif** |
|-------------|-----------|----------------------|
| Boshlang‘ich | FBV / APIView | CRUD’ni qo‘lda yozish |
| O‘rta | GenericAPIView + Mixins | CRUD’ni soddalashtirish |
| Professional | Generic Views (Concrete) | Tayyor CRUD’lar bilan ishlash |
| Ilg‘or | ModelViewSet / ViewSet | Avtomatik routing va to‘liq CRUD |

---

## View’larning to‘liq taqqoslovchi jadvali

| **Turi**                             | **Asosi**                                      | **Tavsif (nima qiladi)**                                                                                                    | **Afzalliklari**                                                       | **Kamchiliklari**                                        | **Qachon ishlatish kerak**                             | **Misol**                                             |
| ------------------------------------ | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------- |
| **1. Function-Based View (FBV)**     | `django.http`                                  | Oddiy funksiya orqali view yoziladi, `request.method` orqali GET, POST, PUT, DELETE ajratiladi.                             | Soddaligi, tushunarli logika                                           | Katta loyihada kod ko‘payadi, qayta ishlatish qiyin      | Kichik loyihalar, o‘rganish bosqichi                   | `def book_list(request): ...`                         |
| **2. Class-Based View (CBV)**        | `django.views`                                 | View sinf ko‘rinishida yoziladi, metodlar orqali (get, post, put, delete) amallar belgilanadi.                              | Kod qayta ishlatiladi, aniq tuzilma                                    | Boshlang‘ichlar uchun murakkabroq                        | Django o‘zining web qismi uchun                        | `class BookView(View): def get(self, request): ...`   |
| **3. APIView**                       | `rest_framework.views.APIView`                 | CBV’ning REST versiyasi. Har bir HTTP metod uchun metod yoziladi (`get`, `post`, `put`, `delete`)                           | So‘rov va javoblar DRF Response bilan ishlaydi, serializer qo‘llanadi  | CRUD’ni qo‘lda yozish kerak                              | REST API boshlang‘ich loyihalar uchun                  | `class BookApiView(APIView): ...`                     |
| **4. GenericAPIView**                | `rest_framework.generics.GenericAPIView`       | APIView’dan voris olgan, qo‘shimcha qulayliklar (queryset, serializer_class, lookup_field) bor                              | DRY tamoyili (kodni qayta ishlatmaslik), serializer bilan integratsiya | CRUD metodlar hali yo‘q — Mixins bilan birga ishlatiladi | Mixins bilan CRUD qilish uchun                         | `class BookGenericView(GenericAPIView): ...`          |
| **5. Mixins**                        | `rest_framework.mixins`                        | CRUD amallarini alohida sinflar sifatida taqdim etadi (`ListModelMixin`, `CreateModelMixin` va h.k.)                        | Qayta ishlatish oson, DRY                                              | Alohida ishlatib bo‘lmaydi — GenericAPIView bilan kerak  | CRUD metodlarini qo‘lda emas, avtomatik qo‘shish uchun | `class BookView(GenericAPIView, ListModelMixin): ...` |
| **6. Generic Views (Concrete View)** | `rest_framework.generics`                      | Mixins va GenericAPIView birlashtirilgan holda tayyor CRUD view’lar (`ListCreateAPIView`, `RetrieveUpdateAPIView`, va h.k.) | CRUD amallari avtomatik, minimal kod                                   | Moslashuvchanligi cheklangan                             | CRUD endpointlar uchun — tez prototiplash              | `class BookListCreateView(ListCreateAPIView): ...`    |
| **7. ViewSet**                       | `rest_framework.viewsets.ViewSet`              | APIView’ga o‘xshaydi, lekin router orqali URL avtomatik generatsiya qiladi                                                  | URL yozishni kamaytiradi, soddalashtiradi                              | Ba’zida ortiqcha moslashuvchanlik                        | O‘rta darajadagi REST API loyihalar uchun              | `class BookViewSet(ViewSet): ...`                     |
| **8. ModelViewSet**                  | `rest_framework.viewsets.ModelViewSet`         | Generic Views + ViewSet birlashmasi — to‘liq CRUD avtomatik                                                                 | CRUD, routing, serializer — hammasi bitta joyda                        | Juda yirik loyihada ba’zida noqulay                      | Tez API yaratish, CRUD’ni to‘liq avtomatlashtirish     | `class BookViewSet(ModelViewSet): ...`                |
| **9. ReadOnlyModelViewSet**          | `rest_framework.viewsets.ReadOnlyModelViewSet` | Faqat `list` va `retrieve` (ya’ni o‘qish) imkonini beradi                                                                   | Faqat o‘qish uchun ideal                                               | CRUD kerak bo‘lsa ishlamaydi                             | Faqat “GET” API’lar uchun                              | `class BookViewSet(ReadOnlyModelViewSet): ...`        |

---

## Xulosa

- **FBV / APIView** — kodni to‘liq nazorat qilish kerak bo‘lsa ishlatiladi.  
- **GenericAPIView + Mixins** — CRUD amallarini soddalashtiradi.  
- **Generic Views (Concrete)** — tez ishlaydigan, tayyor CRUD uchun.  
- **ViewSet / ModelViewSet** — professional REST API yaratish uchun, router bilan birgalikda ishlaydi.  

**Tavsiyam:**  
Boshlanishda `APIView` bilan CRUD yozishni o‘rgan → keyin `GenericAPIView + Mixins` → so‘ng `ModelViewSet` orqali avtomatik CRUD.

---

## Foydali havolalar
-  [Rasmiy DRF hujjati — Views](https://www.django-rest-framework.org/api-guide/views/)
-  [DRF Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
-  [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)

---

✍️ **Muallif:** Uktam Turgun  
🗓 **Tayyorlangan sana:** 2025-11-01  
🏷 **Bo‘lim:** Django REST Framework — Views
