"""
Staging environment settings
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
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=5432, cast=int),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}


# ============================================================================
# CACHE CONFIGURATION
# ============================================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "retry_on_timeout": True,
            },
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
        "KEY_PREFIX": "library_staging",
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
SESSION_COOKIE_SECURE = True  # HTTPS required


# ============================================================================
# CORS CONFIGURATION
# ============================================================================

print("Staging mode: Using CORS_ALLOWED_ORIGINS")
cors_origins_str = config("CORS_ALLOWED_ORIGINS", default="")
if cors_origins_str:
    CORS_ALLOWED_ORIGINS = [
        origin.strip() for origin in cors_origins_str.split(",") if origin.strip()
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://staging.yourdomain.com",
        "https://staging-app.yourdomain.com",
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
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")


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
    "handlers": {
        "file_app": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "staging.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "file_errors": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "staging_errors.log",
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
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
            "handlers": ["file_errors"],
            "level": "ERROR",
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
    },
    "root": {
        "handlers": ["file_app", "file_errors"],
        "level": "INFO",
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
# SECURITY SETTINGS (Moderate)
# ============================================================================

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
JWT_AUTH_SECURE = True
JWT_AUTH_HTTPONLY = True
JWT_AUTH_SAMESITE = "Strict"

# Basic security headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True


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
        """Filter sensitive data"""
        if "request" in event and "data" in event["request"]:
            data = event["request"]["data"]
            if isinstance(data, dict):
                for field in ["password", "token", "api_key", "secret"]:
                    if field in data:
                        data[field] = "[Filtered]"
        return event

    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR,
    )
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],
        traces_sample_rate=0.3,
        profiles_sample_rate=0.3,
        send_default_pii=True,
        environment="staging",
        release=config("RELEASE_VERSION", default="staging"),
        before_send=sentry_before_send,
    )
    
    print("✓ Sentry initialized (Staging)")
else:
    print("⚠ Sentry DSN not configured")


# ============================================================================
# STAGING HELPERS
# ============================================================================

print("\n" + "="*60)
print("STAGING ENVIRONMENT LOADED")
print("="*60)
print(f"BASE_DIR: {BASE_DIR}")
print(f"DATABASE: PostgreSQL")
print(f"EMAIL: SMTP")
print(f"CACHE: Redis")
print(f"HTTPS: Required")
print(f"DEBUG: False")
print("="*60 + "\n")