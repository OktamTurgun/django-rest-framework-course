from django.db import models

class Book(models.Model):
    """
    Kitob modeli - Kutubxona tizimi uchun
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Kitob nomi",
        help_text="Kitobning to'liq nomi"
    )
    author = models.CharField(
        max_length=100,
        verbose_name="Muallif",
        help_text="Kitob muallifining ismi"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="ISBN",
        help_text="13 raqamli ISBN kodi"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Narx",
        help_text="Kitob narxi (so'm)"
    )
    published_date = models.DateField(
        verbose_name="Nashr sanasi",
        help_text="Kitob chop etilgan sana"
    )
    pages = models.IntegerField(
        default=0,
        verbose_name="Sahifalar soni"
    )
    language = models.CharField(
        max_length=50,
        default="O'zbek",
        verbose_name="Til"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Mavjudligi",
        help_text="Kitob sotuvda bormi?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqt"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqt"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def get_absolute_url(self):
        return f"/api/books/{self.pk}/"
    
    @property
    def is_new(self):
        """Kitob yangi ekanligini tekshirish (30 kun ichida qo'shilgan)"""
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(days=30)