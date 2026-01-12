# Lesson 36: Docker

> Django loyihasini Docker container'da ishga tushirish va production'ga deploy qilishga tayyorlash

## Maqsad

Ushbu darsda siz quyidagilarni o'rganasiz:
- Docker nima va nima uchun kerak
- Dockerfile yaratish va optimizatsiya qilish
- Docker Compose bilan multi-container setup
- PostgreSQL va Redis'ni Docker'da ishlatish
- Docker volumes va networks
- Multi-stage builds
- Production-ready Docker setup

## Mundarija

- [Nazariya](#nazariya)
  - [Docker nima?](#docker-nima)
  - [Nega Docker kerak?](#nega-docker-kerak)
  - [Docker asosiy tushunchalari](#docker-asosiy-tushunchalari)
- [Amaliyot](#amaliyot)
  - [Dockerfile](#dockerfile)
  - [Docker Compose](#docker-compose)
  - [Multi-stage builds](#multi-stage-builds)
- [Production Setup](#production-setup)
- [Best Practices](#best-practices)
- [Homework](#homework)

---

## Nazariya

### Docker nima?

**Docker** - bu containerization platform bo'lib, ilovalarni izolatsiya qilingan muhitlarda (containers) ishga tushirish imkonini beradi.

#### Container vs Virtual Machine

```
┌─────────────────────────────┐   ┌─────────────────────────────┐
│      Virtual Machine        │   │         Container           │
├─────────────────────────────┤   ├─────────────────────────────┤
│  App A  │  App B  │  App C  │   │  App A  │  App B  │  App C  │
├─────────┼─────────┼─────────┤   ├─────────┼─────────┼─────────┤
│  Guest  │  Guest  │  Guest  │   │         Docker Engine       │
│   OS    │   OS    │   OS    │   ├─────────────────────────────┤
├─────────────────────────────┤   │         Host OS             │
│       Hypervisor            │   └─────────────────────────────┘
├─────────────────────────────┤   
│         Host OS             │   Lightweight ⚡
└─────────────────────────────┘   Fast startup 🚀
                                  Less resources 💾
Heavy 🐘
Slow startup 🐌
More resources 💻
```

### Nega Docker kerak?

#### 1. **"It works on my machine" muammosini hal qiladi**
```bash
# Developer kompyuterida
Python 3.11, PostgreSQL 15, Redis 7 ✅

# Production serverda
Python 3.9, PostgreSQL 13, Redis 6 ❌

# Docker bilan
Docker image - bir xil muhit hamma joyda ✅
```

#### 2. **Tez deployment**
```bash
# Traditional
- Server setup (soatlab)
- Dependencies install (daqiqalar)
- Configuration (soatlab)

# Docker
- docker-compose up (daqiqalar) 
```

#### 3. **Izolyatsiya**
```bash
# Bir server'da
Project A: Django 4.0, Python 3.9
Project B: Django 5.0, Python 3.11
Project C: Flask 2.0, Python 3.10

# Conflict yo'q! 
```

#### 4. **Scalability**
```bash
# Traffic oshsa
docker-compose scale web=5  # 5 ta instance
```

---

### Docker asosiy tushunchalari

#### 1. **Image** 
Read-only template, loyiha uchun blueprint

```dockerfile
FROM python:3.11-slim
COPY . /app
RUN pip install -r requirements.txt
```

#### 2. **Container** 
Image'dan yaratilgan running instance

```bash
docker run my-django-app
```

#### 3. **Dockerfile** 
Image yaratish uchun instructions

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver"]
```

#### 4. **Docker Compose** 🎼
Multi-container applications uchun orchestration

```yaml
services:
  web:
    build: .
  db:
    image: postgres:15
  redis:
    image: redis:7
```

#### 5. **Volume** 
Data persistence uchun

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

#### 6. **Network** 
Container'lar orasida communication

```yaml
networks:
  app-network:
```

---

## Amaliyot

### Dockerfile

#### Basic Dockerfile

```dockerfile
# Base image
FROM python:3.11-slim

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### Optimized Dockerfile

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "library_project.wsgi:application"]
```

---

### Docker Compose

#### Basic docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=library_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

#### Production docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: gunicorn library_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - 8000
    env_file:
      - .env.production
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env.production
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  nginx:
    build: ./nginx
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  app-network:
    driver: bridge
```

---

### Multi-stage builds

#### Optimizatsiya qilingan Dockerfile (multi-stage)

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create app user
RUN useradd -m -u 1000 appuser && \
    apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy project
COPY --chown=appuser:appuser . .

USER appuser

# Collect static
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "library_project.wsgi:application"]
```

**Afzalliklari:**
-  Kichik image size (400MB → 200MB)
-  Tezroq build
-  Xavfsizroq (build tools production'da yo'q)

---

## Production Setup

### 1. .dockerignore

```
# Git
.git
.gitignore

# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Django
*.log
db.sqlite3
/media/
/staticfiles/

# Environment
.env
.env.*

# IDE
.vscode/
.idea/
*.swp

# Documentation
README.md
docs/

# Tests
tests/
.coverage
htmlcov/
```

### 2. Gunicorn configuration

**gunicorn.conf.py:**

```python
"""Gunicorn configuration"""

bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
```

### 3. Nginx configuration

**nginx/nginx.conf:**

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name localhost;

    client_max_body_size 10M;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

**nginx/Dockerfile:**

```dockerfile
FROM nginx:1.25-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
```

---

## Docker Commands

### Basic Commands

```bash
# Build image
docker build -t my-django-app .

# Run container
docker run -p 8000:8000 my-django-app

# List containers
docker ps
docker ps -a  # Include stopped

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# List images
docker images

# Remove image
docker rmi <image_id>

# Logs
docker logs <container_id>
docker logs -f <container_id>  # Follow

# Execute command
docker exec -it <container_id> bash
docker exec -it <container_id> python manage.py shell
```

### Docker Compose Commands

```bash
# Build services
docker-compose build

# Start services
docker-compose up
docker-compose up -d  # Detached mode

# Stop services
docker-compose down
docker-compose down -v  # Remove volumes

# View logs
docker-compose logs
docker-compose logs -f web  # Follow specific service

# Execute command
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Restart service
docker-compose restart web

# Scale service
docker-compose up -d --scale web=3
```

---

## Best Practices

### 1. **Image size optimization**

```dockerfile
# ❌ YOMON - Katta image
FROM python:3.11
COPY . .
RUN pip install -r requirements.txt

# ✅ YAXSHI - Kichik image
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### 2. **Layer caching**

```dockerfile
# ❌ YOMON - Cache invalidation
COPY . .
RUN pip install -r requirements.txt

# ✅ YAXSHI - Cache reuse
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 3. **Security**

```dockerfile
# ❌ YOMON - Root user
USER root
CMD ["python", "manage.py", "runserver"]

# ✅ YAXSHI - Non-root user
RUN useradd -m appuser
USER appuser
CMD ["gunicorn", "library_project.wsgi:application"]
```

### 4. **Environment variables**

```yaml
# ❌ YOMON - Hardcoded
environment:
  - DEBUG=True
  - SECRET_KEY=hardcoded-key

# ✅ YAXSHI - .env file
env_file:
  - .env
```

### 5. **Health checks**

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## Debugging

### Common Issues

#### 1. Container to'xtab qoladi

```bash
# Logs tekshirish
docker logs <container_id>

# Interactive mode
docker run -it my-app bash
```

#### 2. Database connection failed

```yaml
# depends_on yetarli emas
depends_on:
  - db

# Healthcheck qo'shing
depends_on:
  db:
    condition: service_healthy
```

#### 3. Port already in use

```bash
# Port tekshirish
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Boshqa port ishlatish
docker run -p 8001:8000 my-app
```

---

## Xulosa

### Nimani o'rgandik:

1. Docker asoslari va afzalliklari
2. Dockerfile yaratish va optimizatsiya
3. Docker Compose bilan multi-container setup
4. PostgreSQL va Redis integration
5. Multi-stage builds
6. Production-ready configuration
7. Best practices va debugging

### Keyingi qadamlar:

- [Lesson 37: Deployment](../37-deployment/) - Production deployment
- [Lesson 38: CI/CD](../38-cicd/) - Automated deployment
- [Lesson 39: Kubernetes](../39-kubernetes/) - Container orchestration

---

## Qo'shimcha resurslar

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Django Docker Guide](https://docs.docker.com/samples/django/)

---

## Homework

[Homework topshiriqlari](homework.md) - Docker setup amaliyoti

---

**Keyingi dars:** [37 - Deployment →](../37-deployment/)

**Oldingi dars:** [← 35 - Environment Setup](../35-environment/)

---

<div align="center">

**Happy Dockerizing!** 🐳

Savollar bo'lsa, Issues bo'limida so'rang!

</div>