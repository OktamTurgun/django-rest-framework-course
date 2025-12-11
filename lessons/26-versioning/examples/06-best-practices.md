# API Versioning Best Practices

##  Golden Rules

### 1. Start with Versioning from Day 1

```python
# ✅ CORRECT: Version from the beginning
/api/v1/books/

# ❌ WRONG: No version initially
/api/books/  # Keyin qanday version qo'shasiz?
```

**Why?** Keyinchalik version qo'shish juda qiyin.

---

### 2. Use Semantic Versioning Principles

```
MAJOR.MINOR.PATCH
  ↑      ↑     ↑
  |      |     └─ Bug fixes
  |      └─────── New features (backward compatible)
  └────────────── Breaking changes
```

**For APIs:** Ko'pincha faqat MAJOR (v1, v2, v3...)

---

### 3. Document Everything

```markdown
# API Changelog

## v2.0.0 (2024-01-15)
### Breaking Changes
- `author` field changed from string to object
- `isbn` field is now required

### New Features
- Book reviews endpoint: GET /api/v2/books/{id}/reviews/
- Author statistics: GET /api/v2/authors/{id}/stats/

### Bug Fixes
- Fixed price calculation
- Improved error messages

### Migration Guide
See: https://docs.example.com/v1-to-v2
```

---

##  Version Planning

### Before Creating New Version:

**Questions to Ask:**

1.  Is this change really breaking?
2.  Can we make it backward compatible?
3.  What's the migration path?
4.  How long will we support old version?
5.  What's the cost of maintaining both?

### Decision Tree:

```
Is this a breaking change?
    │
    ├─ No → Add to current version
    │
    └─ Yes → Can we make it backward compatible?
           │
           ├─ Yes → Add with feature flag
           │
           └─ No → New version needed
                   │
                   ├─ Plan migration (6+ months)
                   ├─ Write migration guide
                   ├─ Set sunset date
                   └─ Communicate early
```

---

##  Version Numbering

### ✅ Good Practices:

```
v1, v2, v3
v1.0, v2.0, v3.0
2024-01-v1 (date + version)
```

### ❌ Bad Practices:

```
version1, version2  (too verbose)
1, 2, 3  (confusing with resource IDs)
latest  (ambiguous, cache issues)
```

---

##  Support Policy

### Recommended Timeline:

| Phase | Duration | Status |
|-------|----------|--------|
| Active Development | Ongoing | Latest features |
| Active Support | 12-24 months | Bug fixes, security |
| Deprecated | 6-12 months | Security only |
| Sunset | N/A | 410 Gone |

### Example:

```
v1: Released 2023-01-01
    Active until 2024-01-01 (12 months)
    Deprecated until 2024-07-01 (6 months)
    Sunset on 2024-07-01

v2: Released 2024-01-01
    Currently active
```

---

##  Common Anti-Patterns

### 1. Too Many Versions

```
# ❌ BAD: Version proliferation
/api/v1/
/api/v1.1/
/api/v1.2/
/api/v2/
/api/v2.1/
/api/v2.2/
/api/v2.3/
```

**Fix:** Faqat major versions. Minor changes backward compatible qiling.

---

### 2. Breaking Changes Without New Version

```python
# ❌ BAD: Breaking change in same version
# v1 Before
{"author": "John Doe"}

# v1 After (BREAKING!)
{"author": {"name": "John Doe"}}
```

**Fix:** Yangi version yarating.

---

### 3. No Deprecation Period

```
# ❌ BAD: Immediate shutdown
2024-01-01: v2 released, v1 immediately disabled

# ✅ GOOD: Gradual deprecation
2024-01-01: v2 released
2024-06-01: v1 deprecated (warnings added)
2024-12-31: v1 sunset
```

---

### 4. Poor Documentation

```
# ❌ BAD
"We released v2. Please upgrade."

# ✅ GOOD
"v2 Released! 
 Changes: Author is now object
 Migration: https://docs.example.com/v1-to-v2
 Support until: 2024-12-31
 Questions: api-support@example.com"
```

---

##  Version Documentation Template

```markdown
# API Version: v2

## Status
- **Released:** 2024-01-15
- **Status:** Active
- **Support Until:** 2026-01-15

## Changes from v1

### Breaking Changes
1. **Author Field**
   - Before: `"author": "string"`
   - After: `"author": object`
   - Reason: Need more author information

2. **ISBN Required**
   - Before: Optional
   - After: Required for POST
   - Reason: Data quality

### New Features
- Book reviews endpoint
- Author statistics
- Advanced search

### Improvements
- Faster response times
- Better error messages
- Consistent error format

## Migration Guide
See: [v1 to v2 Migration](./migration-v1-v2.md)

## Support
- Email: api-support@example.com
- Slack: #api-v2
- Docs: https://docs.example.com/v2
```

---

##  Technical Best Practices

### 1. Use Feature Flags

```python
# settings.py
FEATURE_FLAGS = {
    'v2_reviews': True,
    'v2_statistics': False,  # Not ready yet
}

# views.py
class BookDetailView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        data = BookSerializer(book).data
        
        # Feature flag
        if settings.FEATURE_FLAGS.get('v2_reviews'):
            reviews = book.reviews.all()
            data['reviews'] = ReviewSerializer(reviews, many=True).data
        
        return Response(data)
```

---

### 2. Shared Code Between Versions

```python
# api/common/serializers.py
class BaseBookSerializer(serializers.ModelSerializer):
    """Shared logic"""
    class Meta:
        model = Book
        fields = ['id', 'title', 'price']

# api/v1/serializers.py
class BookSerializerV1(BaseBookSerializer):
    """V1 specific"""
    author = serializers.CharField(source='author.name')

# api/v2/serializers.py
class BookSerializerV2(BaseBookSerializer):
    """V2 specific"""
    author = AuthorSerializer()
```

---

### 3. Version-Specific Tests

```python
# tests/test_v1.py
class V1APITest(TestCase):
    def test_book_list_v1(self):
        response = self.client.get('/api/v1/books/')
        self.assertEqual(response.status_code, 200)
        # V1 specific assertions
        self.assertIsInstance(response.data[0]['author'], str)

# tests/test_v2.py
class V2APITest(TestCase):
    def test_book_list_v2(self):
        response = self.client.get('/api/v2/books/')
        self.assertEqual(response.status_code, 200)
        # V2 specific assertions
        self.assertIsInstance(response.data[0]['author'], dict)
```

---

### 4. Backward Compatibility Helpers

```python
# api/compat.py
def v1_to_v2_book(v1_data):
    """Convert v1 book format to v2"""
    return {
        'id': v1_data['id'],
        'title': v1_data['title'],
        'author': {
            'id': v1_data['author_id'],
            'name': v1_data['author'],
        },
        'price': v1_data['price'],
    }

def v2_to_v1_book(v2_data):
    """Convert v2 book format to v1"""
    return {
        'id': v2_data['id'],
        'title': v2_data['title'],
        'author': v2_data['author']['name'],
        'author_id': v2_data['author']['id'],
        'price': v2_data['price'],
    }
```

---

##  Monitoring & Analytics

### Key Metrics:

```python
# Track these metrics
METRICS = {
    'v1_requests': 0,
    'v2_requests': 0,
    'v1_unique_users': set(),
    'v2_unique_users': set(),
    'v1_to_v2_migration_rate': 0,
    'deprecated_endpoint_usage': {},
}

# Dashboard queries
def get_version_analytics():
    return {
        'total_v1': cache.get('api_requests:v1', 0),
        'total_v2': cache.get('api_requests:v2', 0),
        'migration_rate': calculate_migration_rate(),
        'top_v1_endpoints': get_top_endpoints('v1'),
        'unmigrated_users': get_unmigrated_users(),
    }
```

---

##  Checklist for New Version

### Planning Phase:
- [ ] List all breaking changes
- [ ] Estimate migration effort
- [ ] Set support timeline
- [ ] Plan communication strategy

### Development Phase:
- [ ] Create new version endpoints
- [ ] Write migration helpers
- [ ] Update documentation
- [ ] Create migration guide
- [ ] Add deprecation warnings to old version

### Testing Phase:
- [ ] Unit tests for new version
- [ ] Integration tests
- [ ] Backward compatibility tests
- [ ] Performance tests
- [ ] Beta testing program

### Release Phase:
- [ ] Announce 6+ months ahead
- [ ] Release beta version
- [ ] Collect feedback
- [ ] Stable release
- [ ] Mark old version deprecated

### Sunset Phase:
- [ ] Regular migration reminders
- [ ] Monitor migration progress
- [ ] Final warning (30 days)
- [ ] Execute sunset
- [ ] Post-sunset support

---

##  Pro Tips

### 1. Version Headers in Response

```python
response['API-Version'] = request.version
response['API-Supported-Versions'] = 'v1, v2, v3'
response['API-Latest-Version'] = 'v3'
```

### 2. Client Library Versioning

```python
# Python client
from api_client import ClientV1, ClientV2

# V1 client
client_v1 = ClientV1(api_key='...')
books = client_v1.books.list()

# V2 client
client_v2 = ClientV2(api_key='...')
books = client_v2.books.list()
```

### 3. Sandbox Environment

```
Production:
- https://api.example.com/v1/
- https://api.example.com/v2/

Sandbox:
- https://sandbox.example.com/v1/
- https://sandbox.example.com/v2/
```

### 4. Version Discovery Endpoint

```python
# GET /api/
{
  "versions": {
    "v1": {
      "status": "deprecated",
      "sunset_date": "2024-12-31",
      "docs": "https://docs.example.com/v1"
    },
    "v2": {
      "status": "active",
      "docs": "https://docs.example.com/v2"
    },
    "v3": {
      "status": "beta",
      "docs": "https://docs.example.com/v3"
    }
  },
  "latest": "v2",
  "default": "v1"
}
```

---

##  Real-World Examples

### Stripe
- URL versioning with dates: `2023-10-16`
- Long support period (3+ years)
- Excellent documentation

### GitHub
- Accept header versioning
- Clear deprecation timeline
- Migration guides with code examples

### Twitter
- URL path versioning (v1.1, v2)
- Developer portal with migration tools
- Active community support

---

##  Resources

- [Semantic Versioning](https://semver.org/)
- [API Deprecation RFC](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-deprecation-header)
- [Microsoft API Guidelines](https://github.com/microsoft/api-guidelines)
- [Google API Design Guide](https://cloud.google.com/apis/design)

---

##  Summary

**Key Takeaways:**

1.  Version from Day 1
2.  Clear deprecation policy (6-12 months)
3.  Comprehensive documentation
4.  Migration support
5.  Monitor usage metrics
6.  Communicate early and often
7.  Test thoroughly
8.  Be flexible when needed

**Remember:** Good versioning = Happy developers!