# Lesson 35: Environment Setup

> Django loyihasini turli muhitlarda (development, staging, production) ishga tushirish uchun environment sozlamalari

## Maqsad

Ushbu darsda siz quyidagilarni o'rganasiz:
- Environment variables nima va nega kerak
- `.env` fayllari bilan ishlash
- `python-decouple` va `python-dotenv` kutubxonalari
- Settings fayllarni muhitlarga ajratish
- Secrets management (maxfiy ma'lumotlarni saqlash)
- Best practices va security

## Mundarija

- [Nazariya](#nazariya)
  - [Environment Variables nima?](#environment-variables-nima)
  - [Nega kerak?](#nega-kerak)
  - [.env fayllari](#env-fayllari)
- [Amaliyot](#amaliyot)
  - [python-decouple](#python-decouple)
  - [python-dotenv](#python-dotenv)
  - [Settings tashkil qilish](#settings-tashkil-qilish)
- [Best Practices](#best-practices)
- [Xavfsizlik](#xavfsizlik)
- [Homework](#homework)

---

## Nazariya

### Environment Variables nima?

**Environment Variables** - bu operatsion tizim darajasida saqlanadigan o'zgaruvchilar bo'lib, dasturlar uchun konfiguratsiya ma'lumotlarini taqdim etadi.

**Nima uchun muhim?**
```python
# ❌ YOMON - Kod ichida
SECRET_KEY = 'django-insecure-abc123...'
DATABASE_PASSWORD = 'mypassword123'

# ✅ YAXSHI - Environment variable
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_PASSWORD = os.getenv('DB_PASSWORD')
```

### Nega kerak?

#### 1. **Xavfsizlik (Security)**
```python
# Maxfiy ma'lumotlar kodda bo'lmaydi
SECRET_KEY = env('SECRET_KEY')
AWS_SECRET_KEY = env('AWS_SECRET_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
```

#### 2. **Moslashuvchanlik (Flexibility)**
```python
# Turli muhitlarda turli qiymatlar
DEBUG = env('DEBUG', default=False)  # Production: False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')  # ['localhost'] yoki ['example.com']
```

#### 3. **Portability (Ko'chma)**
```python
# Bir xil kod turli serverlarda ishlaydi
# Faqat environment o'zgaradi
```

#### 4. **12-Factor App**
> "Store config in the environment"
> - 12factor.net

---

### .env fayllari

`.env` fayl - environment variablelarni saqlash uchun oddiy text fayl.

**Struktura:**
```bash
# .env
KEY=VALUE
ANOTHER_KEY=another_value
```

**Misollar:**

```bash
# .env.example (template)
# Django settings
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True

# AWS
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# Redis
REDIS_URL=redis://localhost:6379/0

# Sentry
SENTRY_DSN=
```

---

## Amaliyot

### python-decouple

**O'rnatish:**
```bash
pip install python-decouple
```

**Asosiy foydalanish:**

```python
# settings.py
from decouple import config, Csv

# String
SECRET_KEY = config('SECRET_KEY')

# Boolean
DEBUG = config('DEBUG', default=False, cast=bool)

# Integer
MAX_CONNECTIONS = config('MAX_CONNECTIONS', default=10, cast=int)

# Float
TAX_RATE = config('TAX_RATE', cast=float)

# List
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# .env: ALLOWED_HOSTS=localhost,127.0.0.1,example.com

# Dictionary (JSON)
import json
AWS_SETTINGS = config('AWS_SETTINGS', cast=json.loads)
# .env: AWS_SETTINGS={"region": "us-east-1", "bucket": "my-bucket"}
```

**Database sozlamalari:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432', cast=int),
    }
}
```

**Email sozlamalari:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
```

---

### python-dotenv

**O'rnatish:**
```bash
pip install python-dotenv
```

**Asosiy foydalanish:**

```python
# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# .env faylni yuklash
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Environment variablelarni olish
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
DATABASE_URL = os.getenv('DATABASE_URL')
```

**dj-database-url bilan:**
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}
```

---

### Settings tashkil qilish

#### Variant 1: Oddiy struktura

```
config/
├── settings/
│   ├── __init__.py
│   ├── base.py       # Umumiy sozlamalar
│   ├── development.py
│   ├── staging.py
│   └── production.py
```

**base.py:**
```python
# config/settings/base.py
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    # ...
    'rest_framework',
    'books',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ...
]

# Umumiy sozlamalar
```

**development.py:**
```python
# config/settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

**production.py:**
```python
# config/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

**__init__.py:**
```python
# config/settings/__init__.py
from decouple import config

environment = config('ENVIRONMENT', default='development')

if environment == 'production':
    from .production import *
elif environment == 'staging':
    from .staging import *
else:
    from .development import *
```

---

#### Variant 2: Advanced struktura

```
config/
├── settings/
│   ├── __init__.py
│   ├── base.py
│   ├── development.py
│   ├── production.py
│   └── components/
│       ├── __init__.py
│       ├── database.py
│       ├── cache.py
│       ├── email.py
│       ├── storage.py
│       └── security.py
```

**database.py:**
```python
# config/settings/components/database.py
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432', cast=int),
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=600, cast=int),
    }
}
```

**cache.py:**
```python
# config/settings/components/cache.py
from decouple import config

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

## Best Practices

### 1. .env fayl strukturasi

```bash
# .env
# ====================
# DJANGO SETTINGS
# ====================
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1

# ====================
# DATABASE
# ====================
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# ====================
# EMAIL
# ====================
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# ====================
# AWS S3
# ====================
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket
AWS_S3_REGION_NAME=us-east-1

# ====================
# REDIS
# ====================
REDIS_URL=redis://localhost:6379/0

# ====================
# CELERY
# ====================
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ====================
# SENTRY
# ====================
SENTRY_DSN=your_sentry_dsn

# ====================
# THIRD PARTY APIS
# ====================
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
```

### 2. .env.example yaratish

```bash
# .env.example
# Bu faylni Git'ga commit qiling
# Haqiqiy qiymatlar bo'lmagan template

SECRET_KEY=
DEBUG=True
ENVIRONMENT=development

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Va hokazo...
```

### 3. .gitignore

```bash
# .gitignore
.env
.env.local
.env.*.local
*.env

# Lekin .env.example'ni ignore qilmang!
```

### 4. Type casting

```python
# settings.py
from decouple import config

# Boolean
DEBUG = config('DEBUG', default=False, cast=bool)
# .env: DEBUG=True  → True
# .env: DEBUG=False → False
# .env: DEBUG=1     → True
# .env: DEBUG=0     → False

# Integer
MAX_UPLOAD_SIZE = config('MAX_UPLOAD_SIZE', default=5242880, cast=int)
# .env: MAX_UPLOAD_SIZE=10485760

# Float
TAX_RATE = config('TAX_RATE', default=0.15, cast=float)
# .env: TAX_RATE=0.18

# List
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# .env: ALLOWED_HOSTS=localhost,127.0.0.1,example.com
# Result: ['localhost', '127.0.0.1', 'example.com']
```

### 5. Default qiymatlar

```python
# Development uchun default qiymatlar
DEBUG = config('DEBUG', default=True, cast=bool)
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', default='5432')

# Production'da default bo'lmasligi kerak
SECRET_KEY = config('SECRET_KEY')  # Majburiy!
DB_PASSWORD = config('DB_PASSWORD')  # Majburiy!
```

---

## Xavfsizlik

### 1. Hech qachon commit qilmang

```bash
# ❌ Hech qachon!
git add .env
git commit -m "Add env file"

# ✅ .gitignore'ga qo'shing
echo ".env" >> .gitignore
```

### 2. Secret rotation

```python
# Vaqti-vaqti bilan o'zgartiring
SECRET_KEY = config('SECRET_KEY')
DATABASE_PASSWORD = config('DB_PASSWORD')
API_KEYS = config('API_KEYS')
```

### 3. Secrets validator

```python
# utils/validators.py
from django.core.exceptions import ImproperlyConfigured
from decouple import config

def validate_environment():
    """Majburiy environment variablelarni tekshirish"""
    required = [
        'SECRET_KEY',
        'DB_NAME',
        'DB_PASSWORD',
    ]
    
    for var in required:
        try:
            value = config(var)
            if not value:
                raise ImproperlyConfigured(
                    f"{var} environment variable is required"
                )
        except Exception:
            raise ImproperlyConfigured(
                f"{var} environment variable is not set"
            )
```

### 4. Encryption

```python
# cryptography kutubxonasi bilan
from cryptography.fernet import Fernet

# Key generation
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted = cipher.encrypt(b"my_secret_password")

# Decrypt
decrypted = cipher.decrypt(encrypted)
```

---

## Turli muhitlar

### Development (.env.development)

```bash
# .env.development
DEBUG=True
ENVIRONMENT=development

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# AWS mock
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
```

### Staging (.env.staging)

```bash
# .env.staging
DEBUG=False
ENVIRONMENT=staging

DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_staging
DB_USER=staging_user
DB_PASSWORD=staging_password
DB_HOST=staging-db.example.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com

AWS_STORAGE_BUCKET_NAME=library-staging
```

### Production (.env.production)

```bash
# .env.production
DEBUG=False
ENVIRONMENT=production

DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_production
DB_USER=prod_user
DB_PASSWORD=super_secure_password
DB_HOST=prod-db.example.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

AWS_STORAGE_BUCKET_NAME=library-production

SENTRY_DSN=https://...
```

---

## Docker bilan ishlash

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    env_file:
      - .env
    environment:
      - ENVIRONMENT=production
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

---

## Testing

**conftest.py:**
```python
# tests/conftest.py
import os
import pytest
from django.conf import settings

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

@pytest.fixture
def set_test_env(monkeypatch):
    """Test environment variables"""
    monkeypatch.setenv('SECRET_KEY', 'test-secret-key')
    monkeypatch.setenv('DEBUG', 'True')
    monkeypatch.setenv('DB_NAME', 'test_db')
```

---

## Tools va yordamchi dasturlar

### 1. django-environ

```bash
pip install django-environ
```

```python
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
DATABASES = {
    'default': env.db()
}
```

### 2. environs

```bash
pip install environs
```

```python
from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
DATABASE_URL = env.dj_db_url('DATABASE_URL')
```

---

## Xulosa

### Nimani o'rgandik:

1. Environment variables va ularning ahamiyati
2. `.env` fayllari bilan ishlash
3. `python-decouple` va `python-dotenv` kutubxonalari
4. Settings fayllarni tashkil qilish
5. Turli muhitlar uchun sozlamalar
6. Security best practices
7. Docker va testing bilan integratsiya

### Keyingi qadamlar:

- [Lesson 36: Docker](../36-docker/) - Containerization
- [Lesson 37: Deployment](../37-deployment/) - Production deployment
- [Lesson 38: CI/CD](../38-cicd/) - Automated deployment

---

## Qo'shimcha resurslar

- [12 Factor App](https://12factor.net/)
- [python-decouple Documentation](https://github.com/HBNetwork/python-decouple)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)

---

## Homework

[Homework topshiriqlari](homework.md) - Environment setup amaliyoti

---

**Keyingi dars:** [36 - Docker →](../36-docker/)

**Oldingi dars:** [← 34 - Analytics & Reporting](../34-analytics-reporting/)

---

<div align="center">

**Happy Coding!**

Savollar bo'lsa, Issues bo'limida so'rang!

</div>