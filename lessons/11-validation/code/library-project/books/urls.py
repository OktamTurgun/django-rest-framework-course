from django.urls import path
from .views import (
    BookFieldValidationListView,
    BookObjectValidationListView,
    BookCustomValidatorsListView,
    BookBuiltInValidatorsListView,
    BookListCreateView,
    BookDetailView,

     # Homework view
     BookHomeworkFieldValidationView,
)

urlpatterns = [
    # ===== Validation turlarini test qilish =====
    
    # Field-level validation
    path('books/field-validation/', 
         BookFieldValidationListView.as_view(), 
         name='book-field-validation'),
    
    # Object-level validation
    path('books/object-validation/', 
         BookObjectValidationListView.as_view(), 
         name='book-object-validation'),
    
    # Custom validators
    path('books/custom-validators/', 
         BookCustomValidatorsListView.as_view(), 
         name='book-custom-validators'),
    
    # Built-in validators
    path('books/builtin-validators/', 
         BookBuiltInValidatorsListView.as_view(), 
         name='book-builtin-validators'),
    
    # ===== Asosiy CRUD endpoints (Complete validation) =====
    path('books/', 
         BookListCreateView.as_view(), 
         name='book-list'),
    
    path('books/<int:pk>/', 
         BookDetailView.as_view(), 
         name='book-detail'),

     # Homework endpoint
     # ===== Homework endpoints =====
    path('homework/field-validation/', 
         BookHomeworkFieldValidationView.as_view(), 
         name='homework-field-validation'),
]