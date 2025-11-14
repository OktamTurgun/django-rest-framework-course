from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn_number = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    cover_image = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.author}"
