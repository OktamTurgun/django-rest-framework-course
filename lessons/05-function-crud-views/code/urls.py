from django.urls import path
from . import views

"""
URL patterns for Books API

Base URL: /api/books/
"""

urlpatterns = [
    # List & Create
    path('', views.book_list, name='book-list'),
    
    # Search
    path('search/', views.book_search, name='book-search'),
    
    # Stats
    path('stats/', views.book_stats, name='book-stats'),
    
    # Detail operations
    path('<int:pk>/', views.book_detail, name='book-detail'),
    
    # Toggle availability
    path('<int:pk>/toggle/', views.toggle_availability, name='book-toggle'),
]

"""
API Endpoints:

GET     /api/books/                 - Barcha kitoblar ro'yxati
POST    /api/books/                 - Yangi kitob yaratish
GET     /api/books/search/?q=...    - Kitoblarni qidirish
GET     /api/books/stats/           - Statistika
GET     /api/books/{id}/            - Bitta kitobni ko'rish
PUT     /api/books/{id}/            - Kitobni to'liq yangilash
PATCH   /api/books/{id}/            - Kitobni qisman yangilash
DELETE  /api/books/{id}/            - Kitobni o'chirish
POST    /api/books/{id}/toggle/     - Mavjudlikni o'zgartirish

Query Parameters (for list):
    ?author=John        - Muallif bo'yicha filterlash
    ?available=true     - Mavjudlik bo'yicha filterlash
    ?language=English   - Til bo'yicha filterlash

Examples:
    GET /api/books/?author=John&available=true
    GET /api/books/search/?q=python
    POST /api/books/5/toggle/
"""