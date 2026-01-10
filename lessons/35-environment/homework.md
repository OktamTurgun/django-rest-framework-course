# Homework: Environment Setup

> Lesson 35 bo'yicha amaliy topshiriqlar

## Maqsad

Environment variables, `.env` fayllari va settings tashkil qilish bo'yicha amaliy ko'nikmalar hosil qilish.

---

## Topshiriq 1: .env fayl yaratish ⭐

**Vazifa:** Library project uchun to'liq `.env` fayl yaratish

### Talablar:

1. `.env` faylda quyidagi bo'limlar bo'lishi kerak:
   - Django settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
   - Database (PostgreSQL sozlamalari)
   - Email (SMTP sozlamalari)
   - Redis (Cache uchun)
   - AWS S3 (Optional)
   - Sentry (Optional)

2. `.env.example` template yaratish

3. `.gitignore` faylga `.env` qo'shish

### Namuna:

```bash
# .env
# ====================
# DJANGO SETTINGS
# ====================
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1

# ====================
# DATABASE
# ====================
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=yourpassword
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
# REDIS
# ====================
REDIS_URL=redis://localhost:6379/0

# ====================
# CELERY
# ====================
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

### Baholash mezoni:
- `.env` fayl to'liq (10 ball)
- `.env.example` yaratilgan (5 ball)
- `.gitignore` yangilangan (5 ball)

**Jami: 20 ball**

---

## Topshiriq 2: python-decouple integratsiyasi ⭐⭐

**Vazifa:** `settings.py` faylni `python-decouple` yordamida refactor qilish

### Qadamlar:

1. **O'rnatish:**
```bash
pip install python-decouple
```

2. **settings.py'ni yangilash:**
```python
from decouple import config, Csv

# Django settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database
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

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

# Redis
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

3. **Test qiling:**
```bash
python manage.py check
python manage.py runserver
```

### Baholash mezoni:
- python-decouple o'rnatilgan (5 ball)
- SECRET_KEY environment'dan olinadi (5 ball)
- Database sozlamalari (10 ball)
- Email sozlamalari (5 ball)
- Redis sozlamalari (5 ball)

**Jami: 30 ball**

---

## Topshiriq 3: Settings fayllarni ajratish ⭐⭐⭐

**Vazifa:** Settings fayllarni development, staging, production uchun ajratish

### Struktura:

```
library_project/
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── staging.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
```

### 1. base.py (Umumiy sozlamalar)

```python
# config/settings/base.py
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'django_filters',
    
    # Local apps
    'books',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### 2. development.py

```python
# config/settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Console email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ['127.0.0.1']

# Simple cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### 3. staging.py

```python
# config/settings/staging.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

# Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'staging.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 4. production.py

```python
# config/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
        'CONN_MAX_AGE': 600,
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

# Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Sentry (optional)
if config('SENTRY_DSN', default=None):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=config('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'production.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# AWS S3 (optional)
if config('USE_S3', default=False, cast=bool):
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
```

### 5. __init__.py (Automatic loading)

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

print(f"🚀 Running in {environment.upper()} mode")
```

### Test qiling:

```bash
# Development
export ENVIRONMENT=development  # Linux/Mac
set ENVIRONMENT=development     # Windows
python manage.py runserver

# Staging
export ENVIRONMENT=staging
python manage.py runserver

# Production
export ENVIRONMENT=production
python manage.py check --deploy
```

### Baholash mezoni:
- Struktura to'g'ri (10 ball)
- base.py to'liq (10 ball)
- development.py (5 ball)
- staging.py (5 ball)
- production.py (10 ball)
- __init__.py (automatic loading) (10 ball)

**Jami: 50 ball**

---

## Topshiriq 4: Environment Validator ⭐⭐

**Vazifa:** Environment variablelarni tekshiruvchi utility yaratish

### Fayl: `utils/validators.py`

```python
# utils/validators.py
from django.core.exceptions import ImproperlyConfigured
from decouple import config


class EnvironmentValidator:
    """Environment variables validator"""
    
    REQUIRED_VARS = [
        'SECRET_KEY',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
    
    PRODUCTION_REQUIRED = [
        'ALLOWED_HOSTS',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
    ]
    
    @classmethod
    def validate_all(cls):
        """Barcha environment variablelarni tekshirish"""
        print("🔍 Validating environment variables...")
        
        # Required variables
        for var in cls.REQUIRED_VARS:
            cls.validate_var(var)
        
        # Production specific
        environment = config('ENVIRONMENT', default='development')
        if environment == 'production':
            for var in cls.PRODUCTION_REQUIRED:
                cls.validate_var(var)
        
        print("✅ All environment variables are valid!")
    
    @classmethod
    def validate_var(cls, var_name):
        """Bitta variableni tekshirish"""
        try:
            value = config(var_name)
            if not value:
                raise ImproperlyConfigured(
                    f"❌ {var_name} is empty!"
                )
            print(f"✓ {var_name}: OK")
        except Exception as e:
            raise ImproperlyConfigured(
                f"❌ {var_name} is not set! Error: {str(e)}"
            )


def validate_environment():
    """Wrapper function"""
    EnvironmentValidator.validate_all()
```

### Ishlatish:

```python
# config/settings/base.py
from utils.validators import validate_environment

# Settings faylning oxirida
validate_environment()
```

Yoki management command:

```python
# books/management/commands/validate_env.py
from django.core.management.base import BaseCommand
from utils.validators import validate_environment


class Command(BaseCommand):
    help = 'Validate environment variables'
    
    def handle(self, *args, **options):
        try:
            validate_environment()
            self.stdout.write(
                self.style.SUCCESS('✅ Environment validation successful!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Validation failed: {str(e)}')
            )
```

```bash
python manage.py validate_env
```

### Baholash mezoni:
- Validator class yaratilgan (10 ball)
- REQUIRED_VARS ro'yxati (5 ball)
- validate_all() metodi (10 ball)
- Management command (5 ball)

**Jami: 30 ball**

---

## Topshiriq 5: Multi-environment testing ⭐⭐⭐

**Vazifa:** Turli muhitlarda test qilish

### 1. .env fayllar yaratish

```bash
# .env.development
ENVIRONMENT=development
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# .env.staging
ENVIRONMENT=staging
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_staging
DB_USER=staging_user
DB_PASSWORD=staging_pass
DB_HOST=localhost
DB_PORT=5432

# .env.production
ENVIRONMENT=production
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_production
DB_USER=prod_user
DB_PASSWORD=prod_pass
DB_HOST=localhost
DB_PORT=5432
```

### 2. Switch script yaratish

```python
# scripts/switch_env.py
import os
import shutil
import sys


def switch_environment(env):
    """Environment o'zgartirish"""
    env_file = f'.env.{env}'
    
    if not os.path.exists(env_file):
        print(f"❌ {env_file} topilmadi!")
        sys.exit(1)
    
    # Backup
    if os.path.exists('.env'):
        shutil.copy('.env', '.env.backup')
    
    # Switch
    shutil.copy(env_file, '.env')
    print(f"✅ Switched to {env.upper()} environment")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/switch_env.py [development|staging|production]")
        sys.exit(1)
    
    env = sys.argv[1]
    if env not in ['development', 'staging', 'production']:
        print("❌ Invalid environment!")
        sys.exit(1)
    
    switch_environment(env)
```

### Ishlatish:

```bash
# Development
python scripts/switch_env.py development
python manage.py runserver

# Staging
python scripts/switch_env.py staging
python manage.py runserver

# Production
python scripts/switch_env.py production
python manage.py check --deploy
```

### 3. Test qiling

Har bir muhitda quyidagilarni test qiling:
- Database connection
- Email sending (development - console, production - SMTP)
- Cache (development - memory, production - Redis)
- Static files
- Debug mode

### Baholash mezoni:
- .env fayllar yaratilgan (5 ball)
- switch_env.py script (10 ball)
- Development test (3 ball)
- Staging test (3 ball)
- Production test (4 ball)

**Jami: 25 ball**

---

## Bonus Topshiriq: Docker environment ⭐⭐⭐⭐

**Vazifa:** Docker environment yaratish (Docker darsidan oldin amaliyot)

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    environment:
      - ENVIRONMENT=development

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
```

### Ishlatish:

```bash
# Build
docker-compose build

# Run
docker-compose up

# Migrate
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Baholash mezoni:
- docker-compose.yml (10 ball)
- Dockerfile (5 ball)
- Services configured (10 ball)

**Jami: 25 ball (Bonus)**

---

## Topshiriqlarni topshirish

### GitHub PR yaratish:

```bash
# Branch yaratish
git checkout -b homework/lesson-35-environment

# Fayllarni qo'shish
git add .env.example
git add .gitignore
git add config/settings/
git add utils/validators.py
git add scripts/

# Commit
git commit -m "Complete Lesson 35 homework: Environment Setup"

# Push
git push origin homework/lesson-35-environment
```

### PR Description:

```markdown
## Lesson 35: Environment Setup - Homework

### Completed Tasks:

- [x] Task 1: .env fayl yaratish (20/20)
- [x] Task 2: python-decouple integratsiyasi (30/30)
- [x] Task 3: Settings fayllarni ajratish (50/50)
- [x] Task 4: Environment Validator (30/30)
- [x] Task 5: Multi-environment testing (25/25)
- [ ] Bonus: Docker environment (25/25)

### Total Score: 155/155 (+ 25 bonus)

### Screenshots:
- Development mode
- Staging mode
- Production mode
- Validator output

### Notes:
...
```

---

## Baholash jadvali

| Topshiriq | Ball | Status |
|-----------|------|--------|
| Task 1: .env fayl | 20 | ⭐ |
| Task 2: python-decouple | 30 | ⭐⭐ |
| Task 3: Settings ajratish | 50 | ⭐⭐⭐ |
| Task 4: Validator | 30 | ⭐⭐ |
| Task 5: Multi-env testing | 25 | ⭐⭐⭐ |
| **Jami** | **155** | |
| Bonus: Docker | 25 | ⭐⭐⭐⭐ |
| **Grand Total** | **180** | |

### Minimal ball: 100 (Task 1-3)
### O'rtacha ball: 130 (Task 1-4)
### A'lo ball: 155+ (Barcha tasklar)

---

## Yordam

Qiyinchilik bo'lsa:
1. [README.md](README.md) qayta o'qing
2. [Examples](examples/) papkasidagi misollarni ko'ring
3. GitHub Issues'da savol bering

---

**Omad! Keyingi darsda Docker o'rganamiz!**