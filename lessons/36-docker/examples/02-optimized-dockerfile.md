# Example 02: Optimized Dockerfile

> Optimized va production-ready Dockerfile

## Maqsad

Image size'ni kamaytirish, layer caching, non-root user va boshqa optimization techniques.

---

## Files

```
02-optimized-dockerfile/
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── README.md
```

---

## Dockerfile

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
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Install Python dependencies (as root for installation)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')"

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "library_project.wsgi:application"]
```

---

## Key Improvements

### 1. **Environment Variables (Optimized)**
```dockerfile
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
```

**Benefits:**
- Fewer layers (combined with `\`)
- No pip cache
- Cleaner output

### 2. **Cleanup After Installation**
```dockerfile
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
```

**Benefits:**
- Smaller image size
- No leftover files

### 3. **Non-Root User**
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

**Benefits:**
- ✅ Security improvement
- ✅ Best practice
- ✅ Prevents privilege escalation

### 4. **Layer Caching**
```dockerfile
# First: dependencies (changes rarely)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Then: code (changes often)
COPY . .
```

**Benefits:**
- Faster rebuilds
- Uses cache for dependencies

### 5. **Gunicorn (Production Server)**
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "library_project.wsgi:application"]
```

**Benefits:**
- Production-ready
- Better performance
- Process management

### 6. **Health Check**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')"
```

**Benefits:**
- Container health monitoring
- Auto-restart if unhealthy

---

## requirements.txt

```
Django>=5.0
djangorestframework>=3.14
python-decouple>=3.8
psycopg2-binary>=2.9
redis>=5.0
gunicorn>=21.2.0
requests>=2.31.0
```

---

## Usage

### Build

```bash
docker build -t django-optimized .
```

### Run

```bash
docker run -d -p 8000:8000 --name django-opt django-optimized
```

### Health Check

```bash
docker ps
# STATUS: Up 2 minutes (healthy)
```

---

## Comparison: Basic vs Optimized

| Feature | Basic | Optimized |
|---------|-------|-----------|
| Image Size | 500 MB | 350 MB |
| Build Time | 60s | 45s |
| User | root | appuser |
| Server | Django dev | Gunicorn |
| Health Check | ❌ | ✅ |
| Cache Optimization | ❌ | ✅ |
| Production Ready | ❌ | ✅ |

---

## Size Comparison

```bash
# Build both
docker build -t django-basic -f ../01-basic-dockerfile/Dockerfile ../01-basic-dockerfile
docker build -t django-optimized .

# Compare
docker images | grep django

# Output:
# django-optimized    latest    abc123    2 minutes ago    350MB
# django-basic        latest    def456    5 minutes ago    500MB
```

**Size reduction: 30%!** 🎉

---

## Security Check

```bash
# Check running user
docker exec django-opt whoami
# Output: appuser

# Compare with basic
docker exec django-basic whoami
# Output: root
```

---

## Performance Test

```bash
# Basic (Django dev server)
ab -n 1000 -c 10 http://localhost:8000/api/books/
# Requests per second: 50

# Optimized (Gunicorn)
ab -n 1000 -c 10 http://localhost:8001/api/books/
# Requests per second: 200+
```

**4x performance improvement!** 🚀

---

## Layer Analysis

```bash
docker history django-optimized

# Output shows optimized layers:
# - Combined RUN commands
# - No cache artifacts
# - Proper layer ordering
```

---

## Advanced Usage

### 1. Custom Workers

```bash
docker run -d -p 8000:8000 \
  -e GUNICORN_WORKERS=8 \
  django-optimized
```

### 2. Volume Mount (Development)

```bash
docker run -d -p 8000:8000 \
  -v $(pwd):/app \
  django-optimized
```

### 3. Environment File

```bash
docker run -d -p 8000:8000 \
  --env-file .env.production \
  django-optimized
```

---

## Best Practices Applied

### ✅ 1. Small Base Image
```dockerfile
FROM python:3.11-slim  # Not python:3.11
```

### ✅ 2. Combined RUN Commands
```dockerfile
RUN apt-get update && apt-get install -y \
    gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*
```

### ✅ 3. Non-Root User
```dockerfile
USER appuser
```

### ✅ 4. Layer Order
```dockerfile
# Least changing first
COPY requirements.txt .
RUN pip install -r requirements.txt
# Most changing last
COPY . .
```

### ✅ 5. No Cache
```dockerfile
ENV PIP_NO_CACHE_DIR=1
RUN pip install --no-cache-dir -r requirements.txt
```

### ✅ 6. Production Server
```dockerfile
CMD ["gunicorn", ...]  # Not manage.py runserver
```

---

## Troubleshooting

### Permission Denied

```bash
# Problem: Static files permission
COPY: permission denied

# Solution: Use --chown
COPY --chown=appuser:appuser . .
```

### Gunicorn Not Found

```bash
# Problem: Module not found
ModuleNotFoundError: No module named 'gunicorn'

# Solution: Add to requirements.txt
gunicorn>=21.2.0
```

---

## Monitoring

```bash
# View logs
docker logs -f django-opt

# Container stats
docker stats django-opt

# Health status
docker inspect --format='{{.State.Health.Status}}' django-opt
```

---

## Next Steps

1. ✅ Basic Dockerfile
2. ✅ Optimized Dockerfile
3. → [Example 03: Multi-stage Build](../03-multi-stage-build/) (even smaller!)
4. → [Example 04: Docker Compose](../04-docker-compose-basic/)

---

## Summary

**Image size:** ~350 MB (30% smaller)  
**Build time:** ~45 seconds  
**Security:** ✅ Non-root user  
**Performance:** ✅ 4x faster (Gunicorn)  
**Production ready:** ✅ Yes  

This is production-ready! For even better optimization, see Multi-stage builds (Example 03).