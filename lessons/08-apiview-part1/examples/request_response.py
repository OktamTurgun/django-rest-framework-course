"""
Request va Response obyektlari bilan ishlash misollari
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# MISOL 1: Request.data bilan ishlash
class RequestDataView(APIView):
    """
    Request.data - JSON, Form yoki File ma'lumotlarni qabul qilish
    POST /api/request-data/
    """
    def post(self, request):
        # request.data - barcha kelgan ma'lumotlar
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        return Response({
            'message': 'Ma\'lumot qabul qilindi',
            'received': {
                'username': username,
                'email': email,
                'password_length': len(password) if password else 0
            }
        })


# MISOL 2: Query parametrlar (request.query_params)
class QueryParamsView(APIView):
    """
    URL query parametrlari bilan ishlash
    GET /api/query-params/?name=John&age=25&city=Tashkent
    """
    def get(self, request):
        # request.query_params - URL parametrlari
        name = request.query_params.get('name', 'Guest')
        age = request.query_params.get('age')
        city = request.query_params.get('city', 'Unknown')
        
        # Barcha parametrlarni olish
        all_params = dict(request.query_params)
        
        return Response({
            'greeting': f'Salom, {name}!',
            'age': age,
            'city': city,
            'all_params': all_params
        })


# MISOL 3: Request metodlari va headers
class RequestMetaView(APIView):
    """
    Request ning boshqa xususiyatlari
    GET/POST /api/request-meta/
    """
    def get(self, request):
        return self._get_request_info(request)
    
    def post(self, request):
        return self._get_request_info(request)
    
    def _get_request_info(self, request):
        """Request haqida ma'lumot"""
        return Response({
            # HTTP metodi
            'method': request.method,
            
            # Foydalanuvchi
            'user': str(request.user),
            'is_authenticated': request.user.is_authenticated,
            
            # Headers
            'content_type': request.content_type,
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            
            # Request path
            'path': request.path,
            'full_path': request.get_full_path(),
            
            # Query params mavjudligi
            'has_query_params': bool(request.query_params),
            
            # POST data mavjudligi
            'has_data': bool(request.data),
        })


# MISOL 4: File upload (request.FILES)
class FileUploadView(APIView):
    """
    File yuklash
    POST /api/upload/
    Content-Type: multipart/form-data
    """
    def post(self, request):
        # File olish
        uploaded_file = request.data.get('file')
        
        if not uploaded_file:
            return Response(
                {'error': 'File yuklanmadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # File haqida ma'lumot
        file_info = {
            'name': uploaded_file.name,
            'size': uploaded_file.size,
            'content_type': uploaded_file.content_type,
        }
        
        # File ni saqlash (demo)
        # uploaded_file.save() yoki boshqa operatsiyalar
        
        return Response({
            'message': 'File muvaffaqiyatli yuklandi',
            'file': file_info
        }, status=status.HTTP_201_CREATED)


# MISOL 5: Response turli formatda
class ResponseFormatsView(APIView):
    """
    Turli formatdagi Response misollari
    GET /api/response-formats/?format=json|xml|error
    """
    def get(self, request):
        format_type = request.query_params.get('format', 'json')
        
        if format_type == 'json':
            # Oddiy JSON response
            return Response({
                'status': 'success',
                'data': {'message': 'JSON format'}
            })
        
        elif format_type == 'list':
            # List qaytarish
            return Response([
                {'id': 1, 'name': 'Item 1'},
                {'id': 2, 'name': 'Item 2'},
                {'id': 3, 'name': 'Item 3'}
            ])
        
        elif format_type == 'error':
            # Xato qaytarish
            return Response(
                {
                    'error': 'Xatolik yuz berdi',
                    'details': 'Bu demo xato'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        else:
            # Noto'g'ri format
            return Response(
                {'error': 'Noto\'g\'ri format'},
                status=status.HTTP_400_BAD_REQUEST
            )


# MISOL 6: Response headers bilan
class CustomHeadersView(APIView):
    """
    Custom headers bilan Response
    GET /api/custom-headers/
    """
    def get(self, request):
        response = Response({
            'message': 'Custom headers bilan response'
        })
        
        # Custom headerlar qo'shish
        response['X-Custom-Header'] = 'CustomValue'
        response['X-API-Version'] = '1.0'
        
        return response


# MISOL 7: Pagination va metadata
class PaginatedDataView(APIView):
    """
    Pagination bilan data qaytarish
    GET /api/paginated/?page=1&page_size=10
    """
    def get(self, request):
        # Demo data (haqiqiy proyektda DB dan olinadi)
        all_items = [{'id': i, 'name': f'Item {i}'} for i in range(1, 101)]
        
        # Pagination parametrlari
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        # Pagination logikasi
        start = (page - 1) * page_size
        end = start + page_size
        
        items = all_items[start:end]
        total = len(all_items)
        total_pages = (total + page_size - 1) // page_size
        
        # Response metadata bilan
        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'next': page < total_pages,
            'previous': page > 1,
            'results': items
        })


# MISOL 8: Request body validatsiyasi
class ValidatedRequestView(APIView):
    """
    Request ma'lumotlarini validatsiya qilish
    POST /api/validated/
    """
    def post(self, request):
        # Required fields
        required = ['username', 'email', 'password']
        errors = {}
        
        # Mavjudlikni tekshirish
        for field in required:
            if field not in request.data:
                errors[field] = f'{field} majburiy maydon'
            elif not request.data[field]:
                errors[field] = f'{field} bo\'sh bo\'lishi mumkin emas'
        
        if errors:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Email formatini tekshirish
        email = request.data.get('email')
        if '@' not in email:
            return Response(
                {'error': 'Email noto\'g\'ri formatda'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parol uzunligini tekshirish
        password = request.data.get('password')
        if len(password) < 8:
            return Response(
                {'error': 'Parol kamida 8 ta belgidan iborat bo\'lishi kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Hammasi OK
        return Response({
            'message': 'Validation muvaffaqiyatli',
            'username': request.data.get('username')
        }, status=status.HTTP_201_CREATED)


# MISOL 9: Conditional response
class ConditionalResponseView(APIView):
    """
    Shartga qarab turli javob qaytarish
    GET /api/conditional/?status=active|inactive|pending
    """
    def get(self, request):
        status_param = request.query_params.get('status', 'active')
        
        if status_param == 'active':
            return Response({
                'status': 'active',
                'message': 'Faol holatda',
                'data': ['item1', 'item2', 'item3']
            }, status=status.HTTP_200_OK)
        
        elif status_param == 'inactive':
            return Response({
                'status': 'inactive',
                'message': 'Nofaol holatda'
            }, status=status.HTTP_200_OK)
        
        elif status_param == 'pending':
            return Response({
                'status': 'pending',
                'message': 'Kutish holatida'
            }, status=status.HTTP_202_ACCEPTED)
        
        else:
            return Response({
                'error': 'Noto\'g\'ri status parametri'
            }, status=status.HTTP_400_BAD_REQUEST)


# MISOL 10: Kompleks response strukturasi
class ComplexResponseView(APIView):
    """
    Murakkab strukturali response
    GET /api/complex/
    """
    def get(self, request):
        return Response({
            'status': 'success',
            'timestamp': '2024-10-29T10:30:00Z',
            'data': {
                'user': {
                    'id': 1,
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'profile': {
                        'full_name': 'John Doe',
                        'avatar': 'https://example.com/avatar.jpg'
                    }
                },
                'posts': [
                    {
                        'id': 1,
                        'title': 'First Post',
                        'comments_count': 5
                    },
                    {
                        'id': 2,
                        'title': 'Second Post',
                        'comments_count': 3
                    }
                ],
                'stats': {
                    'total_posts': 2,
                    'total_comments': 8,
                    'followers': 150
                }
            },
            'meta': {
                'api_version': '1.0',
                'request_id': 'req-12345'
            }
        })


# URLs konfiguratsiyasi uchun misol:
"""
from django.urls import path
from .views import (
    RequestDataView,
    QueryParamsView,
    RequestMetaView,
    FileUploadView,
    ResponseFormatsView,
    CustomHeadersView,
    PaginatedDataView,
    ValidatedRequestView,
    ConditionalResponseView,
    ComplexResponseView
)

urlpatterns = [
    path('request-data/', RequestDataView.as_view()),
    path('query-params/', QueryParamsView.as_view()),
    path('request-meta/', RequestMetaView.as_view()),
    path('upload/', FileUploadView.as_view()),
    path('response-formats/', ResponseFormatsView.as_view()),
    path('custom-headers/', CustomHeadersView.as_view()),
    path('paginated/', PaginatedDataView.as_view()),
    path('validated/', ValidatedRequestView.as_view()),
    path('conditional/', ConditionalResponseView.as_view()),
    path('complex/', ComplexResponseView.as_view()),
]
"""