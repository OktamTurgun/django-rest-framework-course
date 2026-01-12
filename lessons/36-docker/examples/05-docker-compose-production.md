# Example 05: Docker Compose Production

> Production-ready multi-container setup with Nginx, health checks, and monitoring

## Maqsad

To'liq production-ready Docker Compose setup: Django + PostgreSQL + Redis + Nginx + Health checks.

---

## Files

```
05-docker-compose-production/
├── docker-compose.prod.yml
├── Dockerfile.prod
├── requirements.txt
├── .env.production
├── nginx/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── ssl/  (optional)
├── scripts/
│   └── entrypoint.sh
└── README.md
```

---

## docker-compose.prod.yml

```yaml
version: '3.8'

services:
  # Django Application (Gunicorn)
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: gunicorn library_project.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 30
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - 8000
    env_file:
      - .env.production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Nginx Reverse Proxy
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    volumes:
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      web:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:

networks:
  app-network:
    driver: bridge
```

---

## Dockerfile.prod

```dockerfile
# ============================================================================
# Stage 1: Builder
# ============================================================================
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ============================================================================
# Stage 2: Runtime
# ============================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

WORKDIR /app

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

COPY --chown=appuser:appuser . .

USER appuser

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "library_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

---

## nginx/Dockerfile

```dockerfile
FROM nginx:1.25-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY nginx.conf /etc/nginx/conf.d/

# Health check
RUN apk add --no-cache curl

EXPOSE 80 443
```

---

## nginx/nginx.conf

```nginx
upstream django {
    server web:8000;
}

# HTTP Server
server {
    listen 80;
    server_name localhost;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    client_max_body_size 10M;
    
    # Static files
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /app/media/;
        expires 7d;
    }
    
    # Health check
    location /health/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Django application
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

# HTTPS Server (optional - add SSL certificates)
# server {
#     listen 443 ssl http2;
#     server_name yourdomain.com;
#     
#     ssl_certificate /etc/nginx/ssl/cert.pem;
#     ssl_certificate_key /etc/nginx/ssl/key.pem;
#     
#     # ... same locations as above
# }
```

---

## .env.production

```bash
# Django Settings
SECRET_KEY=super-secure-production-secret-key-change-this
DEBUG=False
ENVIRONMENT=production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_prod
DB_USER=postgres
DB_PASSWORD=super-secure-database-password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

---

## Usage

### 1. Setup Environment

```bash
# Copy and edit environment file
cp .env.production.example .env.production
nano .env.production
```

### 2. Build Images

```bash
docker-compose -f docker-compose.prod.yml build
```

### 3. Start Services

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Run Migrations

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### 5. Create Superuser

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 6. Check Health

```bash
# All services
docker-compose -f docker-compose.prod.yml ps

# Web health
curl http://localhost/health/

# Database health
docker-compose -f docker-compose.prod.yml exec db pg_isready -U postgres

# Redis health
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

---

## Production Features

### 1. Health Checks ✅

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Benefits:**
- Auto-restart unhealthy containers
- Docker monitors service health
- Zero-downtime deployments

### 2. Service Dependencies ✅

```yaml
depends_on:
  db:
    condition: service_healthy
  redis:
    condition: service_healthy
```

**Benefits:**
- Web starts only after db is ready
- No connection errors on startup

### 3. Restart Policies ✅

```yaml
restart: unless-stopped
```

**Benefits:**
- Auto-restart on failure
- Survives server reboots
- High availability

### 4. Volume Management ✅

```yaml
volumes:
  - static_volume:/app/staticfiles:ro  # Read-only
  - media_volume:/app/media:ro
```

**Benefits:**
- Data persistence
- Shared between containers
- Read-only for nginx (security)

### 5. Nginx Reverse Proxy ✅

**Benefits:**
- Static file serving
- SSL termination
- Load balancing
- Security headers
- Caching

---

## Monitoring

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs

# Specific service
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml logs nginx

# Follow logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Service Status

```bash
docker-compose -f docker-compose.prod.yml ps
```

**Output:**
```
NAME     IMAGE          STATUS                    PORTS
web      prod_web       Up (healthy)              
db       postgres:15    Up (healthy)              
redis    redis:7        Up (healthy)              
nginx    prod_nginx     Up (healthy)     80->80, 443->443
```

### Resource Usage

```bash
docker stats

# Output:
CONTAINER   CPU %   MEM USAGE / LIMIT   MEM %   NET I/O
web         2.5%    150MiB / 2GiB      7.5%    1.2MB / 3.4MB
db          1.2%    80MiB / 2GiB       4.0%    500KB / 1.2MB
redis       0.5%    10MiB / 2GiB       0.5%    200KB / 300KB
nginx       0.8%    15MiB / 2GiB       0.75%   2.1MB / 5.6MB
```

---

## Backup & Restore

### Database Backup

```bash
# Backup
docker-compose -f docker-compose.prod.yml exec db \
  pg_dump -U postgres library_prod > backup.sql

# Or with docker
docker-compose -f docker-compose.prod.yml exec db \
  sh -c 'pg_dump -U postgres library_prod' > backup.sql
```

### Database Restore

```bash
# Restore
docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U postgres library_prod < backup.sql
```

### Volume Backup

```bash
# Backup postgres volume
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz -C /data .

# Backup media files
docker run --rm \
  -v media_volume:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/media-backup.tar.gz -C /data .
```

---

## Scaling

### Scale Web Service

```bash
# Run 3 web instances
docker-compose -f docker-compose.prod.yml up -d --scale web=3
```

**nginx automatically load balances:**
```nginx
upstream django {
    server web:8000;  # All 3 instances
}
```

### Update Configuration

```yaml
# docker-compose.prod.yml
services:
  web:
    deploy:
      replicas: 3
```

---

## SSL/HTTPS Setup

### 1. Get SSL Certificate

```bash
# Using Let's Encrypt (certbot)
certbot certonly --standalone -d yourdomain.com
```

### 2. Update nginx.conf

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # ... rest of config
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 3. Mount SSL Certificates

```yaml
nginx:
  volumes:
    - ./nginx/ssl:/etc/nginx/ssl:ro
```

---

## Zero-Downtime Deployment

### 1. Build New Image

```bash
docker-compose -f docker-compose.prod.yml build web
```

### 2. Rolling Update

```bash
# Scale up
docker-compose -f docker-compose.prod.yml up -d --scale web=2 --no-recreate

# Remove old containers
docker-compose -f docker-compose.prod.yml stop web
docker-compose -f docker-compose.prod.yml rm -f web

# Scale down
docker-compose -f docker-compose.prod.yml up -d --scale web=1
```

---

## Security Checklist

### ✅ 1. Secrets Management
- [ ] .env.production not in Git
- [ ] Strong SECRET_KEY (50+ chars)
- [ ] Strong database password
- [ ] Secure Redis (password)

### ✅ 2. Network Security
- [ ] Internal network for services
- [ ] Only nginx exposes ports
- [ ] No direct database access

### ✅ 3. Container Security
- [ ] Non-root user in containers
- [ ] Read-only volumes where possible
- [ ] No unnecessary privileges

### ✅ 4. Application Security
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configured
- [ ] Security headers (nginx)
- [ ] HTTPS enforced

---

## Troubleshooting

### Problem: Service unhealthy

```bash
# Check health
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs web

# Manual health check
docker-compose -f docker-compose.prod.yml exec web curl http://localhost:8000/health/
```

### Problem: Nginx 502 Bad Gateway

```bash
# Check if web is running
docker-compose -f docker-compose.prod.yml ps web

# Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx

# Test upstream
docker-compose -f docker-compose.prod.yml exec nginx curl http://web:8000
```

### Problem: Static files not loading

```bash
# Check volume
docker volume inspect static_volume

# Re-collect static
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

---

## Performance Tuning

### Gunicorn Workers

```yaml
command: gunicorn --workers 4 --worker-class sync --timeout 30
```

**Formula:** `workers = (2 * CPU_CORES) + 1`

### Nginx Caching

```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Database Connection Pooling

```python
# settings.py
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # 10 minutes
    }
}
```

---

## Summary

**Services:** 4 (Web, PostgreSQL, Redis, Nginx)  
**Health checks:** ✅ All services  
**SSL/HTTPS:** ✅ Ready  
**Scaling:** ✅ Horizontal scaling  
**Monitoring:** ✅ Logs, stats, health  
**Backup:** ✅ Database + volumes  
**Zero-downtime:** ✅ Rolling updates  
**Production ready:** ✅ Yes!  

This is a **complete production setup** ready for deployment!