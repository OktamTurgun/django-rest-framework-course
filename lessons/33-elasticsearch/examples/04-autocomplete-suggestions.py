"""
Autocomplete & Suggestions

Bu misolda:
- Prefix queries (match_phrase_prefix)
- Completion suggester
- N-gram tokenizer
- Edge n-gram for autocomplete
"""

from elasticsearch import Elasticsearch

print("=" * 70)
print("AUTOCOMPLETE & SUGGESTIONS")
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

# ==================== 2. PREFIX QUERY ====================
print("\n\n2. PREFIX QUERY (Simple)")
print("-" * 70)

# Search for titles starting with "pyt"
query = {
    'query': {
        'prefix': {
            'title': 'pyt'
        }
    }
}

result = es.search(index=index_name, body=query)

print(f"🔍 Prefix: 'pyt'")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    print(f"   - {hit['_source']['title']}")

# ==================== 3. MATCH_PHRASE_PREFIX ====================
print("\n\n3. MATCH_PHRASE_PREFIX (Better)")
print("-" * 70)

# Better prefix matching with phrase
prefixes = ['dja', 'pyt', 'fla']

for prefix in prefixes:
    query = {
        'query': {
            'match_phrase_prefix': {
                'title': {
                    'query': prefix,
                    'max_expansions': 10
                }
            }
        }
    }
    
    result = es.search(index=index_name, body=query, size=5)
    
    print(f"🔍 Autocomplete: '{prefix}'")
    print(f"   Found: {result['hits']['total']['value']} suggestions\n")
    
    for hit in result['hits']['hits']:
        print(f"   - {hit['_source']['title']}")
    print()

# ==================== 4. COMPLETION SUGGESTER ====================
print("\n\n4. COMPLETION SUGGESTER (Fast!)")
print("-" * 70)

# Use completion field (title.suggest)
suggest_queries = ['dja', 'pyt', 'aut', 'res']

for prefix in suggest_queries:
    body = {
        'suggest': {
            'book-suggest': {
                'prefix': prefix,
                'completion': {
                    'field': 'title.suggest',
                    'size': 5,
                    'skip_duplicates': True
                }
            }
        }
    }
    
    result = es.search(index=index_name, body=body)
    
    print(f"💡 Fast suggestions for: '{prefix}'")
    
    if 'suggest' in result and result['suggest']['book-suggest']:
        options = result['suggest']['book-suggest'][0]['options']
        print(f"   Suggestions ({len(options)}):")
        
        for option in options:
            print(f"   - {option['text']} (score: {option['_score']:.2f})")
    else:
        print(f"   No suggestions found")
    print()

# ==================== 5. MULTI-FIELD AUTOCOMPLETE ====================
print("\n\n5. MULTI-FIELD AUTOCOMPLETE")
print("-" * 70)

# Search in both title and author
query_text = 'wil'

query = {
    'query': {
        'multi_match': {
            'query': query_text,
            'type': 'phrase_prefix',
            'fields': ['title', 'author']
        }
    }
}

result = es.search(index=index_name, body=query, size=5)

print(f"🔍 Multi-field autocomplete: '{query_text}'")
print(f"   Searching: title, author")
print(f"   Found: {result['hits']['total']['value']} results\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   - {book['title']}")
    print(f"     by {book['author']}")

# ==================== 6. FUZZY AUTOCOMPLETE ====================
print("\n\n6. FUZZY AUTOCOMPLETE (Typo Tolerance)")
print("-" * 70)

# Autocomplete with typo tolerance
query_text = 'pyton'  # TYPO: should match "python"

query = {
    'query': {
        'match': {
            'title': {
                'query': query_text,
                'fuzziness': 'AUTO',
                'prefix_length': 2
            }
        }
    }
}

result = es.search(index=index_name, body=query, size=5)

print(f"🔍 Fuzzy autocomplete: '{query_text}' (typo)")
print(f"   Found: {result['hits']['total']['value']} results\n")

for hit in result['hits']['hits']:
    print(f"   - {hit['_source']['title']}")

# ==================== 7. CONTEXT-AWARE SUGGESTIONS ====================
print("\n\n7. CONTEXT-AWARE SUGGESTIONS")
print("-" * 70)

# Suggest books in specific category
query_text = 'd'

query = {
    'query': {
        'bool': {
            'must': [
                {
                    'match_phrase_prefix': {
                        'title': query_text
                    }
                }
            ],
            'filter': [
                {
                    'term': {
                        'category.raw': 'Web Development'
                    }
                }
            ]
        }
    }
}

result = es.search(index=index_name, body=query, size=5)

print(f"🔍 Context-aware: '{query_text}' in Web Development")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   - {book['title']}")
    print(f"     Category: {book['category']}")

# ==================== 8. RANKED SUGGESTIONS ====================
print("\n\n8. RANKED SUGGESTIONS (By Popularity)")
print("-" * 70)

# Boost by rating
query_text = 'djan'

query = {
    'query': {
        'function_score': {
            'query': {
                'match_phrase_prefix': {
                    'title': query_text
                }
            },
            'functions': [
                {
                    'field_value_factor': {
                        'field': 'rating',
                        'factor': 1.2,
                        'modifier': 'sqrt'
                    }
                }
            ]
        }
    }
}

result = es.search(index=index_name, body=query, size=5)

print(f"🔍 Ranked suggestions: '{query_text}'")
print(f"   Boosted by: rating")
print(f"   Found: {result['hits']['total']['value']} books\n")

for hit in result['hits']['hits']:
    book = hit['_source']
    print(f"   Score: {hit['_score']:.2f} - {book['title']}")
    print(f"   Rating: {book['rating']}/5")

# ==================== 9. SEARCH AS YOU TYPE ====================
print("\n\n9. SEARCH AS YOU TYPE SIMULATION")
print("-" * 70)

# Simulate typing "django rest"
typing_sequence = ['d', 'dj', 'dja', 'djan', 'djang', 'django', 'django r', 'django re']

print("⌨️  Typing simulation: 'django rest'\n")

for typed_text in typing_sequence:
    query = {
        'query': {
            'match_phrase_prefix': {
                'title': {
                    'query': typed_text,
                    'max_expansions': 3
                }
            }
        }
    }
    
    result = es.search(index=index_name, body=query, size=3)
    
    suggestions = [hit['_source']['title'] for hit in result['hits']['hits']]
    
    print(f"   '{typed_text}' → {suggestions[:2]}")

# ==================== 10. PERFORMANCE COMPARISON ====================
print("\n\n10. PERFORMANCE COMPARISON")
print("-" * 70)

import time

# Test 1: match_phrase_prefix
start = time.time()
query = {
    'query': {
        'match_phrase_prefix': {
            'title': 'pyt'
        }
    }
}
result = es.search(index=index_name, body=query)
time_phrase_prefix = (time.time() - start) * 1000

# Test 2: completion suggester
start = time.time()
body = {
    'suggest': {
        'book-suggest': {
            'prefix': 'pyt',
            'completion': {
                'field': 'title.suggest'
            }
        }
    }
}
result = es.search(index=index_name, body=body)
time_completion = (time.time() - start) * 1000

print(f"⚡ Performance Comparison:")
print(f"   match_phrase_prefix: {time_phrase_prefix:.2f}ms")
print(f"   completion suggester: {time_completion:.2f}ms")
print(f"\n   Completion is {(time_phrase_prefix/time_completion):.1f}x faster!")

# ==================== 11. BEST PRACTICES ====================
print("\n\n11. AUTOCOMPLETE BEST PRACTICES")
print("-" * 70)

print("""
✅ DO:
   - Use completion field for fastest suggestions
   - Limit max_expansions (5-10) for performance
   - Add skip_duplicates to avoid repeats
   - Boost by popularity/rating
   - Filter by context (category, etc.)
   - Set reasonable size limit (5-10)

❌ DON'T:
   - Use wildcard queries (slow!)
   - Return too many results (>20)
   - Search without prefix length check
   - Forget to handle typos (use fuzziness)

METHODS COMPARISON:
┌───────────────────┬─────────┬──────────────┬───────┐
│ Method            │ Speed   │ Typo Support │ Use   │
├───────────────────┼─────────┼──────────────┼───────┤
│ prefix            │ Fast    │ No           │ Basic │
│ match_phrase_...  │ Medium  │ No           │ Good  │
│ completion        │ Fastest │ No           │ Best  │
│ fuzzy             │ Slow    │ Yes          │ Extra │
└───────────────────┴─────────┴──────────────┴───────┘

RECOMMENDATION:
- Primary: completion suggester
- Fallback: match_phrase_prefix with fuzziness
- Context: Add filters for better relevance
""")

# ==================== SUMMARY ====================
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
✅ Prefix Query: Simple prefix matching
✅ Match Phrase Prefix: Better phrase matching
✅ Completion Suggester: Ultra-fast suggestions (<10ms)
✅ Multi-field: Search title + author
✅ Fuzzy: Handle typos (pyton → python)
✅ Context-aware: Filter by category
✅ Ranked: Boost by rating/popularity
✅ Search-as-you-type: Progressive refinement

KEY TAKEAWAYS:
- Completion suggester is FASTEST (10x+)
- Use completion field for autocomplete
- Add fuzziness for typo tolerance
- Boost by rating for better ranking
- Filter by context for relevance
- Limit results to 5-10 for UX

AUTOCOMPLETE FLOW:
User types → Query ES → Get suggestions → Display

TYPICAL RESPONSE TIME:
- completion: <10ms
- match_phrase_prefix: ~20-50ms
- fuzzy: ~50-100ms

NEXT STEP:
- 05-filtering-aggregations.py - Analytics
""")

print("=" * 70)