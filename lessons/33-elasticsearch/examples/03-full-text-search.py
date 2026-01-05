"""
Full-text Search - Advanced Queries and Relevance

Bu misolda:
- Multi-match query
- Field boosting
- Fuzzy search (typo tolerance)
- Bool queries (must, should, filter)
- Relevance scoring
"""

from elasticsearch import Elasticsearch

print("=" * 70)
print("FULL-TEXT SEARCH & RELEVANCE")
print("=" * 70)

# ==================== 1. CONNECTION ====================
print("\n1. ELASTICSEARCH CONNECTION")
print("-" * 70)

es = Elasticsearch(['http://localhost:9200'])

if es.ping():
    print("✅ Connected to Elasticsearch")
else:
    print("❌ Connection failed!")
    exit(1)

# Use index from previous example
index_name = 'books_with_mapping'

# Check if index exists
if not es.indices.exists(index=index_name):
    print(f"❌ Index '{index_name}' not found!")
    print(f"💡 Run 02-document-indexing.py first")
    exit(1)

print(f"✅ Using index: {index_name}")

# ==================== 2. SIMPLE MATCH QUERY ====================
print("\n\n2. SIMPLE MATCH QUERY")
print("-" * 70)

# Search for "django"
query = {
    'query': {
        'match': {
            'title': 'django'
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Search: 'django' in title")
print(f"   Found: {result['hits']['total']['value']} books")
print(f"   Took: {result['took']}ms\n")

for hit in result['hits']['hits']:
    print(f"   Score: {hit['_score']:.2f} - {hit['_source']['title']}")

# ==================== 3. MULTI-MATCH QUERY ====================
print("\n\n3. MULTI-MATCH QUERY")
print("-" * 70)

# Search across multiple fields
query = {
    'query': {
        'multi_match': {
            'query': 'python programming',
            'fields': ['title', 'description', 'author']
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Multi-match: 'python programming'")
print(f"   Fields: title, description, author")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits'][:5]:
    print(f"   Score: {hit['_score']:.2f} - {hit['_source']['title']}")

# ==================== 4. FIELD BOOSTING ====================
print("\n\n4. FIELD BOOSTING")
print("-" * 70)

# Boost title 3x, author 2x, description 1x
query = {
    'query': {
        'multi_match': {
            'query': 'django',
            'fields': ['title^3', 'author^2', 'description']
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Boosted search: 'django'")
print(f"   title^3 (3x boost)")
print(f"   author^2 (2x boost)")
print(f"   description (1x baseline)\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   Score: {hit['_score']:.2f} - {book['title']}")
    print(f"          by {book['author']}")

# ==================== 5. FUZZY SEARCH (TYPO TOLERANCE) ====================
print("\n\n5. FUZZY SEARCH - TYPO TOLERANCE")
print("-" * 70)

# Intentional typo: "pyton" instead of "python"
query = {
    'query': {
        'multi_match': {
            'query': 'pyton',  # TYPO!
            'fields': ['title', 'description'],
            'fuzziness': 'AUTO'
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Fuzzy search: 'pyton' (typo)")
print(f"   Fuzziness: AUTO (Levenshtein distance)")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits'][:3]:
    print(f"   Score: {hit['_score']:.2f} - {hit['_source']['title']}")

print(f"\n💡 Despite typo, found 'python' books!")

# ==================== 6. BOOL QUERY - MUST ====================
print("\n\n6. BOOL QUERY - MUST (AND)")
print("-" * 70)

# MUST have both "django" AND "web"
query = {
    'query': {
        'bool': {
            'must': [
                {'match': {'title': 'django'}},
                {'match': {'description': 'web'}}
            ]
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Bool Query (MUST):")
print(f"   MUST: title contains 'django'")
print(f"   AND: description contains 'web'")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    print(f"   Score: {hit['_score']:.2f} - {hit['_source']['title']}")

# ==================== 7. BOOL QUERY - SHOULD ====================
print("\n\n7. BOOL QUERY - SHOULD (OR)")
print("-" * 70)

# SHOULD have "django" OR "flask" (boosts if both)
query = {
    'query': {
        'bool': {
            'should': [
                {'match': {'title': 'django'}},
                {'match': {'title': 'flask'}}
            ]
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Bool Query (SHOULD):")
print(f"   SHOULD: title contains 'django' OR 'flask'")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    print(f"   Score: {hit['_score']:.2f} - {hit['_source']['title']}")

# ==================== 8. BOOL QUERY - FILTER ====================
print("\n\n8. BOOL QUERY - FILTER (No Scoring)")
print("-" * 70)

# Search "python" but FILTER price < 45
query = {
    'query': {
        'bool': {
            'must': [
                {'match': {'title': 'python'}}
            ],
            'filter': [
                {'range': {'price': {'lte': 45}}}
            ]
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Bool Query with Filter:")
print(f"   MUST: title contains 'python'")
print(f"   FILTER: price <= $45")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   Score: {hit['_score']:.2f} - {book['title']}")
    print(f"          Price: ${book['price']}")

# ==================== 9. BOOL QUERY - MUST_NOT ====================
print("\n\n9. BOOL QUERY - MUST_NOT (Exclusion)")
print("-" * 70)

# Search books but EXCLUDE "django"
query = {
    'query': {
        'bool': {
            'must': [
                {'match': {'category': 'Web Development'}}
            ],
            'must_not': [
                {'match': {'title': 'django'}}
            ]
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Bool Query (MUST_NOT):")
print(f"   MUST: category = 'Web Development'")
print(f"   MUST_NOT: title contains 'django'")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    print(f"   {hit['_source']['title']}")

# ==================== 10. COMPLEX BOOL QUERY ====================
print("\n\n10. COMPLEX BOOL QUERY")
print("-" * 70)

# Complex: must, should, filter, must_not combined
query = {
    'query': {
        'bool': {
            'must': [
                {'multi_match': {
                    'query': 'python',
                    'fields': ['title^3', 'description']
                }}
            ],
            'should': [
                {'match': {'author': 'Vincent'}},  # Boost if Vincent
                {'match': {'tags': 'beginner'}}    # Boost if beginner
            ],
            'filter': [
                {'range': {'price': {'gte': 30, 'lte': 50}}},
                {'term': {'in_stock': True}}
            ],
            'must_not': [
                {'match': {'category': 'Data Science'}}
            ]
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Complex Bool Query:")
print(f"   MUST: 'python' in title/description")
print(f"   SHOULD: by Vincent OR beginner tag (boosts score)")
print(f"   FILTER: $30-$50, in_stock=true")
print(f"   MUST_NOT: category != 'Data Science'")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   Score: {hit['_score']:.2f} - {book['title']}")
    print(f"          ${book['price']}, by {book['author']}")

# ==================== 11. MATCH PHRASE ====================
print("\n\n11. MATCH PHRASE (Exact Phrase)")
print("-" * 70)

# Search exact phrase
query = {
    'query': {
        'match_phrase': {
            'description': 'web applications'
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Match Phrase: 'web applications'")
print(f"   (Must appear in exact order)")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   {book['title']}")
    print(f"   Description: {book['description'][:80]}...")

# ==================== 12. HIGHLIGHTING ====================
print("\n\n12. SEARCH WITH HIGHLIGHTING")
print("-" * 70)

# Search with highlight
query = {
    'query': {
        'multi_match': {
            'query': 'django web',
            'fields': ['title', 'description']
        }
    },
    'highlight': {
        'fields': {
            'title': {},
            'description': {'fragment_size': 150}
        },
        'pre_tags': ['<mark>'],
        'post_tags': ['</mark>']
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Search with Highlighting: 'django web'")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits'][:2]:
    book = hit['_source']
    print(f"   {book['title']}")
    
    if 'highlight' in hit:
        if 'title' in hit['highlight']:
            print(f"   Title: {hit['highlight']['title'][0]}")
        if 'description' in hit['highlight']:
            print(f"   Desc: {hit['highlight']['description'][0]}")
    print()

# ==================== SUMMARY ====================
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
✅ Match Query: Simple search
✅ Multi-match: Search multiple fields
✅ Boosting: title^3 > author^2 > description
✅ Fuzzy: Typo tolerance (pyton → python)
✅ Bool Must: AND condition
✅ Bool Should: OR condition (boosts)
✅ Bool Filter: Filter without scoring
✅ Bool Must_Not: Exclude results
✅ Match Phrase: Exact phrase order
✅ Highlighting: Mark matched terms

QUERY TYPES:
┌─────────────┬────────────────────────────┐
│ Query       │ Use Case                   │
├─────────────┼────────────────────────────┤
│ match       │ Single field search        │
│ multi_match │ Multiple fields search     │
│ match_phrase│ Exact phrase order         │
│ bool        │ Combine multiple queries   │
│ fuzzy       │ Typo tolerance             │
│ range       │ Numeric/date ranges        │
│ term        │ Exact keyword match        │
└─────────────┴────────────────────────────┘

BOOL QUERY:
┌──────────┬────────────────────────────────┐
│ Clause   │ Behavior                       │
├──────────┼────────────────────────────────┤
│ must     │ AND, affects score             │
│ should   │ OR, boosts score               │
│ filter   │ AND, no score (fast, cached)   │
│ must_not │ NOT, excludes                  │
└──────────┴────────────────────────────────┘

NEXT STEPS:
- 04-autocomplete-suggestions.py - Autocomplete
- 05-filtering-aggregations.py - Analytics
""")

print("=" * 70)