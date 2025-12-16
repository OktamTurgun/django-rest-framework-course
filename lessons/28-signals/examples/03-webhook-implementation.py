"""
Example 3: Webhook Implementation

Demonstrates:
- Webhook sender implementation
- HMAC signature generation
- Webhook retry logic
- Webhook receiver endpoint
- Security best practices
- Logging and monitoring

Webhooks are useful for:
- Real-time notifications to external systems
- Payment gateway integrations
- Third-party app integrations
- Event-driven architectures
"""

import requests
import hmac
import hashlib
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid

# ============================================================================
# MODELS
# ============================================================================

class Webhook(models.Model):
    """Webhook endpoint configuration"""
    
    EVENT_CHOICES = [
        ('book.created', 'Book Created'),
        ('book.updated', 'Book Updated'),
        ('book.deleted', 'Book Deleted'),
        ('user.registered', 'User Registered'),
        ('order.created', 'Order Created'),
        ('order.paid', 'Order Paid'),
        ('order.shipped', 'Order Shipped'),
        ('payment.success', 'Payment Success'),
        ('payment.failed', 'Payment Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Webhook name")
    url = models.URLField(help_text="Webhook endpoint URL")
    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
    secret = models.CharField(max_length=255, help_text="Secret key for HMAC")
    is_active = models.BooleanField(default=True)
    max_retries = models.IntegerField(default=3)
    timeout = models.IntegerField(default=10, help_text="Timeout in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['url', 'event']
    
    def __str__(self):
        return f"{self.name} - {self.event}"


class WebhookLog(models.Model):
    """Webhook delivery log"""
    
    webhook = models.ForeignKey(
        Webhook, 
        on_delete=models.CASCADE, 
        related_name='logs'
    )
    payload = models.JSONField()
    response_status = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    response_headers = models.JSONField(default=dict)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    duration_ms = models.IntegerField(null=True, help_text="Request duration in ms")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        status = "✅" if self.success else "❌"
        return f"{status} {self.webhook.event} - {self.created_at}"


# ============================================================================
# WEBHOOK SERVICE
# ============================================================================

class WebhookService:
    """Service for sending webhooks"""
    
    @staticmethod
    def generate_signature(secret: str, payload: str) -> str:
        """
        Generate HMAC SHA256 signature
        
        Args:
            secret: Secret key
            payload: JSON payload string
        
        Returns:
            Hex signature
        """
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def send_webhook(event_type: str, payload: Dict[str, Any]) -> None:
        """
        Send webhook to all registered endpoints for event type
        
        Args:
            event_type: Event type (e.g., 'book.created')
            payload: Event data
        """
        webhooks = Webhook.objects.filter(
            event=event_type,
            is_active=True
        )
        
        print(f"\n📤 Sending webhook for event: {event_type}")
        print(f"   Found {webhooks.count()} active webhook(s)")
        
        for webhook in webhooks:
            WebhookService._deliver(webhook, payload)
    
    @staticmethod
    def _deliver(webhook: Webhook, payload: Dict[str, Any], retry_count: int = 0) -> bool:
        """
        Deliver webhook to single endpoint
        
        Args:
            webhook: Webhook instance
            payload: Event data
            retry_count: Current retry attempt
        
        Returns:
            Success status
        """
        # Prepare payload with metadata
        full_payload = {
            'event': webhook.event,
            'timestamp': datetime.utcnow().isoformat(),
            'webhook_id': str(webhook.id),
            'data': payload
        }
        
        # Convert to JSON
        payload_json = json.dumps(full_payload, indent=2)
        
        # Generate signature
        signature = WebhookService.generate_signature(webhook.secret, payload_json)
        
        # Prepare headers
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': signature,
            'X-Webhook-Event': webhook.event,
            'X-Webhook-ID': str(webhook.id),
            'User-Agent': 'DjangoWebhook/1.0'
        }
        
        print(f"\n🔐 Webhook Details:")
        print(f"   URL: {webhook.url}")
        print(f"   Event: {webhook.event}")
        print(f"   Signature: {signature[:16]}...")
        print(f"   Retry: {retry_count}/{webhook.max_retries}")
        
        # Send request
        start_time = time.time()
        success = False
        response_status = None
        response_body = ""
        response_headers = {}
        error_message = ""
        
        try:
            response = requests.post(
                webhook.url,
                data=payload_json,
                headers=headers,
                timeout=webhook.timeout
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            response_status = response.status_code
            response_body = response.text[:1000]  # Limit body size
            response_headers = dict(response.headers)
            success = 200 <= response_status < 300
            
            if success:
                print(f"   ✅ Success: {response_status} ({duration_ms}ms)")
            else:
                print(f"   ❌ Failed: {response_status} ({duration_ms}ms)")
                error_message = f"HTTP {response_status}: {response_body[:100]}"
            
        except requests.exceptions.Timeout:
            duration_ms = webhook.timeout * 1000
            error_message = f"Timeout after {webhook.timeout}s"
            print(f"   ⏰ Timeout: {error_message}")
            
        except requests.exceptions.ConnectionError as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_message = f"Connection error: {str(e)[:100]}"
            print(f"   🔌 Connection Error: {error_message}")
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_message = f"Error: {str(e)[:100]}"
            print(f"   ❌ Error: {error_message}")
        
        # Log delivery
        WebhookLog.objects.create(
            webhook=webhook,
            payload=full_payload,
            response_status=response_status,
            response_body=response_body,
            response_headers=response_headers,
            success=success,
            error_message=error_message,
            retry_count=retry_count,
            duration_ms=duration_ms
        )
        
        # Retry logic
        if not success and retry_count < webhook.max_retries:
            retry_delay = 2 ** retry_count  # Exponential backoff: 1s, 2s, 4s
            print(f"   🔄 Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
            return WebhookService._deliver(webhook, payload, retry_count + 1)
        
        return success
    
    @staticmethod
    def verify_signature(request, secret: str) -> bool:
        """
        Verify webhook signature
        
        Args:
            request: Django request object
            secret: Secret key
        
        Returns:
            True if signature is valid
        """
        received_signature = request.headers.get('X-Webhook-Signature', '')
        
        if not received_signature:
            return False
        
        # Calculate expected signature
        body = request.body.decode('utf-8')
        expected_signature = WebhookService.generate_signature(secret, body)
        
        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(received_signature, expected_signature)


# ============================================================================
# WEBHOOK INTEGRATION WITH SIGNALS
# ============================================================================

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=10, decimal_places=2)


@receiver(post_save, sender=Book)
def send_book_webhook(sender, instance, created, **kwargs):
    """Send webhook when book is created or updated"""
    event = 'book.created' if created else 'book.updated'
    
    payload = {
        'id': instance.id,
        'title': instance.title,
        'author': instance.author,
        'isbn': instance.isbn,
        'price': str(instance.price),
    }
    
    WebhookService.send_webhook(event, payload)


@receiver(post_delete, sender=Book)
def send_book_delete_webhook(sender, instance, **kwargs):
    """Send webhook when book is deleted"""
    payload = {
        'id': instance.id,
        'title': instance.title,
    }
    
    WebhookService.send_webhook('book.deleted', payload)


# ============================================================================
# WEBHOOK RECEIVER ENDPOINT
# ============================================================================

@csrf_exempt
@require_POST
def webhook_receiver(request):
    """
    Receive webhook from external service
    
    Example: Receive payment webhooks from Stripe, PayPal, etc.
    """
    try:
        # Get webhook config (example: payment webhook)
        # In real app, determine webhook by URL path or header
        webhook_secret = settings.PAYMENT_WEBHOOK_SECRET
        
        # Verify signature
        if not WebhookService.verify_signature(request, webhook_secret):
            return JsonResponse({
                'error': 'Invalid signature'
            }, status=401)
        
        # Parse payload
        payload = json.loads(request.body)
        event_type = request.headers.get('X-Webhook-Event')
        
        print(f"\n📥 Webhook received:")
        print(f"   Event: {event_type}")
        print(f"   Payload: {json.dumps(payload, indent=2)[:200]}...")
        
        # Process based on event type
        if event_type == 'payment.success':
            process_payment_success(payload)
        elif event_type == 'payment.failed':
            process_payment_failed(payload)
        else:
            print(f"   ⚠️ Unknown event type: {event_type}")
        
        return JsonResponse({
            'status': 'received',
            'event': event_type
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


def process_payment_success(payload):
    """Process successful payment webhook"""
    order_id = payload.get('data', {}).get('order_id')
    print(f"   💰 Processing payment success for order {order_id}")
    # Update order status, send confirmation email, etc.


def process_payment_failed(payload):
    """Process failed payment webhook"""
    order_id = payload.get('data', {}).get('order_id')
    print(f"   ❌ Processing payment failure for order {order_id}")
    # Notify user, log error, etc.


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_webhook_system():
    """
    Demo complete webhook system
    
    Note: Uses webhook.site for testing
    Get your unique URL at https://webhook.site
    """
    
    print("=" * 70)
    print("DEMO: Webhook System")
    print("=" * 70)
    
    # ========== SETUP WEBHOOK ==========
    print("\n" + "=" * 70)
    print("SETUP: Creating webhook configuration")
    print("=" * 70)
    
    webhook = Webhook.objects.create(
        name="Test Webhook",
        url="https://webhook.site/your-unique-id",  # Replace with your URL
        event="book.created",
        secret="my-secret-key-123",
        is_active=True,
        max_retries=3,
        timeout=10
    )
    print(f"✅ Webhook created: {webhook.id}")
    
    # ========== TRIGGER WEBHOOK ==========
    print("\n" + "=" * 70)
    print("TEST 1: Triggering webhook")
    print("=" * 70)
    
    book = Book.objects.create(
        title="Python Programming",
        author="John Doe",
        isbn="1234567890123",
        price=29.99
    )
    # This will automatically trigger webhook via signal
    
    # ========== CHECK LOGS ==========
    print("\n" + "=" * 70)
    print("LOGS: Webhook delivery logs")
    print("=" * 70)
    
    logs = WebhookLog.objects.filter(webhook=webhook).order_by('-created_at')[:5]
    for log in logs:
        status = "✅" if log.success else "❌"
        print(f"{status} {log.webhook.event}")
        print(f"   Time: {log.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Status: {log.response_status}")
        print(f"   Duration: {log.duration_ms}ms")
        if log.error_message:
            print(f"   Error: {log.error_message}")
        print()
    
    # ========== MANUAL WEBHOOK ==========
    print("\n" + "=" * 70)
    print("TEST 2: Manual webhook send")
    print("=" * 70)
    
    WebhookService.send_webhook(
        'order.paid',
        {
            'order_id': 12345,
            'amount': 99.99,
            'currency': 'USD',
            'customer_email': 'customer@example.com'
        }
    )
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETED")
    print("=" * 70)
    print("\n💡 Check your webhook.site URL to see received webhooks!")


# ============================================================================
# WEBHOOK TESTING
# ============================================================================

def test_webhook_signature():
    """Test HMAC signature generation and verification"""
    
    print("\n" + "=" * 70)
    print("TEST: Webhook Signature")
    print("=" * 70)
    
    secret = "my-secret-key"
    payload = json.dumps({"event": "test", "data": {"id": 1}})
    
    # Generate signature
    signature = WebhookService.generate_signature(secret, payload)
    print(f"\n✅ Signature generated: {signature}")
    
    # Verify correct signature
    signature2 = WebhookService.generate_signature(secret, payload)
    is_valid = hmac.compare_digest(signature, signature2)
    print(f"✅ Same payload verification: {is_valid}")
    
    # Verify incorrect signature
    wrong_signature = WebhookService.generate_signature("wrong-secret", payload)
    is_valid = hmac.compare_digest(signature, wrong_signature)
    print(f"❌ Wrong secret verification: {is_valid}")
    
    # Verify tampered payload
    tampered_payload = json.dumps({"event": "test", "data": {"id": 999}})
    tampered_signature = WebhookService.generate_signature(secret, tampered_payload)
    is_valid = hmac.compare_digest(signature, tampered_signature)
    print(f"❌ Tampered payload verification: {is_valid}")


# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
✅ WEBHOOK BEST PRACTICES:

1. Security:
   ✓ Always use HMAC signature verification
   ✓ Use HTTPS only in production
   ✓ Validate signature using constant-time comparison
   ✓ Store secrets securely (environment variables)
   ✓ Implement rate limiting

2. Reliability:
   ✓ Implement retry logic with exponential backoff
   ✓ Set reasonable timeouts
   ✓ Log all webhook attempts
   ✓ Handle network errors gracefully
   ✓ Use queue system (Celery) for async delivery

3. Monitoring:
   ✓ Log webhook delivery status
   ✓ Track success/failure rates
   ✓ Monitor response times
   ✓ Alert on repeated failures
   ✓ Keep delivery logs

4. Payload:
   ✓ Include event type and timestamp
   ✓ Keep payload size reasonable
   ✓ Use consistent data format (JSON)
   ✓ Include webhook ID for debugging
   ✓ Version your payload schema

5. Receiver endpoint:
   ✓ Respond quickly (< 5s)
   ✓ Return 2xx for success
   ✓ Process async if needed
   ✓ Verify signature first
   ✓ Implement idempotency

6. Error handling:
   ✓ Log all errors
   ✓ Return appropriate HTTP status codes
   ✓ Don't expose internal errors
   ✓ Implement circuit breaker pattern
   ✓ Alert on critical failures

❌ AVOID:

1. Blocking operations in webhook send
2. Sending sensitive data without encryption
3. No retry logic
4. Not logging delivery attempts
5. Synchronous webhook delivery in request cycle
6. No timeout configuration
7. Exposing internal error details
8. Not validating received webhooks
"""

# ============================================================================
# PRODUCTION EXAMPLE
# ============================================================================

"""
# settings.py
WEBHOOK_SETTINGS = {
    'MAX_RETRIES': 3,
    'TIMEOUT': 10,
    'RETRY_DELAYS': [1, 2, 4],  # seconds
    'MAX_PAYLOAD_SIZE': 1024 * 100,  # 100KB
    'ALLOWED_EVENTS': [
        'book.created',
        'order.paid',
        'user.registered',
    ]
}

# tasks.py (Celery)
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def send_webhook_async(self, webhook_id, payload):
    '''Send webhook asynchronously'''
    try:
        webhook = Webhook.objects.get(id=webhook_id)
        WebhookService._deliver(webhook, payload)
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

# Usage in signals
@receiver(post_save, sender=Book)
def send_book_webhook(sender, instance, created, **kwargs):
    if created:
        payload = {...}
        webhooks = Webhook.objects.filter(
            event='book.created',
            is_active=True
        )
        for webhook in webhooks:
            send_webhook_async.delay(str(webhook.id), payload)
"""