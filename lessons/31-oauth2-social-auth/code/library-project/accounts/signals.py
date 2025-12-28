"""
Signals for accounts app
Handles automatic email notifications for user-related events
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from emails.services import EmailService
from .models import Profile

logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Agar profile mavjud bo'lmasa, yaratish
        Profile.objects.get_or_create(user=instance)



@receiver(post_save, sender=User)
def send_welcome_email_on_registration(sender, instance, created, **kwargs):
    """Send welcome email after successful registration"""
    if not created:
        return

    if not instance.email:
        logger.warning(
            f"User {instance.username} registered without email"
        )
        return

    try:
        success = EmailService.send_welcome_email(instance)

        if success:
            logger.info(
                f"Welcome email sent successfully to {instance.email}"
            )
        else:
            logger.warning(
                f"Failed to send welcome email to {instance.email}"
            )

    except Exception as e:
        logger.error(
            f"Error sending welcome email to {instance.username}: {str(e)}"
        )
