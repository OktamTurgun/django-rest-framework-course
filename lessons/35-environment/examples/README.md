# Lesson 35: Environment Setup - Examples

> Turli environment setup usullari va patterns

## Misollar ro'yxati

| # | Fayl | Tavsif | Qiyinlik |
|---|------|--------|----------|
| 01 | [basic_env_setup.py](01-basic_env_setup.py) | Oddiy .env setup | ⭐ |
| 02 | [decouple_advanced.py](02-decouple_advanced.py) | python-decouple advanced | ⭐⭐ |
| 03 | [dotenv_usage.py](03-dotenv_usage.py) | python-dotenv examples | ⭐⭐ |
| 04 | [settings_structure.py](04-settings_structure.py) | Multi-environment settings | ⭐⭐⭐ |
| 05 | [env_validator.py](05-env_validator.py) | Environment validator | ⭐⭐ |

---

## Qanday ishlatish

### 1. Fayllarni o'qing
Har bir faylda to'liq ishchi kod va tushuntirishlar bor.

### 2. Local'da test qiling
```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies
pip install python-decouple python-dotenv django

# Run examples
python 01-basic_env_setup.py
python 02-decouple_advanced.py
# ...
```

### 3. O'zgartiring va tajriba qiling
Kodlarni o'zingizga moslashtiring va yangi narsalarni sinab ko'ring.

---

## Har bir misolda nima bor?

### 01 - Basic Env Setup ⭐
- `.env` fayl yaratish
- `os.getenv()` bilan ishlash
- Environment variables types
- Default values

### 02 - Decouple Advanced ⭐⭐
- `python-decouple` kutubxonasi
- Type casting (bool, int, float)
- `Csv()` helper
- Repository pattern

### 03 - Dotenv Usage ⭐⭐
- `python-dotenv` kutubxonasi
- `load_dotenv()` usuli
- Environment priorities
- Multiple .env files

### 04 - Settings Structure ⭐⭐⭐
- Multi-environment settings
- base.py, development.py, production.py
- Settings inheritance
- Automatic loading

### 05 - Env Validator ⭐⭐
- Environment validation
- Required variables checking
- Custom validators
- Error handling

---

## Environment Files

Misollar uchun kerakli `.env` fayllar:

### .env.example
```bash
# Django
SECRET_KEY=your-secret-key-here
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

# Redis
REDIS_URL=redis://localhost:6379/0
```

### .env.development
```bash
ENVIRONMENT=development
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### .env.production
```bash
ENVIRONMENT=production
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_production
DB_USER=prod_user
DB_PASSWORD=super_secure_password
DB_HOST=prod-db.example.com
DB_PORT=5432
```

---

## Tips & Tricks

### 1. .env faylni hech qachon commit qilmang
```bash
# .gitignore
.env
.env.*
!.env.example
```

### 2. Type casting muhim
```python
# ❌ String qaytaradi
DEBUG = os.getenv('DEBUG')  # 'True'

# ✅ Boolean qaytaradi
from decouple import config
DEBUG = config('DEBUG', cast=bool)  # True
```

### 3. Default values ishlating
```python
# Production'da default bo'lmasin
SECRET_KEY = config('SECRET_KEY')  # Required!

# Development uchun default
DB_HOST = config('DB_HOST', default='localhost')
```

### 4. Environment hierarchy
```
1. System environment variables
2. .env file
3. Default values
```

---

## Common Patterns

### Pattern 1: Config class
```python
class Config:
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', cast=bool)
    
    class Database:
        ENGINE = config('DB_ENGINE')
        NAME = config('DB_NAME')
```

### Pattern 2: Settings factory
```python
def get_settings():
    env = config('ENVIRONMENT', default='development')
    
    if env == 'production':
        return ProductionSettings()
    elif env == 'staging':
        return StagingSettings()
    else:
        return DevelopmentSettings()
```

### Pattern 3: Lazy loading
```python
from functools import lru_cache

@lru_cache()
def get_config():
    return {
        'secret_key': config('SECRET_KEY'),
        'debug': config('DEBUG', cast=bool),
    }
```

---

## Testing

Har bir misolni test qilish uchun:

```bash
# 1. .env faylni yarating
cp .env.example .env

# 2. Qiymatlarni to'ldiring
nano .env

# 3. Script'ni ishga tushiring
python 01-basic_env_setup.py

# 4. Natijani tekshiring
echo $?  # Exit code (0 = success)
```

---

## Troubleshooting

### Problem: "SECRET_KEY is not set"
```bash
# Solution: .env faylda SECRET_KEY borligini tekshiring
cat .env | grep SECRET_KEY
```

### Problem: "No module named 'decouple'"
```bash
# Solution: Kutubxonani o'rnating
pip install python-decouple
```

### Problem: ".env fayl o'qilmayapti"
```python
# Solution: To'g'ri yo'l ko'rsating
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
```

---

## Resources

- [python-decouple GitHub](https://github.com/HBNetwork/python-decouple)
- [python-dotenv GitHub](https://github.com/theskumar/python-dotenv)
- [12 Factor App](https://12factor.net/)
- [Django Settings Best Practices](https://django-best-practices.readthedocs.io/)

---

## Next Steps

1. Barcha misollarni o'qing va tushining
2. O'zingizning projektingizda sinab ko'ring
3. [Homework](../homework.md)'ni bajaring
4. Settings strukturasini yaxshilang

---

**Happy Coding!**