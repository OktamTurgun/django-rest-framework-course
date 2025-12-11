"""
Header Versioning - RESTful yondashuv
Version HTTP header orqali yuboriladi
"""

# ==========================================
# METHOD 1: Accept Header Versioning
# ==========================================

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2', 'v3'],
}

"""
Accept Header Format:
Accept: application/json; version=v1
Accept: application/vnd.myapp.v2+json
Accept: application/vnd.myapp+json; version=v2
"""


# urls.py (version parameter KERAK EMAS!)
from django.urls import path
from books.views import BookListView, BookDetailView

urlpatterns = [
    # URL bir xil, version header'da
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(APIView):
    """Accept header versioning"""
    
    def get(self, request):
        # Version header'dan olinadi
        version = request.version  # 'v1', 'v2', or 'v3'
        
        if version == 'v1':
            return Response({
                'version': 'v1',
                'data': self.get_v1_data()
            })
        elif version == 'v2':
            return Response({
                'version': 'v2',
                'data': self.get_v2_data()
            })
        elif version == 'v3':
            return Response({
                'version': 'v3',
                'data': self.get_v3_data()
            })


# ==========================================
# METHOD 2: Custom Header Versioning
# ==========================================

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.CustomHeaderVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2', 'v3'],
    'VERSION_HEADER': 'X-API-Version',  # Custom header name
}

"""
Custom Header:
X-API-Version: v1
X-API-Version: v2
API-Version: v1
"""


# ==========================================
# CUSTOM HEADER VERSIONING CLASS
# ==========================================

from rest_framework.versioning import BaseVersioning
from rest_framework.exceptions import NotFound

class CustomAPIVersioning(BaseVersioning):
    """
    Custom header versioning implementation
    Header: X-API-Version: v1
    """
    
    def determine_version(self, request, *args, **kwargs):
        """Header'dan version olish"""
        version = request.META.get('HTTP_X_API_VERSION')
        
        if not version:
            # Default version
            return self.default_version
        
        # Validate version
        if not self.is_allowed_version(version):
            raise NotFound(f'Invalid API version: {version}')
        
        return version


# settings.py'da ishlatish
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'myapp.versioning.CustomAPIVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2', 'v3'],
}


# ==========================================
# GITHUB-STYLE VERSIONING
# ==========================================

"""
GitHub API style:
Accept: application/vnd.github.v3+json
"""

class GitHubStyleVersioning(BaseVersioning):
    """
    GitHub-style versioning
    Accept: application/vnd.myapp.v2+json
    """
    
    def determine_version(self, request, *args, **kwargs):
        """Parse Accept header"""
        accept = request.META.get('HTTP_ACCEPT', '')
        
        # Extract version from Accept header
        # Example: application/vnd.myapp.v2+json → v2
        import re
        match = re.search(r'\.v(\d+)\+', accept)
        
        if match:
            version = f'v{match.group(1)}'
            if self.is_allowed_version(version):
                return version
        
        return self.default_version


# ==========================================
# HEADER VERSIONING WITH FALLBACK
# ==========================================

class FlexibleVersioning(BaseVersioning):
    """
    Flexible versioning - header yoki query parameter
    """
    
    def determine_version(self, request, *args, **kwargs):
        """Try header first, then query parameter"""
        # Try custom header
        version = request.META.get('HTTP_X_API_VERSION')
        
        if not version:
            # Fallback to query parameter
            version = request.query_params.get('version')
        
        if not version:
            # Default
            return self.default_version
        
        if not self.is_allowed_version(version):
            raise NotFound(f'Invalid version: {version}')
        
        return version


# ==========================================
# TESTING HEADER VERSIONING
# ==========================================

"""
cURL Examples:

# Accept Header Versioning
curl -H "Accept: application/json; version=v1" \\
     http://localhost:8000/api/books/

curl -H "Accept: application/json; version=v2" \\
     http://localhost:8000/api/books/

# Custom Header
curl -H "X-API-Version: v1" \\
     http://localhost:8000/api/books/

curl -H "X-API-Version: v2" \\
     http://localhost:8000/api/books/

# GitHub Style
curl -H "Accept: application/vnd.myapp.v2+json" \\
     http://localhost:8000/api/books/
"""


# ==========================================
# JAVASCRIPT/FRONTEND USAGE
# ==========================================

# JavaScript fetch with header versioning
"""
// Accept Header
fetch('http://localhost:8000/api/books/', {
    headers: {
        'Accept': 'application/json; version=v2'
    }
})

// Custom Header
fetch('http://localhost:8000/api/books/', {
    headers: {
        'X-API-Version': 'v2'
    }
})

// Axios
axios.get('http://localhost:8000/api/books/', {
    headers: {
        'X-API-Version': 'v2'
    }
})

// Axios interceptor (global)
axios.interceptors.request.use(config => {
    config.headers['X-API-Version'] = 'v2';
    return config;
});
"""


# ==========================================
# ADVANTAGES & DISADVANTAGES
# ==========================================

"""
✅ ADVANTAGES:

1. RESTful - HTTP standard'ga mos
2. URL clean - URL o'zgarishsiz
3. Multiple versions - Bir URL, ko'p version
4. Content negotiation - HTTP standard'ning qismi
5. Flexible - Turli formatlar qo'llab-quvvatlash mumkin

❌ DISADVANTAGES:

1. Hidden - Ko'rinmas, unutilishi oson
2. Testing hard - Browser'da test qilish qiyin
3. Documentation complex - Header'larni tushuntirish kerak
4. Client complexity - Har safar header qo'shish kerak
5. Cache issues - Ba'zi cache'lar header'larni ignore qiladi

WHEN TO USE:

- REST purist bo'lsangiz
- Content negotiation muhim bo'lsa
- Multiple response format'lar kerak bo'lsa
- Internal API (team control'ida)

WHEN NOT TO USE:

- Public API (URL versioning yaxshiroq)
- Browser testing muhim
- Simple project
- Cache heavily used
"""


# ==========================================
# BEST PRACTICES
# ==========================================

# 1. Always provide default version
REST_FRAMEWORK = {
    'DEFAULT_VERSION': 'v1',  # Header bo'lmasa
}

# 2. Clear error messages
from rest_framework.exceptions import APIException

class InvalidAPIVersion(APIException):
    status_code = 400
    default_detail = 'Invalid API version in header'
    default_code = 'invalid_version'

# 3. Version response'da ham ko'rsatish
class BookListView(APIView):
    def get(self, request):
        return Response({
            'version': request.version,  # Client'ga version ko'rsatish
            'data': [...]
        })

# 4. Documentation
"""
API Documentation:

Version Header Options:

1. Accept Header:
   Accept: application/json; version=v2

2. Custom Header:
   X-API-Version: v2

3. Default (no header):
   Version: v1

Supported Versions:
- v1 (default)
- v2
- v3

Example:
curl -H "X-API-Version: v2" https://api.example.com/books/
"""


# ==========================================
# COMBINING WITH OTHER STRATEGIES
# ==========================================

class HybridVersioning(BaseVersioning):
    """
    Hybrid: Header yoki URL
    Flexibility uchun
    """
    
    def determine_version(self, request, *args, **kwargs):
        # 1. Try header
        version = request.META.get('HTTP_X_API_VERSION')
        
        # 2. Try URL parameter
        if not version:
            version = kwargs.get('version')
        
        # 3. Default
        if not version:
            return self.default_version
        
        return version


# URLs support both
urlpatterns = [
    # Header only
    path('api/books/', BookListView.as_view()),
    
    # URL parameter (fallback)
    path('api/<version>/books/', BookListView.as_view()),
]


print("✅ Header Versioning examples to'liq!")
print("\nKeyingi qadam:")
print("→ 04-namespace-versioning.py'ni o'qing")