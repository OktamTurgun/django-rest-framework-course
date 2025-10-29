"""
HTTP Status kodlar bilan ishlash misollari
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# MISOL 1: 2xx - Muvaffaqiyatli javoblar
class SuccessResponsesView(APIView):
    """
    Muvaffaqiyatli status kodlar (2xx)
    """
    def get(self, request):
        """200 OK - Standart muvaffaqiyatli javob"""
        return Response(
            {'message': 'Ma\'lumot muvaffaqiyatli olindi'},
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        """201 CREATED - Yangi resurs yaratildi"""
        new_item = {
            'id': 123,
            'name': request.data.get('name'),
            'created': True
        }
        return Response(
            new_item,
            status=status.HTTP_201_CREATED
        )
    
    def delete(self, request, pk=None):
        """204 NO CONTENT - Muvaffaqiyatli, lekin javob yo'q"""
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    
    def put(self, request, pk=None):
        """202 ACCEPTED - So'rov qabul qilindi (asinxron ishlov)"""
        return Response(
            {'message': 'So\'rov qayta ishlanmoqda'},
            status=status.HTTP_202_ACCEPTED
        )


# MISOL 2: 4xx - Mijoz xatolari
class ClientErrorsView(APIView):
    """
    Mijoz xatolari status kodlari (4xx)
    """
    def get(self, request):
        error_type = request.query_params.get('type', '400')
        
        if error_type == '400':
            """400 BAD REQUEST - Noto'g'ri so'rov"""
            return Response(
                {
                    'error': 'Noto\'g\'ri so\'rov',
                    'details': 'Majburiy maydonlar kiritilmagan'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        elif error_type == '401':
            """401 UNAUTHORIZED - Autentifikatsiya kerak"""
            return Response(
                {
                    'error': 'Autentifikatsiya talab qilinadi',
                    'details': 'Token kiritilmagan yoki noto\'g\'ri'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        elif error_type == '403':
            """403 FORBIDDEN - Ruxsat yo'q"""
            return Response(
                {
                    'error': 'Ruxsat berilmagan',
                    'details': 'Bu amalni bajarish uchun huquqingiz yo\'q'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        elif error_type == '404':
            """404 NOT FOUND - Resurs topilmadi"""
            return Response(
                {
                    'error': 'Topilmadi',
                    'details': 'So\'ralgan resurs mavjud emas'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        elif error_type == '405':
            """405 METHOD NOT ALLOWED - Metod ruxsat berilmagan"""
            return Response(
                {
                    'error': 'Metod ruxsat berilmagan',
                    'details': 'Bu endpoint POST metodini qo\'llab-quvvatlamaydi'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        elif error_type == '409':
            """409 CONFLICT - Konflikt"""
            return Response(
                {
                    'error': 'Konflikt',
                    'details': 'Bu nomdagi foydalanuvchi allaqachon mavjud'
                },
                status=status.HTTP_409_CONFLICT
            )
        
        elif error_type == '422':
            """422 UNPROCESSABLE ENTITY - Qayta ishlab bo'lmaydi"""
            return Response(
                {
                    'error': 'Validation xatosi',
                    'details': {
                        'email': ['Email formati noto\'g\'ri'],
                        'age': ['Yosh 0 dan katta bo\'lishi kerak']
                    }
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        elif error_type == '429':
            """429 TOO MANY REQUESTS - Juda ko'p so'rovlar"""
            return Response(
                {
                    'error': 'Juda ko\'p so\'rovlar',
                    'details': 'Iltimos 60 soniyadan keyin qayta urinib ko\'ring'
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        else:
            return Response({'error': 'Noto\'g\'ri error type'})


# MISOL 3: 5xx - Server xatolari
class ServerErrorsView(APIView):
    """
    Server xatolari status kodlari (5xx)
    """
    def get(self, request):
        error_type = request.query_params.get('type', '500')
        
        if error_type == '500':
            """500 INTERNAL SERVER ERROR - Server xatosi"""
            return Response(
                {
                    'error': 'Ichki server xatosi',
                    'details': 'Nimadir noto\'g\'ri ketdi'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        elif error_type == '503':
            """503 SERVICE UNAVAILABLE - Xizmat mavjud emas"""
            return Response(
                {
                    'error': 'Xizmat vaqtincha mavjud emas',
                    'details': 'Texnik ishlar olib borilmoqda'
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        else:
            return Response({'error': 'Noto\'g\'ri error type'})


# MISOL 4: CRUD operatsiyalarida status kodlar
class BookCRUDView(APIView):
    """
    CRUD operatsiyalarida to'g'ri status kodlarni ishlatish
    """
    # Demo ma'lumotlar
    books = {
        1: {'id': 1, 'title': 'Django Book', 'author': 'John'},
        2: {'id': 2, 'title': 'Python Book', 'author': 'Jane'}
    }
    
    def get(self, request, pk=None):
        """
        GET /api/books/ - 200 OK
        GET /api/books/1/ - 200 OK yoki 404 NOT FOUND
        """
        if pk:
            # Bitta kitobni olish
            book = self.books.get(pk)
            if book:
                return Response(book, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Kitob topilmadi'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Barcha kitoblarni olish
            return Response(
                list(self.books.values()),
                status=status.HTTP_200_OK
            )
    
    def post(self, request):
        """
        POST /api/books/ - 201 CREATED yoki 400 BAD REQUEST
        """
        # Validation
        if 'title' not in request.data or 'author' not in request.data:
            return Response(
                {'error': 'title va author majburiy'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Yangi kitob yaratish
        new_id = max(self.books.keys()) + 1 if self.books else 1
        new_book = {
            'id': new_id,
            'title': request.data['title'],
            'author': request.data['author']
        }
        self.books[new_id] = new_book
        
        return Response(
            new_book,
            status=status.HTTP_201_CREATED
        )
    
    def put(self, request, pk):
        """
        PUT /api/books/1/ - 200 OK yoki 404 NOT FOUND
        """
        if pk not in self.books:
            return Response(
                {'error': 'Kitob topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Kitobni yangilash
        self.books[pk] = {
            'id': pk,
            'title': request.data.get('title', self.books[pk]['title']),
            'author': request.data.get('author', self.books[pk]['author'])
        }
        
        return Response(
            self.books[pk],
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, pk):
        """
        PATCH /api/books/1/ - 200 OK yoki 404 NOT FOUND
        """
        if pk not in self.books:
            return Response(
                {'error': 'Kitob topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Qisman yangilash
        if 'title' in request.data:
            self.books[pk]['title'] = request.data['title']
        if 'author' in request.data:
            self.books[pk]['author'] = request.data['author']
        
        return Response(
            self.books[pk],
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, pk):
        """
        DELETE /api/books/1/ - 204 NO CONTENT yoki 404 NOT FOUND
        """
        if pk not in self.books:
            return Response(
                {'error': 'Kitob topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Kitobni o'chirish
        del self.books[pk]
        
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# MISOL 5: Status kodlar bo'yicha qo'llanma
class StatusCodeGuideView(APIView):
    """
    Status kodlar qo'llanmasi
    GET /api/status-guide/
    """
    def get(self, request):
        guide = {
            'success_codes': {
                '200': {
                    'name': 'OK',
                    'description': 'Standart muvaffaqiyatli javob',
                    'use_case': 'GET, PUT operatsiyalari'
                },
                '201': {
                    'name': 'CREATED',
                    'description': 'Yangi resurs yaratildi',
                    'use_case': 'POST operatsiyasi'
                },
                '204': {
                    'name': 'NO CONTENT',
                    'description': 'Muvaffaqiyatli, lekin javob yo\'q',
                    'use_case': 'DELETE operatsiyasi'
                }
            },
            'client_errors': {
                '400': {
                    'name': 'BAD REQUEST',
                    'description': 'Noto\'g\'ri so\'rov',
                    'use_case': 'Validation xatolari'
                },
                '401': {
                    'name': 'UNAUTHORIZED',
                    'description': 'Autentifikatsiya kerak',
                    'use_case': 'Token yo\'q yoki noto\'g\'ri'
                },
                '403': {
                    'name': 'FORBIDDEN',
                    'description': 'Ruxsat yo\'q',
                    'use_case': 'Huquq yetarli emas'
                },
                '404': {
                    'name': 'NOT FOUND',
                    'description': 'Resurs topilmadi',
                    'use_case': 'Mavjud bo\'lmagan ID'
                }
            },
            'server_errors': {
                '500': {
                    'name': 'INTERNAL SERVER ERROR',
                    'description': 'Server xatosi',
                    'use_case': 'Dasturiy xato'
                },
                '503': {
                    'name': 'SERVICE UNAVAILABLE',
                    'description': 'Xizmat mavjud emas',
                    'use_case': 'Texnik ishlar'
                }
            }
        }
        return Response(guide)


# MISOL 6: Custom error handler
class CustomErrorHandlerView(APIView):
    """
    Custom error handling bilan APIView
    """
    def post(self, request):
        try:
            # Ba'zi bir operatsiya
            value = int(request.data.get('value', 0))
            result = 100 / value
            
            return Response({
                'result': result
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            # Noto'g'ri qiymat
            return Response(
                {
                    'error': 'Validation xatosi',
                    'details': 'Qiymat son bo\'lishi kerak'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ZeroDivisionError:
            # Nolga bo'lish
            return Response(
                {
                    'error': 'Matematik xato',
                    'details': 'Nolga bo\'lish mumkin emas'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            # Boshqa xatolar
            return Response(
                {
                    'error': 'Server xatosi',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# URLs konfiguratsiyasi uchun misol:
"""
from django.urls import path
from .views import (
    SuccessResponsesView,
    ClientErrorsView,
    ServerErrorsView,
    BookCRUDView,
    StatusCodeGuideView,
    CustomErrorHandlerView
)

urlpatterns = [
    path('success/', SuccessResponsesView.as_view()),
    path('client-errors/', ClientErrorsView.as_view()),
    path('server-errors/', ServerErrorsView.as_view()),
    path('books/', BookCRUDView.as_view()),
    path('books/<int:pk>/', BookCRUDView.as_view()),
    path('status-guide/', StatusCodeGuideView.as_view()),
    path('error-handler/', CustomErrorHandlerView.as_view()),
]
"""