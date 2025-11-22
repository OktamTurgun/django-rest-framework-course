# 20-dars: Throttling - Uy ishi

## Maqsad
Ushbu uy ishida siz DRF da throttling tizimini amalda qo'llashni o'rganasiz va turli xil throttle strategiyalarini yaratishni mashq qilasiz.

---

## Vazifa 1: Blog API - Basic Throttling (3 ball)

### Tavsif
Blog API yarating va unga basic throttling qo'shing.

### Talablar

**Models:**
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Endpoint lar:**
1. `GET /api/posts/` - Barcha postlar ro'yxati
   - Throttle: 100/hour (anonim), 500/hour (user)

2. `POST /api/posts/` - Yangi post yaratish
   - Throttle: 10/hour (user)

3. `GET /api/posts/{id}/` - Bitta post
   - Throttle: 200/hour (anonim), 1000/hour (user)

4. `POST /api/posts/{id}/comments/` - Komment qo'shish
   - Throttle: 20/hour (user)

### Baholash mezoni
- ✅ Modellar to'g'ri yaratilgan (0.5 ball)
- ✅ ViewSet lar to'g'ri ishlaydi (1 ball)
- ✅ Throttling to'g'ri sozlangan (1 ball)
- ✅ Har xil action lar uchun turli throttle (0.5 ball)

---

## Vazifa 2: E-commerce API - Scoped Throttling (4 ball)

### Tavsif
E-commerce API yarating va turli operatsiyalar uchun turli throttle scope larini qo'llang.

### Talablar

**Models:**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
```

**Endpoint lar va Throttle Scope:**

1. `GET /api/products/` - Mahsulotlar
   - Scope: `product_list` - 1000/hour

2. `GET /api/products/search/` - Qidiruv
   - Scope: `product_search` - 100/minute

3. `POST /api/orders/` - Buyurtma yaratish
   - Scope: `order_create` - 10/hour

4. `GET /api/orders/` - Mening buyurtmalarim
   - Scope: `order_list` - 100/hour

5. `POST /api/orders/{id}/cancel/` - Buyurtmani bekor qilish
   - Scope: `order_cancel` - 5/hour

6. `POST /api/products/{id}/review/` - Sharh yozish
   - Scope: `product_review` - 5/day

### Baholash mezoni
- ✅ Modellar va relatsiyalar to'g'ri (1 ball)
- ✅ Barcha endpoint lar ishlaydi (1 ball)
- ✅ Scope throttling to'g'ri qo'llangan (1.5 ball)
- ✅ Settings.py da scope lar sozlangan (0.5 ball)

---

## Vazifa 3: Custom Throttle - Premium Users (4 ball)

### Tavsif
Foydalanuvchi darajasiga qarab turli xil limitlar qo'yadigan custom throttle yarating.

### Talablar

**User Model Extension:**
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium'),
            ('enterprise', 'Enterprise')
        ],
        default='free'
    )
```

**Custom Throttle:**
Quyidagi limitlar bilan `MembershipThrottle` yarating:
- **Free:** 10 so'rov/soat
- **Basic:** 100 so'rov/soat
- **Premium:** 1000 so'rov/soat
- **Enterprise:** 10000 so'rov/soat

**API:**
1. `GET /api/data/` - Ma'lumotlar olish
   - Throttle: MembershipThrottle

2. `GET /api/profile/quota/` - Quota ma'lumotlari
   - Hozirgi foydalanish va qolgan limitni ko'rsatish

### Baholash mezoni
- ✅ UserProfile modeli to'g'ri (0.5 ball)
- ✅ MembershipThrottle to'g'ri ishlaydi (2 ball)
- ✅ Turli membership lar uchun turli limitlar (1 ball)
- ✅ Quota endpoint ishlaydi (0.5 ball)

---

## Vazifa 4: Advanced - File Upload Throttling (5 ball)

### Tavsif
Fayl yuklash API yarating va fayl hajmiga qarab throttling qo'llang.

### Talablar

**Model:**
```python
class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    size = models.BigIntegerField()  # baytlarda
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

**Custom Throttle:**
`FileSizeThrottle` yarating:
- Har bir foydalanuvchi soatiga 100 MB yuklay oladi
- Har bir fayl hajmi throttle "og'irligiga" ta'sir qiladi
  - 1 MB = 1 birlik
  - 10 MB = 10 birlik
  - va hokazo
- Agar foydalanuvchi 100 MB limitdan oshsa, bloklangan bo'ladi

**API:**
1. `POST /api/upload/` - Fayl yuklash
   - Throttle: FileSizeThrottle
   - File validation (max 20MB per file)

2. `GET /api/upload/stats/` - Yuklash statistikasi
   - Shu soatda yuklangan hajm
   - Qolgan limit
   - Yuklanishlar soni

3. `GET /api/upload/history/` - Yuklash tarixi

### Qo'shimcha talablar
- Custom exception handler yarating
- Agar limit oshsa, qolgan vaqtni ko'rsating
- Response headers ga quota ma'lumotlarini qo'shing

### Baholash mezoni
- ✅ Model va serializer to'g'ri (0.5 ball)
- ✅ FileSizeThrottle to'g'ri ishlaydi (2 ball)
- ✅ Fayl hajmi throttle ga ta'sir qiladi (1 ball)
- ✅ Stats va history endpoint lar (1 ball)
- ✅ Custom exception handler (0.5 ball)

---

## Vazifa 5: Real-world Scenario - API Gateway (4 ball)

### Tavsif
API Gateway yarating va turli xil throttling strategiyalarini birlashtiring.

### Talablar

**Scenario:**
Sizda 3 xil API endpoint bor:
1. Public API - hamma uchun ochiq
2. Partner API - hamkor kompaniyalar uchun
3. Internal API - ichki foydalanuvchilar uchun

**Throttle Strategy:**

**Public API:**
```python
class PublicAPIView(APIView):
    # GET: 1000/day (anonim), 5000/day (user)
    # POST: 100/day (user)
```

**Partner API:**
```python
class PartnerAPIView(APIView):
    # API key orqali autentifikatsiya
    # 10000/day per partner
    # Turli partnerlar uchun turli limitlar
```

**Internal API:**
```python
class InternalAPIView(APIView):
    # JWT token bilan
    # Department ga qarab limit:
    # - Sales: 1000/hour
    # - Support: 5000/hour
    # - Engineering: unlimited
```

**Qo'shimcha:**
- Monitoring dashboard yarating
- Throttle violations log qiling
- Metrics endpoint yarating

### Baholash mezoni
- ✅ Uchta API to'g'ri ishlaydi (1.5 ball)
- ✅ Har xil throttle strategiyalari (1.5 ball)
- ✅ Monitoring va logging (0.5 ball)
- ✅ Metrics endpoint (0.5 ball)

---

## Bonus Vazifa: Testing (2 ball)

### Tavsif
Throttling uchun test yozish.

### Talablar

Quyidagi testlarni yozing:

1. **Test throttle limit:**
   - Limitdan oshganda 429 status qaytarilishini tekshiring

2. **Test throttle reset:**
   - Vaqt o'tgandan keyin throttle reset bo'lishini tekshiring

3. **Test different users:**
   - Har xil foydalanuvchilar uchun alohida limitlar

4. **Test headers:**
   - Response headers da throttle ma'lumotlari borligini tekshiring

5. **Test custom throttle:**
   - Custom throttle to'g'ri ishlashini tekshiring

### Baholash mezoni
- ✅ Kamida 5 ta test (0.5 ball har biri)
- ✅ Testlar o'tadi (0.5 ball)

---

## Topshirish

### Format
```
homework-20-throttling/
├── blog_api/           # Vazifa 1
├── ecommerce_api/      # Vazifa 2
├── premium_api/        # Vazifa 3
├── file_upload_api/    # Vazifa 4
├── api_gateway/        # Vazifa 5
├── tests/              # Bonus
├── README.md           # Loyiha haqida
└── requirements.txt
```

### README.md
Har bir loyihada:
- Loyihani ishga tushirish yo'riqnomasi
- Endpoint lar ro'yxati
- Throttle sozlamalari
- Test qilish yo'riqnomasi

### Deadline
**3 kun ichida**

---

## Baholash tizimi

| Vazifa | Ball | Tavsif |
|--------|------|--------|
| Vazifa 1 | 3 | Basic throttling |
| Vazifa 2 | 4 | Scoped throttling |
| Vazifa 3 | 4 | Custom throttle |
| Vazifa 4 | 5 | Advanced throttling |
| Vazifa 5 | 4 | Real-world scenario |
| **Jami** | **20** | |
| Bonus | 2 | Testing |
| **Maksimal** | **22** | |

### Baholash mezonlari

**18-22 ball:** ⭐⭐⭐⭐⭐ A'lo - Throttling ustasi!
- Barcha vazifalar to'liq bajarilgan
- Code quality yuqori
- Best practices qo'llangan
- Testing qo'shilgan

**14-17 ball:** ⭐⭐⭐⭐ Yaxshi - Ajoyib ish!
- Ko'pchilik vazifalar bajarilgan
- Asosiy tushunchalar tushunilgan
- Yaxshi code yozilgan

**10-13 ball:** ⭐⭐⭐ O'rtacha - Yaxshi urinish
- Asosiy vazifalar bajarilgan
- Ba'zi xatolar bor
- Qo'shimcha ishlash kerak

**0-9 ball:** ⭐⭐ Qayta ishlash kerak
- Ko'p vazifalar bajarilmagan
- Asosiy tushunchalar aniq emas
- Mavzuni qayta o'rganish tavsiya etiladi

---

## Qo'shimcha resurslar

### Foydali havolalar
- [DRF Throttling Documentation](https://www.django-rest-framework.org/api-guide/throttling/)
- [Rate Limiting Best Practices](https://blog.logrocket.com/rate-limiting-django-rest-framework/)
- [Redis for Django Cache](https://github.com/jazzband/django-redis)

### Maslahatlar
1.  Har doim cache backend ni sozlang
2.  Production da Redis ishlatiladi
3.  Throttle exceptions ni to'g'ri handle qiling
4.  Monitoring va logging qo'shing
5.  Test yozishni unutmang
6.  Documentation yozing

---

## Yordam kerakmi?

Agar qiyinchilik bo'lsa:
1. README.md va examples ni qayta o'qing
2. DRF documentation ga qarang
3. Guruhda savol bering
4. Mentor bilan maslahatlashing

**Omad yor bo'lsin!**