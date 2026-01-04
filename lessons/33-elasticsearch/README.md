# Lesson 33: Advanced Search with Elasticsearch

## Mundarija
1. [Kirish](#kirish)
2. [Elasticsearch nima?](#elasticsearch-nima)
3. [Docker bilan o'rnatish](#docker-bilan-ornatish)
4. [Django integratsiya](#django-integratsiya)
5. [Full-text search](#full-text-search)
6. [Autocomplete](#autocomplete)
7. [Search suggestions](#search-suggestions)
8. [Postman testlar](#postman-testlar)

---

## Kirish

Elasticsearch - bu **distributed, RESTful search and analytics engine**. Django bilan integratsiya qilib, juda kuchli qidiruv tizimi yaratamiz.

### Nima uchun Elasticsearch?

**Django ORM vs Elasticsearch:**

| Feature | Django ORM | Elasticsearch |
|---------|-----------|---------------|
| Simple search | ✅ Yaxshi | ✅ Juda yaxshi |
| Full-text search | ⚠️ LIKE qidirish | ✅ Professional |
| Speed | ⚠️ Sekin (large data) | ✅ Milliseconds |
| Fuzzy search | ❌ Yo'q | ✅ Bor |
| Autocomplete | ❌ Qiyin | ✅ Oson |
| Relevance scoring | ❌ Yo'q | ✅ Bor |
| Multi-language | ⚠️ Cheklangan | ✅ 40+ til |

---

## Elasticsearch nima?

### Core Concepts

#### 1. Index (Indeks)
- Database'dagi **table** ga o'xshash
- Misol: `books`, `users`, `products`

#### 2. Document (Hujjat)
- Table'dagi **row** ga o'xshash
- JSON formatda
- Misol: Bitta kitob

```json
{
  "_id": "1",
  "_source": {
    "title": "Django for Beginners",
    "author": "William Vincent",
    "isbn": "978-1735467207",
    "price": 39.99
  }
}
```

#### 3. Field (Maydon)
- Column ga o'xshash
- `title`, `author`, `isbn` - bular fieldlar

#### 4. Mapping (Xaritalash)
- Schema definition
- Field turlarini belgilash

### Elasticsearch Advantages

✅ **Full-text search** - Matnda to'liq qidiruv
```
Query: "django rest"
Matches: "Django REST Framework", "REST API with Django"
```

✅ **Fuzzy search** - Xato bilan qidiruv
```
Query: "pyton" (typo)
Suggests: "python"
```

✅ **Autocomplete** - Avtomatik to'ldirish
```
Input: "dja"
Suggests: "django", "django rest framework", "djangoproject"
```

✅ **Relevance scoring** - Natijalarni reytinglash
```
Query: "python django"
Best match: Document with both words in title
Lower match: Only "python" in description
```

✅ **Aggregations** - Statistika
```
- Books by author
- Average price by category
- Publications by year
```

---

## Docker bilan o'rnatish

### Prerequisite: Docker Desktop

**Windows:**
1. https://www.docker.com/products/docker-desktop/ dan yuklab oling
2. O'rnating va ishga tushiring
3. WSL 2 backend yoqing

**Tekshirish:**
```powershell
docker --version
# Docker version 24.0.x
```

### Elasticsearch va Kibana ishga tushirish

```powershell
# 33-elasticsearch papkasida
cd C:\Users\User\Documents\GitHub\django-rest-framework-course\lessons\33-elasticsearch

# Docker containers ishga tushirish
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f
```

**Kutish:** 1-2 daqiqa (birinchi marta sekin yuklanadi)

### Tekshirish

**Elasticsearch:**
```powershell
# Browser'da yoki curl bilan
curl http://localhost:9200

# Yoki PowerShell'da
Invoke-WebRequest -Uri http://localhost:9200
```

**Expected response:**
```json
{
  "name" : "xxxxx",
  "cluster_name" : "docker-cluster",
  "version" : {
    "number" : "8.11.0"
  },
  "tagline" : "You Know, for Search"
}
```

**Kibana (optional):**
- Browser: http://localhost:5601
- Kibana dashboard ochiladi

---

## Django integratsiya

### 1. Paketlarni o'rnatish

```powershell
cd code/library-project
pipenv shell

# Elasticsearch paketlari
pipenv install elasticsearch==8.11.0
pipenv install django-elasticsearch-dsl==8.0
pipenv install django-elasticsearch-dsl-drf==0.22.5
```

### 2. settings.py sozlash

```python
INSTALLED_APPS = [
    # ...
    'django_elasticsearch_dsl',  # Elasticsearch
    'django_elasticsearch_dsl_drf',  # DRF integration
    # ...
    'books',
]

# Elasticsearch Configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200',
        'timeout': 30,
    },
}
```

### 3. books/documents.py yaratish

Bu fayl Elasticsearch index'ni belgilaydi:

```python
"""
books/documents.py - Elasticsearch Document
"""

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Book


@registry.register_document
class BookDocument(Document):
    """
    Book document for Elasticsearch
    
    This defines how Book model is indexed in Elasticsearch
    """
    
    # Simple fields
    id = fields.IntegerField()
    title = fields.TextField(
        analyzer='standard',
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    
    description = fields.TextField(
        analyzer='standard'
    )
    
    author = fields.TextField(
        analyzer='standard',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    
    isbn = fields.TextField()
    published_date = fields.DateField()
    pages = fields.IntegerField()
    price = fields.FloatField()
    
    # Nested fields
    category = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }
    )
    
    class Index:
        """Index settings"""
        name = 'books'  # Index nomi
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_result_window': 10000,
        }
    
    class Django:
        """Django model mapping"""
        model = Book
        fields = []  # Bo'sh, chunki fieldlarni yuqorida belgiladik
        
        # Qaysi fieldlar o'zgarganda re-index qilish
        related_models = []
    
    def get_queryset(self):
        """Not called by the parent class."""
        return super().get_queryset().select_related('category')
```

### Analyzer nima?

**Analyzer** - matnni qanday qayta ishlashni belgilaydi:

```
Input: "Django REST Framework"

Standard Analyzer:
1. Lowercase: "django rest framework"
2. Tokenize: ["django", "rest", "framework"]
3. Remove stop words (optional)

Query: "django" ✅ Match!
Query: "Django" ✅ Match! (case insensitive)
Query: "REST" ✅ Match!
```

### Field Types

| Type | Misol | Qidiruv |
|------|-------|---------|
| TextField | Title, description | Full-text |
| KeywordField | ISBN, status | Exact match |
| IntegerField | Pages, stock | Numeric |
| DateField | Published date | Date range |
| CompletionField | Suggestions | Autocomplete |

---

## Ma'lumotlarni index'lash

### Commandlar

```powershell
# Index yaratish
python manage.py search_index --create

# Ma'lumotlarni index'ga yuklash
python manage.py search_index --populate

# Index'ni rebuild qilish (delete + create + populate)
python manage.py search_index --rebuild

# Real-time update (auto signal bilan)
# settings.py da:
ELASTICSEARCH_DSL_AUTOSYNC = True
```

### Index tekshirish

```powershell
# Index mavjudligini tekshirish
curl http://localhost:9200/_cat/indices?v

# Books index'ni ko'rish
curl http://localhost:9200/books

# Barcha documents
curl http://localhost:9200/books/_search?pretty
```

---

## Full-text Search

### 1. Search View yaratish

`books/views.py` ga qo'shing:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch_dsl import Q
from .documents import BookDocument


@api_view(['GET'])
def search_books(request):
    """
    Full-text search across books
    
    GET /api/books/search/?q=django
    GET /api/books/search/?q=python&author=Vincent
    """
    query = request.GET.get('q', '')
    author = request.GET.get('author', '')
    
    if not query and not author:
        return Response({
            'error': 'Query parameter required',
            'example': '/api/books/search/?q=django'
        }, status=400)
    
    # Elasticsearch query
    search = BookDocument.search()
    
    # Multi-field search
    if query:
        search = search.query(
            'multi_match',
            query=query,
            fields=['title^3', 'description', 'author^2'],
            fuzziness='AUTO'
        )
    
    # Filter by author
    if author:
        search = search.filter('match', author=author)
    
    # Execute
    response = search.execute()
    
    # Serialize results
    results = []
    for hit in response:
        results.append({
            'id': hit.id,
            'title': hit.title,
            'author': hit.author,
            'description': hit.description[:200],
            'score': hit.meta.score,
        })
    
    return Response({
        'count': response.hits.total.value,
        'results': results,
        'took': response.took,  # milliseconds
    })
```

### Multi-match nima?

```python
'multi_match': {
    'query': 'django',
    'fields': ['title^3', 'description', 'author^2']
}
```

**Boosting:**
- `title^3` - Title'dagi match 3x muhimroq
- `author^2` - Author'dagi match 2x muhimroq
- `description` - Description 1x (default)

**Fuzziness:**
- `AUTO` - Avtomatik typo detection
- `pyton` → `python` ✅
- `djngo` → `django` ✅

---

## Autocomplete

### 1. Autocomplete View

```python
@api_view(['GET'])
def autocomplete_books(request):
    """
    Autocomplete suggestions
    
    GET /api/books/autocomplete/?q=dja
    """
    query = request.GET.get('q', '')
    
    if not query:
        return Response({'suggestions': []})
    
    # Prefix query
    search = BookDocument.search()
    search = search.query(
        'match_phrase_prefix',
        title={
            'query': query,
            'max_expansions': 10
        }
    )
    
    # Limit results
    search = search[:10]
    
    response = search.execute()
    
    suggestions = [
        {
            'id': hit.id,
            'title': hit.title,
            'author': hit.author,
        }
        for hit in response
    ]
    
    return Response({'suggestions': suggestions})
```

**match_phrase_prefix:**
```
Input: "dja"
Matches: "django", "django rest", "django for beginners"
```

---

## Search Suggestions

### Advanced Suggestions with Completion

`books/documents.py` da `CompletionField` ishlatamiz:

```python
title = fields.TextField(
    fields={
        'suggest': fields.CompletionField(),
    }
)
```

### Suggestion View

```python
@api_view(['GET'])
def suggest_books(request):
    """
    Search suggestions (fast!)
    
    GET /api/books/suggest/?q=pyt
    """
    query = request.GET.get('q', '')
    
    if not query:
        return Response({'suggestions': []})
    
    # Completion suggester
    search = BookDocument.search()
    search = search.suggest(
        'book_suggestions',
        query,
        completion={'field': 'title.suggest', 'size': 10}
    )
    
    response = search.execute()
    
    suggestions = []
    if hasattr(response, 'suggest'):
        for suggestion in response.suggest.book_suggestions[0].options:
            suggestions.append({
                'text': suggestion.text,
                'score': suggestion._score,
            })
    
    return Response({'suggestions': suggestions})
```

---

## URLs

`books/urls.py` ga qo'shing:

```python
urlpatterns = [
    # ... existing URLs
    
    # Elasticsearch endpoints
    path('search/', views.search_books, name='search-books'),
    path('autocomplete/', views.autocomplete_books, name='autocomplete-books'),
    path('suggest/', views.suggest_books, name='suggest-books'),
]
```

---

## Postman Testlar

### Test 1: Elasticsearch Health Check

```
GET http://localhost:9200
```

**Expected Response:**
```json
{
  "name": "xxxxx",
  "cluster_name": "docker-cluster",
  "version": {
    "number": "8.11.0"
  },
  "tagline": "You Know, for Search"
}
```

### Test 2: Index Information

```
GET http://localhost:9200/books
```

**Expected Response:**
```json
{
  "books": {
    "mappings": {
      "properties": {
        "title": {
          "type": "text",
          "fields": {
            "raw": {"type": "keyword"},
            "suggest": {"type": "completion"}
          }
        },
        "author": {"type": "text"},
        ...
      }
    }
  }
}
```

### Test 3: Full-text Search

```
GET http://localhost:8000/api/books/search/?q=django
Headers:
  Authorization: Token <your-token>
```

**Expected Response:**
```json
{
  "count": 5,
  "took": 15,
  "results": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "author": "William Vincent",
      "description": "Learn Django web development...",
      "score": 2.5
    },
    {
      "id": 2,
      "title": "Two Scoops of Django",
      "author": "Daniel Greenfeld",
      "description": "Best practices for Django...",
      "score": 1.8
    }
  ]
}
```

### Test 4: Multi-field Search

```
GET http://localhost:8000/api/books/search/?q=python&author=Vincent
```

### Test 5: Fuzzy Search (Typo)

```
GET http://localhost:8000/api/books/search/?q=pyton
# "pyton" typo bo'lsa ham "python" topadi
```

### Test 6: Autocomplete

```
GET http://localhost:8000/api/books/autocomplete/?q=dja
```

**Expected Response:**
```json
{
  "suggestions": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "author": "William Vincent"
    },
    {
      "id": 3,
      "title": "Django REST Framework",
      "author": "John Doe"
    }
  ]
}
```

### Test 7: Suggestions

```
GET http://localhost:8000/api/books/suggest/?q=pyt
```

**Expected Response:**
```json
{
  "suggestions": [
    {
      "text": "Python Crash Course",
      "score": 1.0
    },
    {
      "text": "Python for Data Analysis",
      "score": 0.8
    }
  ]
}
```

---

## Advanced Features

### 1. Filtering

#### Range Filter (Price)

```python
@api_view(['GET'])
def filter_books(request):
    """
    Filter books by price range, pages, date
    
    GET /api/books/filter/?min_price=10&max_price=50
    GET /api/books/filter/?min_pages=200&max_pages=500
    """
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    search = BookDocument.search()
    
    # Price range filter
    if min_price or max_price:
        price_filter = {}
        if min_price:
            price_filter['gte'] = float(min_price)
        if max_price:
            price_filter['lte'] = float(max_price)
        
        search = search.filter('range', price=price_filter)
    
    response = search.execute()
    
    results = [
        {
            'id': hit.id,
            'title': hit.title,
            'price': hit.price,
        }
        for hit in response
    ]
    
    return Response({'results': results})
```

#### Category Filter

```python
# Filter by category
search = search.filter('term', category__id=category_id)

# Multiple categories
search = search.filter('terms', category__id=[1, 2, 3])
```

### 2. Aggregations (Statistics)

```python
@api_view(['GET'])
def book_statistics(request):
    """
    Get book statistics
    
    GET /api/books/statistics/
    """
    search = BookDocument.search()
    
    # Aggregations
    search.aggs.metric('avg_price', 'avg', field='price')
    search.aggs.metric('max_price', 'max', field='price')
    search.aggs.metric('min_price', 'min', field='price')
    search.aggs.bucket('by_author', 'terms', field='author.raw', size=10)
    search.aggs.bucket('by_category', 'terms', field='category.name.raw', size=10)
    
    # Don't need actual documents
    search = search[:0]
    
    response = search.execute()
    
    # Parse aggregations
    statistics = {
        'average_price': response.aggregations.avg_price.value,
        'max_price': response.aggregations.max_price.value,
        'min_price': response.aggregations.min_price.value,
        'top_authors': [
            {
                'name': bucket.key,
                'count': bucket.doc_count
            }
            for bucket in response.aggregations.by_author.buckets
        ],
        'categories': [
            {
                'name': bucket.key,
                'count': bucket.doc_count
            }
            for bucket in response.aggregations.by_category.buckets
        ],
    }
    
    return Response(statistics)
```

**Example Response:**
```json
{
  "average_price": 35.50,
  "max_price": 89.99,
  "min_price": 9.99,
  "top_authors": [
    {"name": "William Vincent", "count": 5},
    {"name": "Daniel Greenfeld", "count": 3}
  ],
  "categories": [
    {"name": "Programming", "count": 15},
    {"name": "Web Development", "count": 10}
  ]
}
```

### 3. Highlighting

```python
@api_view(['GET'])
def search_with_highlighting(request):
    """
    Search with highlighted results
    
    GET /api/books/search-highlight/?q=django
    """
    query = request.GET.get('q', '')
    
    search = BookDocument.search()
    search = search.query('multi_match', query=query, fields=['title', 'description'])
    
    # Add highlighting
    search = search.highlight('title', 'description')
    search = search.highlight_options(
        pre_tags=['<mark>'],
        post_tags=['</mark>'],
        fragment_size=150,
        number_of_fragments=3
    )
    
    response = search.execute()
    
    results = []
    for hit in response:
        result = {
            'id': hit.id,
            'title': hit.title,
            'description': hit.description,
        }
        
        # Add highlights
        if hasattr(hit.meta, 'highlight'):
            if 'title' in hit.meta.highlight:
                result['title_highlight'] = hit.meta.highlight.title[0]
            if 'description' in hit.meta.highlight:
                result['description_highlight'] = hit.meta.highlight.description
        
        results.append(result)
    
    return Response({'results': results})
```

**Example Response:**
```json
{
  "results": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "title_highlight": "<mark>Django</mark> for Beginners",
      "description_highlight": [
        "Learn <mark>Django</mark> web development...",
        "Build <mark>Django</mark> applications..."
      ]
    }
  ]
}
```

### 4. Pagination

```python
@api_view(['GET'])
def search_with_pagination(request):
    """
    Search with pagination
    
    GET /api/books/search-paginated/?q=django&page=1&size=10
    """
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 10))
    
    # Calculate offset
    offset = (page - 1) * size
    
    search = BookDocument.search()
    search = search.query('multi_match', query=query, fields=['title', 'description'])
    
    # Pagination
    search = search[offset:offset + size]
    
    response = search.execute()
    
    return Response({
        'count': response.hits.total.value,
        'page': page,
        'size': size,
        'total_pages': (response.hits.total.value + size - 1) // size,
        'results': [
            {
                'id': hit.id,
                'title': hit.title,
            }
            for hit in response
        ]
    })
```

### 5. Sorting

```python
# Sort by relevance (default)
search = search.sort('_score')

# Sort by price (ascending)
search = search.sort('price')

# Sort by price (descending)
search = search.sort('-price')

# Multiple sorts
search = search.sort('-published_date', 'price')

# Sort by relevance then price
search = search.sort('_score', {'price': {'order': 'asc'}})
```

---

## Best Practices

### 1. Index Management

**Alias Strategy:**
```python
# Use aliases for zero-downtime reindexing
# Old index: books_v1
# New index: books_v2
# Alias: books → books_v1

# Reindex to v2
# Switch alias: books → books_v2
# Delete old: books_v1
```

**Index Settings:**
```python
class Index:
    name = 'books'
    settings = {
        'number_of_shards': 1,  # Single node: 1, Production: 3-5
        'number_of_replicas': 0,  # Development: 0, Production: 1-2
        'refresh_interval': '1s',  # Real-time search
        'max_result_window': 10000,  # Max results
    }
```

### 2. Query Optimization

**Use Filters Instead of Queries:**
```python
# BAD - Full-text search for exact match
search = search.query('match', status='published')

# GOOD - Filter for exact match (faster, cached)
search = search.filter('term', status='published')
```

**Use Bool Query:**
```python
from elasticsearch_dsl import Q

# Combine multiple conditions
search = search.query(
    'bool',
    must=[
        Q('match', title='django'),  # Must have django
    ],
    should=[
        Q('match', author='Vincent'),  # Boost if Vincent
    ],
    filter=[
        Q('range', price={'gte': 10, 'lte': 50}),  # Filter price
    ],
    must_not=[
        Q('term', status='deleted'),  # Exclude deleted
    ]
)
```

### 3. Performance

**Select Only Needed Fields:**
```python
# BAD - Get all fields
search = search.execute()

# GOOD - Get only specific fields
search = search.source(['id', 'title', 'author'])
```

**Use Scroll for Large Results:**
```python
# For exporting all data
search = BookDocument.search()
search = search.params(scroll='2m', size=100)

for hit in search.scan():
    print(hit.title)
```

### 4. Analyzers

**Custom Analyzer:**
```python
class Index:
    name = 'books'
    settings = {
        'analysis': {
            'analyzer': {
                'custom_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ['lowercase', 'asciifolding', 'stop'],
                }
            }
        }
    }
```

### 5. Error Handling

```python
from elasticsearch.exceptions import ConnectionError, NotFoundError

@api_view(['GET'])
def safe_search(request):
    try:
        search = BookDocument.search()
        # ... search logic
        response = search.execute()
        return Response({'results': []})
    
    except ConnectionError:
        return Response({
            'error': 'Elasticsearch connection failed'
        }, status=503)
    
    except NotFoundError:
        return Response({
            'error': 'Index not found'
        }, status=404)
    
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)
```

---

## Signals for Auto-indexing

`books/signals.py` yaratish:

```python
"""
books/signals.py - Auto-indexing signals
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book
from .documents import BookDocument


@receiver(post_save, sender=Book)
def update_book_index(sender, instance, **kwargs):
    """Update Elasticsearch when book is saved"""
    try:
        BookDocument().update(instance)
    except Exception as e:
        print(f"Error updating index: {e}")


@receiver(post_delete, sender=Book)
def delete_book_index(sender, instance, **kwargs):
    """Delete from Elasticsearch when book is deleted"""
    try:
        BookDocument().get(id=instance.id).delete()
    except Exception as e:
        print(f"Error deleting from index: {e}")
```

`books/apps.py` da signal'ni ulash:

```python
from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
    
    def ready(self):
        import books.signals  # Import signals
```

---

## Kibana (Optional)

Kibana - Elasticsearch uchun visualization tool.

### Access Kibana

1. Browser: http://localhost:5601
2. **Dev Tools** → **Console** ga o'ting

### Useful Queries

```json
# Get all indices
GET _cat/indices?v

# Search books
GET books/_search
{
  "query": {
    "match": {
      "title": "django"
    }
  }
}

# Aggregations
GET books/_search
{
  "size": 0,
  "aggs": {
    "avg_price": {
      "avg": {
        "field": "price"
      }
    }
  }
}

# Delete index
DELETE books
```

---

## Troubleshooting

### Problem 1: Elasticsearch not starting

```powershell
# Check logs
docker-compose logs elasticsearch

# Common issue: Not enough memory
# Solution: Increase Docker memory (Settings → Resources)
```

### Problem 2: Connection refused

```python
# Check if Elasticsearch is running
curl http://localhost:9200

# Restart containers
docker-compose restart
```

### Problem 3: Index not found

```powershell
# Rebuild index
python manage.py search_index --rebuild

# Check if index exists
curl http://localhost:9200/_cat/indices?v
```

### Problem 4: Old data in index

```powershell
# Delete and rebuild
python manage.py search_index --delete
python manage.py search_index --create
python manage.py search_index --populate
```

---

## Testing

### Unit Tests

```python
from django.test import TestCase
from elasticsearch_dsl import Search
from .documents import BookDocument
from .models import Book


class ElasticsearchTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test index
        BookDocument.init()
    
    def setUp(self):
        # Create test books
        self.book1 = Book.objects.create(
            title="Django for Beginners",
            author="William Vincent",
            price=39.99
        )
        # Index book
        BookDocument().update(self.book1)
    
    def test_search(self):
        """Test basic search"""
        search = BookDocument.search().query('match', title='django')
        response = search.execute()
        
        self.assertEqual(response.hits.total.value, 1)
        self.assertEqual(response[0].title, "Django for Beginners")
    
    def tearDown(self):
        # Clean up
        Book.objects.all().delete()
```

---

## Production Checklist

### Security

- [ ] Enable Elasticsearch security (xpack.security.enabled=true)
- [ ] Set up authentication (username/password)
- [ ] Use HTTPS for Elasticsearch connection
- [ ] Restrict network access (firewall)
- [ ] Use environment variables for credentials

### Performance

- [ ] Set appropriate number_of_shards (3-5 for production)
- [ ] Set number_of_replicas (1-2 for production)
- [ ] Configure heap size (-Xms and -Xmx)
- [ ] Use connection pooling
- [ ] Enable query cache
- [ ] Monitor slow queries

### Monitoring

- [ ] Set up Elasticsearch monitoring
- [ ] Track index size
- [ ] Monitor query performance
- [ ] Set up alerts for failures
- [ ] Log all errors

### Backup

- [ ] Configure snapshot repository
- [ ] Schedule regular snapshots
- [ ] Test restore process
- [ ] Document backup procedures

---

## Comparison: Django ORM vs Elasticsearch

### Example: Search "python django"

**Django ORM:**
```python
# Simple LIKE query
books = Book.objects.filter(
    Q(title__icontains='python') | Q(title__icontains='django')
)
# Time: ~500ms (10,000 books)
# Relevance: No scoring
# Typos: Not handled
```

**Elasticsearch:**
```python
# Multi-field search with scoring
search = BookDocument.search().query(
    'multi_match',
    query='python django',
    fields=['title^3', 'description']
)
# Time: ~15ms (10,000 books)
# Relevance: Scored and sorted
# Typos: Handled with fuzziness
```

---

## Xulosa

### Nima o'rgandik?

✅ Elasticsearch nima va nima uchun kerak  
✅ Docker bilan Elasticsearch o'rnatish  
✅ django-elasticsearch-dsl integratsiya  
✅ Document definition va mapping  
✅ Full-text search implementation  
✅ Autocomplete va suggestions  
✅ Filtering va aggregations  
✅ Highlighting va pagination  
✅ Best practices va optimization  
✅ Production deployment  

### Elasticsearch Advantages

| Feature | Benefit |
|---------|---------|
| Speed | Milliseconds response time |
| Scalability | Horizontal scaling |
| Full-text | Advanced text analysis |
| Fuzzy search | Typo tolerance |
| Autocomplete | Real-time suggestions |
| Aggregations | Built-in analytics |
| Multi-language | 40+ languages |

### When to Use Elasticsearch?

✅ **Use Elasticsearch when:**
- Large dataset (100,000+ records)
- Complex text search needed
- Autocomplete/suggestions required
- Multi-language support needed
- Real-time analytics required
- High performance critical

❌ **Don't use when:**
- Small dataset (<10,000 records)
- Simple exact-match queries
- Additional infrastructure not acceptable
- Team lacks Elasticsearch expertise

---

## Resources

### Documentation
- [Elasticsearch Official Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [django-elasticsearch-dsl](https://django-elasticsearch-dsl.readthedocs.io/)
- [Elasticsearch DSL Python](https://elasticsearch-dsl.readthedocs.io/)

### Tutorials
- [Elasticsearch Guide](https://www.elastic.co/guide/index.html)
- [Full-text Search Best Practices](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables)

### Tools
- [Kibana](https://www.elastic.co/kibana) - Visualization
- [Elasticvue](https://elasticvue.com/) - GUI for Elasticsearch
- [Cerebro](https://github.com/lmenezes/cerebro) - Admin tool

---

## Homework

`homework.md` faylida topshiriqlar!

---

**Happy Searching!**