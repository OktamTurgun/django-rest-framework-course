# Lesson 07: API Testing & Documentation

## 🎯 Dars maqsadi

API'larni professional darajada test qilish va avtomatik dokumentatsiya yaratishni o'rganish.

---

## 🤔 Nega API testing va dokumentatsiya kerak?

### Muammo: API'ni qanday test qilish?

Siz API yaratdingiz. Endi uni qanday test qilasiz?

**❌ Yomon usul:**
- Brauzerda ochish (faqat GET requests)
- Terminal'da curl (murakkab va noqulay)
- Kod yozib test qilish (vaqt ketadi)

**✅ Yaxshi usul:**
- **Postman** - Barcha HTTP methodlarni test qilish
- **Swagger** - Avtomatik dokumentatsiya + testing
- **ReDoc** - Professional dokumentatsiya

---

## 📚 Bu darsda nima o'rganamiz?

### 1. Postman - API Testing Tool 🧪
**Nimaga kerak:** API'ni tez va oson test qilish

**O'rganamiz:**
- ✅ Request yuborish (GET, POST, PUT, DELETE)
- ✅ Headers, Body, Query parameters
- ✅ Collection yaratish va ulashish
- ✅ Environment variables
- ✅ Tests yozish (automated testing)
- ✅ Team bilan ishlash

**Natija:** 1 soatda 100+ requestni test qilish!

---

### 2. Swagger/OpenAPI - Auto-generated Docs 📖
**Nimaga kerak:** Avtomatik dokumentatsiya yaratish

**O'rganamiz:**
- ✅ drf-spectacular o'rnatish
- ✅ Swagger UI sozlash
- ✅ Interactive API dokumentatsiya
- ✅ "Try it out" functionality
- ✅ Schema customization

**Natija:** Kod yozasiz, dokumentatsiya avtomatik yaratiladi!

---

### 3. ReDoc - Beautiful Documentation 🎨
**Nimaga kerak:** Professional va chiroyli dokumentatsiya

**O'rganamiz:**
- ✅ ReDoc sozlash
- ✅ Responsive dizayn
- ✅ Search functionality
- ✅ Theme customization

**Natija:** Startup'ga tayyor dokumentatsiya!

---

## 🗂️ Dars tuzilishi

### 📄 Fayllar

| Fayl | Tavsif | Sahifalar |
|------|--------|-----------|
| `README.md` | Kirish va umumiy ma'lumot | 5 |
| `postman-guide.md` | Postman to'liq guide | 30+ |
| `swagger-guide.md` | Swagger/OpenAPI guide | 20+ |
| `redoc-guide.md` | ReDoc guide | 10+ |
| `homework.md` | Uyga vazifa | 10+ |

**Jami:** 75+ sahifa professional ma'lumot!

---

### 📂 Papkalar

```
07-api-testing-docs/
├── postman/               ← Postman collection va environment
├── code/                  ← Library project (Swagger/ReDoc bilan)
└── screenshots/           ← Skrinshotlar
```

---

## 🚀 Qayerdan boshlaymiz?

### O'quv tartibi:

1. ✅ **README.md** - Ushbu faylni o'qing (5 daqiqa)
2. ✅ **postman-guide.md** - Postman'ni o'rganing (60 daqiqa)
3. ✅ **swagger-guide.md** - Swagger'ni o'rganing (45 daqiqa)
4. ✅ **redoc-guide.md** - ReDoc'ni o'rganing (30 daqiqa)
5. ✅ **code/library-project** - Amaliy qismni ko'ring (30 daqiqa)
6. ✅ **homework.md** - Vazifani bajaring (3-4 soat)

**Jami:** ~10 soat (nazariya + amaliyot)

---

## 🎯 Darsdan keyin siz nimani bilasiz?

### 1. Postman ✅
- Barcha HTTP methodlarni ishlatish
- Collection yaratish va export qilish
- Environment variables sozlash
- Automated tests yozish
- Team bilan collection ulashish

### 2. Swagger ✅
- drf-spectacular bilan dokumentatsiya
- Interactive API testing
- Schema customization
- OpenAPI 3.0 standard

### 3. ReDoc ✅
- Professional dokumentatsiya
- Responsive dizayn
- Search va navigation
- Custom branding

### 4. Best Practices ✅
- API versiyalash
- Error dokumentatsiya
- Authentication dokumentatsiya
- Real-world examples

---

## 💼 Real loyihalarda qanday ishlatiladi?

### Postman
- **Development:** Har bir endpoint'ni tezda test qilish
- **Testing:** Automated tests yozish
- **Team:** Collection ulashish, sync qilish
- **CI/CD:** Newman bilan automated testing

### Swagger
- **Frontend developers:** API'ni tushunish
- **QA testers:** Test case'lar yaratish
- **Mobile developers:** Endpoint'larni ko'rish
- **Partners:** Public API dokumentatsiya

### ReDoc
- **Public API:** Chiroyli dokumentatsiya
- **Documentation site:** Embed qilish
- **Marketing:** Professional ko'rinish
- **Partners:** API'ni tushuntirish

---

## 🛠️ Kerakli tool'lar

### 1. Postman (Bepul)
- **Desktop app:** [Yuklab olish](https://www.postman.com/downloads/)
- **Web version:** [postman.com](https://web.postman.com/)
- **Account:** [Ro'yxatdan o'tish](https://identity.getpostman.com/signup)

### 2. Python packages
```bash
pip install drf-spectacular
# yoki
pipenv install drf-spectacular
```

### 3. VS Code extensions (Ixtiyoriy)
- REST Client
- Thunder Client
- Postman

---

## 📊 Taqqoslash

| Feature | Postman | Swagger | ReDoc |
|---------|---------|---------|-------|
| **Testing** | ✅ A'lo | ✅ Yaxshi | ❌ Yo'q |
| **Dokumentatsiya** | ⚠️ Qo'lda | ✅ Avtomatik | ✅ Avtomatik |
| **Interactive** | ✅ A'lo | ✅ Yaxshi | ❌ Yo'q |
| **Chiroyli dizayn** | ⚠️ Oddiy | ⚠️ Oddiy | ✅ A'lo |
| **Team sharing** | ✅ A'lo | ⚠️ Link | ⚠️ Link |
| **Free** | ✅ Ha | ✅ Ha | ✅ Ha |
| **Setup** | 5 daqiqa | 10 daqiqa | 5 daqiqa |

### Xulosa:
- **Postman** - Testing uchun eng yaxshi
- **Swagger** - Interactive dokumentatsiya
- **ReDoc** - Chiroyli dokumentatsiya

**Hammasi kerak!** Uchala tool'ni birgalikda ishlating! ✅

---

## 🎓 Prerequisites (Bilish kerak)

Bu darsni boshlashdan oldin bilishingiz kerak:

1. ✅ **Lesson 01-06** - API, HTTP methods, Generic Views
2. ✅ **Django basics** - Models, Views, URLs
3. ✅ **DRF basics** - Serializers, Views
4. ✅ **HTTP methods** - GET, POST, PUT, PATCH, DELETE
5. ✅ **JSON format** - API response format

Agar bilmasangiz, avval oldingi darslarni o'qing!

---

## 🚦 Quick Start

### 5 daqiqada boshlang!

```bash
# 1. Postman yuklab oling
https://www.postman.com/downloads/

# 2. Library project'ga Swagger qo'shing
cd lessons/07-api-testing-docs/code/library-project
pipenv install drf-spectacular
python manage.py runserver

# 3. Brauzerda oching
http://localhost:8000/api/schema/swagger-ui/  # Swagger
http://localhost:8000/api/schema/redoc/       # ReDoc

# 4. Postman'da test qiling
GET http://localhost:8000/books/
```

**5 daqiqada tayyor!** 🎉

---

## 📖 Darsni o'qish tartibi

### 1️⃣ Postman (60 daqiqa)
**Fayl:** `postman-guide.md`

**Mavzular:**
- Postman o'rnatish
- Birinchi request
- Collection yaratish
- Environment variables
- Tests yozish

**Amaliyot:** Library API'ni test qilish

---

### 2️⃣ Swagger (45 daqiqa)
**Fayl:** `swagger-guide.md`

**Mavzular:**
- drf-spectacular o'rnatish
- Swagger UI sozlash
- Schema customization
- Try it out

**Amaliyot:** Library project'ga Swagger qo'shish

---

### 3️⃣ ReDoc (30 daqiqa)
**Fayl:** `redoc-guide.md`

**Mavzular:**
- ReDoc sozlash
- Theme customization
- Navigation

**Amaliyot:** ReDoc'ni customize qilish

---

### 4️⃣ Uyga vazifa (3-4 soat)
**Fayl:** `homework.md`

**Vazifalar:**
1. Library project'ga Swagger/ReDoc qo'shish
2. Postman collection yaratish
3. Barcha endpoints'ni test qilish
4. Screenshots olish

---

## ✅ Success Criteria

Darsni muvaffaqiyatli tugatsangiz:

1. ✅ Postman'da 10+ request yuborasiz
2. ✅ Collection yaratib, export qilasiz
3. ✅ Library project'da Swagger ishlaydi
4. ✅ ReDoc chiroyli ko'rinadi
5. ✅ Barcha endpoints dokumentatsiya qilingan
6. ✅ "Try it out" funksiyasi ishlaydi

---

## 🎯 Keyingi qadamlar

1. ✅ **Hozir:** `postman-guide.md`'ni oching va o'qing
2. ✅ **Keyin:** Postman'ni yuklab oling va o'rganing
3. ✅ **So'ngra:** `swagger-guide.md`'ni o'qing
4. ✅ **Oxirida:** `homework.md`'dagi vazifani bajaring

---

## 💡 Pro Tips

1. **Postman workspace yarating** - Barcha collection'lar bir joyda
2. **Environment variables ishlating** - Development/Production
3. **Collection'larni ulashing** - Team bilan ishlash
4. **Swagger customize qiling** - Brand colors qo'shing
5. **ReDoc'ni embed qiling** - Documentation website'ga

---

## ❓ Savollar?

Agar savol bo'lsa:
- Guide'larni diqqat bilan o'qing
- Screenshots'larga qarang
- code/library-project'dagi kodga qarang
- Telegram guruhida so'rang

---

## 📅 Dars ma'lumotlari

- **Dars raqami:** 07
- **Mavzu:** API Testing & Documentation
- **Davomiyligi:** ~10 soat (nazariya + amaliyot)
- **Qiyinlik:** ⭐⭐ O'rtacha
- **Tool'lar:** Postman, Swagger, ReDoc

---

**Tayyor bo'lsangiz, `postman-guide.md`'ni oching va boshlang!** 🚀

Happy learning! 