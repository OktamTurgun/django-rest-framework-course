from django.core.management.base import BaseCommand
from utils.validators import validate_environment


class Command(BaseCommand):
    help = 'Validate environment variables'
    
    def handle(self, *args, **options):
        try:
            validate_environment()
            self.stdout.write(
                self.style.SUCCESS('✅ Environment validation successful!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Validation failed: {str(e)}')
            )
            exit(1)