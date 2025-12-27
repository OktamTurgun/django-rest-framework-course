from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

"""
Notifications Models
====================

Models:
- NotificationLog: Barcha yuborilgan bildirishnomalar tarixi
- DeviceToken: Foydalanuvchi qurilma tokenlari (FCM)
- UserPreferences: Foydalanuvchi bildirishnoma sozlamalari
"""

class NotificationType(models.TextChoices):
    """Bildirishnoma turlari"""
    EMAIL = 'email', _('Email')
    SMS = 'sms', _('SMS')
    PUSH = 'push', _('Push Notification')


class NotificationStatus(models.TextChoices):
    """Bildirishnoma holatlari"""
    PENDING = 'pending', _('Kutilmoqda')
    SENT = 'sent', _('Yuborildi')
    DELIVERED = 'delivered', _('Yetkazildi')
    FAILED = 'failed', _('Xatolik')
    RETRYING = 'retrying', _('Qayta urinilmoqda')


class NotificationLog(models.Model):
    """
    Barcha yuborilgan bildirishnomalar tarixi
    
    Bu model har bir yuborilgan bildirishnomani log qiladi:
    - Email, SMS yoki Push
    - Kimga yuborildi
    - Qachon yuborildi
    - Holati nima (yuborildi, xatolik, va h.k.)
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Foydalanuvchi')
    )
    
    notification_type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        verbose_name=_('Tur')
    )
    
    status = models.CharField(
        max_length=15,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
        verbose_name=_('Holat')
    )
    
    title = models.CharField(
        max_length=255,
        verbose_name=_('Sarlavha')
    )
    
    message = models.TextField(
        verbose_name=_('Xabar')
    )
    
    recipient = models.CharField(
        max_length=255,
        help_text=_('Email, telefon raqami yoki qurilma tokeni'),
        verbose_name=_('Qabul qiluvchi')
    )
    
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yuborilgan vaqt')
    )
    
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Yetkazilgan vaqt')
    )
    
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("O'qilgan vaqt")
    )
    
    error_message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Xato xabari')
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Qo\'shimcha ma\'lumotlar'),
        verbose_name=_('Metadata')
    )
    
    class Meta:
        verbose_name = _('Bildirishnoma Log')
        verbose_name_plural = _('Bildirishnoma Loglari')
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['-sent_at']),
            models.Index(fields=['user', '-sent_at']),
            models.Index(fields=['notification_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
    
    def mark_as_delivered(self):
        """Bildirishnomani yetkazilgan deb belgilash"""
        from django.utils import timezone
        self.status = NotificationStatus.DELIVERED
        self.delivered_at = timezone.now()
        self.save(update_fields=['status', 'delivered_at'])
    
    def mark_as_failed(self, error_message):
        """Bildirishnomani xatolik deb belgilash"""
        self.status = NotificationStatus.FAILED
        self.error_message = error_message
        self.save(update_fields=['status', 'error_message'])


class DeviceToken(models.Model):
    """
    Foydalanuvchi qurilma tokenlari (Firebase FCM)
    
    Har bir qurilma (mobil yoki web) uchun FCM tokeni saqlanadi.
    Push notification yuborish uchun bu tokenlar ishlatiladi.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='device_tokens',
        verbose_name=_('Foydalanuvchi')
    )
    
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('FCM Token')
    )
    
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('ios', 'iOS'),
            ('android', 'Android'),
            ('web', 'Web'),
        ],
        default='android',
        verbose_name=_('Qurilma Turi')
    )
    
    device_name = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Masalan: iPhone 12, Samsung Galaxy, Chrome Browser'),
        verbose_name=_('Qurilma Nomi')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Noto\'g\'ri tokenlar avtomatik o\'chiriladi'),
        verbose_name=_('Faol')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaratilgan')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yangilangan')
    )
    
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Oxirgi ishlatilgan')
    )
    
    class Meta:
        verbose_name = _('Qurilma Token')
        verbose_name_plural = _('Qurilma Tokenlari')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['token']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.device_type} - {self.token[:20]}..."
    
    def mark_as_used(self):
        """Tokenni ishlatilgan deb belgilash"""
        from django.utils import timezone
        self.last_used = timezone.now()
        self.save(update_fields=['last_used'])
    
    def deactivate(self):
        """Tokenni deaktivatsiya qilish (noto'g'ri token)"""
        self.is_active = False
        self.save(update_fields=['is_active'])


class UserPreferences(models.Model):
    """
    Foydalanuvchi bildirishnoma sozlamalari
    
    Har bir foydalanuvchi qaysi bildirishnomalarni olishni tanlaydi:
    - Email: Ha/Yo'q
    - SMS: Ha/Yo'q
    - Push: Ha/Yo'q
    - Sokin soatlar: 22:00 - 08:00
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name=_('Foydalanuvchi')
    )
    
    # Kanal sozlamalari
    email_enabled = models.BooleanField(
        default=True,
        verbose_name=_('Email Bildirishnomalar')
    )
    
    sms_enabled = models.BooleanField(
        default=True,
        verbose_name=_('SMS Bildirishnomalar')
    )
    
    push_enabled = models.BooleanField(
        default=True,
        verbose_name=_('Push Bildirishnomalar')
    )
    
    # Sokin soatlar
    quiet_hours_enabled = models.BooleanField(
        default=False,
        help_text=_('Belgilangan vaqtda bildirishnoma yuborilmaydi'),
        verbose_name=_('Sokin Soatlar Yoqilgan')
    )
    
    quiet_hours_start = models.TimeField(
        null=True,
        blank=True,
        help_text=_('Masalan: 22:00'),
        verbose_name=_('Sokin Soatlar Boshlanishi')
    )
    
    quiet_hours_end = models.TimeField(
        null=True,
        blank=True,
        help_text=_('Masalan: 08:00'),
        verbose_name=_('Sokin Soatlar Tugashi')
    )
    
    # Bildirishnoma turlari
    new_book_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Yangi Kitob Bildirishnomalari')
    )
    
    due_date_reminders = models.BooleanField(
        default=True,
        verbose_name=_('Muddat Eslatmalari')
    )
    
    overdue_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Muddati O\'tgan Bildirishnomalar')
    )
    
    system_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Tizim Bildirishnomalari')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaratilgan')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yangilangan')
    )
    
    class Meta:
        verbose_name = _('Foydalanuvchi Sozlamalari')
        verbose_name_plural = _('Foydalanuvchi Sozlamalari')
    
    def __str__(self):
        return f"{self.user.username} - Preferences"
    
    def is_channel_enabled(self, channel):
        """Kanal yoqilganligini tekshirish"""
        channel_map = {
            'email': self.email_enabled,
            'sms': self.sms_enabled,
            'push': self.push_enabled,
        }
        return channel_map.get(channel, False)
    
    def should_send_now(self):
        """Hozir bildirishnoma yuborish mumkinligini tekshirish (sokin soatlar)"""
        if not self.quiet_hours_enabled:
            return True
        
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return True
        
        from django.utils import timezone
        now = timezone.localtime().time()
        
        # Sokin soatlar yarim tunni kesib o'tadimi?
        if self.quiet_hours_start > self.quiet_hours_end:
            # Masalan: 22:00 - 08:00
            return now < self.quiet_hours_start and now >= self.quiet_hours_end
        else:
            # Masalan: 01:00 - 06:00
            return now < self.quiet_hours_start or now >= self.quiet_hours_end
