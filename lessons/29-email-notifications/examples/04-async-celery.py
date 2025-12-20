"""
Example 4: Async Email with Celery

Demonstrates:
- Celery setup for Django
- Async email tasks
- Periodic email tasks
- Task retry logic
- Task monitoring
- Best practices for production

Use cases:
- Welcome emails (async)
- Bulk email campaigns
- Scheduled newsletters
- Reminder emails
- Report generation

Prerequisites:
- pip install celery redis
- Redis server running
- Celery worker running
"""

from celery import shared_task, group, chord
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.conf import settings
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# ============================================================================
# BASIC ASYNC TASKS
# ============================================================================

@shared_task
def send_welcome_email_task(user_id):
    """
    Async task to send welcome email
    
    Usage:
        send_welcome_email_task.delay(user.id)
    
    Returns:
        str: Success/error message
    """
    print("\n" + "="*60)
    print("TASK: Send Welcome Email")
    print("="*60)
    
    try:
        user = User.objects.get(id=user_id)
        
        context = {
            'user': user,
            'site_url': 'https://library.com',
        }
        
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Welcome to Library System',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )
        
        logger.info(f"✅ Welcome email sent to {user.email}")
        return f"Email sent to {user.email}"
        
    except User.DoesNotExist:
        logger.error(f"❌ User {user_id} not found")
        return f"User {user_id} not found"
        
    except Exception as e:
        logger.error(f"❌ Error sending email: {e}")
        raise  # Re-raise for Celery retry


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_with_retry(self, to_email, subject, message):
    """
    Email task with automatic retry
    
    Parameters:
    - bind=True: Access task instance (self)
    - max_retries=3: Retry up to 3 times
    - default_retry_delay=60: Wait 60s between retries
    
    Usage:
        send_email_with_retry.delay('user@example.com', 'Subject', 'Message')
    """
    print("\n" + "="*60)
    print("TASK: Send Email with Retry")
    print("="*60)
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
        )
        
        print(f"✅ Email sent to {to_email}")
        return f"Success: {to_email}"
        
    except Exception as exc:
        print(f"❌ Error: {exc}")
        print(f"   Retry: {self.request.retries}/{self.max_retries}")
        
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


# ============================================================================
# BULK EMAIL TASKS
# ============================================================================

@shared_task
def send_bulk_email_task(user_ids, subject, template_name, context_data):
    """
    Send same email to multiple users
    
    Args:
        user_ids: List of user IDs
        subject: Email subject
        template_name: Template path
        context_data: Shared context data
    
    Usage:
        send_bulk_email_task.delay(
            [1, 2, 3],
            'Newsletter',
            'emails/newsletter.html',
            {'month': 'December'}
        )
    """
    print("\n" + "="*60)
    print("TASK: Bulk Email")
    print("="*60)
    
    users = User.objects.filter(id__in=user_ids)
    sent_count = 0
    failed_count = 0
    
    for user in users:
        try:
            # Personalize context for each user
            context = {
                **context_data,
                'user': user,
            }
            
            html_message = render_to_string(template_name, context)
            plain_message = strip_tags(html_message)
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            sent_count += 1
            
        except Exception as e:
            logger.error(f"Failed to send to {user.email}: {e}")
            failed_count += 1
    
    result = f"Sent: {sent_count}, Failed: {failed_count}"
    print(f"✅ {result}")
    return result


@shared_task
def send_personalized_bulk_email(recipients_data):
    """
    Send personalized emails to multiple recipients
    
    Args:
        recipients_data: List of dicts with user_id and custom_data
    
    Example:
        recipients_data = [
            {'user_id': 1, 'custom_data': {'book_count': 5}},
            {'user_id': 2, 'custom_data': {'book_count': 12}},
        ]
    """
    print("\n" + "="*60)
    print("TASK: Personalized Bulk Email")
    print("="*60)
    
    results = []
    
    for recipient in recipients_data:
        user_id = recipient['user_id']
        custom_data = recipient['custom_data']
        
        try:
            user = User.objects.get(id=user_id)
            
            context = {
                'user': user,
                **custom_data  # Merge custom data
            }
            
            html_message = render_to_string('emails/personalized.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject='Your Personalized Update',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
            )
            
            results.append({'user_id': user_id, 'status': 'sent'})
            
        except Exception as e:
            results.append({'user_id': user_id, 'status': 'failed', 'error': str(e)})
    
    return results


# ============================================================================
# CELERY GROUPS & CHAINS
# ============================================================================

@shared_task
def send_single_email(user_id, template_name):
    """Single email task for use in groups"""
    user = User.objects.get(id=user_id)
    context = {'user': user}
    html_message = render_to_string(template_name, context)
    
    send_mail(
        subject='Notification',
        message=strip_tags(html_message),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
    )
    
    return f"Sent to {user.email}"


def example_1_task_group():
    """
    Send multiple emails in parallel using group
    
    All tasks execute simultaneously
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Task Group (Parallel)")
    print("="*60)
    
    user_ids = [1, 2, 3, 4, 5]
    
    # Create group of tasks
    job = group([
        send_single_email.s(user_id, 'emails/notification.html')
        for user_id in user_ids
    ])
    
    # Execute all tasks in parallel
    result = job.apply_async()
    
    print(f"✅ Group task started")
    print(f"   Task ID: {result.id}")
    print(f"   Tasks: {len(user_ids)}")
    
    # Wait for all tasks to complete
    # results = result.get(timeout=30)
    # print(f"   Results: {results}")


@shared_task
def collect_results(results):
    """Callback task for chord"""
    print(f"\n✅ All emails sent!")
    print(f"   Total: {len(results)}")
    return f"Completed: {len(results)} emails"


def example_2_task_chord():
    """
    Send emails and execute callback when done
    
    Chord = Group + Callback
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Task Chord (Group + Callback)")
    print("="*60)
    
    user_ids = [1, 2, 3]
    
    # Chord: Execute tasks in parallel, then callback
    callback = chord([
        send_single_email.s(user_id, 'emails/welcome.html')
        for user_id in user_ids
    ])(collect_results.s())
    
    print(f"✅ Chord task started")
    print(f"   Task ID: {callback.id}")


# ============================================================================
# PERIODIC TASKS
# ============================================================================

from celery import Celery
from celery.schedules import crontab

# Configure periodic tasks
# In celery.py:
"""
app.conf.beat_schedule = {
    'send-daily-digest': {
        'task': 'emails.tasks.send_daily_digest_task',
        'schedule': crontab(hour=9, minute=0),  # 9:00 AM daily
    },
    'send-weekly-newsletter': {
        'task': 'emails.tasks.send_weekly_newsletter_task',
        'schedule': crontab(day_of_week=1, hour=10, minute=0),  # Monday 10:00 AM
    },
    'check-overdue-books': {
        'task': 'emails.tasks.check_overdue_books_task',
        'schedule': crontab(hour='*/6'),  # Every 6 hours
    },
}
"""

@shared_task
def send_daily_digest_task():
    """
    Send daily digest to subscribed users
    
    Runs: Every day at 9:00 AM (configured in beat_schedule)
    """
    print("\n" + "="*60)
    print("PERIODIC TASK: Daily Digest")
    print("="*60)
    
    # Get subscribed users
    users = User.objects.filter(
        profile__subscribed_to_notifications=True
    )
    
    for user in users:
        context = {
            'user': user,
            'date': datetime.now().strftime('%Y-%m-%d'),
            # Add daily stats, new books, etc.
        }
        
        html_message = render_to_string('emails/daily_digest.html', context)
        
        send_mail(
            subject='Your Daily Library Digest',
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )
    
    return f"Digest sent to {users.count()} users"


@shared_task
def send_weekly_newsletter_task():
    """
    Send weekly newsletter
    
    Runs: Every Monday at 10:00 AM
    """
    print("\n" + "="*60)
    print("PERIODIC TASK: Weekly Newsletter")
    print("="*60)
    
    # Implementation here
    pass


@shared_task
def check_overdue_books_task():
    """
    Check for overdue books and send reminders
    
    Runs: Every 6 hours
    """
    print("\n" + "="*60)
    print("PERIODIC TASK: Overdue Books Check")
    print("="*60)
    
    from books.models import BorrowHistory
    from django.utils import timezone
    
    # Find overdue books
    overdue = BorrowHistory.objects.filter(
        returned_at__isnull=True,
        due_date__lt=timezone.now()
    ).select_related('user', 'book')
    
    for borrow in overdue:
        days_overdue = (timezone.now().date() - borrow.due_date.date()).days
        
        context = {
            'user': borrow.user,
            'book': borrow.book,
            'due_date': borrow.due_date,
            'days_overdue': days_overdue,
        }
        
        html_message = render_to_string('emails/overdue_reminder.html', context)
        
        send_mail(
            subject=f'OVERDUE: {borrow.book.title}',
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrow.user.email],
            html_message=html_message,
        )
    
    return f"Reminders sent for {overdue.count()} overdue books"

# ============================================================================
# TASK MONITORING & CALLBACKS
# ============================================================================

def log_success(result, task_id, args, kwargs):
    """Called when task succeeds"""
    logger.info(f"✅ Task {task_id} succeeded: {result}")


def log_failure(task_id, exception, traceback):
    """Called when task fails"""
    logger.error(f"❌ Task {task_id} failed: {exception}")

    
@shared_task(bind=True)
def send_email_with_progress(self, recipients_count):
    """
    Task with progress tracking
    
    Usage:
        task = send_email_with_progress.delay(100)
        # Check progress: task.info
    """
    print("\n" + "="*60)
    print("TASK: Email with Progress Tracking")
    print("="*60)
    
    for i in range(recipients_count):
        # Send email
        # ...
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': recipients_count,
                'percent': int((i + 1) / recipients_count * 100)
            }
        )
    
    return {'current': recipients_count, 'total': recipients_count, 'status': 'Complete'}


@shared_task(bind=True, on_failure=log_failure, on_success=log_success)
def send_email_with_callbacks(self, to_email, subject, message):
    """
    Task with success/failure callbacks
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])


def log_success(result, task_id, args, kwargs):
    """Called when task succeeds"""
    logger.info(f"✅ Task {task_id} succeeded: {result}")


def log_failure(task_id, exception, traceback):
    """Called when task fails"""
    logger.error(f"❌ Task {task_id} failed: {exception}")


# ============================================================================
# PRODUCTION BEST PRACTICES
# ============================================================================

@shared_task(
    bind=True,
    max_retries=5,
    default_retry_delay=300,  # 5 minutes
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=3600,  # Max 1 hour
    retry_jitter=True,
)
def send_important_email(self, user_id, template_name, context):
    """
    Production-ready email task with:
    - Automatic retries
    - Exponential backoff
    - Jitter to prevent thundering herd
    """
    print("\n" + "="*60)
    print("TASK: Production Email")
    print("="*60)
    
    try:
        user = User.objects.get(id=user_id)
        
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        email = EmailMultiAlternatives(
            subject=context.get('subject', 'Notification'),
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        
        logger.info(f"✅ Email sent to {user.email}")
        return f"Success: {user.email}"
        
    except Exception as e:
        logger.error(f"❌ Email error: {e}, Retry: {self.request.retries}")
        raise


# ============================================================================
# TASK RESULT BACKEND
# ============================================================================

def check_task_status(task_id):
    """
    Check status of async task
    
    Usage:
        task = send_welcome_email_task.delay(1)
        check_task_status(task.id)
    """
    from celery.result import AsyncResult
    
    result = AsyncResult(task_id)
    
    print(f"\nTask ID: {task_id}")
    print(f"State: {result.state}")
    print(f"Ready: {result.ready()}")
    
    if result.ready():
        if result.successful():
            print(f"Result: {result.result}")
        else:
            print(f"Error: {result.info}")
    else:
        print("Task still running...")


# ============================================================================
# CELERY CONFIGURATION EXAMPLES
# ============================================================================

"""
# celery.py

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

app = Celery('library_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'send-daily-digest': {
        'task': 'emails.tasks.send_daily_digest_task',
        'schedule': crontab(hour=9, minute=0),
    },
    'check-overdue-books': {
        'task': 'emails.tasks.check_overdue_books_task',
        'schedule': crontab(hour='*/6'),
    },
}

# Task configuration
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'

# Result backend
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.result_expires = 3600  # 1 hour

# Task settings
app.conf.task_track_started = True
app.conf.task_time_limit = 300  # 5 minutes
app.conf.task_soft_time_limit = 240  # 4 minutes
"""

# ============================================================================
# RUNNING CELERY
# ============================================================================

"""
# Start Celery worker
celery -A library_project worker --loglevel=info

# Start Celery beat (for periodic tasks)
celery -A library_project beat --loglevel=info

# Start both (development only)
celery -A library_project worker --beat --loglevel=info

# Monitor with Flower
pip install flower
celery -A library_project flower

# Production (with concurrency)
celery -A library_project worker --loglevel=info --concurrency=4
"""

# ============================================================================
# DEMO RUNNER
# ============================================================================

def run_all_examples():
    """Demonstrate all Celery email patterns"""
    
    print("\n" + "="*70)
    print("CELERY ASYNC EMAIL EXAMPLES")
    print("="*70)
    
    print("\n⚠️  Prerequisites:")
    print("   1. Redis server running")
    print("   2. Celery worker running")
    print("   3. pip install celery redis")
    
    example_1_task_group()
    example_2_task_chord()
    
    print("\n✅ Examples completed")
    print("\n💡 To run tasks:")
    print("   send_welcome_email_task.delay(user_id)")
    print("   send_bulk_email_task.delay([1,2,3], 'Subject', 'template.html', {})")


if __name__ == '__main__':
    run_all_examples()