"""
APIView ning oddiy misollari
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# MISOL 1: Eng oddiy APIView
class HelloWorldView(APIView):
    """
    Eng oddiy APIView misoli
    GET /api/hello/
    """
    def get(self, request):
        return Response({'message': 'Hello, World!'})


# MISOL 2: Bir nechta HTTP metodlar
class MultiMethodView(APIView):
    """
    Turli HTTP metodlarni qo'llab-quvvatlovchi view
    """
    def get(self, request):
        """GET so'rovga javob"""
        return Response({
            'method': 'GET',
            'message': 'Ma\'lumotlarni olish'
        })
    
    def post(self, request):
        """POST so'rovga javob"""
        return Response({
            'method': 'POST',
            'message': 'Ma\'lumot yaratish',
            'received_data': request.data
        }, status=status.HTTP_201_CREATED)
    
    def put(self, request):
        """PUT so'rovga javob"""
        return Response({
            'method': 'PUT',
            'message': 'Ma\'lumotni to\'liq yangilash'
        })
    
    def patch(self, request):
        """PATCH so'rovga javob"""
        return Response({
            'method': 'PATCH',
            'message': 'Ma\'lumotni qisman yangilash'
        })
    
    def delete(self, request):
        """DELETE so'rovga javob"""
        return Response({
            'method': 'DELETE',
            'message': 'Ma\'lumot o\'chirildi'
        }, status=status.HTTP_204_NO_CONTENT)


# MISOL 3: Query parametrlar bilan ishlash
class SearchView(APIView):
    """
    Query parametrlar bilan ishlash
    GET /api/search/?q=django&category=books
    """
    def get(self, request):
        # Query parametrlarni olish
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', 'all')
        page = request.query_params.get('page', 1)
        
        return Response({
            'search_query': query,
            'category': category,
            'page': page,
            'results': []  # Bu yerda haqiqiy qidiruv natijasi bo'ladi
        })


# MISOL 4: URL parametrlar bilan ishlash
class ItemDetailView(APIView):
    """
    URL parametrlar bilan ishlash
    GET /api/items/123/
    """
    def get(self, request, pk):
        return Response({
            'id': pk,
            'message': f'{pk} ID li element'
        })
    
    def put(self, request, pk):
        return Response({
            'id': pk,
            'message': f'{pk} ID li element yangilandi',
            'data': request.data
        })
    
    def delete(self, request, pk):
        return Response({
            'id': pk,
            'message': f'{pk} ID li element o\'chirildi'
        }, status=status.HTTP_204_NO_CONTENT)


# MISOL 5: Custom metodlar
class CalculatorView(APIView):
    """
    Custom biznes logika bilan APIView
    POST /api/calculate/
    Body: {"num1": 10, "num2": 5, "operation": "add"}
    """
    def post(self, request):
        num1 = request.data.get('num1', 0)
        num2 = request.data.get('num2', 0)
        operation = request.data.get('operation', 'add')
        
        result = self._calculate(num1, num2, operation)
        
        return Response({
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'result': result
        })
    
    def _calculate(self, num1, num2, operation):
        """Private metod - hisoblash logikasi"""
        operations = {
            'add': num1 + num2,
            'subtract': num1 - num2,
            'multiply': num1 * num2,
            'divide': num1 / num2 if num2 != 0 else None
        }
        return operations.get(operation, 'Invalid operation')


# MISOL 6: Xatolarni qaytarish
class ValidationView(APIView):
    """
    Xatolarni to'g'ri qaytarish
    POST /api/validate/
    """
    def post(self, request):
        # Required fieldlarni tekshirish
        required_fields = ['name', 'email', 'age']
        errors = {}
        
        for field in required_fields:
            if field not in request.data:
                errors[field] = [f'{field} maydoni majburiy']
        
        # Agar xatolar bo'lsa
        if errors:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Age validatsiyasi
        age = request.data.get('age')
        if not isinstance(age, int) or age < 0:
            return Response(
                {'error': 'Age musbat son bo\'lishi kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Hammasi OK
        return Response({
            'message': 'Validation muvaffaqiyatli',
            'data': request.data
        }, status=status.HTTP_201_CREATED)


# MISOL 7: List va Create
class TodoListView(APIView):
    """
    Oddiy todo ro'yxati (ma'lumotlar bazasiz)
    """
    # Class darajasida ma'lumotlar (demo uchun)
    todos = [
        {'id': 1, 'title': 'Django o\'rganish', 'completed': False},
        {'id': 2, 'title': 'DRF o\'rganish', 'completed': False},
    ]
    
    def get(self, request):
        """Barcha todolarni olish"""
        return Response(self.todos)
    
    def post(self, request):
        """Yangi todo yaratish"""
        # ID generatsiya qilish
        new_id = max([t['id'] for t in self.todos]) + 1 if self.todos else 1
        
        # Yangi todo
        new_todo = {
            'id': new_id,
            'title': request.data.get('title', ''),
            'completed': False
        }
        
        self.todos.append(new_todo)
        
        return Response(new_todo, status=status.HTTP_201_CREATED)


# URLs konfiguratsiyasi uchun misol:
"""
from django.urls import path
from .views import (
    HelloWorldView,
    MultiMethodView,
    SearchView,
    ItemDetailView,
    CalculatorView,
    ValidationView,
    TodoListView
)

urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello'),
    path('methods/', MultiMethodView.as_view(), name='multi-method'),
    path('search/', SearchView.as_view(), name='search'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('calculate/', CalculatorView.as_view(), name='calculate'),
    path('validate/', ValidationView.as_view(), name='validate'),
    path('todos/', TodoListView.as_view(), name='todo-list'),
]
"""