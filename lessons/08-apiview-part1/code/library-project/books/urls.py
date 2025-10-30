from django.urls import path
from .views import (
    BookListApiView,
    BookDetailApiView,
    BookCreateApiView,
    BookUpdateApiView,
    BookDeleteApiView,
    BookListCreateApiView,
    BookRetrieveUpdateApiView,
    BookRetrieveDestroyApiView,
    BookRetrieveUpdateDestroyApiView,
)

urlpatterns = [
    # 1 Faqat ro‘yxat
    path('list/', BookListApiView.as_view(), name='book-list'),

    # 2 Faqat bitta obyektni olish
    path('<int:pk>/', BookDetailApiView.as_view(), name='book-detail'),

    # 3 Faqat yangi obyekt yaratish
    path('create/', BookCreateApiView.as_view(), name='book-create'),

    # 4 Faqat obyektni yangilash
    path('<int:pk>/update/', BookUpdateApiView.as_view(), name='book-update'),

    # 5 Faqat obyektni o‘chirish
    path('<int:pk>/delete/', BookDeleteApiView.as_view(), name='book-delete'),

    # 6 Ro‘yxat + Yaratish
    path('list-create/', BookListCreateApiView.as_view(), name='book-list-create'),

    # 7 Ko‘rsatish + Yangilash
    path('<int:pk>/retrieve-update/', BookRetrieveUpdateApiView.as_view(), name='book-retrieve-update'),

    # 8 Ko‘rsatish + O‘chirish
    path('<int:pk>/retrieve-destroy/', BookRetrieveDestroyApiView.as_view(), name='book-retrieve-destroy'),

    # 9 To‘liq CRUD (ko‘rsatish + yangilash + o‘chirish)
    path('<int:pk>/full/', BookRetrieveUpdateDestroyApiView.as_view(), name='book-full'),
]
