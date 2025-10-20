# 02. HTTP Methods va Status Kodlar

> HTTP - bu web'ning tili. API bilan ishlash uchun HTTP metodlarini bilish shart!

## 🎯 Dars maqsadlari

Ushbu darsdan keyin siz quyidagilarni bilib olasiz:
- [ ] HTTP metodlarini (GET, POST, PUT, DELETE) va ularning farqini
- [ ] Status kodlarni va ularning ma'nosini
- [ ] Request va Response tuzilishini
- [ ] Headers va Query Parameters bilan ishlashni

## ⏱ Taxminiy vaqt: 45-60 daqiqa

---

## 📚 Nazariya

### HTTP Request nima?

HTTP Request - bu client'dan server'ga yuboriladigan so'rov. Har bir request quyidagi qismlardan iborat:

```
METHOD /path/to/resource HTTP/1.1
Header1: value1
Header2: value2

[Request Body - ixtiyoriy]
```

#### Misol:

```http
GET /api/users/1 HTTP/1.1
Host: example.com
Authorization: Bearer token123
Accept: application/json
```

---

### HTTP Methods (CRUD operatsiyalari)

HTTP metodlari - bu server bilan qanday harakat qilishni ko'rsatadi.

| Method | CRUD | Maqsad | Idempotent | Safe |
|--------|------|--------|-----------|------|
| **GET** | Read | Ma'lumot olish | ✅ | ✅ |
| **POST** | Create | Yangi yaratish | ❌ | ❌ |
| **PUT** | Update | To'liq yangilash | ✅ | ❌ |
| **PATCH** | Update | Qisman yangilash | ❌ | ❌ |
| **DELETE** | Delete | O'chirish | ✅ | ❌ |

**Idempotent** - Bir xil so'rovni qayta yuborsangiz, natija o'zgarmaydi  
**Safe** - Server'dagi ma'lumotni o'zgartirmaydi

---

### 1. GET - Ma'lumot olish

**Xususiyatlari:**
- Ma'lumot **faqat o'qiydi**, o'zgartirmaydi
- Query parameters ishlatadi
- Body bo'lmaydi
- Keshlanishi mumkin

**Misollar:**

```python
import requests

# Barcha foydalanuvchilar
response = requests.get("https://api.example.com/users")

# Bitta foydalanuvchi
response = requests.get("https://api.example.com/users/1")

# Query parameters bilan
response = requests.get("https://api.example.com/users", params={
    "age": 25,
    "city": "Tashkent"
})
# URL: https://api.example.com/users?age=25&city=Tashkent
```

---

### 2. POST - Yangi yaratish

**Xususiyatlari:**
- Yangi resurs yaratadi
- Request body'da ma'lumot yuboriladi
- Idempotent emas (har safar yangi yaratadi)
- Status: 201 Created

**Misollar:**

```python
import requests

# Yangi foydalanuvchi yaratish
url = "https://api.example.com/users"
data = {
    "name": "Alisher",
    "email": "alisher@example.com",
    "age": 25
}

response = requests.post(url, json=data)

if response.status_code == 201:
    print("Yaratildi!")
    new_user = response.json()
    print(f"ID: {new_user['id']}")
```

---

### 3. PUT - To'liq yangilash

**Xususiyatlari:**
- Resursni **to'liq** yangilaydi
- Barcha fieldlar yuborilishi kerak
- Idempotent (bir xil so'rov bir xil natija)
- Status: 200 OK

**Misol:**

```python
import requests

url = "https://api.example.com/users/1"
data = {
    "name": "Alisher Karimov",  # Yangilandi
    "email": "alisher@example.com",
    "age": 26  # Yangilandi
}

response = requests.put(url, json=data)

if response.status_code == 200:
    print("Yangilandi!")
```

---

### 4. PATCH - Qisman yangilash

**Xususiyatlari:**
- Faqat **ba'zi** fieldlarni yangilaydi
- Qolgan fieldlar o'zgarmaydi
- PUT'dan farqi - to'liq emas, qisman
- Status: 200 OK

**Misol:**

```python
import requests

url = "https://api.example.com/users/1"
data = {
    "age": 26  # Faqat yoshni o'zgartirish
}

response = requests.patch(url, json=data)

if response.status_code == 200:
    print("Yosh yangilandi!")
```

**PUT vs PATCH farqi:**

```python
# PUT - Barcha fieldlar kerak
data = {"name": "Ali", "email": "ali@mail.com", "age": 30}

# PATCH - Faqat o'zgartirish kerak bo'lganlar
data = {"age": 30}
```

---

### 5. DELETE - O'chirish

**Xususiyatlari:**
- Resursni o'chiradi
- Body bo'lmasligi mumkin
- Idempotent
- Status: 204 No Content yoki 200 OK

**Misol:**

```python
import requests

url = "https://api.example.com/users/1"
response = requests.delete(url)

if response.status_code == 204:
    print("O'chirildi!")
elif response.status_code == 404:
    print("Bunday foydalanuvchi topilmadi")
```

---

## 📊 HTTP Status Kodlar

Status kodlar - server javobining natijasini bildiradi.

### 1️⃣ 1xx - Informational (Ma'lumot)

Kamdan-kam ishlatiladi.

| Kod | Nomi | Ma'nosi |
|-----|------|---------|
| 100 | Continue | Davom eting |

---

### 2️⃣ 2xx - Success (Muvaffaqiyat) ✅

| Kod | Nomi | Ma'nosi | Qachon |
|-----|------|---------|--------|
| **200** | OK | Muvaffaqiyatli | GET, PUT, PATCH |
| **201** | Created | Yaratildi | POST |
| **204** | No Content | Javob yo'q (muvaffaqiyatli) | DELETE |

**Misol:**

```python
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Ma'lumot olindi")
```

---

### 3️⃣ 3xx - Redirection (Qayta yo'naltirish)

| Kod | Nomi | Ma'nosi |
|-----|------|---------|
| 301 | Moved Permanently | Doimiy ko'chirilgan |
| 302 | Found | Vaqtincha ko'chirilgan |
| 304 | Not Modified | O'zgarmagan (cache) |

---

### 4️⃣ 4xx - Client Error (Client xatosi) ❌

Client'ning xatosi - noto'g'ri so'rov yuborilgan.

| Kod | Nomi | Ma'nosi | Sabab |
|-----|------|---------|-------|
| **400** | Bad Request | Noto'g'ri so'rov | Xato ma'lumot |
| **401** | Unauthorized | Autentifikatsiya kerak | Token yo'q |
| **403** | Forbidden | Ruxsat yo'q | Access denied |
| **404** | Not Found | Topilmadi | Bunday resurs yo'q |
| **405** | Method Not Allowed | Method xato | POST o'rniga GET |
| **422** | Unprocessable Entity | Validation xato | Ma'lumot noto'g'ri |
| **429** | Too Many Requests | Juda ko'p so'rov | Rate limit |

**Misollar:**

```python
response = requests.get(url)

if response.status_code == 404:
    print("Topilmadi!")
elif response.status_code == 401:
    print("Login qiling!")
elif response.status_code == 403:
    print("Ruxsatingiz yo'q!")
```

---

### 5️⃣ 5xx - Server Error (Server xatosi) 💥

Server'ning xatosi - backend'da muammo.

| Kod | Nomi | Ma'nosi |
|-----|------|---------|
| **500** | Internal Server Error | Server xato |
| **502** | Bad Gateway | Gateway xato |
| **503** | Service Unavailable | Server ishlamayapti |
| **504** | Gateway Timeout | Timeout |

---

## 💻 Amaliyot

### 1-mashq: CRUD operatsiyalari (JSONPlaceholder)

JSONPlaceholder API bilan barcha CRUD operatsiyalarini sinab ko'ramiz.

#### GET - O'qish

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

print(f"Status: {response.status_code}")
print(f"Post: {response.json()['title']}")
```

#### POST - Yaratish

```python
url = "https://jsonplaceholder.typicode.com/posts"
data = {
    "title": "Yangi post",
    "body": "Bu test post",
    "userId": 1
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")  # 201
print(f"Yangi ID: {response.json()['id']}")
```

#### PUT - To'liq yangilash

```python
url = "https://jsonplaceholder.typicode.com/posts/1"
data = {
    "id": 1,
    "title": "Yangilangan sarlavha",
    "body": "Yangilangan matn",
    "userId": 1
}

response = requests.put(url, json=data)
print(f"Status: {response.status_code}")  # 200
```

#### PATCH - Qisman yangilash

```python
url = "https://jsonplaceholder.typicode.com/posts/1"
data = {
    "title": "Faqat sarlavha o'zgardi"
}

response = requests.patch(url, json=data)
print(f"Status: {response.status_code}")  # 200
```

#### DELETE - O'chirish

```python
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.delete(url)
print(f"Status: {response.status_code}")  # 200
```

---

### 2-mashq: Headers bilan ishlash

Headers - bu so'rov haqida qo'shimcha ma'lumot.

```python
import requests

url = "https://api.example.com/users"

# Headers yuborish
headers = {
    "Authorization": "Bearer token123",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "MyApp/1.0"
}

response = requests.get(url, headers=headers)

# Response headerslarini ko'rish
print(response.headers)
print(response.headers['Content-Type'])
```

**Keng tarqalgan headers:**

| Header | Maqsad | Misol |
|--------|--------|-------|
| Authorization | Autentifikatsiya | Bearer token123 |
| Content-Type | Ma'lumot formati | application/json |
| Accept | Qabul qilinadigan format | application/json |
| User-Agent | Client haqida | MyApp/1.0 |

---

### 3-mashq: Query Parameters

Query parameters - URL orqali ma'lumot yuborish.

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

# Variant 1: Dictionary
params = {
    "userId": 1,
    "id": 5
}
response = requests.get(url, params=params)
# URL: https://.../posts?userId=1&id=5

# Variant 2: To'g'ridan-to'g'ri URL'da
url_with_params = "https://jsonplaceholder.typicode.com/posts?userId=1"
response = requests.get(url_with_params)

print(response.url)  # Yakuniy URL
print(len(response.json()))  # Natijalar soni
```

---

### 4-mashq: To'liq CRUD funksiyasi

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

class PostAPI:
    @staticmethod
    def get_all():
        """Barcha postlarni olish"""
        response = requests.get(f"{BASE_URL}/posts")
        if response.status_code == 200:
            return response.json()
        return None
    
    @staticmethod
    def get_by_id(post_id):
        """ID bo'yicha post olish"""
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("Post topilmadi!")
        return None
    
    @staticmethod
    def create(data):
        """Yangi post yaratish"""
        response = requests.post(f"{BASE_URL}/posts", json=data)
        if response.status_code == 201:
            return response.json()
        return None
    
    @staticmethod
    def update(post_id, data):
        """Post yangilash"""
        response = requests.put(f"{BASE_URL}/posts/{post_id}", json=data)
        if response.status_code == 200:
            return response.json()
        return None
    
    @staticmethod
    def delete(post_id):
        """Post o'chirish"""
        response = requests.delete(f"{BASE_URL}/posts/{post_id}")
        return response.status_code == 200

# Ishlatish
posts = PostAPI.get_all()
print(f"Jami postlar: {len(posts)}")

post = PostAPI.get_by_id(1)
print(f"Post: {post['title']}")

new_post = PostAPI.create({
    "title": "Test",
    "body": "Test body",
    "userId": 1
})
print(f"Yangi post ID: {new_post['id']}")
```

---

## 🎯 Muhim nuqtalar (Cheat Sheet)

### HTTP Methods

```python
# GET - Ma'lumot olish
requests.get(url)

# POST - Yangi yaratish
requests.post(url, json=data)

# PUT - To'liq yangilash
requests.put(url, json=data)

# PATCH - Qisman yangilash
requests.patch(url, json=data)

# DELETE - O'chirish
requests.delete(url)
```

### Status kodlarni tekshirish

```python
response = requests.get(url)

if response.status_code == 200:
    print("OK")
elif response.status_code == 404:
    print("Topilmadi")
elif response.status_code >= 500:
    print("Server xato")
```

### Headers va Params

```python
# Headers
headers = {"Authorization": "Bearer token"}
requests.get(url, headers=headers)

# Query parameters
params = {"search": "python", "limit": 10}
requests.get(url, params=params)
```

---

## ⚠️ Keng tarqalgan xatolar

### 1. PUT va PATCH'ni aralashmaslik

❌ **Noto'g'ri:**
```python
# PUT ishlatib faqat bitta field yuborish
data = {"title": "Yangi"}  # Qolgan fieldlar yo'qoladi!
requests.put(url, json=data)
```

✅ **To'g'ri:**
```python
# PATCH ishlatish
data = {"title": "Yangi"}
requests.patch(url, json=data)
```

### 2. Status kodlarni to'g'ri ishlatmaslik

❌ **Noto'g'ri:**
```python
if response.status_code == 200:
    # DELETE uchun 204 bo'lishi kerak!
```

✅ **To'g'ri:**
```python
if response.status_code in [200, 204]:
    print("Muvaffaqiyatli")
```

---

## 🧪 O'zingizni tekshiring

### Nazariy savollar:

1. **GET va POST'ning farqi nima?**
   <details><summary>Javob</summary>
   GET - Ma'lumot faqat o'qiladi, o'zgartirilmaydi. Query parameters ishlatiladi.
   POST - Yangi resurs yaratadi. Request body'da ma'lumot yuboriladi.
   </details>

2. **Status kod 404 nimani bildiradi?**
   <details><summary>Javob</summary>
   404 Not Found - So'ralgan resurs topilmadi. Masalan, bunday ID'li foydalanuvchi yo'q.
   </details>

3. **PUT va PATCH'ning farqi?**
   <details><summary>Javob</summary>
   PUT - Resursni to'liq yangilaydi, barcha fieldlar yuborilishi kerak.
   PATCH - Faqat ba'zi fieldlarni yangilaydi.
   </details>

### Amaliy topshiriq:

**Vazifa:** JSONPlaceholder API yordamida:
1. Barcha postlarni oling
2. Yangi post yarating
3. Uni yangilang
4. Oxirida o'chiring

<details>
<summary>✅ Yechim</summary>

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"

# 1. Barcha postlar
response = requests.get(BASE_URL)
print(f"Jami postlar: {len(response.json())}")

# 2. Yangi yaratish
new_post = {
    "title": "Mening postim",
    "body": "Test matn",
    "userId": 1
}
response = requests.post(BASE_URL, json=new_post)
post_id = response.json()['id']
print(f"Yangi ID: {post_id}")

# 3. Yangilash
updated_data = {"title": "Yangilangan sarlavha"}
response = requests.patch(f"{BASE_URL}/{post_id}", json=updated_data)
print(f"Yangilandi: {response.status_code}")

# 4. O'chirish
response = requests.delete(f"{BASE_URL}/{post_id}")
print(f"O'chirildi: {response.status_code}")
```

</details>

---

## 📚 Qo'shimcha o'qish

### Tavsiya etilgan manbalar:
- [HTTP Methods - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) - To'liq guide
- [HTTP Status Codes](https://httpstatuses.com/) - Barcha status kodlar
- [REST API Best Practices](https://restfulapi.net/) - Best practices

### Foydali vositalar:
- [HTTP Status Dogs](https://httpstatusdogs.com/) - Status kodlarni qiziqarli o'rganish
- [Postman](https://www.postman.com/) - API test qilish
- [HTTPie](https://httpie.io/) - Terminal'da API test

---

## 🔗 Navigatsiya

- [⬅️ Oldingi dars - API bilan tanishuv](../01-api-basics/)
- [➡️ Keyingi dars - Loyihani boshlash](../03-project-setup/)
- [🏠 Bosh sahifa](../../)

---

## 📝 Eslatmalar

> **💡 Maslahat:** Status kodlarni eslash uchun: 2xx = Yaxshi, 4xx = Sizning xato, 5xx = Server xato

> **⚠️ Diqqat:** PUT ishlatganda barcha fieldlarni yuborish kerak, aks holda ma'lumot yo'qoladi!

> **🔍 Chuqurroq:** Keyingi darsda Django loyihasi yaratib, o'z API'mizni yozamiz!

---

**Keyingi darsda:** Django REST Framework o'rnatamiz va birinchi API endpoint yaratamiz!

**Tabriklayman! Ikkinchi darsni tugatdingiz! 🎉**