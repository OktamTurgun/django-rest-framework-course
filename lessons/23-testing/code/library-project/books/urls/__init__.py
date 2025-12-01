"""
Books app URLs
Barcha URL'larni bu yerda birlashtirish
"""
from django.urls import path, include

app_name = 'books'

urlpatterns = [
    # Lesson 22 URLs (Optimization)
    path('', include('books.urls.lesson22_urls')),
  
    # Lesson 21 URLs (File Upload) - YANGI!
    # path('', include('books.urls.lesson21_urls')),
  
    # Lesson 20 URLs (Throttling) - YANGI!
    # path('', include('books.urls.lesson20_urls')),

    # Lesson 17 URLs (asosiy)
    # path('', include('books.urls.lesson19_urls')),
    
    # Old URLs (agar kerak bo'lsa)
    # path('old/', include('books.urls.old_urls')),
    
    # ViewSet URLs (agar kerak bo'lsa)
    # path('', include('books.urls.router_urls')),
]