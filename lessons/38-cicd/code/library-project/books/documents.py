"""
Elasticsearch document definitions for Books app
"""
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Book, Author, Genre


@registry.register_document
class BookDocument(Document):
    """Elasticsearch document for Book model"""
    
    # Author field
    author = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(
            fields={'keyword': fields.KeywordField()}
        ),
        'bio': fields.TextField(),
    })
    
    # YANGI: ObjectField instead of NestedField
    genres = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(
            fields={'keyword': fields.KeywordField()}
        ),
        'description': fields.TextField(),
    })
    
    # Custom fields
    title = fields.TextField(
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    
    description = fields.TextField()
    published_date = fields.DateField()
    price = fields.FloatField()
    pages = fields.IntegerField()
    stock = fields.IntegerField()
    is_available = fields.BooleanField()
    language = fields.KeywordField()
    
    class Index:
        name = 'books'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Book
        fields = [
            'isbn_number',
            'created_at',
            'updated_at',
        ]
        related_models = [Author, Genre]
    
    def get_queryset(self):
        return Book.objects.select_related('author').prefetch_related('genres').all()
    
    def get_indexing_queryset(self):
        return self.get_queryset()
    
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Author):
            return related_instance.books.all()
        elif isinstance(related_instance, Genre):
            return related_instance.books.all()