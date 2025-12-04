"""
Books app URLs
Barcha URL'larni bu yerda birlashtirish

DIQQAT: Bir vaqtning o'zida faqat BITTA lesson URL'ini uncomment qiling!
Aks holda URL conflict bo'ladi.
"""
from django.urls import path, include

app_name = 'books'

urlpatterns = [
    # === LESSON 24: Caching (HOZIRGI DARS) ===
    # Bu yerda uncomment qiling - hozir ishlayotgan dars
    path('', include('books.urls.lesson24_urls')),
    
    # === OLDINGI DARSLAR (commented) ===
    # Eski darslarni test qilish kerak bo'lsa, yuqoridagini comment qilib,
    # kerakli darsni uncomment qiling
    
    # Lesson 23: Testing
    # path('', include('books.urls.lesson23_urls')),
    
    # Lesson 22: Performance Optimization
    # path('', include('books.urls.lesson22_urls')),
  
    # Lesson 21: File Upload
    # path('', include('books.urls.lesson21_urls')),
  
    # Lesson 20: Throttling
    # path('', include('books.urls.lesson20_urls')),

    # Lesson 19: Filtering & Searching
    # path('', include('books.urls.lesson19_urls')),

    # Lesson 17: Basic CRUD
    # path('', include('books.urls.lesson17_urls')),
    
    # Old URLs (deprecated)
    # path('old/', include('books.urls.old_urls')),
    
    # ViewSet URLs (agar router ishlatgan bo'lsangiz)
    # path('', include('books.urls.router_urls')),
]

"""
IMPORTANT NOTES:

1. Bir vaqtning o'zida faqat BITTA lesson URL'i uncommented bo'lishi kerak!

2. Agar bir nechta lesson URL'larini bir vaqtda ishlatmoqchi bo'lsangiz,
   har biriga PREFIX qo'shing:
   
   path('lesson24/', include('books.urls.lesson24_urls')),
   path('lesson23/', include('books.urls.lesson23_urls')),
   path('lesson22/', include('books.urls.lesson22_urls')),
   
   Bu holda URL'lar:
   - /api/lesson24/books/
   - /api/lesson23/books/
   - /api/lesson22/books/

3. Production'da faqat kerakli URL'larni qoldiring.

4. Development'da har bir darsni alohida test qilish uchun
   library_project/urls.py'da prefix ishlatish yaxshiroq:
   
   path('api/lesson24/', include('books.urls.lesson24_urls')),

5. Hozir ishlatilayotgan struktura:
   Main URLs: library_project/urls.py
   └── api/lesson24/ → books/urls/__init__.py
                    └── → books/urls/lesson24_urls.py
"""