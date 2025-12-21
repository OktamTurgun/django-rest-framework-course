"""
Signals for accounts app
Handles automatic email notifications for user-related events
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from emails.services import EmailService
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_welcome_email_on_registration(sender, instance, created, **kwargs):
    """
    Send welcome email when new user is created.
    
    Args:
        sender: User model
        instance: User instance that was saved
        created: Boolean, True if new user created
        kwargs: Additional keyword arguments
    """
    if created:
        try:
            # Check if user has email
            if instance.email:
                success = EmailService.send_welcome_email(instance)
                
                if success:
                    logger.info(
                        f"Welcome email sent successfully to {instance.email}"
                    )
                else:
                    logger.warning(
                        f"Failed to send welcome email to {instance.email}"
                    )
            else:
                logger.warning(
                    f"User {instance.username} registered without email"
                )
                
        except Exception as e:
            logger.error(
                f"Error sending welcome email to {instance.username}: {str(e)}"
            )