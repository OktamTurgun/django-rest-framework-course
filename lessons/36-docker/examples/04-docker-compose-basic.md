# Example 04: Docker Compose Basic

> Multi-container setup: Django + PostgreSQL + Redis

## Maqsad

Docker Compose yordamida to'liq development environment (web + database + cache) yaratish.

---

## Files

```
04-docker-compose-basic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.docker
├── .dockerignore
└── README.md
```

---

## docker-compose.yml

```yaml
version: '3.8'

services:
  # Django Application
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env.docker
    depends_on:
      - db
      - redis
    networks:
      - app-network
    restart: unless-stopped

  # PostgreSQL Database
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
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## requirements.txt

```
Django>=5.0
djangorestframework>=3.14
python-decouple>=3.8
psycopg2-binary>=2.9
redis>=5.0
django-redis>=5.4
```

---

## .env.docker

```bash
# Django Settings
SECRET_KEY=docker-dev-secret-key-change-in-production
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

---

## Usage

### 1. Start All Services

```bash
docker-compose up
```

**Output:**
```
Creating network "app-network"
Creating volume "postgres_data"
Creating db ... done
Creating redis ... done
Creating web ... done
Attaching to db, redis, web
db      | PostgreSQL init process complete; ready for start up.
redis   | Ready to accept connections
web     | Starting development server at http://0.0.0.0:8000/
```

### 2. Run in Background

```bash
docker-compose up -d
```

### 3. View Logs

```bash
# All services
docker-compose logs

# Follow logs
docker-compose logs -f

# Specific service
docker-compose logs -f web
```

### 4. Check Status

```bash
docker-compose ps
```

**Output:**
```
NAME      IMAGE              STATUS    PORTS
web       app_web            Up        0.0.0.0:8000->8000/tcp
db        postgres:15        Up        0.0.0.0:5432->5432/tcp
redis     redis:7            Up        0.0.0.0:6379->6379/tcp
```

---

## Database Setup

### Run Migrations

```bash
docker-compose exec web python manage.py migrate
```

### Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Access Database

```bash
# Django shell
docker-compose exec web python manage.py shell

# PostgreSQL shell
docker-compose exec db psql -U postgres -d library_db
```

---

## Common Commands

### Service Management

```bash
# Start services
docker-compose up
docker-compose up -d  # Detached

# Stop services
docker-compose stop

# Stop and remove
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart service
docker-compose restart web
```

### Logs

```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs web
```

### Execute Commands

```bash
# Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Shell access
docker-compose exec web bash
docker-compose exec db psql -U postgres
docker-compose exec redis redis-cli
```

### Build

```bash
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Build specific service
docker-compose build web
```

---

## Services Explained

### 1. Web Service (Django)

```yaml
web:
  build: .                    # Build from Dockerfile
  command: ...                # Override CMD
  volumes:                    # Mount code
    - .:/app
  ports:                      # Expose port
    - "8000:8000"
  env_file:                   # Environment variables
    - .env.docker
  depends_on:                 # Wait for dependencies
    - db
    - redis
```

**Key points:**
- Live code reload (volume mount)
- Depends on db and redis
- Uses .env.docker for config

### 2. Database Service (PostgreSQL)

```yaml
db:
  image: postgres:15-alpine   # Official PostgreSQL image
  volumes:                    # Persist data
    - postgres_data:/var/lib/postgresql/data
  environment:                # Database config
    - POSTGRES_DB=library_db
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
```

**Key points:**
- Data persists in volume
- Automatic database creation
- No build needed (uses image)

### 3. Redis Service

```yaml
redis:
  image: redis:7-alpine       # Official Redis image
  ports:
    - "6379:6379"
```

**Key points:**
- Simple cache/broker
- No persistence (default)
- Ready to use

---

## Volumes

### Named Volume (Recommended)

```yaml
volumes:
  postgres_data:              # Named volume
```

**Benefits:**
- Data persists after `docker-compose down`
- Managed by Docker
- Easy backup

### Inspect Volume

```bash
# List volumes
docker volume ls

# Inspect
docker volume inspect postgres_data

# Backup
docker run --rm -v postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/db-backup.tar.gz -C /data .
```

---

## Networks

### Bridge Network

```yaml
networks:
  app-network:
    driver: bridge
```

**How it works:**
- All services on same network
- Services communicate by name
- `web` connects to `db:5432`
- `web` connects to `redis:6379`

### Test Connectivity

```bash
# From web container
docker-compose exec web ping db
docker-compose exec web ping redis

# Check Redis
docker-compose exec web python -c "import redis; r = redis.Redis(host='redis'); print(r.ping())"
```

---

## Development Workflow

### 1. Start Development

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### 2. Code Changes

```bash
# Edit code locally
# Changes reflect immediately (volume mount)

# View logs
docker-compose logs -f web
```

### 3. Database Changes

```bash
# Make migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate
```

### 4. Add Dependencies

```bash
# Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# Rebuild
docker-compose build web
docker-compose up -d
```

### 5. Reset Database

```bash
# Stop and remove volumes
docker-compose down -v

# Start fresh
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate
```

---

## Testing

### Run Tests

```bash
docker-compose exec web python manage.py test
```

### Test with Coverage

```bash
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

---

## Debugging

### View Container Logs

```bash
# All services
docker-compose logs

# Web only
docker-compose logs web

# Follow
docker-compose logs -f web
```

### Access Shell

```bash
# Django shell
docker-compose exec web python manage.py shell

# Bash
docker-compose exec web bash

# Database
docker-compose exec db psql -U postgres -d library_db
```

### Check Environment

```bash
docker-compose exec web env | grep DB
docker-compose exec web python -c "from django.conf import settings; print(settings.DATABASES)"
```

---

## Troubleshooting

### Problem 1: Port already in use

```bash
# Error: port is already allocated

# Solution: Change port
ports:
  - "8001:8000"  # Use 8001 instead
```

### Problem 2: Database connection failed

```bash
# Error: could not connect to server

# Check if db is running
docker-compose ps

# Check logs
docker-compose logs db

# Restart
docker-compose restart db
```

### Problem 3: Volume permission denied

```bash
# Error: permission denied

# Fix permissions
docker-compose exec web chown -R appuser:appuser /app
```

---

## Clean Up

```bash
# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Remove everything
docker-compose down -v --rmi all --remove-orphans
```

---

## Advantages ✅

- Complete development environment
- Easy setup (one command)
- Service isolation
- Data persistence
- Hot reload
- Consistent environment

---

## Next Steps

1. ✅ Basic Dockerfile
2. ✅ Optimized Dockerfile
3. ✅ Multi-stage Build
4. ✅ Docker Compose Basic
5. → [Example 05: Production Compose](../05-docker-compose-production/) (with Nginx)

---

## Summary

**Services:** 3 (Web, PostgreSQL, Redis)  
**Commands:** `docker-compose up` (that's it!)  
**Data persistence:** ✅ PostgreSQL volume  
**Hot reload:** ✅ Code changes reflect immediately  
**Production ready:** ⚠️ Development only  
**Complexity:** ⭐⭐ Medium  

Perfect for development! For production, see Example 05.