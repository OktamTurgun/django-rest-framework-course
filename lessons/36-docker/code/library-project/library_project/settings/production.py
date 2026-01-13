"""
Production environment settings
"""

import sys
from .base import *

# ============================================================================
# DEBUG & SECURITY
# ============================================================================

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# ============================================================================
# DATABASE
# ============================================================================

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default=5432, cast=int),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
            'sslmode': 'require',  # SSL required for production
        }
    }
}


# ============================================================================
# CACHE CONFIGURATION
# ============================================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,
                "retry_on_timeout": True,
            },
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
        "KEY_PREFIX": "library_prod",
        "TIMEOUT": 300,
    }
}


# ============================================================================
# SESSION SETTINGS
# ============================================================================

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_NAME = "library_sessionid"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Strict'


# ============================================================================
# CORS CONFIGURATION
# ============================================================================

print("Production mode: Using CORS_ALLOWED_ORIGINS")
cors_origins_str = config("CORS_ALLOWED_ORIGINS", default="")
if cors_origins_str:
    CORS_ALLOWED_ORIGINS = [
        origin.strip() for origin in cors_origins_str.split(",") if origin.strip()
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "https://app.yourdomain.com",
    ]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_EXPOSE_HEADERS = ["Content-Length", "X-Total-Count", "X-Page-Number"]
CORS_PREFLIGHT_MAX_AGE = 86400


# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGS_DIR = BASE_DIR / "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "[{levelname}] {asctime} - {name} - {funcName}:{lineno} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "file_app": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "production.log",
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
            "formatter": "verbose",
        },
        "file_errors": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "production_errors.log",
            "maxBytes": 1024 * 1024 * 20,  # 20MB
            "backupCount": 15,
            "formatter": "detailed",
        },
        "mail_admins": {
            "level": "CRITICAL",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "detailed",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_app", "file_errors"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file_errors", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "books": {
            "handlers": ["file_app", "file_errors"],
            "level": "INFO",
            "propagate": False,
        },
        "accounts": {
            "handlers": ["file_app", "file_errors"],
            "level": "INFO",
            "propagate": False,
        },
        "library_project.exception_handler": {
            "handlers": ["file_errors"],
            "level": "ERROR",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["file_app", "file_errors"],
        "level": "WARNING",
    },
}


# ============================================================================
# THROTTLING
# ============================================================================

REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [
    "books.throttling.MembershipThrottle",
]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "membership": "100/hour",
    "borrow": "5/day",
    "monitored_books": "100/hour",
    "search": "50/hour",
}


# ============================================================================
# SECURITY SETTINGS (Full Protection)
# ============================================================================

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Proxy headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie security
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_USE_SESSIONS = False
CSRF_COOKIE_AGE = 31536000  # 1 year

# Other security
SECURE_REFERRER_POLICY = 'same-origin'

# Django Allauth
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# JWT
JWT_AUTH_SECURE = True
JWT_AUTH_HTTPONLY = True
JWT_AUTH_SAMESITE = "Strict"


# ============================================================================
# SENTRY
# ============================================================================

SENTRY_DSN = config("SENTRY_DSN", default=None)

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    import logging

    def sentry_before_send(event, hint):
        """Filter sensitive data before sending to Sentry"""
        # Filter request data
        if "request" in event and "data" in event["request"]:
            data = event["request"]["data"]
            if isinstance(data, dict):
                sensitive_fields = ["password", "token", "api_key", "secret"]
                for field in sensitive_fields:
                    if field in data:
                        data[field] = "[Filtered]"
        
        # Filter headers
        if "headers" in event.get("request", {}):
            headers = event["request"]["headers"]
            sensitive_headers = ["Authorization", "Cookie", "X-API-Key"]
            for header in sensitive_headers:
                if header in headers:
                    headers[header] = "[Filtered]"
        
        return event

    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR,
    )
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],
        traces_sample_rate=0.1,  # 10% sampling in production
        profiles_sample_rate=0.1,
        send_default_pii=True,
        environment="production",
        release=config("RELEASE_VERSION", default="v1.0.0"),
        before_send=sentry_before_send,
        ignore_errors=[KeyboardInterrupt, BrokenPipeError],
    )
    
    print("✓ Sentry initialized (Production)")
else:
    print("WARNING: Sentry DSN not configured for production!")


# ============================================================================
# STATIC FILES (Production - use CDN or S3)
# ============================================================================

# If using AWS S3
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
    
    print("✓ AWS S3 storage configured")


# ============================================================================
# PRODUCTION HELPERS
# ============================================================================

print("\n" + "="*60)
print("PRODUCTION ENVIRONMENT LOADED")
print("="*60)
print(f"BASE_DIR: {BASE_DIR}")
print(f"DATABASE: PostgreSQL (SSL)")
print(f"EMAIL: SMTP")
print(f"CACHE: Redis")
print(f"HTTPS: Required")
print(f"HSTS: Enabled (1 year)")
print(f"DEBUG: False")
print(f"S3: {'Enabled' if USE_S3 else 'Disabled'}")
print("="*60 + "\n")


# ============================================================================
# PRODUCTION CHECKS
# ============================================================================

# Check critical settings
assert not DEBUG, "DEBUG must be False in production!"
assert ALLOWED_HOSTS, "ALLOWED_HOSTS must be set in production!"
assert 'localhost' not in ALLOWED_HOSTS, "localhost should not be in ALLOWED_HOSTS!"
assert len(SECRET_KEY) >= 50, "SECRET_KEY must be at least 50 characters!"
assert SECURE_SSL_REDIRECT, "HTTPS must be enforced!"
assert SENTRY_DSN, "Sentry DSN is required for production monitoring!"

print("All production security checks passed!")