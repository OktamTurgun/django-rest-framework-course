# 01. API bilan tanishuv

> Web dasturlash sohasida API - bu dasturlar o'rtasidagi muloqot tili

## 🎯 Dars maqsadlari

Ushbu darsdan keyin siz quyidagilarni bilib olasiz:
- [ ] API nima va nima uchun kerak ekanligini
- [ ] RESTful API tamoyillarini
- [ ] Client-Server arxitekturasini
- [ ] API'ning real hayotdagi qo'llanilishini

## ⏱ Taxminiy vaqt: 30-40 daqiqa

---

## 📚 Nazariya

### API nima?

**API** (Application Programming Interface) - bu dasturlar o'rtasidagi muloqot qoidalari to'plami.

#### Hayotiy misol:

Restoranga tashrif buyurganingizni tasavvur qiling:

- **Siz (Client)** - Ovqat buyurtma qilmoqchisiz
- **Ofitsiant (API)** - Sizning buyurtmangizni oshxonaga yetkazadi
- **Oshxona (Server)** - Ovqat tayyorlaydi
- **Ofitsiant (API)** - Tayyor ovqatni sizga olib keladi

API xuddi ofitsiant kabi ishlaydi - sizning so'rovingizni serverga yetkazadi va javobni qaytaradi.

### Web API turlari

1. **REST API** - Eng mashhur, sodda va tushunarliroq
2. **SOAP API** - Eski, murakkab
3. **GraphQL** - Zamonaviy, moslashuvchan
4. **gRPC** - Tezkor, mikroservislar uchun

Biz kursda **REST API** bilan ishlaymiz.

---

### RESTful API nima?

**REST** (Representational State Transfer) - bu web servislar yaratish uchun arxitektura uslubi.

#### REST asosiy tamoyillari:

1. **Client-Server arxitektura**
   - Client va Server bir-biridan mustaqil
   - Ular faqat HTTP orqali muloqot qiladi

2. **Stateless (Holatsiz)**
   - Har bir so'rov mustaqil
   - Server oldingi so'rovlarni eslamaydi
   - Har bir so'rov to'liq ma'lumotni o'z ichiga oladi

3. **Cacheable (Keshlanuvchi)**
   - Ma'lumotlar keshlanishi mumkin
   - Bu tezlikni oshiradi

4. **Uniform Interface (Yagona interfeys)**
   - Barcha resurslar bir xil tarzda ishlatiladi
   - Standart HTTP metodlar ishlatiladi

5. **Layered System (Qatlamli tizim)**
   - Client serverning ichki tuzilishini bilmasligi kerak
   - Oraliq serverlar (proxy, load balancer) bo'lishi mumkin

---

### HTTP va API

API HTTP protokoli orqali ishlaydi. HTTP - bu brauzer va server o'rtasidagi muloqot tili.

#### HTTP tuzilishi:

```
REQUEST (So'rov)
↓
GET /api/users HTTP/1.1
Host: example.com
Authorization: Bearer token123

↓
RESPONSE (Javob)
↓
HTTP/1.1 200 OK
Content-Type: application/json

{
  "users": [...]
}
```

---

## 💻 Amaliyot

### 1-mashq: Birinchi API so'rov (JSONPlaceholder)

JSONPlaceholder - bu bepul test API xizmati. Uni API'larni o'rganish uchun ishlatish mumkin.

**Vazifa:** Brauzerda quyidagi URLni oching:

```
https://jsonplaceholder.typicode.com/users
```

**Natija:**

```json
[
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    ...
  },
  ...
]
```

Bu yerda:
- **Endpoint:** `/users`
- **Method:** GET (brauzer avtomatik GET ishlatadi)
- **Response:** JSON formatda foydalanuvchilar ro'yxati

---

### 2-mashq: Python bilan API so'rov

Python'da `requests` kutubxonasi yordamida API'ga so'rov yuboramiz.

**Kod:**

```python
import requests

# API endpoint
url = "https://jsonplaceholder.typicode.com/users"

# GET so'rov yuborish
response = requests.get(url)

# Status kodni tekshirish
print(f"Status Code: {response.status_code}")

# Ma'lumotni JSON formatda olish
data = response.json()

# Birinchi foydalanuvchini chiqarish
print(f"Birinchi foydalanuvchi: {data[0]['name']}")
```

**Natija:**

```
Status Code: 200
Birinchi foydalanuvchi: Leanne Graham
```

**Tushuntirish:**
1. `requests.get(url)` - GET so'rov yuboradi
2. `response.status_code` - Server javob kodi (200 = muvaffaqiyatli)
3. `response.json()` - JSON ma'lumotni Python dictionary'ga aylantiradi

---

### 3-mashq: Bitta foydalanuvchini olish

**Vazifa:** ID=1 bo'lgan foydalanuvchini oling.

<details>
<summary>💡 Ko'rsatma (bosing)</summary>

URL oxiriga ID qo'shing:
```
https://jsonplaceholder.typicode.com/users/1
```

</details>

<details>
<summary>✅ Yechim (bosing)</summary>

```python
import requests

user_id = 1
url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

response = requests.get(url)

if response.status_code == 200:
    user = response.json()
    print(f"Ism: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Telefon: {user['phone']}")
else:
    print("Xato yuz berdi!")
```

**Natija:**
```
Ism: Leanne Graham
Email: Sincere@april.biz
Telefon: 1-770-736-8031 x56442
```

</details>

---

## 🔥 Real misol - Ob-havo API

Real loyihalarda API qanday ishlatilishini ko'ramiz.

**Misol:** OpenWeatherMap API orqali ob-havo ma'lumotlarini olish

```python
import requests

# API key (ro'yxatdan o'tib oling: openweathermap.org)
api_key = "YOUR_API_KEY"
city = "Tashkent"

# Endpoint
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    
    print(f"{city} shahri ob-havosi:")
    print(f"Harorat: {temp}°C")
    print(f"Holat: {description}")
else:
    print("Xato!")
```

Bu yerda:
- Real API bilan ishlaymiz
- API key talab qilinadi (authentication)
- Ma'lumot JSON formatda keladi

---

## 🎯 Muhim nuqtalar (Cheat Sheet)

| Tushuncha | Ta'rif | Misol |
|-----------|--------|-------|
| **API** | Dasturlar o'rtasidagi interfeys | Mobil app backend bilan gaplashadi |
| **REST** | Web API yaratish uslubi | GET /api/users |
| **Endpoint** | API'ning manzili | `/api/users`, `/api/products` |
| **HTTP Method** | Harakat turi | GET, POST, PUT, DELETE |
| **JSON** | Ma'lumot formati | `{"name": "John", "age": 30}` |
| **Status Code** | So'rov natijasi | 200 (OK), 404 (Not Found) |

### Esda saqlash kerak:

```python
# GET so'rov - Ma'lumot olish
response = requests.get(url)

# Response'dan ma'lumot olish
data = response.json()
status = response.status_code

# Statusni tekshirish
if status == 200:
    print("Muvaffaqiyatli!")
```

---

## ⚠️ Keng tarqalgan xatolar

### 1. Status kodini tekshirmaslik

❌ **Noto'g'ri:**
```python
response = requests.get(url)
data = response.json()  # Agar 404 bo'lsa xato!
```

✅ **To'g'ri:**
```python
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Xato: {response.status_code}")
```

### 2. Exception'larni handle qilmaslik

❌ **Noto'g'ri:**
```python
response = requests.get(url)  # Internet yo'q bo'lsa crash!
```

✅ **To'g'ri:**
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Xato: {e}")
```

---

## 🧪 O'zingizni tekshiring

### Nazariy savollar:

1. **API nima va nima uchun kerak?**
   <details><summary>Javob</summary>
   API (Application Programming Interface) - bu dasturlar o'rtasidagi muloqot qoidalari. Kerak chunki: turli dasturlar bir-biri bilan ma'lumot almashishi, frontend backend bilan gaplashishi, mobil app server bilan ishlashi uchun zarur.
   </details>

2. **REST API'ning asosiy tamoyillari qaysilar?**
   <details><summary>Javob</summary>
   1. Client-Server arxitektura
   2. Stateless (holatsiz)
   3. Cacheable (keshlanuvchi)
   4. Uniform Interface (yagona interfeys)
   5. Layered System (qatlamli tizim)
   </details>

3. **Status kod 200 nimani anglatadi?**
   <details><summary>Javob</summary>
   200 OK - So'rov muvaffaqiyatli bajarildi. Server kutilgan ma'lumotni qaytardi.
   </details>

### Amaliy topshiriq:

**Vazifa:** JSONPlaceholder API'dan barcha postlarni oling va ulardan faqat `userId=1` bo'lganlarini filterlang.

**Endpoint:** `https://jsonplaceholder.typicode.com/posts`

<details>
<summary>✅ Yechim</summary>

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

if response.status_code == 200:
    posts = response.json()
    
    # userId=1 bo'lgan postlar
    user_posts = [post for post in posts if post['userId'] == 1]
    
    print(f"User 1 ning postlari soni: {len(user_posts)}")
    
    # Birinchi 3 tasini ko'rsatish
    for post in user_posts[:3]:
        print(f"- {post['title']}")
```

</details>

---

## 📚 Qo'shimcha o'qish

### Tavsiya etilgan manbalar:
- [REST API nima?](https://www.redhat.com/en/topics/api/what-is-a-rest-api) - Red Hat blog
- [HTTP status kodlari](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) - MDN hujjatlari
- [JSON nima?](https://www.json.org/json-en.html) - Rasmiy JSON sayti

### Video darslar:
- [What is an API?](https://www.youtube.com/watch?v=s7wmiS2mSXY) - Sodda tushuntirish
- [REST API concepts](https://www.youtube.com/watch?v=-MTSQjw5DrM) - Batafsil

### Amaliyot uchun bepul API'lar:
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Test API
- [ReqRes](https://reqres.in/) - Fake REST API
- [Public APIs](https://github.com/public-apis/public-apis) - 1000+ bepul API ro'yxati

---

## 🔗 Navigatsiya

- [➡️ Keyingi dars - HTTP Methods va Status Kodlar](../02-http-methods/)
- [🏠 Bosh sahifa](../../)

---

## 📝 Eslatmalar

> **💡 Maslahat:** Har bir API bilan ishlashda albatta dokumentatsiyasini o'qing. Har bir API o'z qoidalariga ega.

> **⚠️ Diqqat:** API so'rovlar cheklanishi mumkin (rate limit). Masalan: 100 so'rov/soat. Buni hisobga oling.

> **🔍 Chuqurroq:** Keyingi darslarda HTTP metodlarini (GET, POST, PUT, DELETE) batafsil o'rganamiz.

---

**Keyingi darsda:** HTTP metodlari, Status kodlar va Request/Response tuzilishini chuqurroq o'rganamiz.

**Tabriklayman! Birinchi darsni tugatdingiz! 🎉**