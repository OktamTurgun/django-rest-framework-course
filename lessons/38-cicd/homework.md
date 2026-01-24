# Homework: CI/CD Pipeline with GitHub Actions

## Umumiy ko'rsatmalar

- Barcha topshiriqlarni tartib bilan bajaring
- Har bir workflow'ni alohida test qiling
- GitHub Actions logs'ni screenshot qiling
- Secrets to'g'ri sozlanganini tekshiring
- Workflow fayllari `.github/workflows/` da bo'lishi kerak
- YAML syntax to'g'ri ekanligini validator bilan tekshiring

## Baholash tizimi

- **Level 1:**  (Beginner)
- **Level 2:**  (Intermediate)
- **Level 3:**  (Advanced)
- **Level 4:**  (Expert)
- **Bonus:**  (Master)

---

## Level 1: Basic CI/CD (Beginner)

### Task 1.1: Basic Test Workflow

**Maqsad:** Har push'da testlarni avtomatik run qilish.

**Fayl:** `.github/workflows/test.yml`

```yaml
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-django
      
      - name: Run tests
        run: pytest
```

**Topshiriq:**
1. `.github/workflows/` folder yarating
2. `test.yml` faylni yarating
3. Yuqoridagi kodni yozing
4. Git commit va push qiling
5. GitHub'da "Actions" tab'ni oching
6. Workflow running holatini ko'ring

**Tekshirish:**
- [ ] Workflow created
- [ ] Tests run successfully
- [ ] Green checkmark on GitHub
- [ ] Screenshot of successful run

---

### Task 1.2: Code Formatting Check

**Maqsad:** Black formatter bilan code formatting tekshirish.

**Fayl:** `.github/workflows/format.yml`

```yaml
name: Check Code Format

on: [push, pull_request]

jobs:
  format:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Black
        run: pip install black
      
      - name: Check formatting
        run: black --check .
```

**Topshiriq:**
1. Local'da code'ni format qiling: `black .`
2. Workflow faylni yarating
3. Push qiling
4. Workflow muvaffaqiyatli o'tishini tekshiring

**Tekshirish:**
- [ ] Black installed locally
- [ ] Code formatted before push
- [ ] Workflow passes
- [ ] No formatting errors

---

### Task 1.3: Workflow Badge qo'shish

**Maqsad:** README.md'ga workflow status badge qo'shish.

**README.md'ga qo'shing:**

```markdown
# Library API

[![Tests](https://github.com/username/repo/actions/workflows/test.yml/badge.svg)](https://github.com/username/repo/actions/workflows/test.yml)

Your project description...
```

**Topshiriq:**
1. GitHub'da: Actions → Workflow → "..." → "Create status badge"
2. Badge markdown'ni copy qiling
3. README.md'ga qo'shing
4. Commit va push

**Tekshirish:**
- [ ] Badge visible in README
- [ ] Badge shows "passing" status
- [ ] Clicking badge opens workflow page

---

## Level 2: PostgreSQL & Coverage (Intermediate)

### Task 2.1: PostgreSQL Service (10 ball)

**Maqsad:** GitHub Actions'da PostgreSQL bilan test qilish.

**Fayl:** `.github/workflows/test-postgres.yml`

```yaml
name: Test with PostgreSQL

on: [push, pull_request]

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
      DJANGO_SETTINGS_MODULE: library_project.settings.test
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - run: pip install -r requirements.txt pytest pytest-django psycopg2-binary
      
      - name: Run migrations
        run: python manage.py migrate --noinput
      
      - name: Run tests
        run: pytest
```

**Topshiriq:**
1. Test settings yarating (SQLite o'rniga PostgreSQL)
2. Workflow'ni yarating
3. Local'da tests pass bo'lishini tekshiring
4. GitHub'da workflow run qiling

**Tekshirish:**
- [ ] PostgreSQL service starts
- [ ] Migrations run successfully
- [ ] All tests pass with PostgreSQL
- [ ] No database connection errors

---

### Task 2.2: Code Coverage Report

**Maqsad:** Test coverage o'lchash va report qilish.

**test.yml ni yangilash:**

```yaml
- name: Install coverage
  run: pip install pytest-cov

- name: Run tests with coverage
  run: pytest --cov=. --cov-report=xml --cov-report=term

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    fail_ci_if_error: false
```

**Topshiriq:**
1. Codecov.io'da account yarating
2. Repository connect qiling
3. Coverage workflow qo'shing
4. Coverage badge README.md'ga qo'shing

**Tekshirish:**
- [ ] Coverage measured
- [ ] Report uploaded to Codecov
- [ ] Coverage badge visible
- [ ] Coverage > 70%

---

### Task 2.3: Dependency Caching

**Maqsad:** Pip dependencies cache qilish (tezroq builds).

**Cache qo'shish:**

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Install dependencies
  run: pip install -r requirements.txt
```

**Topshiriq:**
1. Test workflow'ga cache qo'shing
2. Birinchi run: cache miss (sekin)
3. Ikkinchi run: cache hit (tez)
4. Build time'ni taqqoslang

**Tekshirish:**
- [ ] Cache configured
- [ ] First run creates cache
- [ ] Second run uses cache
- [ ] Build time reduced by 30-50%

---

## Level 3: Linting & Deployment (Advanced)

### Task 3.1: Multi-tool Linting (10 ball)

**Maqsad:** Black, Flake8, isort bilan code quality tekshirish.

**Fayl:** `.github/workflows/lint.yml`

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install linting tools
        run: pip install black flake8 isort
      
      - name: Check formatting (Black)
        run: black --check .
      
      - name: Check import sorting (isort)
        run: isort --check-only .
      
      - name: Lint with Flake8
        run: flake8 . --max-line-length=88 --extend-ignore=E203,W503
```

**Topshiriq:**
1. Local'da code format qiling
2. Pre-commit hook sozlang (optional)
3. Lint workflow yarating
4. Barcha check'lar pass bo'lishini ta'minlang

**Configuration files:**

**setup.cfg:**
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    migrations,
    venv

[isort]
profile = black
line_length = 88
```

**Tekshirish:**
- [ ] All linting tools pass
- [ ] Configuration files created
- [ ] No linting errors
- [ ] Consistent code style

---

### Task 3.2: Railway Auto-Deploy 

**Maqsad:** Main branch'ga merge bo'lganda auto-deploy.

**Fayl:** `.github/workflows/deploy.yml`

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
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
```

**Setup:**

1. **Railway Token:**
   - Railway Dashboard → Settings → Tokens
   - Create token, copy value

2. **GitHub Secret:**
   - Repo → Settings → Secrets → New secret
   - Name: `RAILWAY_TOKEN`
   - Value: [paste token]

3. **Test:**
   - Commit to develop → Push
   - Merge PR to main
   - Watch deployment in Actions

**Tekshirish:**
- [ ] Railway token created
- [ ] GitHub secret configured
- [ ] Workflow triggers on main push
- [ ] Deployment successful
- [ ] Migrations run automatically
- [ ] Production site updated

---

## Level 4: Advanced Pipeline (Expert)

### Task 4.1: Matrix Testing

**Maqsad:** Bir necha Python va Django versiyalarda test qilish.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
        django-version: ['4.2', '5.0']
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install Django
        run: pip install Django==${{ matrix.django-version }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
```

**Topshiriq:**
1. Matrix strategy qo'shing
2. 6 ta combination test qiling (3 Python × 2 Django)
3. Barcha combination'lar pass bo'lishini ta'minlang

**Tekshirish:**
- [ ] 6 jobs run in parallel
- [ ] All combinations pass
- [ ] Matrix displayed on GitHub

---

### Task 4.2: Multi-Environment Deploy

**Maqsad:** Staging va Production environment'larga deploy.

**Staging workflow:**

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
      
      - name: Deploy to Staging
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_STAGING_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up --service library-api-staging
```

**Production workflow:**

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
      
      - name: Deploy to Production
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_PRODUCTION_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up --service library-api-production
```

**Setup:**

1. **Railway:** 2 ta service yarating (staging, production)
2. **GitHub Environments:**
   - Settings → Environments → New environment
   - Create: `staging`, `production`
3. **Secrets:** Har bir environment uchun alohida token

**Tekshirish:**
- [ ] 2 Railway services created
- [ ] 2 GitHub environments configured
- [ ] Staging deploys from develop
- [ ] Production deploys from main
- [ ] Separate tokens for each environment

---

## Bonus Tasks 

### Bonus 1: Security Scanning

**Maqsad:** Dependency vulnerabilities scan qilish.

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Safety check
        run: |
          pip install safety
          safety check --json
      
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r . -f json
```

**Tekshirish:**
- [ ] Safety checks dependencies
- [ ] Bandit scans code
- [ ] Vulnerabilities reported

---

### Bonus 2: Scheduled Workflow

**Maqsad:** Har kuni testlarni run qilish (nightly builds).

```yaml
name: Nightly Tests

on:
  schedule:
    - cron: '0 0 * * *'  # Har kuni 00:00 UTC
  workflow_dispatch:      # Manual trigger

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest
```

**Tekshirish:**
- [ ] Cron configured correctly
- [ ] Manual trigger works
- [ ] Runs at scheduled time

---

### Bonus 3: Slack Notifications

**Maqsad:** Deployment notifications Slack'ga yuborish.

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment to production'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
    fields: repo,message,commit,author
```

**Setup:**
1. Slack workspace'da incoming webhook yarating
2. Webhook URL'ni GitHub secret'ga qo'shing
3. Workflow'ga notification qo'shing

**Tekshirish:**
- [ ] Slack webhook created
- [ ] Secret configured
- [ ] Notifications received

---

### Bonus 4: Pull Request Comments

**Maqsad:** Test natijalarini PR comment sifatida qo'shish.

```yaml
- name: Comment PR
  uses: actions/github-script@v6
  if: github.event_name == 'pull_request'
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '✅ All tests passed! Coverage: 85%'
      })
```

**Tekshirish:**
- [ ] Comment appears on PR
- [ ] Shows test results
- [ ] Updates on each push

---

## Topshirish talablari

### Har bir level uchun:

1. **Workflow Files**
   - `.github/workflows/` da barcha workflow'lar
   - To'g'ri YAML syntax
   - Meaningful naming

2. **Screenshots**
   - Successful workflow runs
   - GitHub Actions dashboard
   - Deployment logs (if applicable)
   - Badge'lar README.md'da

3. **Documentation**
   - README.md updated with badges
   - Workflow purpose explained
   - Setup instructions

4. **Repository Structure**
   ```
   .github/
   ├── workflows/
   │   ├── test.yml
   │   ├── lint.yml
   │   ├── deploy-staging.yml
   │   └── deploy-production.yml
   ├── CONTRIBUTING.md
   └── SECURITY.md
   ```

5. **Testing Checklist**
   - [ ] All workflows pass
   - [ ] Badges show "passing"
   - [ ] Deployment successful
   - [ ] Secrets configured correctly
   - [ ] No sensitive data in logs

---

## Baholash mezonlari

### Level 1: Basic 
- Basic test workflow: 
- Format check: 
- Badge: 

### Level 2: Intermediate 
- PostgreSQL testing: 
- Code coverage: 
- Dependency caching: 

### Level 3: Advanced 
- Multi-tool linting: 
- Auto-deployment: 

### Level 4: Expert 
- Matrix testing:
- Multi-environment: 

### Bonus
- Security scanning: 
- Scheduled workflow: 
- Slack notifications: 
- PR comments: 

---

## Deadline

- **Level 1-2:** 2 kun
- **Level 3:** +2 kun
- **Level 4:** +1 kun
- **Bonus:** +1 kun
- **Jami:** 1 hafta

---

## Yordam

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **YAML Validator:** https://www.yamllint.com/
- **Discord:** #cicd-help channel
- **Office hours:** Har kuni 20:00-22:00

---

## Common Issues & Solutions

### Issue 1: Workflow not triggering

**Solution:**
- Check YAML syntax
- Verify file location: `.github/workflows/`
- Check branch name matches

### Issue 2: Tests fail in CI but pass locally

**Solution:**
- Check environment variables
- Verify Python/Django versions
- Use same database (PostgreSQL)

### Issue 3: Secrets not working

**Solution:**
- Check secret name (case-sensitive)
- No extra spaces in value
- Secret is in correct repository

### Issue 4: Deployment fails

**Solution:**
- Verify Railway token
- Check service name
- Review deployment logs

---

## Tips for Success

1. **Start Simple:** Level 1 → Level 4
2. **Test Locally First:** Ensure tests pass
3. **One Workflow at a Time:** Don't create all at once
4. **Read Logs:** GitHub Actions logs very detailed
5. **Use Examples:** Copy from examples folder
6. **Ask for Help:** Don't struggle alone

---

**Good luck with CI/CD! Automate everything!**