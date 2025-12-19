"""
Books Admin - FIXED
Faqat mavjud fieldlar bilan ishlaydi
"""
from django.contrib import admin
from books.models import Book, Author, Genre
from accounts.models import Profile


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin interface"""
    list_display = ['id', 'name', 'email', 'birth_date', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre admin interface"""
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book admin interface - FIXED"""
    
    # Faqat mavjud fieldlar
    list_display = [
        'id',
        'title',
        'author',
        'isbn_number',
        'price',
        'stock',
        'published_date',  # 'published' emas, 'published_date'!
        'created_at',
    ]
    
    list_filter = [
        'author',
        'published_date', 
        'created_at',
    ]
    
    search_fields = [
        'title',
        'isbn_number',
        'author__name',
    ]
    
    filter_horizontal = ['genres']  # ManyToMany field
    
    date_hierarchy = 'created_at'
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'isbn_number', 'description', 'author')
        }),
        ('Details', {
            'fields': ('pages', 'language', 'published_date', 'genres')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Inline editing uchun
    list_editable = ['price', 'stock']
    
    # Per page
    list_per_page = 50

from accounts.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'membership_type', 'is_premium',
        'books_borrowed', 'books_returned', 
        'subscribed_to_notifications', 'created_at'
    ]
    search_fields = ['user__username', 'user__email']
    readonly_fields = [
        'books_borrowed', 'books_returned', 
        'avatar_thumbnail', 'created_at', 'updated_at'
    ]
    list_filter = ['membership_type', 'is_premium', 'subscribed_to_notifications']

# Admin site customization
admin.site.site_header = "Library Management Admin"
admin.site.site_title = "Library Admin Portal"
admin.site.index_title = "Welcome to Library Management System"