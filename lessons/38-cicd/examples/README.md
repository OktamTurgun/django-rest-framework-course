# Lesson 38: CI/CD Examples

GitHub Actions workflow examples for Django REST API.

## Examples ro'yxati

### 1. Basic Test Workflow
**File:** `01-basic-test-workflow.yml`

Eng oddiy test workflow - har push'da testlarni run qiladi.

**Features:**
- Checkout code
- Setup Python
- Install dependencies
- Run pytest

**Use case:** Birinchi CI/CD workflow

---

### 2. Lint and Format
**File:** `02-lint-and-format.yml`

Code quality checks - Black, Flake8, isort.

**Features:**
- Black formatting check
- Flake8 linting
- isort import sorting
- Multiple Python versions

**Use case:** Code quality enforcement

---

### 3. Test with PostgreSQL
**File:** `03-test-with-postgres.yml`

PostgreSQL service bilan testing.

**Features:**
- PostgreSQL service container
- Health checks
- Database migrations
- Full integration tests

**Use case:** Production-like testing

---

### 4. Deploy to Railway
**File:** `04-deploy-to-railway.yml`

Automated deployment to Railway.

**Features:**
- Railway CLI installation
- Secret management
- Migration running
- Static files collection

**Use case:** Production deployment

---

### 5. Multi-Environment Deploy
**File:** `05-multi-environment.yml`

Staging va Production deployment.

**Features:**
- Environment-based deployment
- Branch-specific triggers
- Separate secrets per environment
- Approval workflows

**Use case:** Professional deployment strategy

---

### 6. Complete CI/CD Pipeline
**File:** `06-complete-pipeline.yml`

Full-featured pipeline - all best practices.

**Features:**
- Linting
- Testing with coverage
- Security scanning
- Multi-environment deployment
- Notifications
- Dependency caching

**Use case:** Production-ready pipeline

---

## Qanday ishlatish

### 1. Workflow faylni tanlash

```bash
# Example: Basic test workflow
cp examples/01-basic-test-workflow.yml .github/workflows/test.yml
```

### 2. Customize qilish

Workflow faylni ochib, quyidagilarni o'zgartiring:

```yaml
# Branch names
branches: [main, develop]  # Your branches

# Python version
python-version: '3.11'     # Your version

# Service name (Railway)
railway up --service your-service-name
```

### 3. Secrets sozlash

GitHub repository'da:

```
Settings → Secrets and variables → Actions → New repository secret
```

**Kerakli secrets:**
- `RAILWAY_TOKEN` - Railway API token
- `CODECOV_TOKEN` - Codecov token (optional)
- `SLACK_WEBHOOK` - Slack webhook (optional)

### 4. Commit va push

```bash
git add .github/workflows/
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### 5. GitHub Actions'da ko'rish

```
Repository → Actions tab → Latest workflow run
```

---

## Workflow Comparison

| Feature | Basic | Lint | PostgreSQL | Railway | Multi-Env | Complete |
|---------|-------|------|------------|---------|-----------|----------|
| Run Tests | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Linting | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| PostgreSQL | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Coverage | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Deployment | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Environments | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Caching | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Notifications | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Learning Path

### Beginner (Kun 1-2)

1. **01-basic-test-workflow.yml** (30 min)
   - Workflow syntax o'rganish
   - GitHub Actions interface
   - Logs o'qish

2. **02-lint-and-format.yml** (30 min)
   - Code quality tools
   - Multiple checks
   - Fail conditions

### Intermediate (Kun 3-4)

3. **03-test-with-postgres.yml** (1 soat)
   - Services in GitHub Actions
   - Database setup
   - Environment variables

4. **04-deploy-to-railway.yml** (1 soat)
   - Deployment automation
   - Secrets management
   - Railway CLI

### Advanced (Kun 5-6)

5. **05-multi-environment.yml** (2 soat)
   - Environment strategies
   - Branch protection
   - Approval workflows

6. **06-complete-pipeline.yml** (2 soat)
   - All features combined
   - Best practices
   - Production-ready

---

## Customization Guide

### Python version o'zgartirish

```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.9'  # Change here
```

### Branch'larni o'zgartirish

```yaml
on:
  push:
    branches: [master, dev]  # Your branches
```

### PostgreSQL version

```yaml
services:
  postgres:
    image: postgres:14  # Change version
```

### Railway service name

```yaml
run: railway up --service my-api  # Your service
```

---

## Troubleshooting

### Tests fail in CI

**Check:**
1. Environment variables set correctly
2. Database URL matches PostgreSQL service
3. Python version matches local
4. Dependencies installed completely

**Solution:**
```yaml
env:
  DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
  DJANGO_SETTINGS_MODULE: project.settings.test
```

---

### Deployment fails

**Check:**
1. RAILWAY_TOKEN secret exists
2. Service name is correct
3. Railway CLI installs successfully

**Debug:**
```yaml
- name: Debug Railway
  run: |
    railway whoami
    railway status
```

---

### Secrets not working

**Check:**
1. Secret name exactly matches
2. No spaces in secret value
3. Secret in correct environment

**Test:**
```yaml
- name: Test secret
  env:
    TOKEN: ${{ secrets.RAILWAY_TOKEN }}
  run: |
    if [ -z "$TOKEN" ]; then
      echo "Secret not set!"
      exit 1
    fi
```

---

## Workflow Triggers

### Push to specific branches

```yaml
on:
  push:
    branches: [main, develop]
```

### Pull Request

```yaml
on:
  pull_request:
    branches: [main]
```

### Scheduled (Cron)

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
```

### Manual trigger

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
```

### Multiple triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

---

## Best Practices

### 1. Use caching

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**Benefit:** 2-3x faster builds

### 2. Fail fast

```yaml
strategy:
  fail-fast: true
```

**Benefit:** Save CI minutes

### 3. Conditional steps

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: railway up
```

**Benefit:** Prevent accidental deploys

### 4. Timeouts

```yaml
jobs:
  test:
    timeout-minutes: 10
```

**Benefit:** Don't waste CI time on hung jobs

### 5. Concurrency control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Benefit:** Cancel old runs when new one starts

---

## Advanced Features

### Matrix builds

```yaml
strategy:
  matrix:
    python: ['3.9', '3.10', '3.11']
    django: ['4.2', '5.0']
```

### Artifacts upload

```yaml
- uses: actions/upload-artifact@v3
  with:
    name: coverage-report
    path: htmlcov/
```

### Output variables

```yaml
- id: test
  run: echo "::set-output name=status::passed"

- run: echo "Test status: ${{ steps.test.outputs.status }}"
```

---

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Railway Docs](https://docs.railway.app/)
- [YAML Validator](https://www.yamllint.com/)

---

## Notes

- All examples use **PostgreSQL 15** (latest stable)
- Python **3.11** (recommended)
- Django **5.0+** compatible
- Railway CLI **latest** version
- Ubuntu **latest** runner

---

**Happy automating!**