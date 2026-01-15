# Lesson 37: Production Deployment

> Django REST Framework loyihalarini production serverga deploy qilish

## Maqsad

Ushbu darsda Django REST Framework loyihalarini production serverga deploy qilish, Gunicorn WSGI server, Nginx reverse proxy, SSL/HTTPS sozlash va domain bilan ishlashni o'rganamiz.

## O'rganish natijalari

Ushbu darsdan so'ng siz quyidagilarni qila olasiz:

- Production uchun Django settings sozlash
- Gunicorn WSGI server sozlash
- Nginx reverse proxy konfiguratsiya qilish
- SSL/HTTPS sertifikat sozlash (Let's Encrypt)
- Domain bilan ishlash
- Static va media fayllarni to'g'ri xizmat qilish
- Production database setup (PostgreSQL)
- Environment variables bilan ishlash
- Logging va monitoring sozlash
- Railway, Heroku, DigitalOcean'ga deploy qilish

## Deployment Overview

### Production Stack

```
Internet
    ↓
Domain (example.com)
    ↓
SSL/HTTPS (Let's Encrypt)
    ↓
Nginx (Reverse Proxy) :80, :443
    ↓
Gunicorn (WSGI Server) :8000
    ↓
Django Application
    ↓
PostgreSQL Database :5432
```

### Deployment Workflow

```
1. Local Development
   ├── Git repository
   └── Docker setup

2. Code Preparation
   ├── Settings optimization
   ├── Static files collection
   ├── Database migrations
   └── Dependencies freeze

3. Server Setup
   ├── VPS/Cloud provider
   ├── Domain configuration
   ├── SSL certificate
   └── Server hardening

4. Application Deployment
   ├── Clone repository
   ├── Virtual environment
   ├── Install dependencies
   └── Configure services

5. Web Server Setup
   ├── Gunicorn service
   ├── Nginx configuration
   └── SSL setup

6. Post-deployment
   ├── Testing
   ├── Monitoring
   └── Logging
```

## 1. Production Settings

### Settings Organization

```python
# settings/
#   __init__.py
#   base.py         # Common settings
#   development.py  # Dev settings
#   production.py   # Prod settings
```

### Base Settings (base.py)

```python
import os
from pathlib import Path
from decouple import config

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
    'corsheaders',
    'drf_yasg',
    
    # Local apps
    'books',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

# Database (override in production.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
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
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### Production Settings (production.py)

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'your-server-ip',
]

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# Static files - WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# Cache (Redis)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

## 2. Gunicorn Setup

### Install Gunicorn

```bash
pip install gunicorn
```

### Gunicorn Configuration

**gunicorn_config.py:**

```python
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "library-api"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/gunicorn.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
```

### Systemd Service

**/etc/systemd/system/gunicorn.service:**

```ini
[Unit]
Description=Gunicorn daemon for Django Library API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/library-api
ExecStart=/var/www/library-api/venv/bin/gunicorn \
          --config /var/www/library-api/gunicorn_config.py \
          config.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Start Gunicorn Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start gunicorn

# Enable on boot
sudo systemctl enable gunicorn

# Check status
sudo systemctl status gunicorn

# View logs
sudo journalctl -u gunicorn
```

## 3. Nginx Configuration

### Install Nginx

```bash
sudo apt update
sudo apt install nginx
```

### Nginx Server Block

**/etc/nginx/sites-available/library-api:**

```nginx
upstream library_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logs
    access_log /var/log/nginx/library-api-access.log;
    error_log /var/log/nginx/library-api-error.log;

    # Max upload size
    client_max_body_size 10M;

    # Static files
    location /static/ {
        alias /var/www/library-api/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/library-api/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://library_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Deny access to sensitive files
    location ~ /\.(?!well-known) {
        deny all;
    }
}
```

### Enable Nginx Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/library-api /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

# Check status
sudo systemctl status nginx
```

## 4. SSL/HTTPS Setup (Let's Encrypt)

### Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx
```

### Obtain SSL Certificate

```bash
# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow prompts:
# 1. Enter email address
# 2. Agree to terms
# 3. Choose to redirect HTTP to HTTPS (recommended)
```

### Auto-renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically adds cron job for renewal
# Check: /etc/cron.d/certbot

# Manual renewal
sudo certbot renew
```

### Certificate Info

```bash
# View certificates
sudo certbot certificates

# Certificate locations:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

## 5. Domain Configuration

### DNS Settings

**A Records:**

```
Type    Name    Value               TTL
A       @       your-server-ip      3600
A       www     your-server-ip      3600
```

**CNAME (Optional):**

```
Type    Name    Value               TTL
CNAME   api     yourdomain.com      3600
```

### Domain Verification

```bash
# Check DNS propagation
dig yourdomain.com
nslookup yourdomain.com

# Test connection
curl -I https://yourdomain.com
```

## 6. Deployment Process

### Step-by-Step Deployment

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install python3-pip python3-venv postgresql nginx -y

# 3. Create project directory
sudo mkdir -p /var/www/library-api
sudo chown $USER:$USER /var/www/library-api

# 4. Clone repository
cd /var/www/library-api
git clone https://github.com/yourusername/library-api.git .

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install requirements
pip install -r requirements.txt

# 7. Setup environment variables
nano .env
# Add all required variables

# 8. Collect static files
python manage.py collectstatic --noinput

# 9. Run migrations
python manage.py migrate

# 10. Create superuser
python manage.py createsuperuser

# 11. Test application
python manage.py runserver 0.0.0.0:8000
# Visit: http://your-ip:8000

# 12. Setup Gunicorn service
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 13. Setup Nginx
sudo cp nginx-config /etc/nginx/sites-available/library-api
sudo ln -s /etc/nginx/sites-available/library-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 14. Setup SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 15. Final checks
sudo systemctl status gunicorn
sudo systemctl status nginx
curl -I https://yourdomain.com
```

## 7. Environment Variables

**.env file:**

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Sentry (Optional)
SENTRY_DSN=your-sentry-dsn
```

## 8. Post-Deployment

### Testing

```bash
# Health check endpoint
curl https://yourdomain.com/api/health/

# API endpoints
curl https://yourdomain.com/api/books/
curl https://yourdomain.com/api/swagger/

# Admin panel
https://yourdomain.com/admin/
```

### Monitoring

```bash
# Check logs
sudo tail -f /var/log/nginx/library-api-access.log
sudo tail -f /var/log/nginx/library-api-error.log
sudo tail -f /var/log/gunicorn/access.log
sudo journalctl -u gunicorn -f

# Check processes
ps aux | grep gunicorn
ps aux | grep nginx

# Check disk space
df -h

# Check memory
free -h

# Check network
netstat -tulpn | grep :80
netstat -tulpn | grep :443
```

### Backup

```bash
# Database backup
pg_dump library_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Media files backup
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Full backup script
#!/bin/bash
BACKUP_DIR="/var/backups/library-api"
DATE=$(date +%Y%m%d_%H%M%S)

# Database
pg_dump library_db > $BACKUP_DIR/db_$DATE.sql

# Media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/library-api/media/

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## 9. Platform-Specific Deployments

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Add environment variables
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False

# View logs
railway logs
```

### Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create library-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail
```

**Procfile:**

```
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
```

### DigitalOcean App Platform

```yaml
# app.yaml
name: library-api
services:
  - name: web
    github:
      repo: yourusername/library-api
      branch: main
    build_command: pip install -r requirements.txt && python manage.py collectstatic --noinput
    run_command: gunicorn config.wsgi
    envs:
      - key: SECRET_KEY
        value: your-secret-key
      - key: DEBUG
        value: "False"
      - key: DATABASE_URL
        value: ${db.DATABASE_URL}
    health_check:
      http_path: /api/health/
databases:
  - name: db
    engine: PG
    version: "14"
```

## Deployment Checklist

### Pre-deployment

- [ ] DEBUG = False
- [ ] SECRET_KEY changed
- [ ] ALLOWED_HOSTS configured
- [ ] Environment variables set
- [ ] Database configured
- [ ] Static files collected
- [ ] Migrations run
- [ ] Tests passing
- [ ] Security settings enabled
- [ ] CORS configured
- [ ] HTTPS redirect enabled

### Server Setup

- [ ] Server provisioned
- [ ] Domain configured
- [ ] DNS propagated
- [ ] Firewall configured
- [ ] PostgreSQL installed
- [ ] Redis installed (if needed)
- [ ] Nginx installed
- [ ] SSL certificate installed

### Application

- [ ] Code deployed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Static files served
- [ ] Media files configured
- [ ] Database connected
- [ ] Migrations applied
- [ ] Superuser created

### Services

- [ ] Gunicorn running
- [ ] Nginx running
- [ ] PostgreSQL running
- [ ] Redis running (if needed)
- [ ] Services enabled on boot
- [ ] Logs accessible

### Post-deployment

- [ ] Health check passing
- [ ] API endpoints working
- [ ] Admin panel accessible
- [ ] HTTPS working
- [ ] Static files loading
- [ ] Media files working
- [ ] Email working
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Documentation updated

## Common Issues

### 1. Static Files Not Loading

```bash
# Solution
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl reload nginx
```

### 2. 502 Bad Gateway

```bash
# Check Gunicorn
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50

# Check socket file
ls -la /run/gunicorn.sock

# Restart services
sudo systemctl restart gunicorn
```

### 3. Permission Denied

```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/library-api
sudo chmod -R 755 /var/www/library-api

# Media directory
sudo chown -R www-data:www-data /var/www/library-api/media
sudo chmod -R 755 /var/www/library-api/media
```

### 4. Database Connection Error

```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Check connection
psql -U library_user -d library_db -h localhost

# Update .env
DB_HOST=localhost
DB_PORT=5432
```

## Best Practices

1. **Security**
   - Always use HTTPS
   - Strong SECRET_KEY
   - Secure password policies
   - Regular security updates
   - Firewall configuration

2. **Performance**
   - Use caching (Redis)
   - Database optimization
   - Static files compression
   - CDN for media files
   - Connection pooling

3. **Monitoring**
   - Set up error tracking (Sentry)
   - Monitor logs regularly
   - Set up alerts
   - Track performance metrics
   - Database monitoring

4. **Backups**
   - Daily database backups
   - Media files backup
   - Off-site storage
   - Test restore process
   - Automated backup scripts

5. **Updates**
   - Regular dependency updates
   - Security patches
   - Django/DRF updates
   - Server updates
   - SSL certificate renewal

## Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)

## Homework

[Homework topshiriqlari](homework.md)

## Keyingi dars

[Lesson 38: CI/CD Pipeline](../38-cicd/)

---

**Happy Deploying!**