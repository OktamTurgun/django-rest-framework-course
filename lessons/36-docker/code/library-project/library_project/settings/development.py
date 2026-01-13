"""
Development environment settings
"""

import sys
from .base import *

# ============================================================================
# DEBUG & SECURITY
# ============================================================================

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']


# ============================================================================
# DATABASE
# ============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / config("DB_NAME", default="db.sqlite3"),
    }
}


# ============================================================================
# CACHE CONFIGURATION
# ============================================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


# ============================================================================
# SESSION SETTINGS
# ============================================================================

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_NAME = "library_sessionid"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # HTTP for development


# ============================================================================
# CORS CONFIGURATION
# ============================================================================

print("Development mode: CORS_ALLOW_ALL_ORIGINS = True")
CORS_ALLOW_ALL_ORIGINS = True
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

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


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
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "development.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 3,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "books": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "accounts": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


# ============================================================================
# THROTTLING (Disabled for testing)
# ============================================================================

REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [] if "test" in sys.argv else [
    "books.throttling.MembershipThrottle",
]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {} if "test" in sys.argv else {
    "membership": "100/hour",
    "borrow": "5/day",
    "monitored_books": "100/hour",
    "search": "50/hour",
}


# ============================================================================
# DEBUG TOOLBAR
# ============================================================================

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]


# ============================================================================
# SECURITY SETTINGS (Relaxed for development)
# ============================================================================

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
JWT_AUTH_SECURE = False
JWT_AUTH_HTTPONLY = True
JWT_AUTH_SAMESITE = "Lax"


# ============================================================================
# SENTRY (Optional for development)
# ============================================================================

SENTRY_DSN = config("SENTRY_DSN", default=None)

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    import logging

    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR,
    )
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        send_default_pii=True,
        environment="development",
        release=config("RELEASE_VERSION", default="dev"),
    )
    
    print("✓ Sentry initialized (Development)")
else:
    print("⚠ Sentry DSN not configured")


# ============================================================================
# DEVELOPMENT HELPERS
# ============================================================================

print("\n" + "="*60)
print("DEVELOPMENT ENVIRONMENT LOADED")
print("="*60)
print(f"BASE_DIR: {BASE_DIR}")
print(f"DATABASE: SQLite3")
print(f"EMAIL: Console")
print(f"CACHE: In-Memory")
print(f"CORS: Allow All")
print(f"DEBUG: True")
print("="*60 + "\n")