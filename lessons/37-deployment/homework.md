# Homework: Production Deployment

## Umumiy ko'rsatmalar

- Barcha topshiriqlarni tartib bilan bajaring
- Har bir bosqichni test qiling
- Screenshot yoki video qiling
- GitHub'ga commit va push qiling
- README.md'ga deployment hujjatlarini qo'shing

## Level 1: Basic Deployment (Beginner) ⭐

### Task 1.1: Local Production Setup
**Maqsad:** Local muhitda production settings bilan ishlash

```bash
# 1. Production settings yaratish
project/
├── settings/
│   ├── __init__.py
│   ├── base.py
│   ├── development.py
│   └── production.py

# 2. Environment variables
# .env faylni yarating va kerakli o'zgaruvchilarni qo'shing

# 3. Production mode'da run qiling
python manage.py runserver --settings=config.settings.production

# 4. Test qiling:
- DEBUG=False ishlayotganini tekshiring
- Static files to'g'ri xizmat qilishini tekshiring
- ALLOWED_HOSTS to'g'ri ishlashini tekshiring
```

**Tekshirish:**
- [ ] Settings strukturasi to'g'ri
- [ ] .env fayli to'ldirilgan
- [ ] Production mode'da ishga tushadi
- [ ] Error pages (404, 500) ko'rsatiladi

---

### Task 1.2: Railway Deploy
**Maqsad:** Railway platformasiga deploy qilish

```bash
# 1. Railway CLI o'rnatish
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Environment variables qo'shish
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=*.railway.app

# 5. Deploy
railway up

# 6. Database migration
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

**Tekshirish:**
- [ ] Railway'da deploy bo'ldi
- [ ] Database migrations ishladi
- [ ] API endpoints ishlayapti
- [ ] Admin panel ochiladi

**Natija:**
```
Railway URL: https://your-app.railway.app
Admin: https://your-app.railway.app/admin/
API: https://your-app.railway.app/api/
```

---

### Task 1.3: Static Files with WhiteNoise
**Maqsad:** WhiteNoise bilan static files xizmat qilish

```bash
# 1. Install WhiteNoise
pip install whitenoise

# 2. settings.py'da sozlash
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Test qiling
```

**Tekshirish:**
- [ ] WhiteNoise o'rnatildi
- [ ] Static files collect qilindi
- [ ] Admin panel stillari ishlayapti
- [ ] Swagger/Redoc stillari to'g'ri

---

## Level 2: VPS Deployment (Intermediate) ⭐⭐

### Task 2.1: DigitalOcean Droplet Setup
**Maqsad:** VPS'da server sozlash

```bash
# 1. Create Droplet
# - Ubuntu 22.04 LTS
# - $6/month plan
# - SSH key qo'shing

# 2. SSH orqali ulanish
ssh root@your-server-ip

# 3. Initial setup
apt update && apt upgrade -y
apt install python3-pip python3-venv postgresql nginx -y

# 4. User yaratish
adduser deploy
usermod -aG sudo deploy
su - deploy

# 5. Project directory
mkdir -p /var/www/library-api
cd /var/www/library-api
```

**Tekshirish:**
- [ ] Droplet yaratildi
- [ ] SSH ulanish ishlayapti
- [ ] Kerakli packages o'rnatildi
- [ ] Deploy user yaratildi

---

### Task 2.2: PostgreSQL Setup
**Maqsad:** Production database sozlash

```bash
# 1. PostgreSQL user yaratish
sudo -u postgres psql

CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'strong_password';
ALTER ROLE library_user SET client_encoding TO 'utf8';
ALTER ROLE library_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE library_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
\q

# 2. PostgreSQL remote access (agar kerak bo'lsa)
sudo nano /etc/postgresql/14/main/postgresql.conf
# listen_addresses = '*'

sudo nano /etc/postgresql/14/main/pg_hba.conf
# host all all 0.0.0.0/0 md5

sudo systemctl restart postgresql

# 3. Database connection test
psql -U library_user -d library_db -h localhost
```

**Tekshirish:**
- [ ] Database yaratildi
- [ ] User yaratildi va permissions berildi
- [ ] Local connection ishlayapti
- [ ] Django'dan ulanadi

---

### Task 2.3: Gunicorn Service
**Maqsad:** Gunicorn WSGI server sozlash

```bash
# 1. Project setup
cd /var/www/library-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. gunicorn_config.py
nano gunicorn_config.py
# (Configuration'ni README.md'dan oling)

# 3. Systemd service
sudo nano /etc/systemd/system/gunicorn.service
# (Service file'ni README.md'dan oling)

# 4. Start service
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

# 5. Test
curl http://127.0.0.1:8000/api/books/
```

**Tekshirish:**
- [ ] Gunicorn service yaratildi
- [ ] Service running holatda
- [ ] Boot'da avtomatik ishga tushadi
- [ ] Logs ko'rinadi

---

### Task 2.4: Nginx Configuration
**Maqsad:** Nginx reverse proxy sozlash

```bash
# 1. Nginx config
sudo nano /etc/nginx/sites-available/library-api
# (Configuration'ni README.md'dan oling)

# 2. Enable site
sudo ln -s /etc/nginx/sites-available/library-api /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Optional

# 3. Test configuration
sudo nginx -t

# 4. Reload Nginx
sudo systemctl reload nginx

# 5. Check status
sudo systemctl status nginx

# 6. Test
curl http://your-server-ip/api/books/
```

**Tekshirish:**
- [ ] Nginx config yaratildi
- [ ] Site enabled qilindi
- [ ] Configuration valid
- [ ] Server IP orqali ishlayapti

---

## Level 3: Production Ready (Advanced) ⭐⭐⭐

### Task 3.1: Domain & SSL Setup
**Maqsad:** Domain va HTTPS sozlash

```bash
# 1. Domain DNS sozlash
# A record: @ -> your-server-ip
# A record: www -> your-server-ip

# 2. DNS tekshirish
dig yourdomain.com
nslookup yourdomain.com

# 3. Nginx'da domain qo'shish
sudo nano /etc/nginx/sites-available/library-api
# server_name yourdomain.com www.yourdomain.com;
sudo systemctl reload nginx

# 4. Certbot o'rnatish
sudo apt install certbot python3-certbot-nginx

# 5. SSL certificate olish
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 6. Auto-renewal test
sudo certbot renew --dry-run

# 7. Test HTTPS
curl -I https://yourdomain.com
```

**Tekshirish:**
- [ ] Domain configured
- [ ] DNS propagated
- [ ] SSL certificate installed
- [ ] HTTPS ishlayapti
- [ ] HTTP -> HTTPS redirect
- [ ] Auto-renewal configured

---

### Task 3.2: Security Hardening
**Maqsad:** Server va application security

```bash
# 1. UFW Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status

# 2. Fail2Ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# 3. Django security settings
# settings/production.py'da:
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# 4. Security headers test
curl -I https://yourdomain.com
# Headers'larni tekshiring
```

**Tekshirish:**
- [ ] Firewall configured
- [ ] Fail2Ban installed
- [ ] Django security settings enabled
- [ ] Security headers present
- [ ] No sensitive info exposed

---

### Task 3.3: Logging & Monitoring
**Maqsad:** Log va monitoring setup

```bash
# 1. Log directories
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/www/library-api/logs
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/www/library-api/logs

# 2. Django logging (settings/production.py)
# LOGGING configuration'ni README.md'dan oling

# 3. Log rotation
sudo nano /etc/logrotate.d/library-api

/var/log/gunicorn/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload gunicorn
    endscript
}

# 4. View logs
sudo tail -f /var/log/nginx/library-api-access.log
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/www/library-api/logs/django.log
```

**Tekshirish:**
- [ ] Log directories yaratildi
- [ ] Django logging configured
- [ ] Log rotation sozlandi
- [ ] Logs yozilyapti

---

### Task 3.4: Backup Strategy
**Maqsad:** Automated backup system

```bash
# 1. Backup directory
sudo mkdir -p /var/backups/library-api

# 2. Backup script
sudo nano /usr/local/bin/backup-library-api.sh

#!/bin/bash
BACKUP_DIR="/var/backups/library-api"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/var/www/library-api"

# Database backup
pg_dump -U library_user library_db > $BACKUP_DIR/db_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz $PROJECT_DIR/media/

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"

# 3. Make executable
sudo chmod +x /usr/local/bin/backup-library-api.sh

# 4. Cron job (daily at 2 AM)
sudo crontab -e
0 2 * * * /usr/local/bin/backup-library-api.sh >> /var/log/backup.log 2>&1

# 5. Test backup
sudo /usr/local/bin/backup-library-api.sh
ls -lh /var/backups/library-api/
```

**Tekshirish:**
- [ ] Backup script yaratildi
- [ ] Cron job configured
- [ ] Manual backup ishlaydi
- [ ] Old backups delete qilinadi

---

## Level 4: Enterprise Grade (Expert) ⭐⭐⭐⭐

### Task 4.1: Load Balancing
**Maqsad:** Nginx load balancer sozlash

```nginx
# /etc/nginx/sites-available/library-api

upstream library_api {
    least_conn;
    server 127.0.0.1:8001 weight=1;
    server 127.0.0.1:8002 weight=1;
    server 127.0.0.1:8003 weight=2;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    location / {
        proxy_pass http://library_api;
        # ... other proxy settings
    }
}
```

**Gunicorn multiple instances:**

```bash
# /etc/systemd/system/gunicorn@.service
[Unit]
Description=Gunicorn daemon for Django Library API (instance %i)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/library-api
ExecStart=/var/www/library-api/venv/bin/gunicorn \
          --bind 127.0.0.1:800%i \
          config.wsgi:application

[Install]
WantedBy=multi-user.target

# Enable multiple instances
sudo systemctl enable gunicorn@1
sudo systemctl enable gunicorn@2
sudo systemctl enable gunicorn@3
```

**Tekshirish:**
- [ ] Multiple Gunicorn instances
- [ ] Load balancer configured
- [ ] Requests distributed equally
- [ ] Auto-failover ishlayapti

---

### Task 4.2: Redis Caching
**Maqsad:** Redis cache layer qo'shish

```bash
# 1. Install Redis
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# 2. Django settings
pip install django-redis

# settings/production.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 3. Cache usage
from django.core.cache import cache

# In views
@method_decorator(cache_page(60 * 15))  # 15 minutes
def list(self, request):
    ...

# 4. Test caching
# First request - slow
time curl https://yourdomain.com/api/books/

# Second request - fast (from cache)
time curl https://yourdomain.com/api/books/
```

**Tekshirish:**
- [ ] Redis installed
- [ ] Django connected to Redis
- [ ] Caching ishlayapti
- [ ] Response time improved

---

### Task 4.3: CDN for Static Files
**Maqsad:** AWS S3 + CloudFront CDN

```bash
# 1. Install boto3
pip install boto3 django-storages

# 2. AWS S3 settings
# settings/production.py
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# 3. Upload to S3
python manage.py collectstatic --noinput

# 4. CloudFront distribution
# AWS Console'da CloudFront distribution yarating
# Origin: your-bucket.s3.amazonaws.com
```

**Tekshirish:**
- [ ] S3 bucket configured
- [ ] Static files uploaded
- [ ] Media files working
- [ ] CloudFront distribution active

---

### Task 4.4: Monitoring with Sentry
**Maqsad:** Error tracking va monitoring

```bash
# 1. Install Sentry SDK
pip install sentry-sdk

# 2. Sentry configuration
# settings/production.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment="production",
)

# 3. Test Sentry
# Create test view that raises error
def trigger_error(request):
    division_by_zero = 1 / 0

# 4. Check Sentry dashboard
# Verify error appears in Sentry
```

**Tekshirish:**
- [ ] Sentry account yaratildi
- [ ] SDK o'rnatildi
- [ ] Error tracking ishlayapti
- [ ] Dashboard'da errors ko'rinadi

---

## Bonus Tasks

### Bonus 1: CI/CD Pipeline Preview
**Maqsad:** GitHub Actions bilan automated deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/library-api
            git pull origin main
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate
            python manage.py collectstatic --noinput
            sudo systemctl restart gunicorn
```

---

### Bonus 2: Health Check Endpoint
**Maqsad:** System health monitoring

```python
# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class HealthCheckView(APIView):
    permission_classes = []
    
    def get(self, request):
        # Check database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'database': 'down',
                'error': str(e)
            }, status=503)
        
        # Check cache
        from django.core.cache import cache
        try:
            cache.set('health_check', 'ok', 10)
            cache.get('health_check')
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'cache': 'down',
                'error': str(e)
            }, status=503)
        
        return Response({
            'status': 'healthy',
            'database': 'up',
            'cache': 'up'
        })

# urls.py
path('api/health/', HealthCheckView.as_view()),
```

---

### Bonus 3: Auto-scaling Script
**Maqsad:** Resource monitoring va auto-scaling

```python
#!/usr/bin/env python3
# monitor.py

import psutil
import subprocess
import time

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80

def check_resources():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    
    print(f"CPU: {cpu}% | Memory: {memory}%")
    
    if cpu > CPU_THRESHOLD or memory > MEMORY_THRESHOLD:
        scale_up()
    
def scale_up():
    print("Scaling up...")
    # Start additional Gunicorn instance
    subprocess.run([
        'sudo', 'systemctl', 'start', f'gunicorn@{get_next_instance()}'
    ])

def get_next_instance():
    # Logic to find next available instance number
    pass

if __name__ == '__main__':
    while True:
        check_resources()
        time.sleep(60)  # Check every minute
```

---

## Topshirish talablari

### Har bir task uchun:

1. **Documentation**
   - Deployment steps dokumentatsiyasi
   - Configuration fayllari
   - Troubleshooting guide

2. **Screenshots/Video**
   - Server dashboard
   - Working application
   - Monitoring tools
   - SSL certificate

3. **Repository**
   ```
   deployment/
   ├── docs/
   │   ├── deployment-guide.md
   │   └── troubleshooting.md
   ├── configs/
   │   ├── nginx.conf
   │   ├── gunicorn_config.py
   │   └── systemd/
   │       ├── gunicorn.service
   │       └── gunicorn@.service
   ├── scripts/
   │   ├── backup.sh
   │   ├── deploy.sh
   │   └── monitor.py
   └── README.md
   ```

4. **Testing checklist**
   - [ ] API endpoints working
   - [ ] HTTPS enabled
   - [ ] Admin panel accessible
   - [ ] Static files served
   - [ ] Media upload working
   - [ ] Database connected
   - [ ] Logs accessible
   - [ ] Backups working
   - [ ] Monitoring active

---

## Baholash mezonlari

### Level 1: Basic (1-30 ball)
- Railway/Heroku deploy: 10 ball
- Static files setup: 10 ball
- Environment variables: 10 ball

### Level 2: VPS (31-60 ball)
- Server setup: 10 ball
- Database configuration: 10 ball
- Gunicorn service: 10 ball
- Nginx configuration: 10 ball

### Level 3: Production (61-85 ball)
- Domain & SSL: 10 ball
- Security hardening: 5 ball
- Logging: 5 ball
- Backup system: 5 ball

### Level 4: Enterprise (86-100 ball)
- Load balancing: 5 ball
- Redis caching: 3 ball
- CDN setup: 3 ball
- Monitoring (Sentry): 4 ball

### Bonus (101-115 ball)
- CI/CD pipeline: 5 ball
- Health check: 5 ball
- Auto-scaling: 5 ball

---

## Deadline

- **Level 1-2:** 3 kun
- **Level 3:** +2 kun
- **Level 4:** +2 kun
- **Jami:** 1 hafta

---

## Yordam

- Discord: [#deployment-help](https://discord.gg/...)
- Office hours: Har kuni 20:00-22:00
- Documentation: [deployment/docs/](deployment/docs/)

---

**Good luck with deployment!**