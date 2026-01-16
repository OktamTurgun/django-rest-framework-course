"""
Health Check Endpoint for Production Monitoring
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache

class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring services
    
    GET /health/ or /api/health/
    
    Returns:
        - status: healthy/unhealthy
        - database: connected/disconnected
        - cache: working/unavailable
    """
    permission_classes = []
    authentication_classes = []
    
    def get(self, request):
        health_status = {
            'status': 'healthy',
            'service': 'library-api',
            'database': 'unknown',
            'cache': 'unknown'
        }
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    health_status['database'] = 'connected'
        except Exception as e:
            health_status['database'] = 'disconnected'
            health_status['status'] = 'unhealthy'
            health_status['database_error'] = str(e)
            return Response(
                health_status, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Check cache (Redis)
        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') == 'ok':
                health_status['cache'] = 'working'
            else:
                health_status['cache'] = 'not_working'
        except Exception as e:
            health_status['cache'] = 'unavailable'
            health_status['cache_error'] = str(e)
        
        return Response(health_status, status=status.HTTP_200_OK)