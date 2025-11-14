from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Validation Views (Old - for learning purposes)
    BookFieldValidationListView,
    BookObjectValidationListView,
    BookCustomValidatorsListView,
    BookBuiltInValidatorsListView,

    # CRUD Views (Old - APIView)
    BookListCreateView,
    BookDetailView,

    # Auth Test View
    ProtectedView,

    # Homework Views
    BookHomeworkFieldValidationView,
    BookHomeworkObjectValidationView,

    # ViewSet (Lesson 15 - NEW!)
    BookViewSet,
)

# ========================
# LESSON 15: Router (NEW APPROACH)
# ========================
router = DefaultRouter()

# ViewSet'ni router'ga ro'yxatdan o'tkazamiz
# URL: /api/books/ (ViewSet)
router.register(r'books', BookViewSet, basename='book')

# Router generates these URLs automatically:
# GET    /api/books/                    -> list
# POST   /api/books/                    -> create
# GET    /api/books/{id}/               -> retrieve
# PUT    /api/books/{id}/               -> update
# PATCH  /api/books/{id}/               -> partial_update
# DELETE /api/books/{id}/               -> destroy
# GET    /api/books/published/          -> custom action
# GET    /api/books/statistics/         -> custom action
# POST   /api/books/{id}/publish/       -> custom action
# POST   /api/books/{id}/unpublish/     -> custom action


urlpatterns = [
    # ===== LESSON 15: ViewSet Routes (PRIMARY) =====
    # Bu endpoint'lar asosiy - ViewSet ishlatiladi
    path('', include(router.urls)),
    
    
    # ===== OLD ENDPOINTS (Learning purposes only) =====
    # Bu eski endpoint'lar - o'rganish uchun saqlanadi
    # URL'larga "old/" prefix qo'shildi
    
    # Validation endpoints (Lesson 11)
    path('old/field-validation/',
         BookFieldValidationListView.as_view(),
         name='book-field-validation'),

    path('old/object-validation/',
         BookObjectValidationListView.as_view(),
         name='book-object-validation'),

    path('old/custom-validators/',
         BookCustomValidatorsListView.as_view(),
         name='book-custom-validators'),

    path('old/builtin-validators/',
         BookBuiltInValidatorsListView.as_view(),
         name='book-builtin-validators'),

    # Old CRUD endpoints (APIView)
    path('old/books/',
         BookListCreateView.as_view(),
         name='book-list-old'),

    path('old/books/<int:pk>/',
         BookDetailView.as_view(),
         name='book-detail-old'),

    # Homework endpoints
    path('homework/field-validation/',
         BookHomeworkFieldValidationView.as_view(),
         name='homework-field-validation'),

    path('homework/object-validation/',
         BookHomeworkObjectValidationView.as_view(),
         name='homework-object-validation'),

    # Auth test endpoint (Lesson 13)
    path('protected/',
         ProtectedView.as_view(),
         name='protected'),
]

"""
URL STRUCTURE:
==============

PRIMARY (Lesson 15 - ViewSet):
-------------------------------
GET    /api/books/                     -> BookViewSet.list()
POST   /api/books/                     -> BookViewSet.create()
GET    /api/books/{id}/                -> BookViewSet.retrieve()
PUT    /api/books/{id}/                -> BookViewSet.update()
PATCH  /api/books/{id}/                -> BookViewSet.partial_update()
DELETE /api/books/{id}/                -> BookViewSet.destroy()
GET    /api/books/published/           -> BookViewSet.published()
GET    /api/books/statistics/          -> BookViewSet.statistics()
POST   /api/books/{id}/publish/        -> BookViewSet.publish()
POST   /api/books/{id}/unpublish/      -> BookViewSet.unpublish()

OLD (Previous lessons - kept for reference):
--------------------------------------------
GET    /api/old/field-validation/      -> Field validation example
GET    /api/old/object-validation/     -> Object validation example
GET    /api/old/custom-validators/     -> Custom validators example
GET    /api/old/builtin-validators/    -> Built-in validators example
GET    /api/old/books/                 -> Old APIView list
GET    /api/old/books/{id}/            -> Old APIView detail

HOMEWORK & AUTH:
----------------
GET    /api/homework/field-validation/
GET    /api/homework/object-validation/
GET    /api/protected/                 -> Auth test endpoint
"""