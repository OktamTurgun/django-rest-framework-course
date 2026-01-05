# Elasticsearch Examples - Lesson 33

Bu papkada Elasticsearch'ni tushunish uchun 5 ta amaliy Python misollar mavjud.

---

## Misollar Ro'yxati

### 1. `01-elasticsearch-basics.py`
**Mavzu:** Elasticsearch asoslari - connection, index, CRUD

**O'rganasiz:**
- Elasticsearch'ga ulanish
- Index yaratish
- Document CRUD operations
- Basic queries

**Ishga tushirish:**
```bash
python 01-elasticsearch-basics.py
```

---

### 2. `02-document-indexing.py`
**Mavzu:** Bulk indexing va mapping

**O'rganasiz:**
- Bulk indexing (ko'p document birdan)
- Custom mapping definition
- Analyzers
- Field types

**Ishga tushirish:**
```bash
python 02-document-indexing.py
```

---

### 3. `03-full-text-search.py`
**Mavzu:** Full-text search va relevance

**O'rganasiz:**
- Multi-match query
- Field boosting
- Fuzzy search
- Bool queries
- Scoring

**Ishga tushirish:**
```bash
python 03-full-text-search.py
```

---

### 4. `04-autocomplete-suggestions.py`
**Mavzu:** Autocomplete va suggestions

**O'rganasiz:**
- Prefix queries
- Completion suggester
- N-gram tokenizer
- Edge n-gram analyzer

**Ishga tushirish:**
```bash
python 04-autocomplete-suggestions.py
```

---

### 5. `05-filtering-aggregations.py`
**Mavzu:** Filtering va aggregations

**O'rganasiz:**
- Range filters
- Term filters
- Bool filters
- Aggregations (metrics, buckets)
- Statistics

**Ishga tushirish:**
```bash
python 05-filtering-aggregations.py
```

---

## Prerequisites

### 1. Elasticsearch Running

```bash
# Docker bilan ishga tushirish
cd ..
docker-compose up -d

# Tekshirish
curl http://localhost:9200
```

### 2. Python Packages

```bash
# Virtual environment
pipenv shell

# Paketlarni o'rnatish
pipenv install elasticsearch==8.11.0
```

---

## Dependencies

```txt
elasticsearch==8.11.0
```

**O'rnatish:**
```bash
pipenv install elasticsearch
```

---

## Har bir misol uchun maqsad

| Fayl | Qiyinlik | Vaqt | Maqsad |
|------|----------|------|--------|
| 01-elasticsearch-basics.py | ⭐ | 15 min | Basic operations |
| 02-document-indexing.py | ⭐⭐ | 20 min | Bulk indexing |
| 03-full-text-search.py | ⭐⭐⭐ | 25 min | Search queries |
| 04-autocomplete-suggestions.py | ⭐⭐⭐ | 25 min | Autocomplete |
| 05-filtering-aggregations.py | ⭐⭐⭐⭐ | 30 min | Advanced features |

---

## Misollardan keyin

Ushbu misollarni o'rganganingizdan so'ng:

1.  Elasticsearch basic operations'ni bilasiz
2.  Index va document management'ni tushunasiz
3.  Full-text search qanday ishlashini bilasiz
4.  Autocomplete tizimini qura olasiz
5.  Filtering va aggregations'dan foydalanasiz
6.  Django'ga integratsiya qilishga tayyorsiz

**Keyingi qadam:** `code/library-project` da Django bilan amaliy qo'llash!

---

## Qo'shimcha Resurslar

### Documentation:
- [Elasticsearch Python Client](https://elasticsearch-py.readthedocs.io/)
- [Elasticsearch Reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)

### Tutorials:
- [Elasticsearch Tutorial](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html)
- [Full-text Search Best Practices](https://www.elastic.co/blog/practical-bm25-part-1-how-shards-affect-relevance-scoring-in-elasticsearch)

---

## ❓ Savol-Javoblar

**Q: Elasticsearch nima?**
A: Distributed, RESTful search and analytics engine

**Q: Index nima?**
A: Database'dagi table ga o'xshash - documentlar to'plami

**Q: Document nima?**
A: JSON formatdagi bitta yozuv (table'daki row)

**Q: Analyzer nima?**
A: Matnni tokenize qilish va qayta ishlash

**Q: Fuzzy search nima?**
A: Typo bilan qidiruv (pyton → python)

---

## O'rganish Yo'lxaritasi

```
1. 01-elasticsearch-basics.py
   ↓ (CRUD operations)
   
2. 02-document-indexing.py
   ↓ (Bulk indexing, mapping)
   
3. 03-full-text-search.py
   ↓ (Search queries, scoring)
   
4. 04-autocomplete-suggestions.py
   ↓ (Autocomplete, suggester)
   
5. 05-filtering-aggregations.py
   ↓ (Filtering, statistics)
   
6. Django implementation
   ↓ (library-project)
   
7. Production deployment
```

---

**Omad! Happy Searching!**