"""
Elasticsearch search functionality
"""
from elasticsearch_dsl import Q
from .documents import BookDocument


class BookSearch:
    """Book search using Elasticsearch"""
    
    @staticmethod
    def search_books(query, filters=None):
        """Full-text search with filters"""
        search = BookDocument.search()
        
        # Base query
        if query:
            search = search.query(
                "multi_match",
                query=query,
                fields=['title^3', 'description', 'author.name^2'],
                fuzziness='AUTO'
            )
        
        # Filters
        if filters:
            # Price range
            if 'price_min' in filters:
                search = search.filter('range', price={'gte': float(filters['price_min'])})
            
            if 'price_max' in filters:
                search = search.filter('range', price={'lte': float(filters['price_max'])})
            
            # ✅ Genre filter - simple match on genres.name
            if 'genre' in filters:
                search = search.filter('match', genres__name=filters['genre'])
            
            # ✅ Author filter - simple match on author.name
            if 'author' in filters:
                search = search.filter('match', author__name=filters['author'])
        
        return search
    
    @staticmethod
    def autocomplete(query):
        """Autocomplete suggestions"""
        search = BookDocument.search()
        search = search.suggest(
            'title_suggestions',
            query,
            completion={
                'field': 'title.suggest',
                'size': 5,
                'fuzzy': {'fuzziness': 'AUTO'}
            }
        )
        return search.execute()
    
    @staticmethod
    def aggregate_by_genre():
        """
        Aggregate books by genre
        """
        search = BookDocument.search()
        search.aggs.bucket('genres', 'terms', field='genres.name.keyword', size=10)
        search.aggs['genres'].metric('avg_price', 'avg', field='price')
        return search.execute()