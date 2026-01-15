# Lesson 37 Examples: Production Deployment

Bu yerda production deployment uchun turli xil misollar va ready-to-use configuration fayllar mavjud.

## Examples ro'yxati

### 1. Production Settings Structure
**File:** `01-production-settings.py`

Production muhit uchun Django settings konfiguratsiyasi:
- Settings modularizatsiyasi (base, dev, prod)
- Environment variables
- Security settings
- Database optimization
- Caching configuration
- Logging setup

---

### 2. Gunicorn Configuration
**File:** `02-gunicorn-config.py`

Gunicorn WSGI server uchun optimal configuration:
- Worker processes calculation
- Timeout settings
- Logging configuration
- Performance tuning
- SSL support

---

### 3. Nginx Server Block
**File:** `03-nginx-config.conf`

Nginx reverse proxy full configuration:
- HTTP to HTTPS redirect
- SSL/TLS configuration
- Static files serving
- Media files handling
- Security headers
- Proxy settings
- Rate limiting
- Gzip compression

---

### 4. Deployment Scripts
**File:** `04-deployment-scripts.sh`

Automated deployment bash scripts:
- Full deployment script
- Backup script
- Update script
- Rollback script
- Health check script

---

### 5. Systemd Service Files
**File:** `05-systemd-services.ini`

Systemd service configurations:
- Gunicorn service
- Celery worker service
- Celery beat service
- Auto-restart configuration
- Dependency management

---

## Qanday ishlatish

### 1. Settings setup

```bash
# Copy settings structure
cp examples/01-production-settings.py your_project/settings/production.py

# Update paths and configuration
nano your_project/settings/production.py
```

### 2. Gunicorn setup

```bash
# Copy config
cp examples/02-gunicorn-config.py gunicorn_config.py

# Update settings
nano gunicorn_config.py

# Test
gunicorn --config gunicorn_config.py config.wsgi:application
```

### 3. Nginx setup

```bash
# Copy config
sudo cp examples/03-nginx-config.conf /etc/nginx/sites-available/your-site

# Update domain and paths
sudo nano /etc/nginx/sites-available/your-site

# Enable site
sudo ln -s /etc/nginx/sites-available/your-site /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Deployment automation

```bash
# Copy scripts
cp examples/04-deployment-scripts.sh scripts/

# Make executable
chmod +x scripts/*.sh

# Run deployment
./scripts/deploy.sh
```

### 5. Systemd services

```bash
# Copy service files
sudo cp examples/05-systemd-services.ini /etc/systemd/system/

# Update configuration
sudo nano /etc/systemd/system/gunicorn.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

---

## Configuration checklist

### Pre-deployment
- [ ] Settings environment-ga ko'ra to'g'ri tanlanganini tekshiring
- [ ] SECRET_KEY production uchun alohida bo'lishi kerak
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS to'ldirilgan
- [ ] Database credentials to'g'ri
- [ ] Static va media paths to'g'ri

### Server setup
- [ ] Python 3.8+ o'rnatilgan
- [ ] PostgreSQL configured
- [ ] Redis running (agar caching ishlatilsa)
- [ ] Nginx installed
- [ ] SSL certificate obtained
- [ ] Firewall configured

### Application
- [ ] Virtual environment yaratilgan
- [ ] Dependencies installed
- [ ] Migrations applied
- [ ] Static files collected
- [ ] Media directory created with proper permissions

### Services
- [ ] Gunicorn service running
- [ ] Nginx service running
- [ ] Services enabled on boot
- [ ] Logs accessible va readable

---

## Testing

### Local testing

```bash
# Production settings bilan local test
python manage.py runserver --settings=config.settings.production

# Gunicorn bilan test
gunicorn --bind 0.0.0.0:8000 config.wsgi:application

# Static files test
python manage.py collectstatic --noinput
```

### Server testing

```bash
# Service status
sudo systemctl status gunicorn
sudo systemctl status nginx

# Logs
sudo journalctl -u gunicorn -n 50
sudo tail -f /var/log/nginx/access.log

# Connectivity
curl -I http://localhost
curl -I https://yourdomain.com

# API test
curl https://yourdomain.com/api/books/
```

---

## Troubleshooting

### Gunicorn issues

```bash
# Check if running
ps aux | grep gunicorn

# View logs
sudo journalctl -u gunicorn -f

# Restart
sudo systemctl restart gunicorn

# Check socket
ls -la /run/gunicorn.sock
```

### Nginx issues

```bash
# Test configuration
sudo nginx -t

# View error logs
sudo tail -f /var/log/nginx/error.log

# Reload configuration
sudo systemctl reload nginx

# Restart if needed
sudo systemctl restart nginx
```

### Static files issues

```bash
# Recollect static files
python manage.py collectstatic --noinput --clear

# Check permissions
ls -la staticfiles/
sudo chown -R www-data:www-data staticfiles/

# Check Nginx config
# Verify STATIC_ROOT path matches Nginx config
```

### SSL/HTTPS issues

```bash
# Test certificate
sudo certbot certificates

# Renew certificate
sudo certbot renew --dry-run

# Check certificate expiry
openssl s_client -connect yourdomain.com:443 | openssl x509 -noout -dates
```

---

## Best practices

1. **Settings**
   - Har doim settings'ni environment-ga ko'ra ajrating
   - Sensitive data'ni .env faylda saqlang
   - Production'da DEBUG = False

2. **Security**
   - HTTPS majburiy bo'lsin
   - Security headers qo'shing
   - Firewall sozlang
   - Regular updates

3. **Performance**
   - Caching ishlatilsin (Redis)
   - Static files CDN'dan serve qiling
   - Database connection pooling
   - Gzip compression

4. **Monitoring**
   - Logging to'g'ri sozlangan bo'lsin
   - Health check endpoint
   - Error tracking (Sentry)
   - Uptime monitoring

5. **Backup**
   - Daily automated backups
   - Off-site backup storage
   - Test restore process
   - Database va media files

---

## Qo'shimcha resurslar

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Nginx Docs](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)

---

**Happy Deploying!**