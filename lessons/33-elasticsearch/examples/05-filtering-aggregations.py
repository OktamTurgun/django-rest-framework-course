"""
Filtering & Aggregations - Analytics and Statistics

Bu misolda:
- Range filters (price, pages, date)
- Term filters (exact match)
- Bool filters (combinations)
- Aggregations (metrics: avg, min, max, sum)
- Bucket aggregations (grouping)
"""

from elasticsearch import Elasticsearch
from datetime import datetime

print("=" * 70)
print("FILTERING & AGGREGATIONS")
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

index_name = 'books_with_mapping'

if not es.indices.exists(index=index_name):
    print(f"❌ Index '{index_name}' not found!")
    print(f"💡 Run 02-document-indexing.py first")
    exit(1)

print(f"✅ Using index: {index_name}")

# ==================== 2. RANGE FILTER - PRICE ====================
print("\n\n2. RANGE FILTER - PRICE")
print("-" * 70)

# Books between $30-$45
query = {
    'query': {
        'range': {
            'price': {
                'gte': 30,
                'lte': 45
            }
        }
    },
    'sort': [
        {'price': {'order': 'asc'}}
    ]
}

result = es.search(index=index_name, body=query)

print(f"💰 Books between $30-$45:")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   ${book['price']:5.2f} - {book['title']}")

# ==================== 3. RANGE FILTER - PAGES ====================
print("\n\n3. RANGE FILTER - PAGES")
print("-" * 70)

# Books with 300-600 pages
query = {
    'query': {
        'range': {
            'pages': {
                'gte': 300,
                'lte': 600
            }
        }
    },
    'sort': [
        {'pages': {'order': 'desc'}}
    ]
}

result = es.search(index=index_name, body=query)

print(f"📖 Books with 300-600 pages:")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   {book['pages']:4d} pages - {book['title']}")

# ==================== 4. TERM FILTER - CATEGORY ====================
print("\n\n4. TERM FILTER - CATEGORY")
print("-" * 70)

# Exact match: category = "Web Development"
query = {
    'query': {
        'term': {
            'category.raw': 'Web Development'
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🌐 Category = 'Web Development':")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   - {book['title']}")

# ==================== 5. TERMS FILTER - MULTIPLE VALUES ====================
print("\n\n5. TERMS FILTER - MULTIPLE CATEGORIES")
print("-" * 70)

# Match multiple categories
query = {
    'query': {
        'terms': {
            'category.raw': ['Programming', 'Data Science']
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"📚 Categories: 'Programming' OR 'Data Science':")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   [{book['category']:15}] {book['title']}")

# ==================== 6. BOOL FILTER - COMBINATION ====================
print("\n\n6. BOOL FILTER - MULTIPLE CONDITIONS")
print("-" * 70)

# Complex filter: $30-$50, in_stock, Programming category
query = {
    'query': {
        'bool': {
            'filter': [
                {'range': {'price': {'gte': 30, 'lte': 50}}},
                {'term': {'in_stock': True}},
                {'term': {'category.raw': 'Programming'}}
            ]
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Complex Filter:")
print(f"   - Price: $30-$50")
print(f"   - In stock: Yes")
print(f"   - Category: Programming")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   ${book['price']} - {book['title']}")

# ==================== 7. METRIC AGGREGATIONS ====================
print("\n\n7. METRIC AGGREGATIONS - STATISTICS")
print("-" * 70)

# Price statistics
query = {
    'size': 0,  # Don't need documents, just aggregations
    'aggs': {
        'price_stats': {
            'stats': {
                'field': 'price'
            }
        },
        'avg_price': {
            'avg': {
                'field': 'price'
            }
        },
        'min_price': {
            'min': {
                'field': 'price'
            }
        },
        'max_price': {
            'max': {
                'field': 'price'
            }
        },
        'sum_price': {
            'sum': {
                'field': 'price'
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"💰 Price Statistics:")
stats = result['aggregations']['price_stats']
print(f"   Count:   {stats['count']}")
print(f"   Average: ${stats['avg']:.2f}")
print(f"   Min:     ${stats['min']:.2f}")
print(f"   Max:     ${stats['max']:.2f}")
print(f"   Sum:     ${stats['sum']:.2f}")

# ==================== 8. BUCKET AGGREGATION - BY CATEGORY ====================
print("\n\n8. BUCKET AGGREGATION - BY CATEGORY")
print("-" * 70)

# Group by category
query = {
    'size': 0,
    'aggs': {
        'categories': {
            'terms': {
                'field': 'category.raw',
                'size': 10
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"📚 Books by Category:")

for bucket in result['aggregations']['categories']['buckets']:
    print(f"   {bucket['key']:20} : {bucket['doc_count']} books")

# ==================== 9. BUCKET AGGREGATION - BY AUTHOR ====================
print("\n\n9. BUCKET AGGREGATION - TOP AUTHORS")
print("-" * 70)

# Top authors by book count
query = {
    'size': 0,
    'aggs': {
        'top_authors': {
            'terms': {
                'field': 'author.raw',
                'size': 5,
                'order': {'_count': 'desc'}
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"✍️  Top 5 Authors:")

for i, bucket in enumerate(result['aggregations']['top_authors']['buckets'], 1):
    print(f"   {i}. {bucket['key']:25} - {bucket['doc_count']} book(s)")

# ==================== 10. NESTED AGGREGATION ====================
print("\n\n10. NESTED AGGREGATION - AVG PRICE BY CATEGORY")
print("-" * 70)

# Average price per category
query = {
    'size': 0,
    'aggs': {
        'categories': {
            'terms': {
                'field': 'category.raw'
            },
            'aggs': {
                'avg_price': {
                    'avg': {
                        'field': 'price'
                    }
                }
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"💰 Average Price by Category:")

for bucket in result['aggregations']['categories']['buckets']:
    category = bucket['key']
    count = bucket['doc_count']
    avg_price = bucket['avg_price']['value']
    print(f"   {category:20} : ${avg_price:5.2f} (from {count} books)")

# ==================== 11. HISTOGRAM AGGREGATION ====================
print("\n\n11. HISTOGRAM - PRICE DISTRIBUTION")
print("-" * 70)

# Price histogram (buckets of $10)
query = {
    'size': 0,
    'aggs': {
        'price_histogram': {
            'histogram': {
                'field': 'price',
                'interval': 10,
                'min_doc_count': 1
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"📊 Price Distribution (by $10):")

for bucket in result['aggregations']['price_histogram']['buckets']:
    price_range = f"${bucket['key']:.0f}-${bucket['key']+10:.0f}"
    count = bucket['doc_count']
    bar = '█' * count
    print(f"   {price_range:15} : {bar} ({count})")

# ==================== 12. FILTERING AGGREGATION ====================
print("\n\n12. FILTERED AGGREGATION")
print("-" * 70)

# Average price of in-stock programming books
query = {
    'size': 0,
    'query': {
        'bool': {
            'filter': [
                {'term': {'in_stock': True}},
                {'term': {'category.raw': 'Programming'}}
            ]
        }
    },
    'aggs': {
        'avg_price': {
            'avg': {
                'field': 'price'
            }
        },
        'count': {
            'value_count': {
                'field': 'price'
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 In-stock Programming Books:")
print(f"   Count:        {result['aggregations']['count']['value']}")
print(f"   Average Price: ${result['aggregations']['avg_price']['value']:.2f}")

# ==================== 13. DATE HISTOGRAM ====================
print("\n\n13. DATE HISTOGRAM - PUBLICATIONS BY YEAR")
print("-" * 70)

# Publications by year
query = {
    'size': 0,
    'aggs': {
        'publications_by_year': {
            'date_histogram': {
                'field': 'published_date',
                'calendar_interval': 'year',
                'format': 'yyyy'
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"📅 Books Published by Year:")

for bucket in result['aggregations']['publications_by_year']['buckets']:
    if bucket['doc_count'] > 0:
        year = bucket['key_as_string']
        count = bucket['doc_count']
        bar = '█' * count
        print(f"   {year} : {bar} ({count})")

# ==================== 14. PERCENTILES ====================
print("\n\n14. PERCENTILES - PRICE DISTRIBUTION")
print("-" * 70)

# Price percentiles
query = {
    'size': 0,
    'aggs': {
        'price_percentiles': {
            'percentiles': {
                'field': 'price',
                'percents': [25, 50, 75, 95]
            }
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"📊 Price Percentiles:")
percentiles = result['aggregations']['price_percentiles']['values']

for percent, value in percentiles.items():
    print(f"   {percent:5}th : ${value:.2f}")

# ==================== 15. COMPLETE ANALYTICS DASHBOARD ====================
print("\n\n15. COMPLETE ANALYTICS DASHBOARD")
print("-" * 70)

# Complex aggregation with multiple metrics
query = {
    'size': 0,
    'aggs': {
        'total_books': {
            'value_count': {'field': 'title.raw'}
        },
        'total_value': {
            'sum': {'field': 'price'}
        },
        'avg_price': {
            'avg': {'field': 'price'}
        },
        'avg_pages': {
            'avg': {'field': 'pages'}
        },
        'avg_rating': {
            'avg': {'field': 'rating'}
        },
        'categories': {
            'terms': {
                'field': 'category.raw',
                'size': 10
            },
            'aggs': {
                'avg_price': {'avg': {'field': 'price'}},
                'avg_rating': {'avg': {'field': 'rating'}}
            }
        },
        'price_ranges': {
            'range': {
                'field': 'price',
                'ranges': [
                    {'key': 'Budget', 'to': 35},
                    {'key': 'Standard', 'from': 35, 'to': 45},
                    {'key': 'Premium', 'from': 45}
                ]
            }
        }
    }
}

result = es.search(index=index_name, body=query)
aggs = result['aggregations']

print(f"📊 COMPLETE ANALYTICS DASHBOARD")
print(f"=" * 70)

print(f"\n📚 Overview:")
print(f"   Total Books:  {aggs['total_books']['value']}")
print(f"   Total Value:  ${aggs['total_value']['value']:.2f}")
print(f"   Average Price: ${aggs['avg_price']['value']:.2f}")
print(f"   Average Pages: {aggs['avg_pages']['value']:.0f}")
print(f"   Average Rating: {aggs['avg_rating']['value']:.1f}/5.0")

print(f"\n📁 By Category:")
for bucket in aggs['categories']['buckets']:
    print(f"   {bucket['key']:20} - {bucket['doc_count']} books")
    print(f"   {'':20}   Avg Price: ${bucket['avg_price']['value']:.2f}")
    print(f"   {'':20}   Avg Rating: {bucket['avg_rating']['value']:.1f}/5")

print(f"\n💰 Price Ranges:")
for bucket in aggs['price_ranges']['buckets']:
    print(f"   {bucket['key']:12} : {bucket['doc_count']} books")

# ==================== SUMMARY ====================
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
✅ Range Filters: Price, pages, date ranges
✅ Term Filters: Exact match (category, in_stock)
✅ Bool Filters: Combine multiple conditions
✅ Metric Aggregations: avg, min, max, sum, stats
✅ Bucket Aggregations: Group by category, author
✅ Nested Aggregations: Avg price per category
✅ Histogram: Price and date distributions
✅ Percentiles: Statistical distribution
✅ Complete Dashboard: All metrics combined

AGGREGATION TYPES:
┌───────────────┬────────────────────────────────┐
│ Type          │ Use Case                       │
├───────────────┼────────────────────────────────┤
│ avg           │ Average value                  │
│ sum           │ Total sum                      │
│ min/max       │ Minimum/Maximum                │
│ stats         │ All statistics at once         │
│ terms         │ Group by field values          │
│ histogram     │ Numeric distribution           │
│ date_histogram│ Time-based distribution        │
│ percentiles   │ Statistical percentiles        │
│ range         │ Custom ranges                  │
└───────────────┴────────────────────────────────┘

FILTER vs QUERY:
- Filter: YES/NO, cached, no scoring, FAST
- Query: Relevance scoring, slower

USE CASES:
- Filter: Price ranges, category selection
- Query: Full-text search
- Aggregations: Statistics, analytics, reporting

PERFORMANCE TIPS:
- Use filters instead of queries when possible
- Cache filters automatically
- Set size=0 for aggregation-only queries
- Use appropriate interval for histograms
- Limit bucket size (top 10, not all)

NEXT:
- Implement in Django
- Build real-time dashboard
- Add to production application
""")

print("=" * 70)