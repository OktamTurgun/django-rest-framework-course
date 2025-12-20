from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from books.models import Book
import time


class Command(BaseCommand):
    help = 'Test query performance'

    def handle(self, *args, **kwargs):
        # Test 1: Without optimization
        reset_queries()
        start = time.time()
        books = Book.objects.all()[:100]
        for book in books:
            _ = book.author.name
        time_without = time.time() - start
        queries_without = len(connection.queries)

        # Test 2: With optimization
        reset_queries()
        start = time.time()
        books = Book.objects.select_related('author').all()[:100]
        for book in books:
            _ = book.author.name
        time_with = time.time() - start
        queries_with = len(connection.queries)

        # Results
        self.stdout.write(self.style.SUCCESS(f'\nPerformance Test Results:'))
        self.stdout.write(f'Without optimization: {queries_without} queries, {time_without:.4f}s')
        self.stdout.write(f'With optimization: {queries_with} queries, {time_with:.4f}s')
        self.stdout.write(self.style.SUCCESS(f'Improvement: {((queries_without - queries_with) / queries_without * 100):.1f}%'))