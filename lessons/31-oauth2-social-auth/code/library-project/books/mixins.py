"""
Reusable mixins for query optimization
"""


class QueryOptimizationMixin:
    """
    Mixin for optimizing querysets with select_related and prefetch_related
    
    Usage:
        class BookViewSet(QueryOptimizationMixin, viewsets.ModelViewSet):
            queryset = Book.objects.all()
            serializer_class = BookSerializer
            select_related_fields = ['author']
            prefetch_related_fields = ['genres']
    """
    select_related_fields = []
    prefetch_related_fields = []
    
    def get_queryset(self):
        """
        Apply select_related and prefetch_related to queryset
        """
        queryset = super().get_queryset()
        
        # Apply select_related for ForeignKey relationships
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        
        # Apply prefetch_related for ManyToMany relationships
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        
        return queryset