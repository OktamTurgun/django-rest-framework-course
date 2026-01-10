"""
Lesson 35: Environment Setup - Example 02
Advanced usage with python-decouple

Bu misolda:
- python-decouple kutubxonasi
- Type casting (bool, int, float)
- Csv() helper
- RepositoryEnv
- Custom casting functions
"""

from decouple import config, Csv, RepositoryEnv
import json
from pathlib import Path


# =====================================
# 1. BASIC DECOUPLE USAGE
# =====================================

def basic_decouple():
    """python-decouple asosiy foydalanish"""
    print("=" * 50)
    print("1. BASIC DECOUPLE USAGE")
    print("=" * 50)
    
    # Oddiy string
    secret_key = config('SECRET_KEY')
    print(f"SECRET_KEY: {secret_key}")
    
    # With default
    api_key = config('API_KEY', default='default-api-key')
    print(f"API_KEY: {api_key}")
    
    # Debug mode
    debug = config('DEBUG')
    print(f"DEBUG: {debug} (type: {type(debug)})")
    print()


# =====================================
# 2. TYPE CASTING
# =====================================

def type_casting():
    """Turli type'larga casting"""
    print("=" * 50)
    print("2. TYPE CASTING")
    print("=" * 50)
    
    # Boolean
    debug = config('DEBUG', default=False, cast=bool)
    print(f"DEBUG: {debug} (type: {type(debug)})")
    
    # Integer
    db_port = config('DB_PORT', default=5432, cast=int)
    print(f"DB_PORT: {db_port} (type: {type(db_port)})")
    
    max_connections = config('MAX_CONNECTIONS', default=10, cast=int)
    print(f"MAX_CONNECTIONS: {max_connections}")
    
    # Float
    tax_rate = config('TAX_RATE', default=0.15, cast=float)
    print(f"TAX_RATE: {tax_rate} (type: {type(tax_rate)})")
    
    version = config('API_VERSION', default=1.0, cast=float)
    print(f"API_VERSION: {version}")
    print()


# =====================================
# 3. CSV HELPER
# =====================================

def csv_helper():
    """Csv() helper bilan ishlash"""
    print("=" * 50)
    print("3. CSV HELPER")
    print("=" * 50)
    
    # List of strings
    allowed_hosts = config('ALLOWED_HOSTS', cast=Csv())
    print(f"ALLOWED_HOSTS: {allowed_hosts}")
    print(f"Type: {type(allowed_hosts)}")
    
    # List with custom delimiter
    tags = config('TAGS', default='python,django,api', cast=Csv(delimiter=','))
    print(f"TAGS: {tags}")
    
    # List of integers
    allowed_ports = config('ALLOWED_PORTS', default='8000,8001,8002', 
                          cast=Csv(cast=int))
    print(f"ALLOWED_PORTS: {allowed_ports}")
    print(f"Type of first item: {type(allowed_ports[0])}")
    print()


# =====================================
# 4. CUSTOM CASTING
# =====================================

def custom_cast_json(value):
    """JSON string'ni dict'ga o'tkazish"""
    return json.loads(value)


def custom_cast_tuple(value):
    """String'ni tuple'ga o'tkazish"""
    return tuple(value.split(','))


def custom_cast_bool_strict(value):
    """Strict boolean casting"""
    if value.lower() in ('true', '1', 'yes', 'on'):
        return True
    elif value.lower() in ('false', '0', 'no', 'off'):
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")


def custom_casting():
    """Custom casting functions"""
    print("=" * 50)
    print("4. CUSTOM CASTING")
    print("=" * 50)
    
    # JSON casting
    aws_config = config(
        'AWS_CONFIG', 
        default='{"region": "us-east-1", "bucket": "my-bucket"}',
        cast=custom_cast_json
    )
    print(f"AWS_CONFIG: {aws_config}")
    print(f"Region: {aws_config['region']}")
    
    # Tuple casting
    database_tuple = config(
        'DATABASE_TUPLE',
        default='localhost,5432,library_db',
        cast=custom_cast_tuple
    )
    print(f"DATABASE_TUPLE: {database_tuple}")
    print(f"Type: {type(database_tuple)}")
    
    # Lambda casting
    upper_env = config(
        'ENVIRONMENT',
        default='development',
        cast=lambda x: x.upper()
    )
    print(f"ENVIRONMENT: {upper_env}")
    print()


# =====================================
# 5. REPOSITORY ENV
# =====================================

def repository_env_example():
    """RepositoryEnv bilan ishlash"""
    print("=" * 50)
    print("5. REPOSITORY ENV")
    print("=" * 50)
    
    # Create .env.test file in memory
    env_content = """
SECRET_KEY=test-secret-key
DEBUG=True
DB_NAME=test_db
DB_HOST=localhost
DB_PORT=5432
"""
    
    # Write to file
    test_env_file = Path('.env.test')
    test_env_file.write_text(env_content)
    
    # Load from specific file
    env = RepositoryEnv(test_env_file)
    
    secret_key = env('SECRET_KEY')
    print(f"SECRET_KEY from .env.test: {secret_key}")
    
    debug = env('DEBUG', cast=bool)
    print(f"DEBUG from .env.test: {debug}")
    
    # Cleanup
    test_env_file.unlink()
    print("\n✓ .env.test cleaned up")
    print()


# =====================================
# 6. DJANGO SETTINGS WITH DECOUPLE
# =====================================

def django_settings_example():
    """Django settings.py'da decouple ishlatish"""
    print("=" * 50)
    print("6. DJANGO SETTINGS EXAMPLE")
    print("=" * 50)
    
    print("""
# settings.py
from decouple import config, Csv

# Basic settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=5432, cast=int),
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=600, cast=int),
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

# Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/2')

# AWS S3
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
    """)


# =====================================
# 7. CONFIG CLASS WITH DECOUPLE
# =====================================

class DatabaseConfig:
    """Database konfiguratsiyasi"""
    ENGINE = config('DB_ENGINE', default='django.db.backends.postgresql')
    NAME = config('DB_NAME')
    USER = config('DB_USER')
    PASSWORD = config('DB_PASSWORD')
    HOST = config('DB_HOST', default='localhost')
    PORT = config('DB_PORT', default=5432, cast=int)
    CONN_MAX_AGE = config('DB_CONN_MAX_AGE', default=600, cast=int)
    
    @classmethod
    def get_config(cls):
        """Django format database config"""
        return {
            'ENGINE': cls.ENGINE,
            'NAME': cls.NAME,
            'USER': cls.USER,
            'PASSWORD': cls.PASSWORD,
            'HOST': cls.HOST,
            'PORT': cls.PORT,
            'CONN_MAX_AGE': cls.CONN_MAX_AGE,
        }
    
    @classmethod
    def get_url(cls):
        """Database URL"""
        return f"postgresql://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.NAME}"


class EmailConfig:
    """Email konfiguratsiyasi"""
    BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    PORT = config('EMAIL_PORT', default=587, cast=int)
    HOST_USER = config('EMAIL_HOST_USER', default='')
    HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
    
    @classmethod
    def get_config(cls):
        """Django format email config"""
        return {
            'EMAIL_BACKEND': cls.BACKEND,
            'EMAIL_HOST': cls.HOST,
            'EMAIL_PORT': cls.PORT,
            'EMAIL_HOST_USER': cls.HOST_USER,
            'EMAIL_HOST_PASSWORD': cls.HOST_PASSWORD,
            'EMAIL_USE_TLS': cls.USE_TLS,
            'EMAIL_USE_SSL': cls.USE_SSL,
        }


class RedisConfig:
    """Redis konfiguratsiyasi"""
    URL = config('REDIS_URL', default='redis://localhost:6379/0')
    
    @classmethod
    def get_cache_config(cls):
        """Django cache config"""
        return {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': cls.URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                }
            }
        }


class AppConfig:
    """Umumiy application konfiguratsiyasi"""
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
    ENVIRONMENT = config('ENVIRONMENT', default='development')
    
    # Components
    Database = DatabaseConfig
    Email = EmailConfig
    Redis = RedisConfig
    
    @classmethod
    def print_config(cls):
        """Konfiguratsiyani ko'rsatish"""
        print("Application Configuration:")
        print(f"  Environment: {cls.ENVIRONMENT}")
        print(f"  Debug: {cls.DEBUG}")
        print(f"  Allowed Hosts: {cls.ALLOWED_HOSTS}")
        print(f"\nDatabase:")
        print(f"  Host: {cls.Database.HOST}")
        print(f"  Port: {cls.Database.PORT}")
        print(f"  Name: {cls.Database.NAME}")
        print(f"\nEmail:")
        print(f"  Host: {cls.Email.HOST}")
        print(f"  Port: {cls.Email.PORT}")
        print(f"\nRedis:")
        print(f"  URL: {cls.Redis.URL}")


def config_classes_example():
    """Config classes'dan foydalanish"""
    print("=" * 50)
    print("7. CONFIG CLASSES")
    print("=" * 50)
    
    AppConfig.print_config()
    print()
    
    # Database config
    db_config = DatabaseConfig.get_config()
    print("Database Config for Django:")
    for key, value in db_config.items():
        if key == 'PASSWORD':
            value = '*' * len(str(value))
        print(f"  {key}: {value}")
    print()


# =====================================
# 8. VALIDATION
# =====================================

def validate_config():
    """Config validation"""
    print("=" * 50)
    print("8. CONFIG VALIDATION")
    print("=" * 50)
    
    required_vars = {
        'SECRET_KEY': str,
        'DB_NAME': str,
        'DB_USER': str,
        'DB_PASSWORD': str,
    }
    
    errors = []
    
    for var_name, var_type in required_vars.items():
        try:
            value = config(var_name)
            if not value:
                errors.append(f"{var_name} is empty")
            elif not isinstance(value, var_type):
                errors.append(f"{var_name} must be {var_type.__name__}")
            else:
                print(f"✓ {var_name}: OK")
        except Exception as e:
            errors.append(f"{var_name}: {str(e)}")
            print(f"✗ {var_name}: ERROR")
    
    if errors:
        print(f"\n❌ Validation failed:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"\n✅ All validations passed!")
    print()


# =====================================
# 9. ADVANCED PATTERNS
# =====================================

def advanced_patterns():
    """Advanced configuration patterns"""
    print("=" * 50)
    print("9. ADVANCED PATTERNS")
    print("=" * 50)
    
    # Pattern 1: Nested configuration
    print("Pattern 1: Nested Configuration")
    aws_region = config('AWS_REGION', default='us-east-1')
    aws_bucket = config('AWS_BUCKET', default='my-bucket')
    print(f"  AWS: {aws_region} / {aws_bucket}")
    
    # Pattern 2: Conditional configuration
    print("\nPattern 2: Conditional Configuration")
    environment = config('ENVIRONMENT', default='development')
    if environment == 'production':
        db_engine = config('DB_ENGINE')
        print(f"  Production DB: {db_engine}")
    else:
        db_engine = 'django.db.backends.sqlite3'
        print(f"  Development DB: {db_engine}")
    
    # Pattern 3: Feature flags
    print("\nPattern 3: Feature Flags")
    use_s3 = config('USE_S3', default=False, cast=bool)
    use_redis = config('USE_REDIS', default=True, cast=bool)
    use_celery = config('USE_CELERY', default=False, cast=bool)
    
    print(f"  S3: {'Enabled' if use_s3 else 'Disabled'}")
    print(f"  Redis: {'Enabled' if use_redis else 'Disabled'}")
    print(f"  Celery: {'Enabled' if use_celery else 'Disabled'}")
    
    # Pattern 4: URL parsing
    print("\nPattern 4: URL Parsing")
    database_url = config('DATABASE_URL', 
                         default='postgresql://user:pass@localhost:5432/dbname')
    print(f"  Database URL: {database_url}")
    print()


# =====================================
# 10. BEST PRACTICES
# =====================================

def best_practices():
    """Best practices with decouple"""
    print("=" * 50)
    print("10. BEST PRACTICES")
    print("=" * 50)
    
    print("""
1. ALWAYS use type casting:
   ✓ DEBUG = config('DEBUG', cast=bool)
   ✗ DEBUG = config('DEBUG')  # Returns string!

2. Provide defaults for non-critical settings:
   ✓ DB_HOST = config('DB_HOST', default='localhost')
   ✗ SECRET_KEY = config('SECRET_KEY', default='dev-key')  # NO!

3. Use Csv() for lists:
   ✓ ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
   ✗ ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

4. Validate required variables:
   try:
       SECRET_KEY = config('SECRET_KEY')
   except:
       raise ImproperlyConfigured("SECRET_KEY is required!")

5. Organize configs in classes:
   class DatabaseConfig:
       NAME = config('DB_NAME')
       USER = config('DB_USER')

6. Use RepositoryEnv for testing:
   env = RepositoryEnv('.env.test')
   secret_key = env('SECRET_KEY')

7. Document your .env.example:
   # .env.example
   # Required
   SECRET_KEY=
   DB_PASSWORD=
   
   # Optional (defaults provided)
   DEBUG=True
   DB_HOST=localhost

8. Never commit .env files:
   # .gitignore
   .env
   .env.*
   !.env.example
    """)


# =====================================
# MAIN EXECUTION
# =====================================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "=" * 50)
    print("LESSON 35: PYTHON-DECOUPLE ADVANCED")
    print("=" * 50 + "\n")
    
    # Create test .env file
    env_content = """SECRET_KEY=django-insecure-test-key-12345
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=testpassword
DB_HOST=localhost
DB_PORT=5432
MAX_CONNECTIONS=20
TAX_RATE=0.18
TAGS=python,django,rest,api
ALLOWED_PORTS=8000,8001,8002
AWS_CONFIG={"region": "us-east-1", "bucket": "my-bucket"}
DATABASE_TUPLE=localhost,5432,library_db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=test@example.com
EMAIL_HOST_PASSWORD=testpassword
EMAIL_USE_TLS=True
REDIS_URL=redis://localhost:6379/0
"""
    
    env_file = Path('.env')
    env_file.write_text(env_content)
    print("✓ Created test .env file\n")
    
    # Examples
    basic_decouple()
    type_casting()
    csv_helper()
    custom_casting()
    repository_env_example()
    django_settings_example()
    config_classes_example()
    validate_config()
    advanced_patterns()
    best_practices()
    
    # Cleanup
    env_file.unlink()
    print("\n✓ Cleaned up test .env file")
    
    print("\n" + "=" * 50)
    print("✅ All examples completed!")
    print("=" * 50)


if __name__ == '__main__':
    main()