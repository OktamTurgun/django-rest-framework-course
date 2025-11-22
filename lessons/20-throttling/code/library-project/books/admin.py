from django.contrib import admin
from .models import Book, Author, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin panel"""
    list_display = ['name', 'email', 'birth_date', 'total_books', 'created_at']
    list_filter = ['birth_date', 'created_at']
    search_fields = ['name', 'email', 'bio']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'birth_date')
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_books(self, obj):
        """Jami kitoblar soni"""
        return obj.books.count()
    total_books.short_description = 'Total Books'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre admin panel"""
    list_display = ['name', 'total_books', 'created_at']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    def total_books(self, obj):
        """Jami kitoblar soni"""
        return obj.books.count()
    total_books.short_description = 'Total Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book admin panel"""
    list_display = [
        'title', 'id', 'author', 'price', 'pages', 
        'published', 'published_date', 'owner', 'created_at'
    ]
    list_filter = ['author', 'genres', 'published', 'language', 'published_date', 'created_at']
    search_fields = ['title', 'subtitle', 'isbn_number', 'author__name', 'publisher']
    date_hierarchy = 'published_date'
    filter_horizontal = ['genres']  # ManyToMany uchun yaxshi UI
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'author', 'owner')
        }),
        ('Publication Details', {
            'fields': ('isbn_number', 'publisher', 'published_date', 'published')
        }),
        ('Content Details', {
            'fields': ('pages', 'language', 'genres')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Automatically set owner to current user when creating
    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt yaratilayotgan bo'lsa
            obj.owner = request.user
        super().save_model(request, obj, form, change)