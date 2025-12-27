"""
V1 API Pagination
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class V1Pagination(PageNumberPagination):
    """
    V1 API pagination with version info
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """Add version field to paginated response"""
        return Response({
            'version': 'v1',
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })