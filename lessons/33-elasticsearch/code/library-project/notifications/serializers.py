"""
Notifications Serializers
=========================

API uchun serializers:
- NotificationLogSerializer: Notification tarixi
- DeviceTokenSerializer: Device token boshqarish
- UserPreferencesSerializer: Foydalanuvchi sozlamalari
- SendNotificationSerializer: Notification yuborish
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NotificationLog, DeviceToken, UserPreferences


class NotificationLogSerializer(serializers.ModelSerializer):
    """
    NotificationLog serializer
    
    Foydalanuvchi o'z notification tarixini ko'rishi uchun
    """
    
    user = serializers.StringRelatedField(read_only=True)
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = NotificationLog
        fields = [
            'id',
            'user',
            'notification_type',
            'notification_type_display',
            'status',
            'status_display',
            'title',
            'message',
            'recipient',
            'sent_at',
            'delivered_at',
            'error_message',
            'metadata',
            'time_ago',
        ]
        read_only_fields = [
            'id',
            'user',
            'sent_at',
            'delivered_at',
            'error_message',
        ]
    
    def get_time_ago(self, obj):
        """Necha vaqt oldin yuborilgan"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.sent_at
        
        if diff < timedelta(minutes=1):
            return "Hozirgina"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} daqiqa oldin"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} soat oldin"
        else:
            days = diff.days
            return f"{days} kun oldin"


class NotificationLogListSerializer(serializers.ModelSerializer):
    """
    NotificationLog list serializer (qisqaroq versiya)
    """
    
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = NotificationLog
        fields = [
            'id',
            'notification_type',
            'notification_type_display',
            'status',
            'status_display',
            'title',
            'sent_at',
        ]


class DeviceTokenSerializer(serializers.ModelSerializer):
    """
    DeviceToken serializer
    
    Foydalanuvchi o'z qurilmalarini boshqarishi uchun
    """
    
    user = serializers.StringRelatedField(read_only=True)
    device_type_display = serializers.CharField(
        source='get_device_type_display',
        read_only=True
    )
    is_current = serializers.SerializerMethodField()
    
    class Meta:
        model = DeviceToken
        fields = [
            'id',
            'user',
            'token',
            'device_type',
            'device_type_display',
            'device_name',
            'is_active',
            'created_at',
            'updated_at',
            'last_used',
            'is_current',
        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
            'last_used',
        ]
        extra_kwargs = {
            'token': {'write_only': True}  # Tokenni faqat yozish uchun
        }
    
    def get_is_current(self, obj):
        """Joriy qurilma ekanligini aniqlash"""
        # Request'dan token olish va taqqoslash
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            current_token = request.data.get('token')
            return obj.token == current_token
        return False
    
    def validate_token(self, value):
        """Token validatsiyasi"""
        if not value or len(value) < 10:
            raise serializers.ValidationError(
                "Token juda qisqa yoki noto'g'ri"
            )
        return value
    
    def create(self, validated_data):
        """
        Token yaratish yoki yangilash
        
        Agar token mavjud bo'lsa, uni yangilaydi
        """
        user = self.context['request'].user
        token = validated_data.get('token')
        
        # Mavjud tokenni topish
        existing_token = DeviceToken.objects.filter(token=token).first()
        
        if existing_token:
            # Tokenni yangilash
            for key, value in validated_data.items():
                setattr(existing_token, key, value)
            existing_token.save()
            return existing_token
        
        # Yangi token yaratish
        validated_data['user'] = user
        return super().create(validated_data)


class DeviceTokenCreateSerializer(serializers.ModelSerializer):
    """
    Device token yaratish uchun sodda serializer
    """
    
    class Meta:
        model = DeviceToken
        fields = ['token', 'device_type', 'device_name']
    
    def validate_token(self, value):
        """Token validatsiyasi"""
        if not value or len(value) < 10:
            raise serializers.ValidationError("Token noto'g'ri")
        return value
    
    def create(self, validated_data):
        """Token yaratish"""
        user = self.context['request'].user
        token = validated_data.get('token')
        
        # Mavjud tokenni topish
        existing_token = DeviceToken.objects.filter(token=token).first()
        
        if existing_token:
            # Tokenni yangilash
            existing_token.device_type = validated_data.get('device_type', existing_token.device_type)
            existing_token.device_name = validated_data.get('device_name', existing_token.device_name)
            existing_token.is_active = True
            existing_token.save()
            return existing_token
        
        # Yangi token
        validated_data['user'] = user
        return super().create(validated_data)


class UserPreferencesSerializer(serializers.ModelSerializer):
    """
    UserPreferences serializer
    
    Foydalanuvchi o'z sozlamalarini boshqarishi uchun
    """
    
    user = serializers.StringRelatedField(read_only=True)
    quiet_hours_status = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPreferences
        fields = [
            'id',
            'user',
            'email_enabled',
            'sms_enabled',
            'push_enabled',
            'quiet_hours_enabled',
            'quiet_hours_start',
            'quiet_hours_end',
            'quiet_hours_status',
            'new_book_notifications',
            'due_date_reminders',
            'overdue_notifications',
            'system_notifications',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_quiet_hours_status(self, obj):
        """Sokin soatlar holati"""
        if not obj.quiet_hours_enabled:
            return {
                'enabled': False,
                'message': 'Sokin soatlar o\'chirilgan'
            }
        
        if obj.should_send_now():
            return {
                'enabled': True,
                'active': False,
                'message': 'Bildirishnomalar yoqilgan'
            }
        else:
            return {
                'enabled': True,
                'active': True,
                'message': 'Sokin soatlar faol (bildirishnomalar o\'chirilgan)'
            }
    
    def validate(self, data):
        """Validatsiya"""
        # Agar quiet_hours yoqilgan bo'lsa, vaqtlar kiritilgan bo'lishi kerak
        if data.get('quiet_hours_enabled'):
            if not data.get('quiet_hours_start') or not data.get('quiet_hours_end'):
                raise serializers.ValidationError({
                    'quiet_hours': 'Sokin soatlar vaqtlarini kiriting'
                })
        
        return data


class SendNotificationSerializer(serializers.Serializer):
    """
    Notification yuborish uchun serializer
    
    Admin yoki tizim tomonidan notification yuborish
    """
    
    NOTIFICATION_TYPES = [
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('email', 'Email'),
    ]
    
    notification_type = serializers.ChoiceField(
        choices=NOTIFICATION_TYPES,
        help_text="Notification turi"
    )
    
    # Qabul qiluvchilar
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="Foydalanuvchi ID'lari ro'yxati"
    )
    
    all_users = serializers.BooleanField(
        default=False,
        help_text="Barcha foydalanuvchilarga yuborish"
    )
    
    # Xabar
    title = serializers.CharField(
        max_length=255,
        required=False,
        help_text="Sarlavha (push uchun)"
    )
    
    message = serializers.CharField(
        help_text="Xabar matni"
    )
    
    # Qo'shimcha
    data = serializers.JSONField(
        required=False,
        help_text="Qo'shimcha ma'lumotlar"
    )
    
    def validate(self, data):
        """Validatsiya"""
        # Kamida bitta recipient bo'lishi kerak
        if not data.get('all_users') and not data.get('user_ids'):
            raise serializers.ValidationError(
                "user_ids yoki all_users ni tanlang"
            )
        
        # Push uchun title majburiy
        if data.get('notification_type') == 'push' and not data.get('title'):
            raise serializers.ValidationError({
                'title': 'Push notification uchun sarlavha majburiy'
            })
        
        return data
    
    def send(self):
        """
        Notificationni yuborish
        
        Returns:
            dict: Natija
        """
        from .services import notification_manager
        
        notification_type = self.validated_data['notification_type']
        all_users = self.validated_data.get('all_users', False)
        user_ids = self.validated_data.get('user_ids', [])
        title = self.validated_data.get('title', '')
        message = self.validated_data['message']
        data = self.validated_data.get('data', {})
        
        results = []
        
        # Barcha foydalanuvchilarga
        if all_users:
            result = notification_manager.send_to_all_users(
                title=title,
                body=message,
                notification_type=notification_type,
                data=data
            )
            return result
        
        # Tanlangan foydalanuvchilarga
        users = User.objects.filter(id__in=user_ids)
        
        for user in users:
            if notification_type == 'sms':
                result = notification_manager.send_sms(
                    user=user,
                    message=message,
                    metadata=data
                )
            elif notification_type == 'push':
                result = notification_manager.send_push(
                    user=user,
                    title=title,
                    body=message,
                    data=data
                )
            else:
                continue
            
            results.append({
                'user_id': user.id,
                'username': user.username,
                'success': result.get('success', False),
                'error': result.get('error')
            })
        
        success_count = sum(1 for r in results if r['success'])
        failure_count = len(results) - success_count
        
        return {
            'success': True,
            'total': len(results),
            'success_count': success_count,
            'failure_count': failure_count,
            'results': results
        }


class SendSMSSerializer(serializers.Serializer):
    """
    SMS yuborish uchun sodda serializer
    """
    
    phone_number = serializers.CharField(
        max_length=20,
        help_text="Telefon raqami (+998901234567)"
    )
    
    message = serializers.CharField(
        max_length=160,
        help_text="SMS matni (max 160 belgi)"
    )
    
    def validate_phone_number(self, value):
        """Telefon raqam validatsiyasi"""
        # + belgisini olib tashlash
        clean = value.replace('+', '').replace(' ', '').replace('-', '')
        
        if not clean.isdigit():
            raise serializers.ValidationError("Faqat raqamlar")
        
        if len(clean) < 10:
            raise serializers.ValidationError("Juda qisqa telefon raqami")
        
        return value


class SendPushSerializer(serializers.Serializer):
    """
    Push notification yuborish uchun sodda serializer
    """
    
    title = serializers.CharField(
        max_length=100,
        help_text="Sarlavha"
    )
    
    body = serializers.CharField(
        help_text="Xabar matni"
    )
    
    data = serializers.JSONField(
        required=False,
        help_text="Qo'shimcha data (JSON)"
    )


class NotificationStatsSerializer(serializers.Serializer):
    """
    Notification statistikasi
    """
    
    total_sent = serializers.IntegerField()
    total_delivered = serializers.IntegerField()
    total_failed = serializers.IntegerField()
    
    sms_count = serializers.IntegerField()
    push_count = serializers.IntegerField()
    email_count = serializers.IntegerField()
    
    success_rate = serializers.FloatField()
    
    recent_notifications = NotificationLogListSerializer(many=True)