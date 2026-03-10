from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task
from django.conf import settings


@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, created, **kwargs):

    if created:
        print(f"Task created: {instance.title}")

@receiver(post_save, sender=Task)
def task_assigned_notification(sender, instance, created, **kwargs):

    if instance.assigned_to:
        
        send_mail(
            subject="New Task Assigned",
            message=f"You have been assigned a new task {instance.title}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.assigned_to.email],
            fail_silently=True,
        )