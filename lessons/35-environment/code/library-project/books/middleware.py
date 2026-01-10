"""
API Versioning Middleware
"""
from datetime import datetime, date
from django.conf import settings
from django.core.cache import cache

# ============================================
# SENTRY USER CONTEXT MIDDLEWARE
# ============================================

class SentryUserContextMiddleware:
    """
    Middleware to automatically set Sentry user context
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Set user context for Sentry
        try:
            import sentry_sdk
            from django.conf import settings
            
            if hasattr(settings, 'SENTRY_DSN') and settings.SENTRY_DSN:
                if hasattr(request, 'user') and request.user.is_authenticated:
                    sentry_sdk.set_user({
                        "id": request.user.id,
                        "username": request.user.username,
                        "email": getattr(request.user, 'email', None),
                    })
                else:
                    sentry_sdk.set_user({
                        "ip_address": request.META.get('REMOTE_ADDR'),
                    })
                
                # Add request context
                sentry_sdk.set_context("request", {
                    "url": request.build_absolute_uri(),
                    "method": request.method,
                    "query_string": request.META.get('QUERY_STRING', ''),
                })
        except ImportError:
            # Sentry not installed, skip
            pass
        except Exception as e:
            # Log error but don't break the request
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Sentry middleware error: {e}")
        
        response = self.get_response(request)
        return response

class APIVersionDeprecationMiddleware:
    """
    Add deprecation warnings to V1 API responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.sunset_date = getattr(settings, 'V1_SUNSET_DATE', datetime(2025, 12, 31))
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add deprecation headers for V1
        if request.path.startswith('/api/v1/'):
            # Calculate days until sunset
            days_left = (self.sunset_date - datetime.now()).days
            
            # Warning header
            response['Warning'] = (
                '299 - "API v1 is deprecated. '
                f'Please migrate to v2 by {self.sunset_date.strftime("%Y-%m-%d")}. '
                'See https://docs.example.com/api/v1-to-v2"'
            )
            
            # Sunset header
            response['Sunset'] = self.sunset_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            # Link to new version
            response['Link'] = '<https://api.example.com/v2/>; rel="successor-version"'
            
            # Custom header with days left
            response['X-Days-Until-Sunset'] = str(max(0, days_left))
        
        return response


class APIVersionMetricsMiddleware:
    """
    Track API version usage for analytics
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Extract version from path
        version = self.get_version_from_path(request.path)
        
        if version:
            # Log version usage with safe caching
            self._track_usage(version)
            
            # Track authenticated users
            if hasattr(request, 'user') and request.user.is_authenticated:
                self._track_user(version, request.user.id)
        
        response = self.get_response(request)
        
        # Add version to response header
        if version:
            response['X-API-Version'] = version
        
        return response
    
    def _track_usage(self, version):
        """Safely track API usage count"""
        try:
            today = date.today()
            cache_key = f'api_usage:{version}:{today}'
            
            # Get current count
            current_count = cache.get(cache_key)
            
            if current_count is None:
                # Initialize if doesn't exist
                cache.set(cache_key, 1, timeout=86400 * 7)  # Keep for 7 days
            else:
                # Increment existing count
                cache.set(cache_key, current_count + 1, timeout=86400 * 7)
                
        except Exception as e:
            # Silently fail for metrics (not critical)
            pass
    
    def _track_user(self, version, user_id):
        """Track unique users per version"""
        try:
            today = date.today()
            users_key = f'api_users:{version}:{today}'
            
            # Get existing set or create new
            users_set = cache.get(users_key, set())
            users_set.add(user_id)
            cache.set(users_key, users_set, timeout=86400 * 7)
            
        except Exception as e:
            # Silently fail for metrics (not critical)
            pass
    
    def get_version_from_path(self, path):
        """Extract version from URL path"""
        if '/api/v1/' in path:
            return 'v1'
        elif '/api/v2/' in path:
            return 'v2'
        return None