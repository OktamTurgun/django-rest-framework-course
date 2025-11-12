from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ("id","title", "author", "published_date", "isbn_number", "price", "published")
  search_fields = ("title", "author", "isbn_number", "language")
  list_filter = ("published_date", "language", "published")