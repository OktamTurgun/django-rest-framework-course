# Example 03: Multi-stage Build

> Multi-stage Dockerfile - eng kichik va eng xavfsiz image

## Maqsad

Builder va runtime stage'larni ajratish orqali image size'ni maksimal darajada kamaytirish va xavfsizlikni oshirish.

---

## Files

```
03-multi-stage-build/
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── README.md
```

---

## Dockerfile

```dockerfile
# ============================================================================
# Stage 1: Builder
# ============================================================================
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies as wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ============================================================================
# Stage 2: Runtime
# ============================================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

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
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run with gunicorn
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "library_project.wsgi:application"]
```

---

## How Multi-stage Works

### Stage 1: Builder (Build environment)

```dockerfile
FROM python:3.11-slim as builder

# Install build tools
RUN apt-get install -y gcc g++ make

# Build Python packages as wheels
RUN pip wheel --wheel-dir /app/wheels -r requirements.txt
```

**Purpose:**
- Install build tools (gcc, g++, make)
- Compile Python packages
- Create wheel files
- **This stage is discarded in final image!**

### Stage 2: Runtime (Production environment)

```dockerfile
FROM python:3.11-slim

# Copy ONLY wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install /wheels/*
```

**Purpose:**
- Minimal runtime dependencies
- Install pre-built wheels
- No build tools
- Much smaller image

---

## Visual Representation

```
┌─────────────────────────────────────┐
│     Stage 1: Builder (500MB)       │
├─────────────────────────────────────┤
│  - Python 3.11-slim                │
│  - gcc, g++, make (100MB)          │
│  - Build dependencies              │
│  - Compile packages                │
│  - Create wheels                   │
└──────────────┬──────────────────────┘
               │
               │ COPY --from=builder
               │ (Only wheels, ~50MB)
               ▼
┌─────────────────────────────────────┐
│    Stage 2: Runtime (250MB)        │
├─────────────────────────────────────┤
│  - Python 3.11-slim                │
│  - Runtime dependencies only       │
│  - Pre-built wheels                │
│  - Application code                │
│  - NO build tools                  │
└─────────────────────────────────────┘
         Final Image: 250MB
    (50% smaller than optimized!)
```

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
docker build -t django-multistage .
```

**Build process:**
```
Step 1/15 : FROM python:3.11-slim as builder
Step 2/15 : WORKDIR /app
Step 3/15 : RUN apt-get update...
Step 4/15 : RUN pip wheel...
Step 5/15 : FROM python:3.11-slim       ← New stage!
Step 6/15 : COPY --from=builder...      ← Copy from builder
...
Successfully built abc123
```

### Run

```bash
docker run -d -p 8000:8000 --name django-multi django-multistage
```

---

## Size Comparison

```bash
# Build all three versions
docker build -t django-basic -f ../01-basic-dockerfile/Dockerfile ../01-basic-dockerfile
docker build -t django-optimized -f ../02-optimized-dockerfile/Dockerfile ../02-optimized-dockerfile
docker build -t django-multistage .

# Compare sizes
docker images | grep django

# Output:
# django-multistage   latest    abc123    250MB  ← Smallest!
# django-optimized    latest    def456    350MB
# django-basic        latest    ghi789    500MB
```

**Results:**
- Basic → Multi-stage: **50% reduction** 🎉
- Optimized → Multi-stage: **28% reduction** 🎉

---

## Security Benefits

### What's NOT in final image:

```bash
# Builder stage has:
❌ gcc, g++, make (build tools)
❌ Development headers
❌ Compilation artifacts

# Runtime stage has:
✅ Only runtime libraries
✅ Pre-compiled packages
✅ Application code
```

### Security scan:

```bash
# Scan for vulnerabilities
docker scan django-multistage

# Fewer vulnerabilities because:
# - No build tools
# - Smaller attack surface
# - Minimal dependencies
```

---

## Build Time Comparison

```bash
# First build (no cache)
docker build --no-cache -t django-multistage .
# Time: 120 seconds

# Rebuild with code change (cache hit on builder stage)
docker build -t django-multistage .
# Time: 15 seconds

# Rebuild with dependency change (cache miss)
docker build -t django-multistage .
# Time: 90 seconds
```

**Cache efficiency:** 87% faster on code changes! 🚀

---

## Advanced: Inspect Stages

```bash
# Build and inspect builder stage
docker build --target builder -t django-builder .

# Compare sizes
docker images | grep django
# django-builder      latest    500MB  (builder stage)
# django-multistage   latest    250MB  (final image)

# What's in builder
docker run -it django-builder bash
$ which gcc  # /usr/bin/gcc
$ which g++  # /usr/bin/g++

# What's in runtime
docker run -it django-multistage bash
$ which gcc  # (not found) ✅
```

---

## Production Configuration

### With environment variables:

```bash
docker run -d -p 8000:8000 \
  -e GUNICORN_WORKERS=8 \
  -e GUNICORN_TIMEOUT=60 \
  --name django-prod \
  django-multistage
```

### With custom gunicorn config:

```dockerfile
# Add to Dockerfile
COPY gunicorn.conf.py /app/

CMD ["gunicorn", \
     "--config", "gunicorn.conf.py", \
     "library_project.wsgi:application"]
```

---

## Layer Analysis

```bash
docker history django-multistage

# Only shows FINAL stage layers:
IMAGE          CREATED BY                                      SIZE
abc123         CMD ["gunicorn"...]                            0B
abc123         HEALTHCHECK {...}                              0B
abc123         EXPOSE 8000                                    0B
abc123         RUN python manage.py collectstatic...          5MB
abc123         COPY . . # buildkit                            10MB
abc123         RUN pip install /wheels/*                      45MB
abc123         COPY --from=builder /app/wheels /wheels        50MB
abc123         RUN useradd...                                 1MB
abc123         RUN apt-get update...                          20MB
abc123         FROM python:3.11-slim                          120MB
```

**Total: 250MB** (No builder stage layers!)

---

## Best Practices Applied

### ✅ 1. Separate Build and Runtime

```dockerfile
FROM python:3.11-slim as builder  # Build stage
FROM python:3.11-slim             # Runtime stage
```

### ✅ 2. Copy Only Necessary Files

```dockerfile
COPY --from=builder /app/wheels /wheels  # Only wheels, not source
```

### ✅ 3. Minimal Runtime Dependencies

```dockerfile
# Builder: gcc, g++, make (100MB)
# Runtime: libpq5 only (5MB)
```

### ✅ 4. Security Hardening

```dockerfile
# No build tools in production
# Non-root user
# Health checks
```

### ✅ 5. Cache Optimization

```dockerfile
# Dependencies first (rare changes)
COPY requirements.txt .
RUN pip wheel...

# Code last (frequent changes)
COPY . .
```

---

## Troubleshooting

### Problem: Wheel not found

```bash
# Error: No matching distribution found

# Solution: Check COPY command
COPY --from=builder /app/wheels /wheels  # Correct path
```

### Problem: Missing runtime library

```bash
# Error: libpq.so.5: cannot open shared object

# Solution: Install runtime library
RUN apt-get install -y libpq5
```

---

## Comparison Table

| Feature | Basic | Optimized | Multi-stage |
|---------|-------|-----------|-------------|
| Image Size | 500 MB | 350 MB | 250 MB ✅ |
| Build Time (first) | 60s | 45s | 120s |
| Build Time (cached) | 60s | 30s | 15s ✅ |
| Build Tools | ✅ | ✅ | ❌ ✅ |
| Security | ❌ | ⚠️ | ✅ ✅ |
| Production Ready | ❌ | ✅ | ✅ ✅ |
| Complexity | ⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## Real-world Impact

### Deployment Time

```bash
# 500MB image → 250MB image
# Upload time: 10 minutes → 5 minutes
# Download time: 5 minutes → 2.5 minutes

# Total deployment time reduction: 50% 🎉
```

### Storage Costs

```bash
# 10 images × 500MB = 5GB
# 10 images × 250MB = 2.5GB

# Storage savings: 50% 💰
```

---

## Next Steps

1. ✅ Basic Dockerfile
2. ✅ Optimized Dockerfile
3. ✅ Multi-stage Build (smallest image!)
4. → [Example 04: Docker Compose](../04-docker-compose-basic/)
5. → [Example 05: Production Compose](../05-docker-compose-production/)

---

## Summary

**Image size:** ~250 MB (50% smaller than basic) ⭐⭐⭐  
**Build time:** 15s (cached) 🚀  
**Security:** ✅ No build tools in production  
**Production ready:** ✅ Yes  
**Recommended:** ✅ Best choice for production!  

This is the **recommended approach** for production Django applications!