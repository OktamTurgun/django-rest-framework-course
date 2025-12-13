"""
Example 04: Sentry Integration

Bu file'da Sentry error tracking service bilan integratsiya qilishni ko'ramiz.

Topics:
- Sentry installation
- Basic configuration
- Error capture
- Performance monitoring
- User context
- Custom tags and breadcrumbs
- Release tracking
"""

from os import name
import sentry_sdk
import logging
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from books.models import Book
from books.serializers import BookSerializer
from django.http import Http404


# ============================================
# 1. BASIC SENTRY SETUP
# ============================================

def basic_sentry_setup():
    """
    Basic Sentry initialization
    
    Get your DSN from: https://sentry.io/settings/projects/
    """
    sentry_sdk.init(
        dsn="https://your-dsn@sentry.io/project-id",
        
        # Enable performance monitoring
        traces_sample_rate=1.0,
        
        # Environment
        environment="development",
    )


# ============================================
# 2. DJANGO SENTRY CONFIGURATION
# ============================================

def django_sentry_config():
    """
    Complete Django Sentry configuration for settings.py
    """
    
    import os
    
    sentry_sdk.init(
        # DSN from environment variable
        dsn=os.environ.get('SENTRY_DSN'),
        
        # Integrations
        integrations=[
            DjangoIntegration(),
            RedisIntegration(),
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=logging.ERROR  # Send errors as events
            ),
        ],
        
        # Performance monitoring
        traces_sample_rate=1.0,  # 100% of transactions
        
        # Profiles
        profiles_sample_rate=1.0,
        
        # Send user PII (Personal Identifiable Information)
        send_default_pii=True,
        
        # Environment
        environment=os.environ.get('ENVIRONMENT', 'development'),
        
        # Release tracking
        release=os.environ.get('RELEASE_VERSION', 'dev'),
        
        # Before send hook
        before_send=before_send_hook,
        
        # Ignore specific errors
        ignore_errors=[KeyboardInterrupt, SystemExit],
    )


def before_send_hook(event, hint):
    """
    Modify or filter events before sending to Sentry
    """
    # Don't send events from anonymous users (optional)
    if event.get('user', {}).get('username') == 'anonymous':
        return None
    
    # Add custom data
    event['extra']['custom_data'] = 'some value'
    
    return event


# ============================================
# 3. CAPTURING EXCEPTIONS
# ============================================

def capture_exceptions_examples():
    """Examples of capturing exceptions"""
    
    # Automatic capture (handled by Django integration)
    def automatic_capture():
        """
        Django integration automatically captures unhandled exceptions
        """
        result = 1 / 0  # This will be automatically sent to Sentry
    
    
    # Manual capture
    def manual_capture():
        """
        Manually capture exceptions
        """
        try:
            result = 1 / 0
        except ZeroDivisionError as e:
            sentry_sdk.capture_exception(e)
    
    
    # Capture with context
    def capture_with_context():
        """
        Capture exception with additional context
        """
        try:
            process_payment(amount=100)
        except PaymentError as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("payment", {
                    "amount": 100,
                    "currency": "USD",
                    "user_id": 123
                })
                scope.set_tag("payment_method", "credit_card")
                sentry_sdk.capture_exception(e)
    
    
    # Capture message (not exception)
    def capture_message():
        """
        Capture custom message
        """
        sentry_sdk.capture_message(
            "Something important happened",
            level="info"  # debug, info, warning, error, fatal
        )


# ============================================
# 4. USER CONTEXT
# ============================================

def set_user_context(request):
    """
    Set user context for error tracking
    """
    if request.user.is_authenticated:
        sentry_sdk.set_user({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "ip_address": request.META.get('REMOTE_ADDR'),
        })
    else:
        sentry_sdk.set_user({
            "ip_address": request.META.get('REMOTE_ADDR'),
        })


# Middleware for automatic user context
class SentryUserContextMiddleware:
    """
    Middleware to automatically set user context
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Set user context
        if request.user.is_authenticated:
            sentry_sdk.set_user({
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            })
        
        response = self.get_response(request)
        return response


# ============================================
# 5. CUSTOM TAGS
# ============================================

def using_custom_tags():
    """
    Use custom tags to categorize errors
    """
    
    # Set single tag
    sentry_sdk.set_tag("page_locale", "en-US")
    sentry_sdk.set_tag("api_version", "v2")
    
    # Set multiple tags in view
    def book_detail_view(request, pk):
        sentry_sdk.set_tag("book_id", pk)
        sentry_sdk.set_tag("view", "book_detail")
        
        try:
            book = Book.objects.get(pk=pk)
            return Response(BookSerializer(book).data)
        except Book.DoesNotExist:
            sentry_sdk.set_tag("error_type", "not_found")
            raise Http404()


# ============================================
# 6. BREADCRUMBS
# ============================================

def using_breadcrumbs():
    """
    Add breadcrumbs to track user actions leading to error
    """
    
    # Manual breadcrumb
    sentry_sdk.add_breadcrumb(
        category='auth',
        message='User logged in',
        level='info',
        data={
            'user_id': 123,
            'username': 'john_doe'
        }
    )
    
    # In a view
    def process_order(request):
        sentry_sdk.add_breadcrumb(
            category='order',
            message='Processing order',
            data={'order_id': request.data.get('order_id')}
        )
        
        # ... processing logic ...
        
        sentry_sdk.add_breadcrumb(
            category='order',
            message='Order processed successfully',
        )


# ============================================
# 7. PERFORMANCE MONITORING
# ============================================

def performance_monitoring():
    """
    Track performance with transactions
    """
    
    # Manual transaction
    with sentry_sdk.start_transaction(
        op="task",
        name="process_books"
    ) as transaction:
        
        # Start a span for database query
        with transaction.start_child(
            op="db",
            description="Fetch books"
        ) as span:
            books = Book.objects.all()[:100]
        
        # Start another span for processing
        with transaction.start_child(
            op="process",
            description="Process books"
        ) as span:
            for book in books:
                process_book(book)


# Decorator for automatic transaction tracking
from functools import wraps

def track_performance(op="function", description=None):
    """
    Decorator to track function performance
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with sentry_sdk.start_transaction(
                op=op,
                name=description or func.__name__
            ):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# Usage
@track_performance(op="api", description="Create Book")
def create_book_view(request):
    # View logic
    pass


# ============================================
# 8. RELEASE TRACKING
# ============================================

def setup_release_tracking():
    """
    Track releases in Sentry
    """
    
    import os
    
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        
        # Release version
        release=f"library-api@{os.environ.get('VERSION', '1.0.0')}",
        
        # Environment
        environment=os.environ.get('ENVIRONMENT', 'production'),
    )


# Upload source maps and create release
"""
# In your CI/CD pipeline:

# 1. Create release
sentry-cli releases new library-api@1.0.0

# 2. Upload source maps
sentry-cli releases files library-api@1.0.0 upload-sourcemaps ./dist

# 3. Finalize release
sentry-cli releases finalize library-api@1.0.0

# 4. Create deploy
sentry-cli releases deploys library-api@1.0.0 new -e production
"""


# ============================================
# 9. ADVANCED CONFIGURATION
# ============================================

ADVANCED_SENTRY_CONFIG = {
    'dsn': 'https://your-dsn@sentry.io/project-id',
    
    # Integrations
    'integrations': [
        DjangoIntegration(),
        RedisIntegration(),
        CeleryIntegration(),
        LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        ),
    ],
    
    # Performance
    'traces_sample_rate': 0.1,  # 10% in production
    'profiles_sample_rate': 0.1,
    
    # Data privacy
    'send_default_pii': False,  # Don't send PII in production
    
    # Environment
    'environment': 'production',
    
    # Release
    'release': 'library-api@1.0.0',
    
    # Filters
    'ignore_errors': [
        KeyboardInterrupt,
        'OperationalError',
    ],
    
    # Before send
    'before_send': lambda event, hint: filter_sensitive_data(event, hint),
    
    # Sample rate for errors
    'sample_rate': 1.0,  # 100% of errors
    
    # Attach stack trace
    'attach_stacktrace': True,
    
    # Max breadcrumbs
    'max_breadcrumbs': 50,
}


def filter_sensitive_data(event, hint):
    """
    Filter sensitive data before sending to Sentry
    """
    # Remove password from request data
    if 'request' in event:
        if 'data' in event['request']:
            data = event['request']['data']
            if isinstance(data, dict) and 'password' in data:
                data['password'] = '[Filtered]'
    
    # Remove sensitive headers
    if 'headers' in event.get('request', {}):
        headers = event['request']['headers']
        sensitive_headers = ['Authorization', 'Cookie', 'X-API-Key']
        for header in sensitive_headers:
            if header in headers:
                headers[header] = '[Filtered]'
    
    return event


# ============================================
# 10. DJANGO VIEWS INTEGRATION
# ============================================

class BookViewSetWithSentry:
    """
    Example ViewSet with Sentry integration
    """
    
    def create(self, request):
        # Set user context
        sentry_sdk.set_user({
            "id": request.user.id,
            "username": request.user.username,
        })
        
        # Add breadcrumb
        sentry_sdk.add_breadcrumb(
            category='book',
            message='Creating new book',
            data={'title': request.data.get('title')}
        )
        
        # Set tags
        sentry_sdk.set_tag("operation", "create_book")
        sentry_sdk.set_tag("api_version", "v2")
        
        # Start transaction for performance monitoring
        with sentry_sdk.start_transaction(
            op="http.server",
            name="POST /api/v2/books/"
        ) as transaction:
            
            try:
                # Validation span
                with transaction.start_child(
                    op="validate",
                    description="Validate book data"
                ):
                    serializer = BookSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                
                # Database span
                with transaction.start_child(
                    op="db.query",
                    description="Create book in database"
                ):
                    book = serializer.save()
                
                # Success breadcrumb
                sentry_sdk.add_breadcrumb(
                    category='book',
                    message='Book created successfully',
                    data={'book_id': book.id}
                )
                
                return Response(serializer.data, status=201)
                
            except ValidationError as e:
                # Capture validation error
                sentry_sdk.capture_exception(e)
                raise
                
            except Exception as e:
                # Capture unexpected error with context
                with sentry_sdk.push_scope() as scope:
                    scope.set_context("book_data", request.data)
                    scope.set_tag("error_type", "unexpected")
                    sentry_sdk.capture_exception(e)
                raise


# ============================================
# TESTING SENTRY
# ============================================

def test_sentry():
    """
    Test Sentry integration
    """
    print("=" * 60)
    print("TESTING SENTRY INTEGRATION")
    print("=" * 60)


# Test 1: Capture exception
print("\n1. Testing exception capture:")
try:
    result = 1 / 0
except ZeroDivisionError as e:
    sentry_sdk.capture_exception(e)
    print("   ✓ Exception captured")

# Test 2: Capture message
print("\n2. Testing message capture:")
sentry_sdk.capture_message("Test message from Sentry example", level="info")
print("   ✓ Message captured")

# Test 3: Add breadcrumb
print("\n3. Testing breadcrumb:")
sentry_sdk.add_breadcrumb(
    category='test',
    message='Test breadcrumb',
    level='info'
)
print("   ✓ Breadcrumb added")

# Test 4: Set user context
print("\n4. Testing user context:")
sentry_sdk.set_user({
    "id": 123,
    "username": "test_user",
    "email": "test@example.com"
})
print("   ✓ User context set")

# Test 5: Set tags
print("\n5. Testing tags:")
sentry_sdk.set_tag("test_tag", "test_value")
print("   ✓ Tag set")

print("\n" + "=" * 60)
print("Check your Sentry dashboard at: https://sentry.io/")
print("=" * 60)


# ============================================
# BEST PRACTICES
# ============================================

"""
BEST PRACTICES FOR SENTRY:

✅ Use environment variables for DSN
✅ Set appropriate sample rates (lower in production)
✅ Filter sensitive data (passwords, tokens)
✅ Set user context for all requests
✅ Use tags to categorize errors
✅ Add breadcrumbs for user journey
✅ Track releases for better debugging
✅ Use performance monitoring for slow operations
✅ Set up alerts for critical errors
✅ Regularly review and resolve errors
✅ Don't send PII in production
✅ Use before_send hook to filter data
✅ Integrate with CI/CD pipeline
✅ Monitor error trends and patterns
✅ Set up proper team permissions
"""


# ============================================
# INSTALLATION INSTRUCTIONS
# ============================================

"""
Install Sentry SDK
pip install sentry-sdk
Install integrations (if needed)
pip install sentry-sdk[django]
Environment variables (.env)
SENTRY_DSN=https://your-dsn@sentry.io/project-id
ENVIRONMENT=production
RELEASE_VERSION=1.0.0
In settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
sentry_sdk.init(
dsn=os.environ.get('SENTRY_DSN'),
integrations=[DjangoIntegration()],
traces_sample_rate=0.1,
environment=os.environ.get('ENVIRONMENT', 'development'),
)
"""


# ============================================
# RUN TESTS
# ============================================

if name == 'main':
    # Note: You need to configure Sentry DSN first
    print("To test Sentry, configure your DSN in settings.py")
    print("Then run: python examples_04_sentry.py")
    # Uncomment to test (after configuring DSN)
    # basic_sentry_setup()
    # test_sentry()
