from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    """
    Book model with owner field for permissions
    """
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=100)
    isbn_number = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    pages = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    language = models.CharField(max_length=50, default='English')
    published_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    
    # YANGI: Owner field for permissions
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books',
        help_text='User who created this book'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    
    def __str__(self):
        return f"{self.title} by {self.author}"