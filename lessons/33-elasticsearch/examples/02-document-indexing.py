"""
Document Indexing - Bulk Operations and Mapping

Bu misolda:
- Custom mapping yaratish
- Analyzers configuration
- Bulk indexing
- Field types
"""

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime
import json

print("=" * 70)
print("DOCUMENT INDEXING & MAPPING")
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

# ==================== 2. CUSTOM MAPPING ====================
print("\n\n2. CUSTOM MAPPING DEFINITION")
print("-" * 70)

index_name = 'books_with_mapping'

# Delete if exists
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"🗑️  Deleted existing index")

# Custom mapping
mapping = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0,
        'analysis': {
            'analyzer': {
                'custom_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ['lowercase', 'asciifolding', 'stop']
                }
            }
        }
    },
    'mappings': {
        'properties': {
            'title': {
                'type': 'text',
                'analyzer': 'custom_analyzer',
                'fields': {
                    'raw': {
                        'type': 'keyword'
                    },
                    'suggest': {
                        'type': 'completion'
                    }
                }
            },
            'author': {
                'type': 'text',
                'fields': {
                    'raw': {
                        'type': 'keyword'
                    }
                }
            },
            'description': {
                'type': 'text',
                'analyzer': 'custom_analyzer'
            },
            'isbn': {
                'type': 'keyword'
            },
            'price': {
                'type': 'float'
            },
            'pages': {
                'type': 'integer'
            },
            'published_date': {
                'type': 'date',
                'format': 'yyyy-MM-dd'
            },
            'category': {
                'type': 'text',
                'fields': {
                    'raw': {
                        'type': 'keyword'
                    }
                }
            },
            'in_stock': {
                'type': 'boolean'
            },
            'rating': {
                'type': 'float'
            },
            'tags': {
                'type': 'keyword'
            },
            'created_at': {
                'type': 'date'
            }
        }
    }
}

# Create index with mapping
es.indices.create(index=index_name, body=mapping)
print(f"✅ Index created with custom mapping: {index_name}")

# Show mapping
index_mapping = es.indices.get_mapping(index=index_name)
print(f"\n📋 Mapping configured:")
print(f"   Fields: {len(index_mapping[index_name]['mappings']['properties'])}")
print(f"   Title type: {index_mapping[index_name]['mappings']['properties']['title']['type']}")
print(f"   Price type: {index_mapping[index_name]['mappings']['properties']['price']['type']}")

# ==================== 3. FIELD TYPES EXPLANATION ====================
print("\n\n3. FIELD TYPES TUSHUNTIRISH")
print("-" * 70)

field_types = {
    'text': 'Full-text search (analyzed, tokenized)',
    'keyword': 'Exact match (not analyzed)',
    'integer': 'Whole numbers',
    'float': 'Decimal numbers',
    'boolean': 'true/false',
    'date': 'Date values',
    'completion': 'Autocomplete suggestions'
}

print("📚 Field Types:")
for field_type, description in field_types.items():
    print(f"   {field_type:12} - {description}")

# ==================== 4. SAMPLE DATA ====================
print("\n\n4. SAMPLE DATA PREPARATION")
print("-" * 70)

books = [
    {
        'title': 'Python Crash Course',
        'author': 'Eric Matthes',
        'description': 'A hands-on, project-based introduction to programming',
        'isbn': '978-1593279288',
        'price': 39.99,
        'pages': 544,
        'published_date': '2019-05-03',
        'category': 'Programming',
        'in_stock': True,
        'rating': 4.5,
        'tags': ['python', 'programming', 'beginner'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Django for Beginners',
        'author': 'William Vincent',
        'description': 'Build websites with Python and Django',
        'isbn': '978-1735467207',
        'price': 39.00,
        'pages': 354,
        'published_date': '2021-01-28',
        'category': 'Web Development',
        'in_stock': True,
        'rating': 4.8,
        'tags': ['django', 'web', 'python'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Learning Python',
        'author': 'Mark Lutz',
        'description': 'Powerful object-oriented programming',
        'isbn': '978-1449355739',
        'price': 49.99,
        'pages': 1600,
        'published_date': '2013-07-06',
        'category': 'Programming',
        'in_stock': True,
        'rating': 4.3,
        'tags': ['python', 'advanced', 'oop'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Two Scoops of Django',
        'author': 'Daniel Greenfeld',
        'description': 'Best practices for Django development',
        'isbn': '978-0692915727',
        'price': 45.00,
        'pages': 532,
        'published_date': '2017-11-15',
        'category': 'Web Development',
        'in_stock': False,
        'rating': 4.7,
        'tags': ['django', 'best-practices', 'advanced'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Flask Web Development',
        'author': 'Miguel Grinberg',
        'description': 'Developing web applications with Python',
        'isbn': '978-1491991732',
        'price': 44.99,
        'pages': 316,
        'published_date': '2018-03-05',
        'category': 'Web Development',
        'in_stock': True,
        'rating': 4.6,
        'tags': ['flask', 'web', 'python'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Automate the Boring Stuff with Python',
        'author': 'Al Sweigart',
        'description': 'Practical programming for total beginners',
        'isbn': '978-1593279929',
        'price': 34.99,
        'pages': 592,
        'published_date': '2019-11-12',
        'category': 'Programming',
        'in_stock': True,
        'rating': 4.7,
        'tags': ['python', 'automation', 'beginner'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Effective Python',
        'author': 'Brett Slatkin',
        'description': '90 specific ways to write better Python',
        'isbn': '978-0134853987',
        'price': 42.99,
        'pages': 352,
        'published_date': '2019-11-13',
        'category': 'Programming',
        'in_stock': True,
        'rating': 4.4,
        'tags': ['python', 'best-practices', 'advanced'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'REST APIs with Django',
        'author': 'William Vincent',
        'description': 'Build powerful web APIs with Django REST framework',
        'isbn': '978-1735467214',
        'price': 39.00,
        'pages': 298,
        'published_date': '2022-02-15',
        'category': 'Web Development',
        'in_stock': True,
        'rating': 4.9,
        'tags': ['django', 'rest', 'api', 'web'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Python for Data Analysis',
        'author': 'Wes McKinney',
        'description': 'Data wrangling with pandas, NumPy, and IPython',
        'isbn': '978-1491957660',
        'price': 54.99,
        'pages': 544,
        'published_date': '2017-09-25',
        'category': 'Data Science',
        'in_stock': True,
        'rating': 4.6,
        'tags': ['python', 'data-science', 'pandas'],
        'created_at': datetime.now().isoformat()
    },
    {
        'title': 'Django 3 By Example',
        'author': 'Antonio Mele',
        'description': 'Build powerful and reliable Python web applications',
        'isbn': '978-1838981952',
        'price': 44.99,
        'pages': 568,
        'published_date': '2020-03-31',
        'category': 'Web Development',
        'in_stock': True,
        'rating': 4.5,
        'tags': ['django', 'web', 'projects'],
        'created_at': datetime.now().isoformat()
    }
]

print(f"📚 Prepared {len(books)} books for indexing")

# ==================== 5. BULK INDEXING ====================
print("\n\n5. BULK INDEXING")
print("-" * 70)

# Prepare bulk actions
actions = [
    {
        '_index': index_name,
        '_id': f'book_{i}',
        '_source': book
    }
    for i, book in enumerate(books, 1)
]

# Bulk index
success, failed = bulk(es, actions, stats_only=True)

print(f"✅ Bulk indexing completed:")
print(f"   Success: {success}")
print(f"   Failed: {failed}")

# Wait for indexing
es.indices.refresh(index=index_name)

# ==================== 6. VERIFY INDEXED DATA ====================
print("\n\n6. VERIFY INDEXED DATA")
print("-" * 70)

# Count documents
count = es.count(index=index_name)
print(f"📊 Total documents: {count['count']}")

# Get all documents
result = es.search(index=index_name, body={'query': {'match_all': {}}}, size=20)

print(f"\n📚 Indexed Books:")
for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   {hit['_id']}: {book['title']} - ${book['price']}")

# ==================== 7. ANALYZERS IN ACTION ====================
print("\n\n7. ANALYZERS IN ACTION")
print("-" * 70)

# Analyze text
analyze_body = {
    'analyzer': 'custom_analyzer',
    'text': 'Django REST Framework'
}

result = es.indices.analyze(index=index_name, body=analyze_body)

print("🔍 Analyzing: 'Django REST Framework'")
print("   Tokens:")
for token in result['tokens']:
    print(f"   - {token['token']} (position: {token['position']})")

# ==================== 8. MULTI-FIELD SEARCH ====================
print("\n\n8. MULTI-FIELD TESTING")
print("-" * 70)

# Search in title (text field - analyzed)
query1 = {
    'query': {
        'match': {
            'title': 'django'
        }
    }
}

result = es.search(index=index_name, body=query1)
print(f"🔍 Search 'django' in title (text field):")
print(f"   Found: {result['hits']['total']['value']} books")

# Search in title.raw (keyword field - exact match)
query2 = {
    'query': {
        'term': {
            'title.raw': 'Django for Beginners'
        }
    }
}

result = es.search(index=index_name, body=query2)
print(f"\n🔍 Exact match 'Django for Beginners' (keyword field):")
print(f"   Found: {result['hits']['total']['value']} books")

# ==================== 9. COMPLETION SUGGESTER ====================
print("\n\n9. COMPLETION SUGGESTER TEST")
print("-" * 70)

# Suggestion query
suggest_body = {
    'suggest': {
        'book-suggest': {
            'prefix': 'dja',
            'completion': {
                'field': 'title.suggest',
                'size': 5
            }
        }
    }
}

result = es.search(index=index_name, body=suggest_body)

print("💡 Suggestions for 'dja':")
if 'suggest' in result:
    for option in result['suggest']['book-suggest'][0]['options']:
        print(f"   - {option['text']}")

# ==================== 10. STATISTICS ====================
print("\n\n10. INDEX STATISTICS")
print("-" * 70)

# Get statistics
stats = es.indices.stats(index=index_name)

print(f"📊 Index Statistics:")
print(f"   Documents: {stats['_all']['primaries']['docs']['count']}")
print(f"   Store size: {stats['_all']['primaries']['store']['size_in_bytes']} bytes")
print(f"   Indexing operations: {stats['_all']['primaries']['indexing']['index_total']}")
print(f"   Search operations: {stats['_all']['primaries']['search']['query_total']}")

# ==================== SUMMARY ====================
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
✅ Custom Mapping: Configured
✅ Analyzers: Custom analyzer created
✅ Field Types: Multiple types used
✅ Bulk Indexing: 10 books indexed
✅ Multi-field: text + keyword fields
✅ Completion Field: Suggestions ready

KEY CONCEPTS:
- text field: Full-text search (analyzed)
- keyword field: Exact match (not analyzed)
- Multi-field: Same data, multiple types
- Bulk API: Fast bulk operations
- Custom analyzer: Lowercase + stop words
- Completion field: Autocomplete suggestions

FIELD STRUCTURE:
title (text)
  ├─ title (analyzed for search)
  ├─ title.raw (keyword for exact match)
  └─ title.suggest (completion for autocomplete)

NEXT STEPS:
- 03-full-text-search.py - Advanced queries
- 04-autocomplete-suggestions.py - More suggestions
""")

print("=" * 70)