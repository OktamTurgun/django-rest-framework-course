# Homework: Docker

> Lesson 36 bo'yicha amaliy topshiriqlar

## Maqsad

Docker containerization, Docker Compose va production-ready setup bo'yicha amaliy ko'nikmalar hosil qilish.

---

## Topshiriq 1: Basic Dockerfile yaratish ⭐

**Vazifa:** Library project uchun asosiy Dockerfile yaratish

### Talablar:

1. **Dockerfile yaratish**
   - Python 3.11-slim base image
   - Environment variables
   - Dependencies installation
   - Project files copy
   - Port expose
   - Run command

### Namuna:

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Test qilish:

```bash
# Build
docker build -t library-app .

# Run
docker run -p 8000:8000 library-app

# Test
curl http://localhost:8000/api/books/
```

### Baholash mezoni:
- Dockerfile yaratilgan (5 ball)
- Base image to'g'ri (5 ball)
- Environment variables (5 ball)
- Dependencies install (5 ball)
- Project copy (5 ball)
- Port expose (5 ball)
- CMD to'g'ri (5 ball)
- Build successful (5 ball)

**Jami: 40 ball**

---

## Topshiriq 2: .dockerignore yaratish ⭐

**Vazifa:** .dockerignore fayl yaratish va optimizatsiya qilish

### Talablar:

```
# .dockerignore

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
!.env.example

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

# OS
.DS_Store
Thumbs.db
```

### Test qilish:

```bash
# Build va size tekshirish
docker build -t library-app .
docker images library-app

# Container ichini ko'rish
docker run -it library-app ls -la
```

### Baholash mezoni:
- .dockerignore yaratilgan (5 ball)
- Python files excluded (5 ball)
- Django files excluded (5 ball)
- Env files excluded (5 ball)

**Jami: 20 ball**

---

## Topshiriq 3: Docker Compose setup ⭐⭐

**Vazifa:** Multi-container setup (Django + PostgreSQL + Redis)

### Talablar:

**docker-compose.yml:**

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
    networks:
      - app-network

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
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### Test qilish:

```bash
# Build va run
docker-compose build
docker-compose up

# Migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Test API
curl http://localhost:8000/api/books/
```

### Baholash mezoni:
- docker-compose.yml yaratilgan (10 ball)
- Web service configured (10 ball)
- PostgreSQL configured (10 ball)
- Redis configured (5 ball)
- Volumes configured (5 ball)
- Networks configured (5 ball)
- Migrations working (5 ball)

**Jami: 50 ball**

---

## Topshiriq 4: Environment variables (Docker) ⭐⭐

**Vazifa:** Docker uchun environment setup

### Talablar:

1. **.env.docker yaratish:**

```bash
# .env.docker

# Django
SECRET_KEY=docker-secret-key-for-development
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL in Docker)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis (Redis in Docker)
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

2. **docker-compose.yml update:**

```yaml
services:
  web:
    env_file:
      - .env.docker
```

3. **Settings update:**

```python
# settings/development.py
DB_HOST = config('DB_HOST', default='localhost')  # 'db' for Docker
```

### Test qilish:

```bash
docker-compose up
docker-compose exec web python manage.py shell

# Python shell'da:
from django.conf import settings
print(settings.DATABASES)
```

### Baholash mezoni:
- .env.docker yaratilgan (5 ball)
- Database settings (10 ball)
- Redis settings (5 ball)
- docker-compose integration (10 ball)

**Jami: 30 ball**

---

## Topshiriq 5: Optimized Dockerfile ⭐⭐⭐

**Vazifa:** Production-ready optimized Dockerfile

### Talablar:

**Dockerfile.prod:**

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
RUN pip install --no-cache /wheels/*

# Copy project
COPY --chown=appuser:appuser . .

USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "library_project.wsgi:application"]
```

### Qo'shimcha:

**requirements.txt'ga qo'shing:**
```
gunicorn==21.2.0
```

**docker-compose.prod.yml:**

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
      - .env.docker
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env.docker

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:1.25-alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

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

### Test qilish:

```bash
# Build
docker-compose -f docker-compose.prod.yml build

# Run
docker-compose -f docker-compose.prod.yml up

# Test
curl http://localhost/api/books/
```

### Baholash mezoni:
- Multi-stage build (15 ball)
- Non-root user (10 ball)
- Gunicorn configured (10 ball)
- Nginx setup (15 ball)
- Static files served (10 ball)

**Jami: 60 ball**

---

## Topshiriq 6: Docker management commands ⭐⭐

**Vazifa:** Docker utilities va helper scripts

### Talablar:

1. **scripts/docker-setup.sh:**

```bash
#!/bin/bash
# Docker setup script

echo "🐳 Setting up Docker environment..."

# Build images
echo "📦 Building images..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for database
echo "⏳ Waiting for database..."
sleep 5

# Run migrations
echo "🔄 Running migrations..."
docker-compose exec web python manage.py migrate

# Create superuser (optional)
echo "👤 Create superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker-compose exec web python manage.py createsuperuser
fi

echo "✅ Setup complete!"
echo "🌐 Application running at http://localhost:8000"
```

2. **scripts/docker-clean.sh:**

```bash
#!/bin/bash
# Docker cleanup script

echo "🧹 Cleaning Docker environment..."

# Stop containers
echo "⏹ Stopping containers..."
docker-compose down

# Remove volumes (optional)
echo "🗑 Remove volumes? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker-compose down -v
    echo "✅ Volumes removed"
fi

# Remove images (optional)
echo "🗑 Remove images? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker-compose down --rmi all
    echo "✅ Images removed"
fi

echo "✅ Cleanup complete!"
```

3. **Makefile:**

```makefile
.PHONY: build up down logs shell migrate test clean

build:
	docker-compose build

up:
	docker-compose up

up-d:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

bash:
	docker-compose exec web bash

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose exec web python manage.py test

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

clean:
	docker-compose down -v --rmi all
```

### Ishlatish:

```bash
# Setup
bash scripts/docker-setup.sh

# Yoki Makefile
make build
make up-d
make migrate
make createsuperuser

# Cleanup
bash scripts/docker-clean.sh
# yoki
make clean
```

### Baholash mezoni:
- docker-setup.sh (10 ball)
- docker-clean.sh (10 ball)
- Makefile (15 ball)
- Scripts working (15 ball)

**Jami: 50 ball**

---

## Bonus Topshiriq: Health checks ⭐⭐⭐

**Vazifa:** Health checks va monitoring

### Talablar:

1. **Health check endpoint:**

```python
# accounts/views.py (yoki books/views.py)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        cache_status = "healthy" if cache.get('health_check') == 'ok' else "unhealthy"
    except Exception as e:
        cache_status = f"unhealthy: {str(e)}"
    
    status = "healthy" if db_status == "healthy" and cache_status == "healthy" else "unhealthy"
    
    return Response({
        'status': status,
        'database': db_status,
        'cache': cache_status,
    })
```

```python
# urls.py
path('health/', health_check, name='health-check'),
```

2. **docker-compose.yml update:**

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
```

### Test qilish:

```bash
# Health status
docker-compose ps

# Health check endpoint
curl http://localhost:8000/health/
```

### Baholash mezoni:
- Health check endpoint (15 ball)
- Docker health checks (10 ball)
- All checks working (15 ball)

**Jami: 40 ball (Bonus)**

---

## Topshiriqlarni topshirish

### GitHub PR yaratish:

```bash
# Branch yaratish
git checkout -b homework/lesson-36-docker

# Fayllarni qo'shish
git add Dockerfile
git add .dockerignore
git add docker-compose.yml
git add docker-compose.prod.yml
git add Dockerfile.prod
git add nginx/
git add scripts/
git add Makefile

# Commit
git commit -m "Complete Lesson 36 homework: Docker Setup"

# Push
git push origin homework/lesson-36-docker
```

### PR Description:

```markdown
## Lesson 36: Docker - Homework

### Completed Tasks:

- [x] Task 1: Basic Dockerfile (40/40)
- [x] Task 2: .dockerignore (20/20)
- [x] Task 3: Docker Compose (50/50)
- [x] Task 4: Environment variables (30/30)
- [x] Task 5: Optimized Dockerfile (60/60)
- [x] Task 6: Management commands (50/50)
- [ ] Bonus: Health checks (40/40)

### Total Score: 250/250 (+ 40 bonus)

### Screenshots:
- docker-compose up output
- Container list (docker ps)
- API response
- Nginx serving static files

### Notes:
...
```

---

## Baholash jadvali

| Topshiriq | Ball | Status |
|-----------|------|--------|
| Task 1: Basic Dockerfile | 40 | ⭐ |
| Task 2: .dockerignore | 20 | ⭐ |
| Task 3: Docker Compose | 50 | ⭐⭐ |
| Task 4: Environment | 30 | ⭐⭐ |
| Task 5: Optimized | 60 | ⭐⭐⭐ |
| Task 6: Commands | 50 | ⭐⭐ |
| **Jami** | **250** | |
| Bonus: Health checks | 40 | ⭐⭐⭐ |
| **Grand Total** | **290** | |

### Minimal ball: 140 (Task 1-4)
### O'rtacha ball: 200 (Task 1-5)
### A'lo ball: 250+ (Barcha tasklar)

---

## Yordam

Qiyinchilik bo'lsa:
1. [README.md](README.md) qayta o'qing
2. [Examples](examples/) papkasidagi misollarni ko'ring
3. [Docker Documentation](https://docs.docker.com/)
4. GitHub Issues'da savol bering

---

**Omad! Keyingi darsda Deployment o'rganamiz!**