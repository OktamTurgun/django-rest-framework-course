# Lesson 36: Docker - Examples

> Docker setup examples va patterns

## Misollar ro'yxati

| # | Fayl | Tavsif | Qiyinlik |
|---|------|--------|----------|
| 01 | [basic-dockerfile](01-basic-dockerfile/) | Oddiy Dockerfile | ⭐ |
| 02 | [optimized-dockerfile](02-optimized-dockerfile/) | Optimized Dockerfile | ⭐⭐ |
| 03 | [multi-stage-build](03-multi-stage-build/) | Multi-stage build | ⭐⭐⭐ |
| 04 | [docker-compose-basic](04-docker-compose-basic/) | Basic compose | ⭐⭐ |
| 05 | [docker-compose-production](05-docker-compose-production/) | Production compose | ⭐⭐⭐ |

---

## Qanday ishlatish

### 1. Fayllarni o'qing
Har bir papkada to'liq Docker setup misoli bor.

### 2. Local'da test qiling
```bash
# Example papkasiga o'ting
cd 01-basic-dockerfile

# Build
docker build -t example-01 .

# Run
docker run -p 8000:8000 example-01
```

### 3. O'zgartiring va tajriba qiling
Kodlarni o'zingizga moslashtiring.

---

## Har bir misolda nima bor?

### 01 - Basic Dockerfile ⭐
- Oddiy Dockerfile
- Base image selection
- Dependencies installation
- Basic configuration

### 02 - Optimized Dockerfile ⭐⭐
- Layer caching
- Image size optimization
- .dockerignore usage
- Non-root user

### 03 - Multi-stage Build ⭐⭐⭐
- Builder stage
- Runtime stage
- Size reduction
- Security improvements

### 04 - Docker Compose Basic ⭐⭐
- Multi-container setup
- Django + PostgreSQL + Redis
- Volumes
- Networks

### 05 - Docker Compose Production ⭐⭐⭐
- Production-ready setup
- Nginx reverse proxy
- Health checks
- Restart policies
- Volume management

---

## Quick Start

### Example 1: Basic Setup
```bash
cd 01-basic-dockerfile
docker build -t django-basic .
docker run -p 8000:8000 django-basic
```

### Example 4: Full Stack
```bash
cd 04-docker-compose-basic
docker-compose up
```

### Example 5: Production
```bash
cd 05-docker-compose-production
docker-compose -f docker-compose.prod.yml up
```

---

## Common Commands

```bash
# Build
docker build -t my-app .

# Run
docker run -p 8000:8000 my-app

# Compose
docker-compose up
docker-compose down

# Logs
docker logs <container>
docker-compose logs -f

# Shell
docker exec -it <container> bash
docker-compose exec web bash
```

---

## Tips & Tricks

### 1. Image size comparison
```bash
docker images
```

### 2. Layer inspection
```bash
docker history my-app
```

### 3. Build cache
```bash
docker build --no-cache -t my-app .
```

### 4. Cleanup
```bash
docker system prune -a
docker volume prune
```

---

## Troubleshooting

### Problem: Port already in use
```bash
# Check port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Use different port
docker run -p 8001:8000 my-app
```

### Problem: Build failed
```bash
# Clear cache
docker builder prune

# Rebuild
docker build --no-cache -t my-app .
```

### Problem: Container stops immediately
```bash
# Check logs
docker logs <container_id>

# Run interactively
docker run -it my-app bash
```

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

---

## Next Steps

1. Barcha misollarni sinab ko'ring
2. O'zingizning projektingizda qo'llang
3. [Homework](../homework.md)'ni bajaring
4. Production deployment qiling

---

**Happy Dockerizing!** 🐳