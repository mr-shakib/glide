from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Profile
from django.conf import settings
from users.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        send_mail(
            subject="Welcome to Glide",
            message="Your account has been created successfully!",
            from_email=settings.DEFAULT_FROM_EMIAL,
            recipient_list= [instance.email],
            fail_silently=True
        )