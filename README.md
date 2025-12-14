# Django REST Framework - Professional Kurs

> Django REST Framework'ni 0 dan professional darajagacha o'rganish uchun to'liq qo'llanma

[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

## Kurs haqida

Ushbu kurs Django REST Framework (DRF) asoslaridan tortib, murakkab production-ready loyihalar qurishgacha bo'lgan barcha kerakli bilimlarni o'z ichiga oladi. Har bir dars nazariy qism, amaliy mashqlar va real-world misollar bilan to'ldirilgan.

### Kurs maqsadlari

- ✅ Professional RESTful API yaratish
- ✅ Production-ready backend development
- ✅ Security best practices
- ✅ Testing va deployment
- ✅ Real-world loyihalar

## Kimlar uchun?

- ✅ Django asoslarini biladigan dasturchilar
- ✅ Backend development o'rganmoqchi bo'lganlar
- ✅ RESTful API yaratishni xohlaganlar
- ✅ Junior → Middle → Senior yo'lida borayotganlar
- ✅ Real loyihalarda ishlashni istaydiganlar

## Kurs statistikasi

```
📈 Progress: [██████░░░░] 32% Complete

✅ Completed: 15 lessons
🔄 In Progress: Lesson 16
⏳ Remaining: 32 lessons
🎯 Total: 47 lessons + 3 projects

⏱ Estimated time: 140 hours (3.5 months)
💼 Job-ready after: 38 lessons (~100 hours) - Deployment tugagach
🏆 Professional level: 42 lessons (~115 hours) - Advanced Topics tugagach
🌟 Expert level: 47 lessons (~140 hours) - Barcha darslar
```

## 🗂 Repository strukturasi

```
📦 django-rest-framework-course
 ┣ 📂 lessons/                # Barcha darslar
 ┃ ┣ 📂 01-api-basics/
 ┃ ┣ 📂 02-http-methods/
 ┃ ┣ 📂 ...
 ┃ ┗ 📂 40-final-project/
 ┣ 📂 projects/               # Katta loyihalar
 ┃ ┣ 📂 instagram-clone/
 ┃ ┗ 📂 warehouse-system/
 ┣ 📂 resources/              # Qo'shimcha materiallar
 ┃ ┣ 📂 cheatsheets/
 ┃ ┣ 📂 tools/
 ┃ ┗ 📂 references/
 ┗ 📄 README.md               # Ushbu fayl
```

##  Tezkor boshlash

### Talablar

```
Python 3.8+
Django 5.0+
Django REST Framework 3.14+
PostgreSQL 13+
Redis 6+ (caching uchun)
```

### O'rnatish

```bash
# 1. Repository'ni clone qiling
git clone https://github.com/your-username/django-rest-framework-course.git
cd django-rest-framework-course

# 2. Virtual muhit yaratish
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Dependencies o'rnatish
pip install -r requirements.txt

# 4. Database setup
python manage.py migrate

# 5. Superuser yaratish
python manage.py createsuperuser

# 6. Server ishga tushirish
python manage.py runserver
```

## Darslar ro'yxati

### SECTION 1: Foundation (Lessons 1-7)
**Status:** COMPLETED

#### 1.1 API Asoslari
- [x] [01 - API bilan tanishuv](lessons/01-api-basics/) - REST, HTTP, JSON
- [x] [02 - HTTP Methods va Status Kodlar](lessons/02-http-methods/) - GET, POST, PUT, DELETE
- [x] [03 - Loyihani boshlash](lessons/03-project-setup/) - Django + DRF setup

#### 1.2 Views
- [x] [04 - ListAPIView](lessons/04-list-api-view/) - Oddiy list view
- [x] [05 - Function va CRUD Views](lessons/05-function-crud-views/) - @api_view decorator
- [x] [06 - Generic Views](lessons/06-generic-views/) - Mixins, Generic views

#### 1.3 Testing & Documentation
- [x] [07 - Postman, Swagger, Redoc](lessons/07-api-testing-docs/) - API testing tools

---

### SECTION 2: Core Concepts (Lessons 8-15)
**Status:** COMPLETED

#### 2.1 APIView
- [x] [08 - APIView - Part 1](lessons/08-apiview-part1/) - APIView basics
- [x] [09 - APIView - Part 2](lessons/09-apiview-part2/) - Advanced APIView

#### 2.2 Serializers
- [x] [10 - ModelSerializer vs Serializer](lessons/10-serializers/) - Serializer types
- [x] [11 - Validation](lessons/11-validation/) - Field & Object validation

#### 2.3 Authentication
- [x] [12 - Authentication turlari](lessons/12-auth-types/) - Token, Session, JWT
- [x] [13 - Auth implementation](lessons/13-auth-implementation/) - Login/Logout
- [x] [14 - User Registration](lessons/14-user-registration/) - Signup endpoint

#### 2.4 ViewSet & Router
- [x] [15 - ViewSet va Router](lessons/15-viewset-router/) - Modern approach

---

### SECTION 3: Security & Permissions (Lessons 16-17)
**Status:** IN PROGRESS

#### 3.1 Permissions CRITICAL
- [ ] [16 - Permissions](lessons/16-permissions/) - IsAuthenticated, Custom permissions
  - Built-in permissions
  - Django model permissions
  - Custom permissions (IsOwner)
  - Object-level permissions
  - Combining permissions

#### 3.2 Advanced Serializers
- [ ] [17 - Nested Serializers & Relations](lessons/17-nested-serializers/)
  - Nested serializers
  - Serializer relations
  - Many-to-Many
  - Writable nested

---

### SECTION 4: Data Management (Lessons 18-20)
**Status:** TODO

#### 4.1 Filtering & Search
- [ ] [18 - Filtering, Search, Ordering](lessons/18-filtering-search/)
  - DjangoFilterBackend
  - SearchFilter
  - OrderingFilter
  - Custom filters

#### 4.2 Pagination
- [ ] [19 - Pagination](lessons/19-pagination/)
  - PageNumberPagination
  - LimitOffsetPagination
  - CursorPagination
  - Custom pagination

#### 4.3 File Upload
- [ ] [20 - File Upload](lessons/20-file-upload/)
  - ImageField, FileField
  - MultiPartParser
  - File validation
  - Storage backends

---

### SECTION 5: Performance & Quality (Lessons 21-23)
**Status:** TODO

#### 5.1 Throttling
- [ ] [21 - Throttling](lessons/21-throttling/)
  - Rate limiting
  - AnonRateThrottle
  - UserRateThrottle
  - Custom throttles

#### 5.2 Optimization
- [ ] [22 - Query Optimization](lessons/22-optimization/)
  - select_related()
  - prefetch_related()
  - N+1 problem
  - Database indexes

#### 5.3 Testing
- [ ] [23 - Unit Testing](lessons/23-testing/)
  - APITestCase
  - Test fixtures
  - Test coverage
  - Integration tests

---

### SECTION 6: Production Features (Lessons 24-28)
**Status:** TODO

#### 6.1 Caching 
- [ ] [24 - Caching](lessons/24-caching/)
  - Redis cache
  - Cache strategies
  - Cache invalidation

#### 6.2 CORS 
- [ ] [25 - CORS](lessons/25-cors/)
  - django-cors-headers
  - CORS configuration
  - Security

#### 6.3 Versioning 
- [ ] [26 - API Versioning](lessons/26-versioning/)
  - URL versioning
  - Header versioning
  - Namespace versioning

#### 6.4 Error Handling 
- [ ] [27 - Error Handling](lessons/27-error-handling/)
  - Custom exceptions
  - Exception handler
  - Logging
  - Sentry

#### 6.5 Signals 
- [ ] [28 - Signals & Webhooks](lessons/28-signals/)
  - Django signals
  - Custom signals
  - Webhooks

---

###  SECTION 7: Notifications & Communication (Lessons 29-30)
**Status:**  TODO

#### 7.1 Email Notifications
- [ ] [29 - Email Notifications](lessons/29-email-notifications/)
  - SMTP configuration
  - SendGrid integration
  - Email templates
  - Async email sending

#### 7.2 SMS & Push Notifications
- [ ] [30 - SMS & Push Notifications](lessons/30-sms-push-notifications/)
  - Twilio SMS integration
  - Firebase Cloud Messaging (FCM)
  - Push notification strategies

---

###  SECTION 8: Advanced Authentication (Lessons 31-32)
**Status:**  TODO

#### 8.1 Social Authentication
- [ ] [31 - OAuth2 & Social Authentication](lessons/31-oauth2-social-auth/)
  - Google OAuth2
  - GitHub OAuth
  - Facebook Login
  - django-allauth

#### 8.2 Two-Factor Authentication
- [ ] [32 - Two-Factor Authentication (2FA)](lessons/32-two-factor-auth/)
  - TOTP (Google Authenticator)
  - SMS verification
  - Backup codes

---

###  SECTION 9: Advanced Features (Lessons 33-34)
**Status:**  TODO

#### 9.1 Advanced Search
- [ ] [33 - Advanced Search (Elasticsearch)](lessons/33-elasticsearch/)
  - Elasticsearch setup
  - django-elasticsearch-dsl
  - Full-text search
  - Search suggestions & autocomplete

#### 9.2 Analytics & Reporting
- [ ] [34 - Analytics & Reporting](lessons/34-analytics-reporting/)
  - Excel export (openpyxl)
  - PDF generation (ReportLab)
  - Dashboard statistics
  - Aggregation queries

---

###  SECTION 10: Deployment (Lessons 35-38)
**Status:**  TODO

#### 10.1 Environment
- [ ] [35 - Environment Setup](lessons/35-environment/)
  - .env files
  - Settings organization
  - Secrets management

#### 10.2 Docker
- [ ] [36 - Docker](lessons/36-docker/)
  - Dockerfile
  - docker-compose
  - PostgreSQL + Redis

#### 10.3 Production Deployment
- [ ] [37 - Deployment](lessons/37-deployment/)
  - Gunicorn
  - Nginx
  - SSL/HTTPS
  - Domain setup
  - Railway/Heroku/AWS

#### 10.4 CI/CD
- [ ] [38 - CI/CD](lessons/38-cicd/)
  - GitHub Actions
  - Automated testing
  - Automated deployment

---

###  SECTION 11: Advanced Topics (Lessons 39-42)
**Status:**  TODO

#### 11.1 Real-time
- [ ] [39 - WebSockets](lessons/39-websockets/)
  - Django Channels
  - Real-time notifications

#### 11.2 Background Tasks
- [ ] [40 - Celery](lessons/40-celery/)
  - Async tasks
  - Periodic tasks
  - Task queues

#### 11.3 GraphQL (Optional)
- [ ] [41 - GraphQL](lessons/41-graphql/)
  - Graphene-Django
  - Queries & Mutations

#### 11.4 Microservices (Optional)
- [ ] [42 - Microservices](lessons/42-microservices/)
  - Service architecture
  - API Gateway

---

###  SECTION 12: Best Practices (Lessons 43-46)
**Status:**  TODO

#### 12.1 Design Patterns
- [ ] [43 - Design Patterns](lessons/43-design-patterns/)
  - Repository pattern
  - Service layer
  - Dependency injection

#### 12.2 Code Organization
- [ ] [44 - Code Organization](lessons/44-code-organization/)
  - App structure
  - Reusable components
  - Utils & helpers

#### 12.3 Security
- [ ] [45 - Security Best Practices](lessons/45-security/)
  - SQL injection prevention
  - XSS, CSRF protection
  - Input validation
  - API key management

#### 12.4 Final Project
- [ ] [46 - Final Project](lessons/46-final-project/)
  - E-commerce API
  - All concepts combined
  - Production deployment

---

###  SECTION 13: Infrastructure (Lesson 47) - Optional
**Status:**  TODO

#### 13.1 Kubernetes
- [ ] [47 - Kubernetes Basics](lessons/47-kubernetes/)
  - Kubernetes concepts
  - Deployment configuration
  - Helm charts
  - Scaling strategies

---

## 🏗 Loyihalar

###  Project 1: Instagram Clone
To'liq Instagram kabi ijtimoiy tarmoq loyihasi.

**Features:**
- User authentication & profiles
- Posts (images, videos)
- Comments & Likes
- Follow system
- Real-time notifications
- Stories

 [Loyihaga o'tish](projects/instagram-clone/)

---

###  Project 2: Warehouse System
Omborxona boshqaruv tizimi (Mock Task)

**Features:**
- Product management
- Inventory tracking
- Suppliers & Orders
- Reports & Analytics
- Role-based access

 [Loyihaga o'tish](projects/warehouse-system/)

---

###  Project 3: E-commerce API
To'liq e-commerce backend

**Features:**
- Products & Categories
- Shopping cart
- Payment integration
- Order management
- Admin dashboard

 [Loyihaga o'tish](projects/ecommerce-api/)

---

##  Qo'shimcha resurslar

###  Cheatsheets
- [DRF Cheatsheet](resources/cheatsheets/drf-cheatsheet.md)
- [Django ORM](resources/cheatsheets/django-orm.md)
- [Git Commands](resources/cheatsheets/git-commands.md)
- [PostgreSQL](resources/cheatsheets/postgresql.md)

### 🛠 Tools
- [Postman Collections](resources/tools/postman/)
- [Docker Configs](resources/tools/docker/)
- [VS Code Settings](resources/tools/vscode/)
- [Helper Scripts](resources/tools/scripts/)

### References
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [REST API Guidelines](resources/references/rest-guidelines.md)
- [Best Practices](resources/references/best-practices.md)

---

## O'rganish strategiyasi

### Beginner Path (Job-ready)
**Time:** ~70 hours | **Lessons:** 1-23

```
Foundation → Core → Security → Data Management → Testing → Deployment
```

**Result:** Junior Backend Developer position

---

### Intermediate Path (Professional)
**Time:** ~85 hours | **Lessons:** 1-28

```
Beginner Path + Production Features + Performance
```

**Result:** Middle Backend Developer position

---

### Advanced Path (Expert)
**Time:** ~120 hours | **Lessons:** 1-40

```
All lessons + All projects + Advanced topics
```

**Result:** Senior Backend Developer position

---

## O'rganish maslahatlari

###  Do'st (Qiling)
-  Har kuni 1-2 soat ajrating
-  Kodlarni o'zingiz yozing
-  Xatolar bilan ishlashni o'rganing
-  GitHub'ga commit qiling
-  Homework'larni bajaring
-  Loyihalar ustida ishlang

### ❌ Don'ts (Qilmang)
- ❌ Darslarni o'tkazib yubormang
- ❌ Copy-paste qilmang
- ❌ Tushunmay keyingisiga o'tmang
- ❌ Testing'ni skip qilmang
- ❌ Documentation yozishni unutmang

---

## 📈 Progress Tracking

### Sizning progressingiz
```python
# lessons/progress.py da track qiling

completed_lessons = 15
total_lessons = 40

progress = (completed_lessons / total_lessons) * 100
print(f"Progress: {progress}%")  # 37.5%

# Keyingi milestone
next_milestone = 23  # Job-ready
remaining = next_milestone - completed_lessons
print(f"Remaining to job-ready: {remaining} lessons")  # 8 lessons
```

---

## Contributing

Xatolarni topdingizmi yoki yaxshilash taklifingiz bormi?

1.  Fork the repository
2.  Create feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to branch (`git push origin feature/AmazingFeature`)
5.  Open Pull Request

---

## Bog'lanish

- 💬 **GitHub Issues** - Savol va muammolar
- 🗨️ **Discussions** - Muhokamalar
- 📧 **Email** - uktamturgunov30@gmail.com

---

## License

MIT License - [LICENSE](LICENSE)

---

## Support

Agar kurs foydali bo'lsa:
-  Star this repository
-  Fork va share qiling
-  Boshqalarga tavsiya qiling

---

## Acknowledgments

- Django Team
- DRF Community
- All contributors
- You for learning! 

---

## Stats

![GitHub stars](https://img.shields.io/github/stars/username/repo?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/repo?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/username/repo?style=social)

---

<div align="center">

### Ready to build amazing APIs?

**Start with Lesson 1 →** [API bilan tanishuv](lessons/01-api-basics/)

---

**Made with ❤️ by Django Developers**

**Happy Coding!**

</div>

---

## Roadmap

### 2024 Q4
- [x] Lessons 1-15
- [ ] Lessons 16-23
- [ ] Instagram Clone Project

### 2025 Q1
- [ ] Lessons 24-32
- [ ] Warehouse System Project
- [ ] Video tutorials

### 2025 Q2
- [ ] Lessons 33-40
- [ ] E-commerce Project
- [ ] Live coding sessions

---

> "The best way to learn is by building real projects" - Unknown

> "API - zamonaviy dasturlashning tili" - Django REST Framework Course