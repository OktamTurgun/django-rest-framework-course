# Lesson 38: CI/CD Pipeline with GitHub Actions 

> Automated Testing, Deployment, and Continuous Integration for Django REST API

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue.svg)](https://github.com/features/actions)
[![Tests](https://img.shields.io/badge/Tests-Automated-green.svg)](.)
[![Deploy](https://img.shields.io/badge/Deploy-Railway-purple.svg)](https://railway.app)

##  Ushbu darsda nima o'rganamiz?

### Asosiy mavzular

-  CI/CD nima va nega kerak?
-  GitHub Actions asoslari
-  Workflow syntax va structure
-  Automated testing pipeline
-  Code quality checks (linting, formatting)
-  Automated deployment (Railway, Heroku)
-  Environment variables va secrets management
-  Multi-environment deployment (staging, production)
-  Notifications va monitoring

### O'rganish natijalari

Ushbu darsdan keyin siz:
-  GitHub Actions workflow yoza olasiz
-  Automated test pipeline sozlay olasiz
-  Code quality checks qo'sha olasiz
-  Auto-deployment setup qila olasiz
-  Secrets va environment variables boshqara olasiz
-  Multi-environment deploy qila olasiz
-  CI/CD best practices'ni bilasiz

---

##  CI/CD nima?

### CI - Continuous Integration

**Ta'rif:** Kod o'zgarishlari avtomatik ravishda test qilinadi va merge qilinadi.

**Jarayon:**
```
Developer commits code
    ↓
GitHub detects changes
    ↓
GitHub Actions runs:
    ├── Install dependencies
    ├── Run tests
    ├── Check code quality
    └── Build project
    ↓
If all pass: ✅ Ready to merge
If fail: ❌ Fix issues
```

**Foydalari:**
-  Xatolar erta topiladi
-  Code quality yaxshi
-  Team collaboration oson
-  Manual testing kerak emas

---

### CD - Continuous Deployment/Delivery

**Ta'rif:** Kod avtomatik ravishda production'ga deploy qilinadi.

**Jarayon:**
```
Code merged to main
    ↓
GitHub Actions runs:
    ├── Run all tests
    ├── Build application
    ├── Deploy to staging
    ├── Run integration tests
    └── Deploy to production
    ↓
✅ Live in production!
```

**Foydalari:**
-  Tez release
-  Manual deployment yo'q
-  Rollback oson
-  Consistent deployments

---

##  GitHub Actions nima?

GitHub Actions - bu GitHub'ning built-in CI/CD service'i.

### Asosiy tushunchalar

#### 1. Workflow

**Ta'rif:** YAML fayl - avtomatik jarayonlarni belgilaydi.

**Location:** `.github/workflows/`

**Example:**
```yaml
name: CI Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest
```

#### 2. Events (Triggers)

**Qachon workflow ishga tushadi:**

```yaml
on:
  push:                    # Har push'da
    branches: [main]       # Faqat main branch
  pull_request:            # PR ochilganda
  schedule:                # Vaqt bo'yicha
    - cron: '0 0 * * *'   # Har kuni 00:00
  workflow_dispatch:       # Manual trigger
```

#### 3. Jobs

**Ta'rif:** Workflow ichidagi alohida vazifalar.

```yaml
jobs:
  test:           # Job 1
    runs-on: ubuntu-latest
    steps: [...]
  
  deploy:         # Job 2
    needs: test   # test'dan keyin
    runs-on: ubuntu-latest
    steps: [...]
```

#### 4. Steps

**Ta'rif:** Job ichidagi individual commands.

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v3
  
  - name: Setup Python
    uses: actions/setup-python@v4
    with:
      python-version: '3.11'
  
  - name: Install dependencies
    run: pip install -r requirements.txt
  
  - name: Run tests
    run: pytest
```

#### 5. Actions

**Ta'rif:** Reusable building blocks.

**Official Actions:**
- `actions/checkout@v3` - Kod checkout
- `actions/setup-python@v4` - Python setup
- `actions/cache@v3` - Dependency caching
- `actions/upload-artifact@v3` - File upload

**Community Actions:**
- `coverallsapp/github-action@v2` - Code coverage
- `codecov/codecov-action@v3` - Coverage report
- `railway/deploy@v1` - Railway deploy

#### 6. Runners

**Ta'rif:** Workflow run qiladigan server.

**GitHub-hosted:**
- `ubuntu-latest` (Linux)
- `windows-latest` (Windows)
- `macos-latest` (macOS)

**Self-hosted:**
- O'zingizning serveringiz

---

##  Project Structure

```
library-project/
├── .github/
│   └── workflows/
│       ├── test.yml                  # Run tests
│       ├── lint.yml                  # Code quality
│       ├── deploy-staging.yml        # Deploy to staging
│       └── deploy-production.yml     # Deploy to production
├── library_project/
├── books/
├── tests/
├── requirements.txt
├── requirements-dev.txt              # Development dependencies
├── pytest.ini                        # Pytest configuration
├── .coveragerc                       # Coverage configuration
└── README.md
```

---

##  Workflow 1: Automated Testing

### test.yml

**Maqsad:** Har push/PR'da testlarni run qilish.

**Location:** `.github/workflows/test.yml`

```yaml
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    env:
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
      DJANGO_SETTINGS_MODULE: library_project.settings.development
      SECRET_KEY: test-secret-key-for-github-actions
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-django pytest-cov
      
      - name: Run migrations
        run: python manage.py migrate --noinput
      
      - name: Run tests
        run: pytest --cov=. --cov-report=xml --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
```

**Nima bo'ladi:**
1.  Code checkout
2.  Python 3.11 setup
3.  PostgreSQL service start
4.  Dependencies install (cached)
5.  Database migrations
6.  Tests run (with coverage)
7.  Coverage report upload

---

##  Workflow 2: Code Quality (Linting)

### lint.yml

**Maqsad:** Code quality checks (Black, Flake8, isort).

**Location:** `.github/workflows/lint.yml`

```yaml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install linting tools
        run: |
          pip install black flake8 isort pylint
      
      - name: Check code formatting with Black
        run: black --check .
      
      - name: Check import sorting with isort
        run: isort --check-only .
      
      - name: Lint with Flake8
        run: flake8 . --max-line-length=88 --extend-ignore=E203,W503
      
      - name: Lint with Pylint
        run: pylint **/*.py --fail-under=8.0 || true
```

**Nima tekshiriladi:**
-  Code formatting (Black)
-  Import sorting (isort)
-  PEP8 compliance (Flake8)
-  Code quality (Pylint)

---

## Workflow 3: Deploy to Railway

### deploy-production.yml

**Maqsad:** Main branch'ga merge bo'lganda auto-deploy.

**Location:** `.github/workflows/deploy-production.yml`

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up --service library-api
      
      - name: Run migrations
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway run python manage.py migrate --noinput
      
      - name: Collect static files
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway run python manage.py collectstatic --noinput
```

**Setup:**

1. **Railway Token olish:**
   ```
   Railway Dashboard → Settings → Tokens → Create Token
   ```

2. **GitHub Secrets'ga qo'shish:**
   ```
   GitHub Repo → Settings → Secrets → New repository secret
   Name: RAILWAY_TOKEN
   Value: [paste token]
   ```

---

##  Workflow 4: Multi-Environment Deployment

### deploy-staging.yml

**Maqsad:** Develop branch → Staging environment.

```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway (Staging)
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_STAGING_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up --service library-api-staging
```

### deploy-production.yml

**Maqsad:** Main branch → Production environment.

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway (Production)
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_PRODUCTION_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up --service library-api-production
```

---

##  Secrets Management

### GitHub Secrets

**Qo'shish:**
```
Repository → Settings → Secrets and variables → Actions → New repository secret
```

**Common secrets:**
```
RAILWAY_TOKEN           # Railway API token
DATABASE_URL            # Production database URL
SECRET_KEY              # Django secret key
SENTRY_DSN              # Sentry error tracking
AWS_ACCESS_KEY_ID       # AWS credentials
AWS_SECRET_ACCESS_KEY   # AWS credentials
```

### Environment-specific secrets

**Staging:**
```
RAILWAY_STAGING_TOKEN
DATABASE_STAGING_URL
```

**Production:**
```
RAILWAY_PRODUCTION_TOKEN
DATABASE_PRODUCTION_URL
```

### Workflow'da ishlatish

```yaml
steps:
  - name: Deploy
    env:
      RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
    run: railway up
```

---

##  Complete CI/CD Pipeline

### Full workflow example

```yaml
name: Complete CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Job 1: Lint
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install black flake8 isort
      - run: black --check .
      - run: flake8 .
      - run: isort --check-only .
  
  # Job 2: Test
  test:
    needs: lint
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pytest pytest-django
      - run: pytest --cov
  
  # Job 3: Deploy (only on main branch)
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install -g @railway/cli
      - env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up
```

**Flow:**
```
Lint → Test → Deploy
  ↓      ↓       ↓
 Pass   Pass   (main only)
  ↓      ↓       ↓
 ✅     ✅      ✅
```

---

##  Best Practices

### 1. Caching Dependencies

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**Foydasi:** 2-3x tezroq builds.

### 2. Matrix Testing

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    django-version: ['4.2', '5.0']

steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
  - run: pip install Django==${{ matrix.django-version }}
```

**Test:** 6 combinations (3 Python × 2 Django).

### 3. Conditional Steps

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: railway up
```

### 4. Fail Fast

```yaml
strategy:
  fail-fast: true  # Stop all jobs if one fails
```

### 5. Timeout

```yaml
jobs:
  test:
    timeout-minutes: 10  # Kill if takes >10 min
```

---

##  Monitoring & Notifications

### GitHub Status Checks

**Branches'da enable qilish:**
```
Settings → Branches → Branch protection rules → Add rule
✓ Require status checks to pass before merging
✓ Require branches to be up to date before merging
Select: lint, test
```

### Slack Notifications

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Email Notifications

GitHub automatically emails on:
- ❌ Workflow failures
- ✅ Fixed workflows

---

##  Troubleshooting

### Common Issues

**1. Tests fail in CI but pass locally**

**Solution:** Environment variables, database differences.
```yaml
env:
  DATABASE_URL: postgresql://...
  DJANGO_SETTINGS_MODULE: project.settings.test
```

**2. Secrets not working**

**Check:**
- Secret name matches exactly
- No extra spaces in secret value
- Secret is in correct repository

**3. Workflow not triggering**

**Check:**
- YAML syntax (use validator)
- File location: `.github/workflows/`
- Branch names match

---

##  Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Railway CLI](https://docs.railway.app/develop/cli)

---

##  Homework

[Homework topshiriqlari](homework.md)

---

##  Keyingi dars

[Lesson 39: WebSockets & Real-time Features](../39-websockets/)

---

**Happy CI/CD! Automate everything!**