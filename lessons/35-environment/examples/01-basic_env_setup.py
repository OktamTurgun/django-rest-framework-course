"""
Lesson 35: Environment Setup - Example 01
Basic .env setup with os.getenv()

Bu misolda:
- .env fayl yaratish
- os.getenv() bilan ishlash
- Environment variable types
- Default values
"""

import os
from pathlib import Path


# =====================================
# 1. BASIC USAGE
# =====================================

def basic_getenv():
    """os.getenv() asosiy foydalanish"""
    print("=" * 50)
    print("1. BASIC GETENV")
    print("=" * 50)
    
    # Oddiy string
    secret_key = os.getenv('SECRET_KEY')
    print(f"SECRET_KEY: {secret_key}")
    
    # Debug mode
    debug = os.getenv('DEBUG')
    print(f"DEBUG: {debug} (type: {type(debug)})")
    
    # Database name
    db_name = os.getenv('DB_NAME')
    print(f"DB_NAME: {db_name}")
    print()


# =====================================
# 2. DEFAULT VALUES
# =====================================

def default_values():
    """Default qiymatlar bilan ishlash"""
    print("=" * 50)
    print("2. DEFAULT VALUES")
    print("=" * 50)
    
    # Mavjud variable
    secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
    print(f"SECRET_KEY: {secret_key}")
    
    # Mavjud bo'lmagan variable
    api_key = os.getenv('API_KEY', 'default-api-key')
    print(f"API_KEY: {api_key}")
    
    # Database host
    db_host = os.getenv('DB_HOST', 'localhost')
    print(f"DB_HOST: {db_host}")
    
    # Port with default
    db_port = os.getenv('DB_PORT', '5432')
    print(f"DB_PORT: {db_port}")
    print()


# =====================================
# 3. TYPE CONVERSION
# =====================================

def type_conversion():
    """String'dan boshqa typelarga o'tkazish"""
    print("=" * 50)
    print("3. TYPE CONVERSION")
    print("=" * 50)
    
    # Boolean (manual conversion)
    debug_str = os.getenv('DEBUG', 'False')
    debug = debug_str.lower() in ('true', '1', 'yes')
    print(f"DEBUG: {debug} (type: {type(debug)})")
    
    # Integer
    db_port_str = os.getenv('DB_PORT', '5432')
    db_port = int(db_port_str)
    print(f"DB_PORT: {db_port} (type: {type(db_port)})")
    
    # Float
    tax_rate_str = os.getenv('TAX_RATE', '0.15')
    tax_rate = float(tax_rate_str)
    print(f"TAX_RATE: {tax_rate} (type: {type(tax_rate)})")
    
    # List (manual parsing)
    allowed_hosts_str = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    allowed_hosts = [host.strip() for host in allowed_hosts_str.split(',')]
    print(f"ALLOWED_HOSTS: {allowed_hosts} (type: {type(allowed_hosts)})")
    print()


# =====================================
# 4. ENV FILE EXAMPLE
# =====================================

def create_env_example():
    """
    .env fayl example yaratish
    
    Real loyihada .env faylni qo'lda yaratishingiz kerak:
    
    # .env
    SECRET_KEY=django-insecure-your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=library_db
    DB_USER=postgres
    DB_PASSWORD=yourpassword
    DB_HOST=localhost
    DB_PORT=5432
    
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_app_password
    """
    
    print("=" * 50)
    print("4. .ENV FILE EXAMPLE")
    print("=" * 50)
    
    env_content = """# Django Settings
SECRET_KEY=django-insecure-example-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Redis
REDIS_URL=redis://localhost:6379/0
"""
    
    print("Create this file as '.env' in your project root:")
    print(env_content)


# =====================================
# 5. DJANGO SETTINGS EXAMPLE
# =====================================

def django_settings_example():
    """Django settings.py'da qanday ishlatish"""
    print("=" * 50)
    print("5. DJANGO SETTINGS EXAMPLE")
    print("=" * 50)
    
    print("""
# settings.py
import os

# Basic settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Allowed hosts
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', 'localhost')
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_str.split(',')]

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
    """)


# =====================================
# 6. ENVIRONMENT VARIABLES CHECKER
# =====================================

def check_environment():
    """Required environment variablelarni tekshirish"""
    print("=" * 50)
    print("6. ENVIRONMENT CHECKER")
    print("=" * 50)
    
    required_vars = [
        'SECRET_KEY',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
    
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: OK")
        else:
            print(f"✗ {var}: MISSING")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing variables: {', '.join(missing_vars)}")
        print("Please set them in .env file")
    else:
        print("\n✅ All required variables are set!")
    print()


# =====================================
# 7. COMMON PATTERNS
# =====================================

class Config:
    """Configuration class pattern"""
    
    # Basic Django settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database
    DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
    DB_NAME = os.getenv('DB_NAME', 'db.sqlite3')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    # Email
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    
    @classmethod
    def get_database_config(cls):
        """Database konfiguratsiyasini olish"""
        return {
            'ENGINE': cls.DB_ENGINE,
            'NAME': cls.DB_NAME,
            'USER': cls.DB_USER,
            'PASSWORD': cls.DB_PASSWORD,
            'HOST': cls.DB_HOST,
            'PORT': cls.DB_PORT,
        }
    
    @classmethod
    def print_config(cls):
        """Barcha konfiguratsiyalarni ko'rsatish"""
        print("Current Configuration:")
        print(f"  DEBUG: {cls.DEBUG}")
        print(f"  DB_ENGINE: {cls.DB_ENGINE}")
        print(f"  DB_NAME: {cls.DB_NAME}")
        print(f"  DB_HOST: {cls.DB_HOST}")
        print(f"  EMAIL_HOST: {cls.EMAIL_HOST}")


def config_class_example():
    """Config class pattern"""
    print("=" * 50)
    print("7. CONFIG CLASS PATTERN")
    print("=" * 50)
    
    Config.print_config()
    print()
    
    # Database config
    db_config = Config.get_database_config()
    print("Database Config:")
    for key, value in db_config.items():
        print(f"  {key}: {value}")
    print()


# =====================================
# 8. SECURITY BEST PRACTICES
# =====================================

def security_tips():
    """Security best practices"""
    print("=" * 50)
    print("8. SECURITY BEST PRACTICES")
    print("=" * 50)
    
    print("""
1. HECH QACHON .env faylni Git'ga commit qilmang!
   
   # .gitignore
   .env
   .env.*
   !.env.example

2. .env.example template yarating:
   
   # .env.example
   SECRET_KEY=
   DB_PASSWORD=
   API_KEY=

3. Production'da real qiymatlardan foydalaning:
   
   SECRET_KEY=super-secure-random-key-here
   DB_PASSWORD=very-strong-password

4. Environment variablelarni tekshiring:
   
   if not os.getenv('SECRET_KEY'):
       raise ValueError("SECRET_KEY is required!")

5. Default qiymatlar faqat development uchun:
   
   # ✓ Development
   DEBUG = os.getenv('DEBUG', 'True') == 'True'
   
   # ✗ Production (majburiy bo'lsin)
   SECRET_KEY = os.getenv('SECRET_KEY')  # No default!

6. Sensitive ma'lumotlarni log qilmang:
   
   # ✗ YOMON
   print(f"SECRET_KEY: {secret_key}")
   
   # ✓ YAXSHI
   print(f"SECRET_KEY: {'*' * len(secret_key)}")
    """)


# =====================================
# MAIN EXECUTION
# =====================================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "=" * 50)
    print("LESSON 35: BASIC ENVIRONMENT SETUP")
    print("=" * 50 + "\n")
    
    # Examples
    basic_getenv()
    default_values()
    type_conversion()
    create_env_example()
    django_settings_example()
    check_environment()
    config_class_example()
    security_tips()
    
    print("=" * 50)
    print("✅ All examples completed!")
    print("=" * 50)


if __name__ == '__main__':
    # Set some example environment variables for testing
    os.environ['SECRET_KEY'] = 'django-insecure-test-key-12345'
    os.environ['DEBUG'] = 'True'
    os.environ['DB_NAME'] = 'library_db'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = 'testpassword'
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
    os.environ['DB_PORT'] = '5432'
    os.environ['TAX_RATE'] = '0.18'
    
    main()