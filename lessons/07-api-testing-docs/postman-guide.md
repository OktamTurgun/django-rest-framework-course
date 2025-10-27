# Postman - Complete Guide

## 📋 Mundarija

1. [Postman nima?](#1-postman-nima)
2. [O'rnatish va sozlash](#2-ornatish-va-sozlash)
3. [Birinchi request](#3-birinchi-request)
4. [Collection yaratish](#4-collection-yaratish)
5. [Environment variables](#5-environment-variables)
6. [Tests yozish](#6-tests-yozish)
7. [Advanced features](#7-advanced-features)

---

## 1. Postman nima?

### Muammo

Siz API yaratdingiz. Endi uni qanday test qilasiz?

**❌ Yomon usullar:**
```bash
# Terminal'da curl - murakkab!
curl -X POST http://localhost:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Book", "author": "Author", "price": 50000}'

# Python kod yozish - vaqt ketadi!
import requests
response = requests.post('http://localhost:8000/books/', json={...})
```

**✅ Yaxshi usul: Postman!**
- Grafik interfeys
- 1 click'da request yuborish
- History saqlash
- Collection'lar yaratish
- Team bilan ulashish

---

### 🎯 Postman nima uchun kerak?

| Vazifa | Postmansiz | Postman bilan |
|--------|-----------|---------------|
| GET request | Brauzer yoki curl | 1 click |
| POST request | curl yoki kod | Form to'ldirish |
| Headers qo'shish | Qo'lda yozish | Dropdown tanlash |
| Test qilish | Kod yozish | Tests tab |
| Ulashish | Qiyin | Export → Import |
| History | Yo'q | Avtomatik saqlanadi |

---

### 📊 Postman'ning asosiy features

1. **Request yuborish** - Barcha HTTP methods (GET, POST, PUT, DELETE, PATCH)
2. **Collections** - Request'larni guruhlash
3. **Environment** - Development, Production variables
4. **Tests** - Automated testing
5. **Mock servers** - Fake API yaratish
6. **Documentation** - Avtomatik docs
7. **Team collaboration** - Ulashish va sync
8. **History** - Barcha request'lar saqlanadi

---

## 2. O'rnatish va sozlash

### O'rnatish (3 usul)

#### Usul 1: Desktop App (Tavsiya ✅)

1. **Yuklab olish:** [postman.com/downloads](https://www.postman.com/downloads/)
2. **O'rnatish:** Installer'ni ishga tushiring
3. **Ochish:** Postman'ni oching

**Afzalliklari:**
- ✅ Tezroq ishlaydi
- ✅ Offline ishlaydi
- ✅ Ko'proq feature'lar

---

#### Usul 2: Web Version

1. **Kirish:** [web.postman.com](https://web.postman.com/)
2. **Login:** Google yoki Email bilan

**Afzalliklari:**
- ✅ O'rnatish kerak emas
- ✅ Istalgan kompyuterdan
- ❌ Lekin, internet kerak

---

#### Usul 3: VS Code Extension

1. VS Code'da Extensions'ga o'ting
2. "Postman" ni qidiring
3. Install tugmasini bosing

**Afzalliklari:**
- ✅ VS Code ichida ishlaydi
- ❌ Lekin, kamroq feature'lar

---

### 🔐 Account yaratish

1. **Postman'ni oching**
2. **Sign Up** tugmasini bosing
3. **Email yoki Google** bilan ro'yxatdan o'ting
4. **Verify email** - Email'ingizni tasdiqlang

**Nega account kerak?**
- ✅ Collection'larni saqlay olasiz
- ✅ Team bilan ulashish
- ✅ Sync (barcha qurilmalarda)
- ✅ Cloud backup

---

### ⚙️ Dastlabki sozlash

#### 1. Theme tanlash

```
Settings (⚙️) → Themes → Dark/Light
```

**Tavsiya:** Dark theme - ko'zga yengil

---

#### 2. Auto-save yoqish

```
Settings → General → Auto-save requests ✅
```

---

#### 3. SSL verification o'chirish (Development uchun)

```
Settings → General → SSL certificate verification ❌
```

**Diqqat:** Faqat development'da! Production'da SSL yoniq bo'lishi kerak!

---

## 3. Birinchi request

### 🚀 GET request yuborish

#### Qadam 1: Yangi request yaratish

1. **"New"** tugmasini bosing yoki `Ctrl + N`
2. **"HTTP Request"** ni tanlang
3. Yangi tab ochiladi

---

#### Qadam 2: Request sozlash

```
Method: GET
URL: http://localhost:8000/books/
```

**Yozish:**
1. Dropdown'dan **GET** tanlang (default)
2. URL maydoniga yozing: `http://localhost:8000/books/`

---

#### Qadam 3: Send bosing!

1. **"Send"** tugmasini bosing
2. Pastda **Response** ko'rinadi

**Response:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Django for Beginners",
            "author": "William Vincent",
            "price": 75000,
            "available": true
        },
        ...
    ]
}
```

---

#### Qadam 4: Response tahlil qilish

**Response'da nimalar bor:**

1. **Status:** `200 OK` - Muvaffaqiyatli
2. **Time:** `234ms` - Javob vaqti
3. **Size:** `1.2 KB` - Javob hajmi
4. **Body:** JSON ma'lumotlar
5. **Headers:** Response headers
6. **Cookies:** Cookie'lar (agar bor bo'lsa)

---

### 📝 POST request yuborish

#### Qadam 1: Yangi request yaratish

```
Method: POST
URL: http://localhost:8000/books/
```

---

#### Qadam 2: Body qo'shish

1. **Body** tabga o'ting
2. **raw** ni tanlang
3. Dropdown'dan **JSON** tanlang
4. JSON ma'lumotlarni yozing:

```json
{
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "price": 95000,
    "pages": 544,
    "publish_date": "2024-01-15",
    "isbn": "978-1593279288",
    "available": true,
    "description": "A hands-on, project-based introduction to programming"
}
```

---

#### Qadam 3: Headers qo'shish (avtomatik)

Postman **JSON** tanlaganda avtomatik qo'shadi:
```
Content-Type: application/json
```

Agar qo'lda qo'shmoqchi bo'lsangiz:
1. **Headers** tabga o'ting
2. Key: `Content-Type`
3. Value: `application/json`

---

#### Qadam 4: Send va Response

**Request yuborish:**
1. **Send** bosing

**Response:**
```json
{
    "id": 11,
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "price": 95000,
    "pages": 544,
    "publish_date": "2024-01-15",
    "isbn": "978-1593279288",
    "available": true,
    "description": "A hands-on, project-based introduction to programming"
}
```

**Status:** `201 Created` ✅

---

### 🔍 GET single item (Detail)

```
Method: GET
URL: http://localhost:8000/books/1/
```

**Response:**
```json
{
    "id": 1,
    "title": "Django for Beginners",
    "author": "William Vincent",
    "price": 75000,
    ...
}
```

---

### ✏️ PUT request (Full update)

```
Method: PUT
URL: http://localhost:8000/books/1/
```

**Body:**
```json
{
    "title": "Django for Beginners (Updated)",
    "author": "William Vincent",
    "price": 80000,
    "pages": 350,
    "publish_date": "2024-01-01",
    "isbn": "978-1735467221",
    "available": true,
    "description": "Updated description"
}
```

**Eslatma:** PUT'da barcha field'lar kerak!

---

### ✏️ PATCH request (Partial update)

```
Method: PATCH
URL: http://localhost:8000/books/1/
```

**Body:**
```json
{
    "price": 85000,
    "available": false
}
```

**Eslatma:** PATCH'da faqat o'zgartirmoqchi bo'lgan field'lar!

---

### 🗑️ DELETE request

```
Method: DELETE
URL: http://localhost:8000/books/1/
```

**Body yo'q!**

**Response:**
- Status: `204 No Content`
- Body: bo'sh

---

### 🔍 Query Parameters

```
Method: GET
URL: http://localhost:8000/books/?search=django&ordering=-price&page=2
```

**Postman'da 2 usul:**

#### Usul 1: URL'ga yozish (yuqoridagi kabi)

#### Usul 2: Params tabdan qo'shish
1. **Params** tabga o'ting
2. Key-Value qo'shing:
   - Key: `search`, Value: `django`
   - Key: `ordering`, Value: `-price`
   - Key: `page`, Value: `2`

Postman avtomatik URL yaratadi!

---

## 4. Collection yaratish

### 📚 Collection nima?

**Collection** - Request'larni guruhlash usuli.

**Misol:**
```
Library API Collection
├── Books
│   ├── List Books (GET)
│   ├── Create Book (POST)
│   ├── Get Book (GET)
│   ├── Update Book (PUT)
│   ├── Partial Update (PATCH)
│   └── Delete Book (DELETE)
├── Authors
│   ├── List Authors (GET)
│   └── Create Author (POST)
└── Categories
    ├── List Categories (GET)
    └── Create Category (POST)
```

---

### 📦 Collection yaratish

#### Qadam 1: Yangi collection

1. Sidebar'da **Collections** tugmasini bosing
2. **"New Collection"** yoki `Ctrl + N`
3. Nom bering: `Library API`

---

#### Qadam 2: Request qo'shish

**Usul 1: Yangi request yaratish**
1. Collection'ga o'ng click
2. **"Add request"**
3. Nom: `List Books`
4. Method: `GET`, URL: `http://localhost:8000/books/`
5. **Save**

**Usul 2: Mavjud request'ni qo'shish**
1. Request'ni oching
2. **"Save"** tugmasini bosing (yuqori o'ng burchak)
3. Collection tanlang: `Library API`
4. Nom bering: `List Books`
5. **Save**

---

#### Qadam 3: Folder yaratish (Organize qilish)

1. Collection'ga o'ng click
2. **"Add folder"**
3. Nom: `Books`
4. Request'larni folder ichiga sudrab tashlang (drag & drop)

---

### 📋 To'liq Library API Collection

```
Library API
│
├── 📁 Books
│   ├── GET - List Books
│   ├── POST - Create Book
│   ├── GET - Get Single Book
│   ├── PUT - Update Book
│   ├── PATCH - Partial Update
│   └── DELETE - Delete Book
│
├── 📁 Filters & Search
│   ├── GET - Search Books (?search=django)
│   ├── GET - Order Books (?ordering=-price)
│   ├── GET - Available Books (/books/available/)
│   └── GET - Expensive Books (/books/expensive/)
│
└── 📁 Authors (Bonus)
    ├── GET - List Authors
    ├── POST - Create Author
    └── GET - Author's Books
```

---

### 💾 Collection saqilash

#### Usul 1: Auto-save (Tavsiya)
```
Settings → General → Auto-save requests ✅
```

#### Usul 2: Qo'lda save
Har bir request'ni o'zgartirgandan keyin **Save** (`Ctrl + S`)

---

### 📤 Collection export qilish

1. Collection'ga o'ng click
2. **"Export"**
3. Format tanlang: **Collection v2.1** (tavsiya)
4. **Export** tugmasini bosing
5. Fayl saqlash (masalan, `Library-API.postman_collection.json`)

**Nima uchun export?**
- ✅ Team bilan ulashish
- ✅ Backup
- ✅ GitHub'ga qo'shish
- ✅ CI/CD'da ishlatish (Newman)

---

### 📥 Collection import qilish

1. **Import** tugmasini bosing (sidebar)
2. **File** tanlang yoki drag & drop
3. JSON faylni tanlang
4. **Import** tugmasini bosing

---

## 5. Environment Variables

### 🌍 Environment nima?

**Environment** - O'zgaruvchilarni saqlash usuli.

**Misol:**
```
Development:
- base_url = http://localhost:8000
- api_key = dev_key_123

Production:
- base_url = https://api.myapp.com
- api_key = prod_key_xyz
```

**Foyda:** URL'ni bir joyda o'zgartirasiz, barcha request'lar yangilanadi!

---

### ⚙️ Environment yaratish

#### Qadam 1: Yangi environment

1. **Environments** tugmasini bosing (sidebar)
2. **"Create Environment"** yoki `+`
3. Nom: `Development`

---

#### Qadam 2: Variables qo'shish

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `api_version` | `v1` | `v1` |
| `port` | `8000` | `8000` |

**Save** tugmasini bosing.

---

#### Qadam 3: Environment'ni aktivlashtirish

1. Yuqori o'ng burchakda dropdown
2. **"Development"** ni tanlang

---

### 🔧 Variable ishlatish

**Eski usul (qiyin):**
```
URL: http://localhost:8000/books/
```

**Yangi usul (oson):**
```
URL: {{base_url}}/books/
```

**Postman avtomatik almashtiradi:**
```
http://localhost:8000/books/
```

---

### 📚 Ko'proq environment'lar

#### Development Environment
```
base_url: http://localhost:8000
username: admin
password: admin123
```

#### Staging Environment
```
base_url: https://staging.myapp.com
username: test_user
password: test_pass
```

#### Production Environment
```
base_url: https://api.myapp.com
username: real_user
password: strong_pass_xyz
```

**Foydalanish:**
1. Dropdown'dan environment tanlang
2. Barcha request'lar yangi qiymatlarni ishlatadi!

---

### 💡 Variable types

**1. Environment Variable:** Environment ichida
**2. Global Variable:** Barcha environment'larda
**3. Collection Variable:** Faqat collection ichida
**4. Local Variable:** Faqat bitta request'da

---

## 6. Tests yozish

### 🧪 Tests nima uchun kerak?

**Muammo:** Har safar qo'lda tekshirish - vaqt ketadi!

**Yechim:** Automated tests!

```javascript
// Test: Status 200 bo'lishi kerak
pm.test("Status is 200", function () {
    pm.response.to.have.status(200);
});

// Test: Response JSON bo'lishi kerak
pm.test("Response is JSON", function () {
    pm.response.to.be.json;
});
```

---

### ✅ Birinchi test

#### Request: GET /books/

**Tests tab:**
```javascript
// Test 1: Status code 200
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test 2: Response time < 500ms
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Test 3: Response has "results" key
pm.test("Response has results", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
});
```

**Send bosing!**

**Natija:**
```
✅ Status code is 200
✅ Response time is less than 500ms (234ms)
✅ Response has results
```

---

### 📝 POST request test

#### Request: POST /books/

**Tests tab:**
```javascript
// Test 1: Status 201 Created
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

// Test 2: Response has id
pm.test("Book has ID", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
});

// Test 3: Title is correct
pm.test("Title is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.title).to.eql("Python Crash Course");
});

// Test 4: Save book ID for later use
var jsonData = pm.response.json();
pm.environment.set("book_id", jsonData.id);
```

---

### 🔗 Ketma-ket test'lar (Chaining)

**Scenario:** Kitob yaratish → O'qish → Yangilash → O'chirish

#### 1. POST - Create Book
```javascript
pm.test("Book created", function () {
    pm.response.to.have.status(201);
    var jsonData = pm.response.json();
    pm.environment.set("book_id", jsonData.id);
});
```

#### 2. GET - Get Book
```
URL: {{base_url}}/books/{{book_id}}/
```
```javascript
pm.test("Book exists", function () {
    pm.response.to.have.status(200);
});
```

#### 3. PATCH - Update Book
```
URL: {{base_url}}/books/{{book_id}}/
```
```javascript
pm.test("Book updated", function () {
    pm.response.to.have.status(200);
});
```

#### 4. DELETE - Delete Book
```
URL: {{base_url}}/books/{{book_id}}/
```
```javascript
pm.test("Book deleted", function () {
    pm.response.to.have.status(204);
});
```

---

### 🎯 Advanced tests

```javascript
// Data validation
pm.test("Price is a number", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.price).to.be.a('number');
});

// Array checks
pm.test("Results is an array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results).to.be.an('array');
});

// Array not empty
pm.test("Results not empty", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results.length).to.be.above(0);
});

// Headers check
pm.test("Content-Type is JSON", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});
```

---

## 7. Advanced Features

### 🔄 Pre-request Script

**Vazifa:** Request yuborishdan oldin biror ishni bajarish.

**Misol: Token olish**
```javascript
// Pre-request Script
const loginRequest = {
    url: pm.environment.get("base_url") + "/api/login/",
    method: 'POST',
    header: {
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            username: "admin",
            password: "admin123"
        })
    }
};

pm.sendRequest(loginRequest, function (err, response) {
    const token = response.json().token;
    pm.environment.set("auth_token", token);
});
```

---

### 📤 Collection Runner

**Vazifa:** Barcha request'larni bir vaqtda ishga tushirish.

**Qadamlar:**
1. Collection'ga o'ng click
2. **"Run collection"**
3. Request'larni tanlang
4. **"Run Library API"** tugmasini bosing

**Natija:**
```
✅ List Books - 200 OK
✅ Create Book - 201 Created
✅ Get Book - 200 OK
✅ Update Book - 200 OK
✅ Delete Book - 204 No Content

Total: 5/5 passed
```

---

### 📊 Postman Console

**Vazifa:** Debug qilish, log'larni ko'rish.

**Ochish:**
- `View → Show Postman Console`
- Yoki `Ctrl + Alt + C`

**Console'da nimalar bor:**
- Request details
- Response details
- console.log() output
- Errors

---

### 🤝 Team Collaboration

#### 1. Workspace yaratish
```
File → New Workspace → Team Workspace
```

#### 2. Team member qo'shish
```
Workspace Settings → Invite people → Email kiriting
```

#### 3. Sync
Barcha o'zgarishlar avtomatik sync bo'ladi!

---

## ✅ Xulosa

### Siz nimalarni o'rgandingiz:

1. ✅ **Postman nima** - API testing tool
2. ✅ **O'rnatish** - Desktop app, web version
3. ✅ **Request yuborish** - GET, POST, PUT, PATCH, DELETE
4. ✅ **Collection** - Request'larni guruhlash
5. ✅ **Environment** - Variables ishlatish
6. ✅ **Tests** - Automated testing
7. ✅ **Advanced** - Pre-request, Runner, Console

---

### 🎯 Keyingi qadamlar

1. ✅ Library API uchun to'liq collection yarating
2. ✅ Barcha endpoints'ni test qiling
3. ✅ Tests yozing
4. ✅ Collection export qiling
5. ✅ `swagger-guide.md`'ni o'qing

---

**Keyingi:** [swagger-guide.md](swagger-guide.md) - Swagger/OpenAPI dokumentatsiya

Happy testing! 🚀