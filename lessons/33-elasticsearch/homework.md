# Homework - Lesson 33: Advanced Search with Elasticsearch

## Maqsad
Ushbu topshiriqda siz Elasticsearch bilan to'liq qidiruv tizimini yaratishni o'rganasiz.

---

## Topshiriq 1: Elasticsearch Setup va Integration ⭐⭐

### Vazifa:
Docker bilan Elasticsearch'ni o'rnating va Django bilan integratsiya qiling.

### Talablar:
1.  Docker Compose bilan Elasticsearch va Kibana
2.  django-elasticsearch-dsl o'rnatilgan
3.  settings.py da ELASTICSEARCH_DSL sozlangan
4.  BookDocument yaratilgan va configured

### Steps:
```powershell
# 1. Docker containers
docker-compose up -d

# 2. Elasticsearch health check
curl http://localhost:9200

# 3. Django packages
pipenv install elasticsearch django-elasticsearch-dsl

# 4. Create index
python manage.py search_index --create

# 5. Populate data
python manage.py search_index --populate
```

### Qabul qilish mezonlari:
- [ ] Elasticsearch http://localhost:9200 da ishlayapti
- [ ] Kibana http://localhost:5601 da ochiladi (optional)
- [ ] BookDocument to'g'ri configured
- [ ] Books index yaratilgan
- [ ] Ma'lumotlar index'ga yuklangan

### Test:
```powershell
# Index tekshirish
curl http://localhost:9200/books

# Documents count
curl http://localhost:9200/books/_count
```

---

## Topshiriq 2: Full-text Search ⭐⭐⭐

### Vazifa:
Multi-field full-text search endpoint yarating.

### Talablar:
1.  `/api/books/search/` endpoint
2.  Query parameter: `q` (search term)
3.  Multi-field search: title, description, author
4.  Field boosting: title^3, author^2, description^1
5.  Fuzziness enabled (typo tolerance)
6.  Response includes score

### Example Request:
```
GET /api/books/search/?q=django
GET /api/books/search/?q=pyton (typo)
```

### Expected Response:
```json
{
  "count": 5,
  "took": 15,
  "results": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "author": "William Vincent",
      "description": "Learn Django...",
      "score": 2.5
    }
  ]
}
```

### Qabul qilish mezonlari:
- [ ] Search title, description, author
- [ ] Title matches score higher (boosting)
- [ ] Typos handled (fuzziness)
- [ ] Results sorted by relevance
- [ ] Response time < 100ms

---

## Topshiriq 3: Autocomplete ⭐⭐

### Vazifa:
Autocomplete endpoint yarating (prefix matching).

### Talablar:
1. ✅ `/api/books/autocomplete/` endpoint
2. ✅ Query parameter: `q` (partial term)
3. ✅ match_phrase_prefix query
4. ✅ Limit: 10 suggestions
5. ✅ Fast response (< 50ms)

### Example Request:
```
GET /api/books/autocomplete/?q=dja
GET /api/books/autocomplete/?q=pyt
```

### Expected Response:
```json
{
  "suggestions": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "author": "William Vincent"
    },
    {
      "id": 2,
      "title": "Django REST Framework",
      "author": "John Doe"
    }
  ]
}
```

### Qabul qilish mezonlari:
- [ ] Prefix matching works
- [ ] Returns top 10 results
- [ ] Fast response time
- [ ] Sorted by relevance

---

## Topshiriq 4: Advanced Filtering ⭐⭐⭐

### Vazifa:
Multiple filter options bilan qidiruv.

### Talablar:
1. ✅ Price range filter (min_price, max_price)
2. ✅ Category filter
3. ✅ Author filter
4. ✅ Published date range
5. ✅ Combine filters with search

### Example Requests:
```
GET /api/books/search/?q=django&min_price=10&max_price=50
GET /api/books/search/?q=python&category=Programming
GET /api/books/search/?author=Vincent&min_pages=200
```

### Expected Response:
```json
{
  "count": 3,
  "filters_applied": {
    "price": {"min": 10, "max": 50},
    "category": "Programming"
  },
  "results": [...]
}
```

### Qabul qilish mezonlari:
- [ ] Price range filtering works
- [ ] Category filtering works
- [ ] Author filtering works
- [ ] Multiple filters combine correctly
- [ ] Filters work with search query

---

## Topshiriq 5: Aggregations (Statistics) ⭐⭐⭐⭐

### Vazifa:
Book statistics endpoint yarating.

### Talablar:
1. ✅ `/api/books/statistics/` endpoint
2. ✅ Average price calculation
3. ✅ Min/Max price
4. ✅ Top 10 authors by book count
5. ✅ Books by category count
6. ✅ Books by year

### Expected Response:
```json
{
  "price_statistics": {
    "average": 35.50,
    "min": 9.99,
    "max": 89.99
  },
  "top_authors": [
    {"name": "William Vincent", "count": 5},
    {"name": "Daniel Greenfeld", "count": 3}
  ],
  "categories": [
    {"name": "Programming", "count": 15},
    {"name": "Web Development", "count": 10}
  ],
  "by_year": [
    {"year": 2023, "count": 20},
    {"year": 2022, "count": 15}
  ]
}
```

### Qabul qilish mezonlari:
- [ ] Price statistics accurate
- [ ] Top authors calculated
- [ ] Category counts correct
- [ ] Year distribution shown
- [ ] Fast response (< 100ms)

---

## Topshiriq 6: Search Highlighting ⭐⭐⭐

### Vazifa:
Search results'da match qilingan so'zlarni highlight qiling.

### Talablar:
1. ✅ Highlight matched terms in title
2. ✅ Highlight matched terms in description
3. ✅ Use `<mark>` tags for highlighting
4. ✅ Fragment size: 150 characters
5. ✅ Show 3 fragments per field

### Expected Response:
```json
{
  "results": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "title_highlight": "<mark>Django</mark> for Beginners",
      "description_highlight": [
        "Learn <mark>Django</mark> web development...",
        "Build <mark>Django</mark> applications from scratch..."
      ]
    }
  ]
}
```

### Qabul qilish mezonlari:
- [ ] Matched terms highlighted
- [ ] Multiple fragments shown
- [ ] HTML tags correct (<mark>)
- [ ] Fragment size appropriate

---

## Topshiriq 7: Pagination ⭐⭐

### Vazifa:
Search results uchun pagination qo'shing.

### Talablar:
1. ✅ Query parameters: `page`, `size`
2. ✅ Default: page=1, size=10
3. ✅ Calculate total pages
4. ✅ Return page info in response

### Example Request:
```
GET /api/books/search/?q=django&page=2&size=10
```

### Expected Response:
```json
{
  "count": 45,
  "page": 2,
  "size": 10,
  "total_pages": 5,
  "results": [...]
}
```

### Qabul qilish mezonlari:
- [ ] Pagination works correctly
- [ ] Page count accurate
- [ ] Default values applied
- [ ] Edge cases handled (page > total_pages)

---

## Topshiriq 8: Auto-indexing with Signals (Bonus) ⭐⭐⭐⭐

### Vazifa:
Django signals bilan avtomatik indexing.

### Talablar:
1. ✅ post_save signal: Update/Create in index
2. ✅ post_delete signal: Delete from index
3. ✅ Error handling
4. ✅ Logging

### Implementation:
```python
# books/signals.py
@receiver(post_save, sender=Book)
def update_book_index(sender, instance, **kwargs):
    # Update Elasticsearch
    
@receiver(post_delete, sender=Book)
def delete_book_index(sender, instance, **kwargs):
    # Delete from Elasticsearch
```

### Qabul qilish mezonlari:
- [ ] New books auto-indexed
- [ ] Updated books re-indexed
- [ ] Deleted books removed from index
- [ ] Errors logged
- [ ] No performance issues

---

## Topshiriq 9: Suggestions with Completion Field ⭐⭐⭐⭐

### Vazifa:
CompletionField bilan fast suggestions.

### Talablar:
1. ✅ `/api/books/suggest/` endpoint
2. ✅ Use CompletionField in document
3. ✅ Completion suggester query
4. ✅ Response time < 10ms
5. ✅ Up to 10 suggestions

### Document Update:
```python
title = fields.TextField(
    fields={
        'suggest': fields.CompletionField(),
    }
)
```

### Expected Response:
```json
{
  "suggestions": [
    {"text": "Django for Beginners", "score": 1.0},
    {"text": "Django REST Framework", "score": 0.9}
  ]
}
```

### Qabul qilish mezonlari:
- [ ] CompletionField configured
- [ ] Suggestions very fast (< 10ms)
- [ ] Relevant suggestions
- [ ] Scored results

---

## Topshiriq 10: Production Optimization (Advanced) ⭐⭐⭐⭐⭐

### Vazifa:
Production uchun optimization qiling.

### Talablar:
1. ✅ Connection pooling
2. ✅ Query caching
3. ✅ Select only needed fields (source filtering)
4. ✅ Use filters instead of queries where possible
5. ✅ Error handling va fallback
6. ✅ Monitoring va logging
7. ✅ Security (authentication)

### Example Optimizations:

**Source Filtering:**
```python
search = search.source(['id', 'title', 'author'])
```

**Connection Pooling:**
```python
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200',
        'http_auth': ('user', 'password'),
        'timeout': 30,
        'max_retries': 3,
    },
}
```

**Error Handling:**
```python
try:
    response = search.execute()
except ConnectionError:
    # Fallback to Django ORM
    books = Book.objects.filter(title__icontains=query)
```

### Qabul qilish mezonlari:
- [ ] Connection pooling configured
- [ ] Query performance optimized
- [ ] Error handling comprehensive
- [ ] Logging implemented
- [ ] Security configured
- [ ] Monitoring setup

---

## Bonus Challenges

### Bonus 1: Multi-language Search ⭐⭐⭐⭐⭐
- Configure analyzers for multiple languages
- Support Uzbek, Russian, English
- Language-specific stemming

### Bonus 2: Geo-spatial Search ⭐⭐⭐⭐⭐
- Add location field to books (bookstore location)
- Search books by distance
- "Books available within 5km"

### Bonus 3: Custom Scoring ⭐⭐⭐⭐⭐
- Boost recent books
- Boost popular books (by rating/sales)
- Custom relevance algorithm

### Bonus 4: Search Analytics ⭐⭐⭐⭐
- Track popular search queries
- Log search performance
- Analyze search patterns

---

## Topshiriqni Topshirish

### 1. GitHub Repository

```bash
# Branch yarating
git checkout -b feature/lesson-33-elasticsearch

# Commit qiling
git add .
git commit -m "feat: Implement Elasticsearch advanced search system"

# Push qiling
git push origin feature/lesson-33-elasticsearch
```

### 2. Pull Request

**Title:** `[Homework 33] Elasticsearch Advanced Search`

**Description:**
```markdown
## Qilingan Ishlar
- [ ] Elasticsearch Docker setup
- [ ] Django integration
- [ ] Full-text search
- [ ] Autocomplete
- [ ] Filtering
- [ ] Aggregations
- [ ] Highlighting
- [ ] Pagination
- [ ] Auto-indexing signals
- [ ] Suggestions

## Test Qilingan
- Postman collection attached
- All endpoints working
- Performance benchmarks documented

## Performance Results
- Search response time: < 50ms
- Autocomplete: < 20ms
- Suggestions: < 10ms

## Screenshots
[Kibana dashboard screenshot]
[Postman tests screenshot]
```

### 3. Documentation

`ELASTICSEARCH_GUIDE.md` yarating:
```markdown
# Elasticsearch Setup Guide

## Installation
...

## Usage
...

## Testing
...

## Troubleshooting
...
```

---

## Baholash Mezonlari

| Topshiriq | Ball | Talablar |
|-----------|------|----------|
| Setup & Integration | 10 | Docker, django-elasticsearch-dsl |
| Full-text Search | 15 | Multi-field, boosting, fuzziness |
| Autocomplete | 10 | Prefix matching, fast |
| Filtering | 15 | Multiple filters, combinations |
| Aggregations | 15 | Statistics, grouping |
| Highlighting | 10 | Mark matched terms |
| Pagination | 5 | Page navigation |
| Auto-indexing | 10 | Signals |
| Suggestions | 5 | CompletionField |
| Optimization | 5 | Performance, security |
| **Jami** | **100** | |

### Bonus Balllar:
- Multi-language: +15
- Geo-spatial: +15
- Custom scoring: +10
- Analytics: +10

---

## Yordam Resurslari

### Documentation:
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [django-elasticsearch-dsl](https://django-elasticsearch-dsl.readthedocs.io/)
- [Elasticsearch DSL](https://elasticsearch-dsl.readthedocs.io/)

### Video Tutorials:
- [Elasticsearch Crash Course](https://www.youtube.com/results?search_query=elasticsearch+crash+course)
- [Django + Elasticsearch](https://www.youtube.com/results?search_query=django+elasticsearch)

### Tools:
- [Kibana](https://www.elastic.co/kibana)
- [Elasticvue](https://elasticvue.com/)

---

## Deadline

**Topshirish muddati:** Darsdan keyingi 10 kun ichida

---

## Omad!

Elasticsearch - juda kuchli tool! Bu topshiriqni tugatganingizdan so'ng, siz professional darajadagi qidiruv tizimlarini yaratishni bilasiz!