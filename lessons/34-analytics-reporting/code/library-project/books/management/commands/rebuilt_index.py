"""
Management command to rebuild Elasticsearch index
"""
from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry


class Command(BaseCommand):
    help = 'Rebuild Elasticsearch index'
    
    def handle(self, *args, **options):
        self.stdout.write('Rebuilding Elasticsearch index...')
        
        # Delete and recreate index
        registry.update()
        
        self.stdout.write(self.style.SUCCESS('Index rebuilt successfully!'))