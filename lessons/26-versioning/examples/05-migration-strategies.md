# API Version Migration Strategies

##  Migration Nima?

API version migration - bu client'larni eski version'dan yangi version'ga o'tkazish jarayoni.

---

##  Migration Timeline

### Standard Timeline:

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Announcement (T-6 months)                         │
│  - Blog post, email notification                            │
│  - Migration guide published                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Beta Release (T-3 months)                         │
│  - V2 available as beta                                     │
│  - Early adopters test                                      │
│  - Feedback collection                                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Stable Release (T)                                │
│  - V2 production ready                                      │
│  - V1 marked deprecated                                     │
│  - Warning headers added                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: Grace Period (T+6 months)                         │
│  - Both versions active                                     │
│  - Migration support                                        │
│  - Regular reminders                                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 5: Final Warning (T+11 months)                       │
│  - Last 30 days warning                                     │
│  - Intensive communication                                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 6: Sunset (T+12 months)                              │
│  - V1 returns 410 Gone                                      │
│  - V2 only active                                           │
└─────────────────────────────────────────────────────────────┘
```

---

##  Phase 1: Announcement

### Communication Channels:

1. **Blog Post**
```markdown
# Announcing API v2

We're excited to announce API v2 with improved features!

## What's New
- Author as nested object
- Better error messages
- Improved performance

## Timeline
- Beta: June 1, 2024
- Stable: July 1, 2024
- v1 Sunset: January 1, 2025

## Migration Guide
See our [migration guide](https://docs.example.com/migration)
```

2. **Email Notification**
```
Subject: Important: API v2 Coming Soon

Dear API Users,

We're releasing API v2 on July 1, 2024. 
API v1 will be sunset on January 1, 2025.

What you need to do:
1. Review the migration guide
2. Update your application
3. Test with v2 beta

Need help? Contact: api-support@example.com
```

3. **In-App Notification**
```json
{
  "notification": {
    "type": "api_deprecation",
    "message": "API v1 will be deprecated on Jan 1, 2025",
    "action_url": "https://docs.example.com/migration",
    "severity": "warning"
  }
}
```

---

##  Phase 2: Beta Testing

### Beta Access:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2-beta', 'v2'],
}

# Middleware for beta users
class BetaAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('/api/v2-beta/'):
            # Check beta access
            if not self.has_beta_access(request.user):
                return JsonResponse({
                    'error': 'Beta access required',
                    'message': 'Contact api-support@example.com'
                }, status=403)
        
        return self.get_response(request)
    
    def has_beta_access(self, user):
        """Check if user has beta access"""
        return user.is_authenticated and user.groups.filter(
            name='beta_testers'
        ).exists()
```

### Beta Feedback Collection:

```python
# views.py
class BetaFeedbackView(APIView):
    """Collect feedback on v2 beta"""
    
    def post(self, request):
        feedback = {
            'user': request.user.id,
            'endpoint': request.data.get('endpoint'),
            'feedback': request.data.get('feedback'),
            'rating': request.data.get('rating'),
            'timestamp': timezone.now()
        }
        
        # Save to database
        BetaFeedback.objects.create(**feedback)
        
        # Notify team
        send_slack_notification(
            channel='#api-feedback',
            text=f"New beta feedback: {feedback['feedback']}"
        )
        
        return Response({'message': 'Thank you for your feedback!'})
```

---

##  Phase 3: Deprecation Warnings

### HTTP Headers:

```python
# middleware.py
from datetime import datetime

class DeprecationMiddleware:
    """Add deprecation headers to v1 responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.sunset_date = datetime(2025, 1, 1)
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add deprecation headers for v1
        if request.path.startswith('/api/v1/'):
            response['Warning'] = (
                '299 - "API v1 is deprecated. '
                'Please migrate to v2 by 2025-01-01. '
                'See https://docs.example.com/migration"'
            )
            response['Sunset'] = self.sunset_date.strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            )
            response['Link'] = (
                '<https://api.example.com/v2/>; '
                'rel="successor-version"'
            )
            
            # Days until sunset
            days_left = (self.sunset_date - datetime.now()).days
            response['X-Days-Until-Sunset'] = str(days_left)
        
        return response
```

### Response Body Warning:

```python
# serializers.py
class DeprecatedSerializerMixin:
    """Add deprecation warning to response"""
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Add deprecation notice
        if self.context['request'].version == 'v1':
            data['_deprecated'] = {
                'message': 'This API version is deprecated',
                'sunset_date': '2025-01-01',
                'migration_guide': 'https://docs.example.com/migration',
                'new_version': 'v2'
            }
        
        return data
```

---

##  Phase 4: Monitoring & Metrics

### Track Version Usage:

```python
# middleware.py
class VersionMetricsMiddleware:
    """Track API version usage"""
    
    def __call__(self, request):
        version = getattr(request, 'version', 'unknown')
        
        # Increment counter
        cache.incr(f'api_usage:{version}:{date.today()}')
        
        # Log user-specific usage
        if request.user.is_authenticated:
            cache.sadd(
                f'api_users:{version}',
                request.user.id
            )
        
        response = self.get_response(request)
        return response

# Analytics view
class VersionAnalyticsView(APIView):
    """API version usage analytics"""
    
    def get(self, request):
        today = date.today()
        
        analytics = {
            'v1': {
                'requests_today': cache.get(f'api_usage:v1:{today}', 0),
                'unique_users': cache.scard('api_users:v1'),
            },
            'v2': {
                'requests_today': cache.get(f'api_usage:v2:{today}', 0),
                'unique_users': cache.scard('api_users:v2'),
            }
        }
        
        return Response(analytics)
```

### Email Notifications to Unmigrated Users:

```python
# management/commands/notify_unmigrated_users.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail

class Command(BaseCommand):
    help = 'Notify users still using v1'
    
    def handle(self, *args, **options):
        # Get v1 users
        v1_users = cache.smembers('api_users:v1')
        v2_users = cache.smembers('api_users:v2')
        
        # Users only on v1 (not migrated)
        unmigrated = v1_users - v2_users
        
        # Send emails
        messages = []
        for user_id in unmigrated:
            user = User.objects.get(id=user_id)
            messages.append((
                'Action Required: Migrate to API v2',
                f'Hello {user.first_name}, ...',
                'noreply@example.com',
                [user.email]
            ))
        
        send_mass_mail(messages)
        
        self.stdout.write(
            f'Sent {len(messages)} migration reminders'
        )
```

---

##  Phase 5: Final Warning

### 30 Days Before Sunset:

```python
# middleware.py
class FinalWarningMiddleware:
    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path.startswith('/api/v1/'):
            days_left = (self.sunset_date - datetime.now()).days
            
            if days_left <= 30:
                # Critical warning
                response['Warning'] = (
                    '299 - "CRITICAL: API v1 will be shutdown in '
                    f'{days_left} days! Migrate NOW!"'
                )
                
                # Response body warning
                if isinstance(response.data, dict):
                    response.data['_critical_warning'] = {
                        'message': f'API v1 shuts down in {days_left} days!',
                        'action': 'Migrate to v2 immediately',
                        'support': 'api-support@example.com'
                    }
        
        return response
```

### Daily Email Reminders:

```python
# celery task
@shared_task
def send_daily_sunset_reminders():
    """Send daily reminders for last 30 days"""
    days_left = (SUNSET_DATE - datetime.now()).days
    
    if days_left <= 30:
        unmigrated_users = get_unmigrated_users()
        
        for user in unmigrated_users:
            send_mail(
                subject=f'URGENT: {days_left} days until v1 shutdown',
                message=f'Your app still uses v1. Migrate NOW!',
                from_email='urgent@example.com',
                recipient_list=[user.email]
            )
```

---

##  Phase 6: Sunset (Shutdown)

### Return 410 Gone:

```python
# middleware.py
class SunsetMiddleware:
    """Return 410 Gone for sunset versions"""
    
    def __call__(self, request):
        if request.path.startswith('/api/v1/'):
            return JsonResponse({
                'error': 'API version sunset',
                'message': 'API v1 was sunset on 2025-01-01',
                'code': 'version_sunset',
                'details': {
                    'sunset_date': '2025-01-01',
                    'current_version': 'v2',
                    'migration_guide': 'https://docs.example.com/migration',
                    'support': 'api-support@example.com'
                }
            }, status=410)  # 410 Gone
        
        return self.get_response(request)
```

### Gradual Rollout:

```python
# Gradually increase error rate before full sunset
class GradualSunsetMiddleware:
    """Gradually sunset v1"""
    
    def __call__(self, request):
        if request.path.startswith('/api/v1/'):
            days_until_sunset = (SUNSET_DATE - datetime.now()).days
            
            if days_until_sunset <= 0:
                # Full sunset
                return sunset_response()
            
            elif days_until_sunset <= 7:
                # Last week: 50% requests fail
                if random.random() < 0.5:
                    return sunset_response()
            
            elif days_until_sunset <= 14:
                # 2 weeks before: 25% fail
                if random.random() < 0.25:
                    return sunset_response()
        
        return self.get_response(request)
```

---

##  Migration Documentation

### Complete Migration Guide Template:

```markdown
# API Migration Guide: v1 → v2

## Overview
This guide helps you migrate from API v1 to v2.

## Timeline
- v1 Sunset: January 1, 2025
- Migration deadline: December 31, 2024

## Breaking Changes

### 1. Author Field Structure
**Before (v1):**
```json
{
  "author": "John Doe"
}
```

**After (v2):**
```json
{
  "author": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Code Change:**
```javascript
// v1
const authorName = book.author;

// v2
const authorName = book.author.name;
```

### 2. ISBN Required
ISBN field is now required in POST requests.

**Migration:**
```javascript
// v1
POST /api/v1/books/
{
  "title": "Book"
}

// v2
POST /api/v2/books/
{
  "title": "Book",
  "isbn": "1234567890123"  // REQUIRED
}
```

## Testing
1. Update to v2 in development
2. Run integration tests
3. Deploy to staging
4. Test thoroughly
5. Deploy to production

## Support
- Email: api-support@example.com
- Slack: #api-migration
- Office hours: Mon-Fri 9am-5pm PST
```

---

## Migration Checklist

### For API Providers:

- [ ] Announce migration 6+ months ahead
- [ ] Publish detailed migration guide
- [ ] Release beta version for testing
- [ ] Add deprecation warnings to v1
- [ ] Monitor version usage metrics
- [ ] Provide migration support
- [ ] Send regular reminders
- [ ] Final warning 30 days before
- [ ] Execute sunset on scheduled date
- [ ] Post-sunset monitoring

### For API Consumers:

- [ ] Read migration guide
- [ ] Test v2 in development
- [ ] Update application code
- [ ] Update tests
- [ ] Deploy to staging
- [ ] Verify functionality
- [ ] Deploy to production
- [ ] Monitor for errors
- [ ] Complete before deadline

---

##  Best Practices

1. **Long Grace Period**: Minimum 6 months, 12 months better
2. **Clear Communication**: Multiple channels, regular updates
3. **Support Team**: Dedicated migration support
4. **Gradual Approach**: Beta → Stable → Deprecation → Sunset
5. **Metrics**: Track adoption rates
6. **Flexibility**: Extend deadline if needed
7. **Documentation**: Comprehensive migration guide
8. **Testing**: Provide sandbox environment

---

Remember: Good migration = Happy developers!