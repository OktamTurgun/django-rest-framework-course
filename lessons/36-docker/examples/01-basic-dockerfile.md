# Example 01: Basic Dockerfile

> Oddiy Django loyihasi uchun basic Dockerfile

## Maqsad

Eng oddiy Docker setup - minimal configuration bilan Django loyihasini containerize qilish.

---

## Files

```
01-basic-dockerfile/
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── README.md
```

---

## Dockerfile

```dockerfile
# Base image
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

---

## requirements.txt

```
Django>=5.0
djangorestframework>=3.14
python-decouple>=3.8
psycopg2-binary>=2.9
redis>=5.0
```

---

## .dockerignore

```
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

# Git
.git
.gitignore

# Documentation
README.md
docs/
```

---

## Usage

### 1. Build Image

```bash
docker build -t django-basic .
```

**Expected output:**
```
[+] Building 45.2s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 234B
 => [internal] load .dockerignore
 => [1/5] FROM python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/django-basic
```

### 2. Run Container

```bash
docker run -p 8000:8000 django-basic
```

**Expected output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 11, 2025 - 12:00:00
Django version 5.0, using settings 'library_project.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

### 3. Test

```bash
# In another terminal
curl http://localhost:8000/api/books/
```

---

## Environment Variables

```bash
# Pass env variables
docker run -p 8000:8000 \
  -e DEBUG=True \
  -e SECRET_KEY=your-secret-key \
  django-basic
```

**Or with .env file:**
```bash
docker run -p 8000:8000 \
  --env-file .env \
  django-basic
```

---

## Common Commands

```bash
# Build
docker build -t django-basic .

# Run (foreground)
docker run -p 8000:8000 django-basic

# Run (background)
docker run -d -p 8000:8000 django-basic

# Run with name
docker run -d -p 8000:8000 --name my-django django-basic

# View logs
docker logs my-django
docker logs -f my-django  # Follow

# Stop
docker stop my-django

# Start
docker start my-django

# Remove
docker rm my-django

# Shell access
docker exec -it my-django bash

# Django shell
docker exec -it my-django python manage.py shell
```

---

## Inspect

```bash
# View image details
docker inspect django-basic

# View image history (layers)
docker history django-basic

# View container details
docker inspect my-django

# View container stats
docker stats my-django
```

---

## Cleanup

```bash
# Stop and remove container
docker stop my-django
docker rm my-django

# Remove image
docker rmi django-basic

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune
```

---

## Troubleshooting

### Problem 1: Port already in use
```
Error: bind: address already in use
```

**Solution:**
```bash
# Check what's using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Use different port
docker run -p 8001:8000 django-basic
```

### Problem 2: Module not found
```
ModuleNotFoundError: No module named 'rest_framework'
```

**Solution:**
```bash
# Rebuild without cache
docker build --no-cache -t django-basic .
```

### Problem 3: Container exits immediately
```bash
# Check logs
docker logs <container_id>

# Run interactively
docker run -it django-basic bash
```

---

## Advantages ✅

- Simple setup
- Easy to understand
- Quick start
- Good for development

## Limitations ❌

- No optimization
- Large image size
- Runs as root
- Single container
- No persistence

---

## Next Steps

1. ✅ Basic Dockerfile working
2. → [Example 02: Optimized Dockerfile](../02-optimized-dockerfile/)
3. → [Example 03: Multi-stage Build](../03-multi-stage-build/)
4. → [Example 04: Docker Compose](../04-docker-compose-basic/)

---

## Summary

**Image size:** ~400-500 MB  
**Build time:** ~40-60 seconds  
**Complexity:** ⭐ Low  
**Production ready:** ❌ No  

This is a starting point. For production, use optimized Dockerfile with multi-stage builds!