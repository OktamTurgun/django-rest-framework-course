from django.shortcuts import render

"""
Notifications Views
===================

API endpoints:
- NotificationLogViewSet: Notification tarixi
- DeviceTokenViewSet: Device token boshqarish
- UserPreferencesViewSet: Foydalanuvchi sozlamalari
- SendNotificationView: Notification yuborish (admin)
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import NotificationLog, DeviceToken, UserPreferences
from .serializers import (
    NotificationLogSerializer,
    NotificationLogListSerializer,
    DeviceTokenSerializer,
    DeviceTokenCreateSerializer,
    UserPreferencesSerializer,
    SendNotificationSerializer,
    SendSMSSerializer,
    SendPushSerializer,
    NotificationStatsSerializer,
)
from .services import notification_manager


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Notification tarixi ViewSet
    
    Foydalanuvchi o'z notification tarixini ko'radi.
    
    Endpoints:
    - GET /api/notifications/ - Barcha notificationlar
    - GET /api/notifications/{id}/ - Bitta notification
    - GET /api/notifications/stats/ - Statistika
    - POST /api/notifications/mark_as_read/ - O'qilgan deb belgilash
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Serializer tanlash"""
        if self.action == 'list':
            return NotificationLogListSerializer
        elif self.action == 'stats':
            return NotificationStatsSerializer
        return NotificationLogSerializer
    
    def get_queryset(self):
        """
        Foydalanuvchining o'z notificationlari
        
        Filters:
        - ?type=sms - Faqat SMS
        - ?type=push - Faqat Push
        - ?status=sent - Faqat yuborilganlar
        - ?search=kitob - Qidirish
        """
        user = self.request.user
        queryset = NotificationLog.objects.filter(user=user)
        
        # Type filter
        notification_type = self.request.query_params.get('type')
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        # Status filter
        notification_status = self.request.query_params.get('status')
        if notification_status:
            queryset = queryset.filter(status=notification_status)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(message__icontains=search)
            )
        
        # Date range
        days = self.request.query_params.get('days')
        if days:
            try:
                days = int(days)
                date_from = timezone.now() - timedelta(days=days)
                queryset = queryset.filter(sent_at__gte=date_from)
            except ValueError:
                pass
        
        return queryset.order_by('-sent_at')
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Notification statistikasi
        
        GET /api/notifications/stats/
        
        Returns:
            Umumiy statistika va so'nggi notificationlar
        """
        user = request.user
        
        # Umumiy statistika
        total_sent = NotificationLog.objects.filter(user=user).count()
        total_delivered = NotificationLog.objects.filter(
            user=user,
            status='delivered'
        ).count()
        total_failed = NotificationLog.objects.filter(
            user=user,
            status='failed'
        ).count()
        
        # Turlari bo'yicha
        sms_count = NotificationLog.objects.filter(
            user=user,
            notification_type='sms'
        ).count()
        push_count = NotificationLog.objects.filter(
            user=user,
            notification_type='push'
        ).count()
        email_count = NotificationLog.objects.filter(
            user=user,
            notification_type='email'
        ).count()
        
        # Success rate
        success_rate = (
            (total_delivered / total_sent * 100)
            if total_sent > 0
            else 0
        )
        
        # So'nggi notificationlar
        recent = NotificationLog.objects.filter(user=user).order_by('-sent_at')[:5]
        
        data = {
            'total_sent': total_sent,
            'total_delivered': total_delivered,
            'total_failed': total_failed,
            'sms_count': sms_count,
            'push_count': push_count,
            'email_count': email_count,
            'success_rate': round(success_rate, 2),
            'recent_notifications': NotificationLogListSerializer(
                recent,
                many=True
            ).data
        }
        
        serializer = NotificationStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Notificationni o'qilgan deb belgilash
        
        POST /api/notifications/{id}/mark_as_read/
        """
        notification = self.get_object()
        
        if notification.status != 'read':
            notification.read_at = timezone.now()
            notification.status = 'read'
            notification.save(update_fields=['status', 'read_at'])
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Barcha notificationlarni o'qilgan deb belgilash
        
        POST /api/notifications/mark_all_as_read/
        """
        user = request.user
        updated = NotificationLog.objects.filter(
            user=user,
            status__in=['sent', 'delivered']
        ).update(
            status='read',
            read_at=timezone.now()
        )
        
        return Response({
            'success': True,
            'updated_count': updated,
            'message': f'{updated} ta notification o\'qilgan deb belgilandi'
        })
    
    @action(detail=False, methods=['delete'])
    def clear_old(self, request):
        """
        Eski notificationlarni o'chirish (30 kundan eski)
        
        DELETE /api/notifications/clear_old/
        """
        user = request.user
        date_limit = timezone.now() - timedelta(days=30)
        
        deleted_count, _ = NotificationLog.objects.filter(
            user=user,
            sent_at__lt=date_limit
        ).delete()
        
        return Response({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'{deleted_count} ta eski notification o\'chirildi'
        })


class DeviceTokenViewSet(viewsets.ModelViewSet):
    """
    Device Token ViewSet
    
    Foydalanuvchi o'z qurilmalarini boshqaradi.
    
    Endpoints:
    - GET /api/device-tokens/ - Barcha tokenlar
    - POST /api/device-tokens/ - Yangi token qo'shish
    - DELETE /api/device-tokens/{id}/ - Token o'chirish
    - POST /api/device-tokens/{id}/deactivate/ - Deaktivatsiya
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Serializer tanlash"""
        if self.action == 'create':
            return DeviceTokenCreateSerializer
        return DeviceTokenSerializer
    
    def get_queryset(self):
        """Foydalanuvchining o'z tokenlari"""
        return DeviceToken.objects.filter(
            user=self.request.user
        ).order_by('-last_used')
    
    def perform_create(self, serializer):
        """Token yaratish"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Tokenni deaktivatsiya qilish
        
        POST /api/device-tokens/{id}/deactivate/
        """
        token = self.get_object()
        token.deactivate()
        
        return Response({
            'success': True,
            'message': 'Token deaktivatsiya qilindi'
        })
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Tokenni aktivatsiya qilish
        
        POST /api/device-tokens/{id}/activate/
        """
        token = self.get_object()
        token.is_active = True
        token.save(update_fields=['is_active'])
        
        return Response({
            'success': True,
            'message': 'Token aktivatsiya qilindi'
        })
    
    @action(detail=False, methods=['delete'])
    def clear_inactive(self, request):
        """
        Faol bo'lmagan tokenlarni o'chirish
        
        DELETE /api/device-tokens/clear_inactive/
        """
        user = request.user
        deleted_count, _ = DeviceToken.objects.filter(
            user=user,
            is_active=False
        ).delete()
        
        return Response({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'{deleted_count} ta nofaol token o\'chirildi'
        })


class UserPreferencesViewSet(viewsets.ModelViewSet):
    """
    User Preferences ViewSet
    
    Foydalanuvchi notification sozlamalarini boshqaradi.
    
    Endpoints:
    - GET /api/preferences/ - Sozlamalarni olish
    - PUT /api/preferences/ - Sozlamalarni yangilash
    - PATCH /api/preferences/ - Qisman yangilash
    """
    
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'post']  # Faqat GET, PUT, PATCH
    
    
    def get_object(self):
        """Foydalanuvchi sozlamalarini olish yoki yaratish"""
        obj, created = UserPreferences.objects.get_or_create(
            user=self.request.user
        )
        return obj
    
    def list(self, request, *args, **kwargs):
        """
        Sozlamalarni olish
        
        GET /api/preferences/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Sozlamalarni yangilash
        
        PUT /api/preferences/
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=kwargs.get('partial', False)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'message': 'Sozlamalar yangilandi',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['put', 'patch'])
    def update_preferences(self, request):
        prefs = self.get_object()
        partial = request.method.lower() == 'patch'
        serializer = self.get_serializer(prefs, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'message': 'Sozlamalar yangilandi',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def enable_all(self, request):
        """
        Barcha notificationlarni yoqish
        
        POST /api/preferences/enable_all/
        """
        prefs = self.get_object()
        prefs.email_enabled = True
        prefs.sms_enabled = True
        prefs.push_enabled = True
        prefs.save()
        
        serializer = self.get_serializer(prefs)
        return Response({
            'success': True,
            'message': 'Barcha notificationlar yoqildi',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def disable_all(self, request):
        """
        Barcha notificationlarni o'chirish
        
        POST /api/preferences/disable_all/
        """
        prefs = self.get_object()
        prefs.email_enabled = False
        prefs.sms_enabled = False
        prefs.push_enabled = False
        prefs.save()
        
        serializer = self.get_serializer(prefs)
        return Response({
            'success': True,
            'message': 'Barcha notificationlar o\'chirildi',
            'data': serializer.data
        })


class SendNotificationView(APIView):
    """
    Notification yuborish (Admin only)
    
    POST /api/send-notification/
    
    Body:
    {
        "notification_type": "push",
        "user_ids": [1, 2, 3],
        "title": "Yangi kitob!",
        "message": "Yangi kitob qo'shildi",
        "data": {"book_id": 123}
    }
    """
    
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        """Notification yuborish"""
        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Yuborish
        result = serializer.send()
        
        return Response(result, status=status.HTTP_200_OK)


class SendSMSView(APIView):
    """
    SMS yuborish
    
    POST /api/send-sms/
    
    Body:
    {
        "phone_number": "+998901234567",
        "message": "Test SMS"
    }
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """SMS yuborish"""
        serializer = SendSMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        message = serializer.validated_data['message']
        
        # SMS yuborish
        result = notification_manager.send_sms(
            user=request.user,
            message=message,
            phone_number=phone_number
        )
        
        if result.get('success'):
            return Response({
                'success': True,
                'message': 'SMS yuborildi',
                'message_id': result.get('message_id')
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'SMS yuborishda xatolik')
            }, status=status.HTTP_400_BAD_REQUEST)


class SendPushView(APIView):
    """
    Push notification yuborish
    
    POST /api/send-push/
    
    Body:
    {
        "title": "Yangi kitob",
        "body": "Yangi kitob qo'shildi",
        "data": {"book_id": 123}
    }
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Push yuborish"""
        serializer = SendPushSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        title = serializer.validated_data['title']
        body = serializer.validated_data['body']
        data = serializer.validated_data.get('data', {})
        
        # Push yuborish
        result = notification_manager.send_push(
            user=request.user,
            title=title,
            body=body,
            data=data
        )
        
        if result.get('success'):
            return Response({
                'success': True,
                'message': 'Push yuborildi',
                'message_id': result.get('message_id')
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'Push yuborishda xatolik')
            }, status=status.HTTP_400_BAD_REQUEST)


class TestNotificationView(APIView):
    """
    Test notification yuborish
    
    POST /api/test-notification/
    
    Foydalanuvchiga test notification yuboradi
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Test notification"""
        user = request.user
        
        # SMS test
        sms_result = notification_manager.send_sms(
            user=user,
            message="Bu test SMS. Agar bu xabarni ko'rsangiz, SMS tizimi ishlayapti!",
            phone_number="+998901234567"
        )
        
        # Push test
        push_result = notification_manager.send_push(
            user=user,
            title="Test Push Notification",
            body="Agar bu xabarni ko'rsangiz, push notification ishlayapti!",
            data={'test': True}
        )
        
        return Response({
            'success': True,
            'message': 'Test notificationlar yuborildi',
            'sms': {
                'success': sms_result.get('success'),
                'message_id': sms_result.get('message_id')
            },
            'push': {
                'success': push_result.get('success'),
                'message_id': push_result.get('message_id')
            }
        })
