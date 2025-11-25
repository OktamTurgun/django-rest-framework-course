"""
Books app URLs
Barcha URL'larni bu yerda birlashtirish
"""
from django.urls import path, include

app_name = 'books'

urlpatterns = [
  
    # Lesson 20 URLs (Throttling) - YANGI!
    path('', include('books.urls.lesson20_urls')),

    # Lesson 17 URLs (asosiy)
    # path('', include('books.urls.lesson19_urls')),
    
    # Old URLs (agar kerak bo'lsa)
    # path('old/', include('books.urls.old_urls')),
    
    # ViewSet URLs (agar kerak bo'lsa)
    # path('', include('books.urls.router_urls')),
]