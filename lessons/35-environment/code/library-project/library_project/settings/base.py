"""
Base settings - Common configuration for all environments
"""

import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ============================================================================
# SECURITY SETTINGS
# ============================================================================

SECRET_KEY = config("SECRET_KEY")


# ============================================================================
# INSTALLED APPS
# ============================================================================

INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "corsheaders",
    "django_filters",
    # "django_elasticsearch_dsl",

    # 2FA apps
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'phonenumber_field',
    
    # Authentication apps
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "dj_rest_auth.registration",

    # Local apps
    "books.apps.BooksConfig",
    "accounts.apps.AccountsConfig",
    "users.apps.UsersConfig",
    "emails.apps.EmailsConfig",
    "notifications.apps.NotificationsConfig",
]


# ============================================================================
# MIDDLEWARE
# ============================================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'django_otp.middleware.OTPMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "books.middleware.APIVersionDeprecationMiddleware",
    "books.middleware.APIVersionMetricsMiddleware",
    "books.middleware.SentryUserContextMiddleware",
]


# ============================================================================
# OTP SETTINGS
# ============================================================================

OTP_TOTP_ISSUER = 'Library Project'
OTP_LOGIN_URL = '/api/v1/users/2fa/verify/'


# ============================================================================
# URL & TEMPLATE CONFIGURATION
# ============================================================================

ROOT_URLCONF = "library_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "library_project.wsgi.application"


# ============================================================================
# PASSWORD VALIDATION
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ============================================================================
# INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")
TIME_ZONE = config("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True


# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================================
# REST FRAMEWORK CONFIGURATION
# ============================================================================

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_VERSIONING_CLASS": None,
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "library_project.exception_handler.custom_exception_handler",
}


# ============================================================================
# DRF SPECTACULAR (API DOCUMENTATION)
# ============================================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Library API",
    "DESCRIPTION": "Complete REST API for Library Management System",
    "VERSION": "2.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "filter": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVERS": [
        {"url": "http://127.0.0.1:8000/api/v1/", "description": "V1 API (Deprecated)"},
        {"url": "http://127.0.0.1:8000/api/v2/", "description": "V2 API (Current)"},
    ],
    "TAGS": [
        {"name": "v1", "description": "Version 1 Endpoints (Deprecated)"},
        {"name": "v2", "description": "Version 2 Endpoints (Current)"},
    ],
}


# ============================================================================
# JWT CONFIGURATION
# ============================================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}


# ============================================================================
# API VERSIONING & DEPRECATION
# ============================================================================

from datetime import datetime

V1_SUNSET_DATE = datetime(2025, 12, 31)

API_VERSIONS = {
    "v1": {
        "status": "deprecated",
        "release_date": "2023-01-15",
        "sunset_date": "2025-12-31",
        "migration_guide": "https://docs.example.com/api/v1-to-v2",
    },
    "v2": {
        "status": "active",
        "release_date": "2024-01-15",
        "sunset_date": None,
        "migration_guide": None,
    },
}


# ============================================================================
# FIREBASE & SMS CONFIGURATION
# ============================================================================

FIREBASE_CREDENTIALS_PATH = BASE_DIR / config(
    "FIREBASE_CREDENTIALS_PATH", default="firebase-credentials.json"
)

SMS_BACKEND = config("SMS_BACKEND", default="mock")
SMS_ENABLED = config("SMS_ENABLED", default=True, cast=bool)

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default="")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default="")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER", default="")

NOTIFICATION_SETTINGS = {
    "SMS_ENABLED": SMS_ENABLED,
    "SMS_BACKEND": SMS_BACKEND,
    "PUSH_ENABLED": config("PUSH_ENABLED", default=True, cast=bool),
    "EMAIL_ENABLED": config("EMAIL_ENABLED", default=True, cast=bool),
    "DEFAULT_COUNTRY_CODE": "UZ",
    "RATE_LIMIT_SMS": "10/hour",
    "RATE_LIMIT_PUSH": "100/hour",
    "MOCK_MODE": SMS_BACKEND == "mock",
}


# ============================================================================
# DJANGO-ALLAUTH & SOCIAL AUTH CONFIGURATION
# ============================================================================

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Account settings
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGIN_BY_CODE_ENABLED = False

# New allauth settings
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]

# Rate limiting
ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/5m",
    "signup": "10/h",
    "change_password": "5/5m",
    "reset_password": "5/5m",
    "reset_password_email": "5/5m",
}

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default=''),
            'secret': config('GOOGLE_CLIENT_SECRET', default=''),
            'key': '',
        },
        'VERIFIED_EMAIL': True,
    },
    'github': {
        'SCOPE': ['user', 'user:email'],
        'APP': {
            'client_id': config('GITHUB_CLIENT_ID', default=''),
            'secret': config('GITHUB_CLIENT_SECRET', default=''),
        },
        'SCOPE_DELIMITER': ' ',
        'OAUTH_PKCE_ENABLED': False,
        'VERIFIED_EMAIL': True,
    },
}

SOCIALACCOUNT_ADAPTER = "accounts.adapters.CustomSocialAccountAdapter"
ACCOUNT_ADAPTER = "accounts.adapters.CustomAccountAdapter"

# dj-rest-auth settings
REST_USE_JWT = False
JWT_AUTH_COOKIE = "auth-token"
JWT_AUTH_REFRESH_COOKIE = "refresh-token"
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "accounts.serializers.UserSerializer",
}

# Redirect URLs
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Elasticsearch Configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://localhost:9200',
        'timeout': 30,
    },
}

# Email defaults
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="Library System <noreply@library.com>")
EMAIL_TIMEOUT = 10
EMAIL_USE_LOCALTIME = True
SITE_URL = "http://localhost:8000"

ADMINS = [("Admin", "admin@library.com")]
MANAGERS = ADMINS