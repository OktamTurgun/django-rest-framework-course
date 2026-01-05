"""
Elasticsearch Basics - Connection, Index, CRUD Operations

Bu misolda:
- Elasticsearch'ga ulanish
- Index yaratish va o'chirish
- Document CRUD operations
- Basic queries
"""

from elasticsearch import Elasticsearch
from datetime import datetime
import json

print("=" * 70)
print("ELASTICSEARCH BASICS")
print("=" * 70)

# ==================== 1. CONNECTION ====================
print("\n1. ELASTICSEARCH CONNECTION")
print("-" * 70)

# Create client
es = Elasticsearch(
    ['http://localhost:9200'],
    request_timeout=30
)

# Check connection
if es.ping():
    print("✅ Connected to Elasticsearch")
    
    # Get cluster info
    info = es.info()
    print(f"✅ Cluster: {info['cluster_name']}")
    print(f"✅ Version: {info['version']['number']}")
else:
    print("❌ Connection failed!")
    exit(1)

# ==================== 2. INDEX MANAGEMENT ====================
print("\n\n2. INDEX MANAGEMENT")
print("-" * 70)

index_name = 'books_demo'

# Delete index if exists (clean slate)
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"🗑️  Deleted existing index: {index_name}")

# Create index
es.indices.create(index=index_name)
print(f"✅ Created index: {index_name}")

# Get index info
index_info = es.indices.get(index=index_name)
print(f"📊 Index settings:")
print(f"   Shards: {index_info[index_name]['settings']['index']['number_of_shards']}")
print(f"   Replicas: {index_info[index_name]['settings']['index']['number_of_replicas']}")

# ==================== 3. CREATE DOCUMENTS ====================
print("\n\n3. CREATE DOCUMENTS")
print("-" * 70)

# Single document
doc1 = {
    'title': 'Python Crash Course',
    'author': 'Eric Matthes',
    'isbn': '978-1593279288',
    'price': 39.99,
    'pages': 544,
    'published_date': '2019-05-03',
    'category': 'Programming',
    'description': 'A hands-on, project-based introduction to programming',
    'in_stock': True,
    'rating': 4.5,
    'timestamp': datetime.now().isoformat()
}

# Index document (with auto ID)
response = es.index(index=index_name, document=doc1)
print(f"✅ Document created:")
print(f"   ID: {response['_id']}")
print(f"   Result: {response['result']}")

# Index document with specific ID
doc2 = {
    'title': 'Django for Beginners',
    'author': 'William Vincent',
    'isbn': '978-1735467207',
    'price': 39.00,
    'pages': 354,
    'published_date': '2021-01-28',
    'category': 'Web Development',
    'description': 'Build websites with Python and Django',
    'in_stock': True,
    'rating': 4.8,
    'timestamp': datetime.now().isoformat()
}

response = es.index(index=index_name, id='book_1', document=doc2)
print(f"\n✅ Document created with ID:")
print(f"   ID: {response['_id']}")
print(f"   Result: {response['result']}")

# Add more books
books = [
    {
        'title': 'Learning Python',
        'author': 'Mark Lutz',
        'isbn': '978-1449355739',
        'price': 49.99,
        'pages': 1600,
        'published_date': '2013-07-06',
        'category': 'Programming',
        'description': 'Powerful object-oriented programming',
        'in_stock': True,
        'rating': 4.3
    },
    {
        'title': 'Two Scoops of Django',
        'author': 'Daniel Greenfeld',
        'isbn': '978-0692915727',
        'price': 45.00,
        'pages': 532,
        'published_date': '2017-11-15',
        'category': 'Web Development',
        'description': 'Best practices for Django',
        'in_stock': False,
        'rating': 4.7
    }
]

for book in books:
    book['timestamp'] = datetime.now().isoformat()
    response = es.index(index=index_name, document=book)
    print(f"✅ Added: {book['title']}")

# ==================== 4. READ DOCUMENTS ====================
print("\n\n4. READ DOCUMENTS")
print("-" * 70)

# Get by ID
doc = es.get(index=index_name, id='book_1')
print(f"📖 Document by ID:")
print(f"   Title: {doc['_source']['title']}")
print(f"   Author: {doc['_source']['author']}")
print(f"   Price: ${doc['_source']['price']}")

# Search all documents
search_result = es.search(index=index_name, query={'match_all': {}})
print(f"\n📚 Total documents: {search_result['hits']['total']['value']}")

print(f"\n📖 All books:")
for hit in search_result['hits']['hits']:
    book = hit['_source']
    print(f"   - {book['title']} by {book['author']}")

# ==================== 5. UPDATE DOCUMENTS ====================
print("\n\n5. UPDATE DOCUMENTS")
print("-" * 70)

# Partial update
update_data = {
    'doc': {
        'price': 35.99,
        'discount': 10
    }
}

response = es.update(index=index_name, id='book_1', body=update_data)
print(f"✅ Document updated:")
print(f"   ID: {response['_id']}")
print(f"   Result: {response['result']}")

# Get updated document
doc = es.get(index=index_name, id='book_1')
print(f"   New price: ${doc['_source']['price']}")
print(f"   Discount: {doc['_source']['discount']}%")

# ==================== 6. SEARCH QUERIES ====================
print("\n\n6. BASIC SEARCH QUERIES")
print("-" * 70)

# Search by field (match query)
search_query = {
    'query': {
        'match': {
            'title': 'python'
        }
    }
}

result = es.search(index=index_name, body=search_query)
print(f"🔍 Search 'python' in title:")
print(f"   Found: {result['hits']['total']['value']} books")
for hit in result['hits']['hits']:
    print(f"   - {hit['_source']['title']} (score: {hit['_score']})")

# Range query (price)
range_query = {
    'query': {
        'range': {
            'price': {
                'gte': 40,
                'lte': 50
            }
        }
    }
}

result = es.search(index=index_name, body=range_query)
print(f"\n🔍 Books between $40-$50:")
print(f"   Found: {result['hits']['total']['value']} books")
for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   - {book['title']}: ${book['price']}")

# Term query (exact match)
term_query = {
    'query': {
        'term': {
            'category.keyword': 'Web Development'
        }
    }
}

result = es.search(index=index_name, body=term_query)
print(f"\n🔍 Category = 'Web Development':")
print(f"   Found: {result['hits']['total']['value']} books")
for hit in result['hits']['hits']:
    print(f"   - {hit['_source']['title']}")

# ==================== 7. DELETE DOCUMENTS ====================
print("\n\n7. DELETE DOCUMENTS")
print("-" * 70)

# Delete by ID
# response = es.delete(index=index_name, id='book_1')
# print(f"🗑️  Document deleted: {response['result']}")

# Delete by query
delete_query = {
    'query': {
        'match': {
            'in_stock': False
        }
    }
}

response = es.delete_by_query(index=index_name, body=delete_query)
print(f"🗑️  Deleted out-of-stock books:")
print(f"   Deleted: {response['deleted']} documents")

# Count remaining
count = es.count(index=index_name)
print(f"📊 Remaining documents: {count['count']}")

# ==================== 8. STATISTICS ====================
print("\n\n8. INDEX STATISTICS")
print("-" * 70)

# Index stats
stats = es.indices.stats(index=index_name)
print(f"📊 Index Statistics:")
print(f"   Total docs: {stats['_all']['primaries']['docs']['count']}")
print(f"   Deleted docs: {stats['_all']['primaries']['docs']['deleted']}")
print(f"   Store size: {stats['_all']['primaries']['store']['size_in_bytes']} bytes")

# ==================== 9. AGGREGATIONS ====================
print("\n\n9. SIMPLE AGGREGATIONS")
print("-" * 70)

# Average price
agg_query = {
    'size': 0,
    'aggs': {
        'avg_price': {
            'avg': {
                'field': 'price'
            }
        },
        'max_price': {
            'max': {
                'field': 'price'
            }
        },
        'min_price': {
            'min': {
                'field': 'price'
            }
        }
    }
}

result = es.search(index=index_name, body=agg_query)
print(f"💰 Price Statistics:")
print(f"   Average: ${result['aggregations']['avg_price']['value']:.2f}")
print(f"   Max: ${result['aggregations']['max_price']['value']:.2f}")
print(f"   Min: ${result['aggregations']['min_price']['value']:.2f}")

# Books by category
category_agg = {
    'size': 0,
    'aggs': {
        'categories': {
            'terms': {
                'field': 'category.keyword'
            }
        }
    }
}

result = es.search(index=index_name, body=category_agg)
print(f"\n📚 Books by Category:")
for bucket in result['aggregations']['categories']['buckets']:
    print(f"   - {bucket['key']}: {bucket['doc_count']} books")

# ==================== 10. CLEANUP ====================
print("\n\n10. CLEANUP")
print("-" * 70)

# Uncomment to delete index
# es.indices.delete(index=index_name)
# print(f"🗑️  Index deleted: {index_name}")

print(f"✅ Index kept for inspection: {index_name}")
print(f"💡 View at: http://localhost:9200/{index_name}/_search?pretty")

# ==================== SUMMARY ====================
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
✅ Connection: Established
✅ Index: Created and managed
✅ CRUD: Create, Read, Update, Delete
✅ Search: Match, range, term queries
✅ Aggregations: Statistics calculated
✅ Cleanup: Index ready for inspection

KEY OPERATIONS:
- es.index() - Add document
- es.get() - Get by ID
- es.update() - Update document
- es.delete() - Delete by ID
- es.search() - Search documents
- es.delete_by_query() - Delete multiple

QUERY TYPES:
- match_all: Get everything
- match: Full-text search
- term: Exact match
- range: Numeric/date range

NEXT STEPS:
- 02-document-indexing.py - Bulk operations
- 03-full-text-search.py - Advanced queries
""")

print("=" * 70)