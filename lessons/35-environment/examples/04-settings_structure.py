"""
Lesson 35: Environment Setup - Example 04
Settings Structure and Organization

Bu misolda:
- Multi-environment settings structure
- Settings inheritance
- Component-based settings
- Automatic environment loading
- Settings factory pattern
"""

import os
from pathlib import Path
from decouple import config, Csv


# =====================================
# 1. SIMPLE SETTINGS STRUCTURE
# =====================================

def simple_structure_example():
    """Oddiy settings strukturasi"""
    print("=" * 50)
    print("1. SIMPLE SETTINGS STRUCTURE")
    print("=" * 50)
    
    print("""
Directory structure:
    
config/
├── __init__.py
├── settings.py          # Single file (simple projects)
├── urls.py
└── wsgi.py

# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
    }
}
    """)
    print()


# =====================================
# 2. SPLIT SETTINGS STRUCTURE
# =====================================

def split_structure_example():
    """Settings fayllarni ajratish"""
    print("=" * 50)
    print("2. SPLIT SETTINGS STRUCTURE")
    print("=" * 50)
    
    print("""
Directory structure:

config/
├── settings/
│   ├── __init__.py      # Automatic loader
│   ├── base.py          # Common settings
│   ├── development.py   # Development settings
│   ├── staging.py       # Staging settings
│   └── production.py    # Production settings
├── urls.py
└── wsgi.py

Usage:
    export ENVIRONMENT=development  # Linux/Mac
    set ENVIRONMENT=development     # Windows
    python manage.py runserver
    """)
    print()


# =====================================
# 3. BASE SETTINGS
# =====================================

class BaseSettings:
    """Base settings - umumiy sozlamalar"""
    
    # Build paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Security
    SECRET_KEY = config('SECRET_KEY')
    
    # Application definition
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
        'corsheaders',
        
        # Local apps
        'books',
        'users',
    ]
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'corsheaders.middleware.CorsMiddleware',
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
    
    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True
    
    # Static files
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_DIRS = [BASE_DIR / 'static']
    
    # Media files
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    
    # Default primary key field type
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    
    # REST Framework
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
        'DEFAULT_FILTER_BACKENDS': [
            'django_filters.rest_framework.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',
            'rest_framework.filters.OrderingFilter',
        ],
    }
    
    @classmethod
    def print_config(cls):
        """Configuration'ni ko'rsatish"""
        print("Base Settings:")
        print(f"  BASE_DIR: {cls.BASE_DIR}")
        print(f"  INSTALLED_APPS: {len(cls.INSTALLED_APPS)} apps")
        print(f"  MIDDLEWARE: {len(cls.MIDDLEWARE)} middlewares")


def base_settings_example():
    """Base settings example"""
    print("=" * 50)
    print("3. BASE SETTINGS")
    print("=" * 50)
    
    BaseSettings.print_config()
    print()


# =====================================
# 4. DEVELOPMENT SETTINGS
# =====================================

class DevelopmentSettings(BaseSettings):
    """Development environment settings"""
    
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
    
    # Database - SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BaseSettings.BASE_DIR / 'db.sqlite3',
        }
    }
    
    # Email - Console backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    # Cache - Simple in-memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    
    # Debug Toolbar
    INSTALLED_APPS = BaseSettings.INSTALLED_APPS + [
        'debug_toolbar',
    ]
    
    MIDDLEWARE = BaseSettings.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    
    INTERNAL_IPS = ['127.0.0.1']
    
    # CORS - Allow all for development
    CORS_ALLOW_ALL_ORIGINS = True
    
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
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    
    @classmethod
    def print_config(cls):
        """Configuration'ni ko'rsatish"""
        print("Development Settings:")
        print(f"  DEBUG: {cls.DEBUG}")
        print(f"  ALLOWED_HOSTS: {cls.ALLOWED_HOSTS}")
        print(f"  DATABASE: SQLite")
        print(f"  EMAIL: Console backend")
        print(f"  CACHE: In-memory")
        print(f"  Debug Toolbar: Enabled")


def development_settings_example():
    """Development settings example"""
    print("=" * 50)
    print("4. DEVELOPMENT SETTINGS")
    print("=" * 50)
    
    DevelopmentSettings.print_config()
    print()


# =====================================
# 5. STAGING SETTINGS
# =====================================

class StagingSettings(BaseSettings):
    """Staging environment settings"""
    
    DEBUG = False
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
    
    # Database - PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default=5432, cast=int),
            'CONN_MAX_AGE': 600,
        }
    }
    
    # Email - SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    
    # Cache - Redis
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
    
    # CORS
    CORS_ALLOWED_ORIGINS = config(
        'CORS_ALLOWED_ORIGINS',
        default='http://localhost:3000',
        cast=Csv()
    )
    
    # Security (moderate)
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': BaseSettings.BASE_DIR / 'logs' / 'staging.log',
                'formatter': 'verbose',
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
    
    @classmethod
    def print_config(cls):
        """Configuration'ni ko'rsatish"""
        print("Staging Settings:")
        print(f"  DEBUG: {cls.DEBUG}")
        print(f"  DATABASE: PostgreSQL")
        print(f"  EMAIL: SMTP")
        print(f"  CACHE: Redis")
        print(f"  Security: Moderate")


def staging_settings_example():
    """Staging settings example"""
    print("=" * 50)
    print("5. STAGING SETTINGS")
    print("=" * 50)
    
    # Mock environment variables
    os.environ['ALLOWED_HOSTS'] = 'staging.example.com'
    os.environ['DB_NAME'] = 'library_staging'
    os.environ['DB_USER'] = 'staging_user'
    os.environ['DB_PASSWORD'] = 'staging_pass'
    os.environ['EMAIL_HOST'] = 'smtp.example.com'
    os.environ['EMAIL_PORT'] = '587'
    os.environ['EMAIL_HOST_USER'] = 'staging@example.com'
    os.environ['EMAIL_HOST_PASSWORD'] = 'email_pass'
    os.environ['REDIS_URL'] = 'redis://staging-redis:6379/0'
    
    StagingSettings.print_config()
    print()


# =====================================
# 6. PRODUCTION SETTINGS
# =====================================

class ProductionSettings(BaseSettings):
    """Production environment settings"""
    
    DEBUG = False
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
    
    # Database - PostgreSQL with connection pooling
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default=5432, cast=int),
            'CONN_MAX_AGE': 600,
            'OPTIONS': {
                'connect_timeout': 10,
            }
        }
    }
    
    # Email - SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')
    
    # Cache - Redis
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
            },
            'KEY_PREFIX': 'library',
            'TIMEOUT': 300,
        }
    }
    
    # CORS
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
    CORS_ALLOW_CREDENTIALS = True
    
    # Security settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Session
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # CSRF
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Strict'
    
    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': BaseSettings.BASE_DIR / 'logs' / 'production.log',
                'maxBytes': 1024 * 1024 * 15,  # 15MB
                'backupCount': 10,
                'formatter': 'verbose',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false'],
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file', 'mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['file', 'mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }
    
    # AWS S3 (optional)
    USE_S3 = config('USE_S3', default=False, cast=bool)
    
    if USE_S3:
        AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
        AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        
        # Static files
        STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
        
        # Media files
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    
    @classmethod
    def print_config(cls):
        """Configuration'ni ko'rsatish"""
        print("Production Settings:")
        print(f"  DEBUG: {cls.DEBUG}")
        print(f"  DATABASE: PostgreSQL (pooled)")
        print(f"  EMAIL: SMTP")
        print(f"  CACHE: Redis")
        print(f"  Security: Full")
        print(f"  HTTPS: Required")
        print(f"  HSTS: Enabled (1 year)")
        print(f"  S3: {'Enabled' if cls.USE_S3 else 'Disabled'}")


def production_settings_example():
    """Production settings example"""
    print("=" * 50)
    print("6. PRODUCTION SETTINGS")
    print("=" * 50)
    
    # Mock environment variables
    os.environ['ALLOWED_HOSTS'] = 'example.com,www.example.com'
    os.environ['DB_NAME'] = 'library_production'
    os.environ['DB_USER'] = 'prod_user'
    os.environ['DB_PASSWORD'] = 'super_secure_password'
    os.environ['DB_HOST'] = 'prod-db.example.com'
    os.environ['EMAIL_HOST'] = 'smtp.example.com'
    os.environ['EMAIL_PORT'] = '587'
    os.environ['EMAIL_HOST_USER'] = 'noreply@example.com'
    os.environ['EMAIL_HOST_PASSWORD'] = 'email_password'
    os.environ['REDIS_URL'] = 'redis://prod-redis:6379/0'
    os.environ['CORS_ALLOWED_ORIGINS'] = 'https://example.com,https://www.example.com'
    
    ProductionSettings.print_config()
    print()


# =====================================
# 7. AUTOMATIC ENVIRONMENT LOADING
# =====================================

def get_settings():
    """
    Automatic settings loader
    
    config/settings/__init__.py'ga qo'yiladi
    """
    environment = config('ENVIRONMENT', default='development')
    
    settings_map = {
        'development': DevelopmentSettings,
        'staging': StagingSettings,
        'production': ProductionSettings,
    }
    
    settings_class = settings_map.get(environment, DevelopmentSettings)
    
    print(f"🚀 Loading {environment.upper()} settings...")
    
    return settings_class


def automatic_loading_example():
    """Automatic loading example"""
    print("=" * 50)
    print("7. AUTOMATIC ENVIRONMENT LOADING")
    print("=" * 50)
    
    print("""
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

# Usage:
# export ENVIRONMENT=production
# python manage.py runserver
    """)
    
    # Test
    os.environ['ENVIRONMENT'] = 'development'
    settings = get_settings()
    settings.print_config()
    print()


# =====================================
# 8. COMPONENT-BASED SETTINGS
# =====================================

def component_based_example():
    """Component-based settings organization"""
    print("=" * 50)
    print("8. COMPONENT-BASED SETTINGS")
    print("=" * 50)
    
    print("""
Structure:

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
│       ├── security.py
│       └── logging.py

# components/database.py
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        ...
    }
}

# components/cache.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        ...
    }
}

# production.py
from .base import *
from .components.database import *
from .components.cache import *
from .components.email import *
from .components.storage import *
from .components.security import *
    """)
    print()


# =====================================
# 9. SETTINGS VALIDATOR
# =====================================

class SettingsValidator:
    """Settings validator"""
    
    @staticmethod
    def validate_required_settings(settings_class):
        """Required settings'ni tekshirish"""
        required = [
            'SECRET_KEY',
            'DATABASES',
            'INSTALLED_APPS',
            'MIDDLEWARE',
        ]
        
        missing = []
        for setting in required:
            if not hasattr(settings_class, setting):
                missing.append(setting)
        
        if missing:
            raise ValueError(f"Missing required settings: {', '.join(missing)}")
        
        return True
    
    @staticmethod
    def validate_production_settings(settings_class):
        """Production settings'ni tekshirish"""
        if settings_class.DEBUG:
            raise ValueError("DEBUG must be False in production!")
        
        if 'localhost' in settings_class.ALLOWED_HOSTS:
            raise ValueError("localhost in ALLOWED_HOSTS (production)!")
        
        if not hasattr(settings_class, 'SECURE_SSL_REDIRECT'):
            raise ValueError("SECURE_SSL_REDIRECT not set!")
        
        return True


def validator_example():
    """Settings validator example"""
    print("=" * 50)
    print("9. SETTINGS VALIDATOR")
    print("=" * 50)
    
    # Validate base settings
    print("Validating BaseSettings:")
    try:
        SettingsValidator.validate_required_settings(BaseSettings)
        print("  ✓ Required settings OK")
    except ValueError as e:
        print(f"  ✗ Error: {e}")
    
    # Validate production
    print("\nValidating ProductionSettings:")
    try:
        SettingsValidator.validate_required_settings(ProductionSettings)
        print("  ✓ Required settings OK")
        SettingsValidator.validate_production_settings(ProductionSettings)
        print("  ✓ Production settings OK")
    except ValueError as e:
        print(f"  ✗ Error: {e}")
    
    print()


# =====================================
# 10. BEST PRACTICES
# =====================================

def best_practices():
    """Settings organization best practices"""
    print("=" * 50)
    print("10. BEST PRACTICES")
    print("=" * 50)
    
    print("""
1. Settings Hierarchy:
   base.py → development.py
   base.py → staging.py
   base.py → production.py

2. Keep base.py minimal:
   - Only common settings
   - No environment-specific code
   - No secrets

3. Use inheritance:
   class ProductionSettings(BaseSettings):
       DEBUG = False
       ...

4. Component-based for large projects:
   components/database.py
   components/cache.py
   components/email.py

5. Validate on startup:
   if environment == 'production':
       validate_production_settings()

6. Document each setting:
   # Cache backend (Redis for production)
   CACHES = {...}

7. Use constants for repeated values:
   BASE_URL = 'https://example.com'
   API_URL = f'{BASE_URL}/api'

8. Group related settings:
   # === DATABASE ===
   DATABASES = {...}
   
   # === EMAIL ===
   EMAIL_BACKEND = ...

9. Never hardcode secrets:
   ✗ SECRET_KEY = 'hardcoded-key'
   ✓ SECRET_KEY = config('SECRET_KEY')

10. Test each environment:
    python manage.py check --deploy
    """)


# =====================================
# MAIN EXECUTION
# =====================================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "=" * 50)
    print("LESSON 35: SETTINGS STRUCTURE")
    print("=" * 50 + "\n")
    
    # Set test environment
    os.environ['SECRET_KEY'] = 'django-insecure-test-key-12345'
    
    # Examples
    simple_structure_example()
    split_structure_example()
    base_settings_example()
    development_settings_example()
    staging_settings_example()
    production_settings_example()
    automatic_loading_example()
    component_based_example()
    validator_example()
    best_practices()
    
    print("=" * 50)
    print("✅ All examples completed!")
    print("=" * 50)


if __name__ == '__main__':
    main()