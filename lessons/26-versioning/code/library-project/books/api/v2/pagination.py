"""
V2 API Pagination
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class V2Pagination(PageNumberPagination):
    """
    V2 API pagination with enhanced metadata
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """Enhanced response with version and features info"""
        return Response({
            'version': 'v2',
            'features': ['filtering', 'search', 'ordering', 'nested_objects'],
            'pagination': {
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
            },
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })