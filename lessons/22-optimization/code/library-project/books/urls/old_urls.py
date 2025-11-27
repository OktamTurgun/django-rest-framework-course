from django.urls import path
from ..views import (
    # Validation views
    BookFieldValidationListView,
    BookObjectValidationListView,
    BookCustomValidatorsListView,
    BookBuiltInValidatorsListView,

    # Old CRUD
    BookListCreateView,
    BookDetailView,

    # Homework
    BookHomeworkFieldValidationView,
    BookHomeworkObjectValidationView,

    # Authentication test
    ProtectedView,
)

urlpatterns = [
    # Validation (Lesson 11)
    path('old/field-validation/', BookFieldValidationListView.as_view()),
    path('old/object-validation/', BookObjectValidationListView.as_view()),
    path('old/custom-validators/', BookCustomValidatorsListView.as_view()),
    path('old/builtin-validators/', BookBuiltInValidatorsListView.as_view()),

    # Old CRUD (APIView)
    path('old/books/', BookListCreateView.as_view()),
    path('old/books/<int:pk>/', BookDetailView.as_view()),

    # Homework
    path('homework/field-validation/', BookHomeworkFieldValidationView.as_view()),
    path('homework/object-validation/', BookHomeworkObjectValidationView.as_view()),

    # Auth Test
    path('protected/', ProtectedView.as_view()),
]
