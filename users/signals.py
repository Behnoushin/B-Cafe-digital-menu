from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            subject="Welcome to B-Cafe.",
            message=f"Hi {instance.username}! Thanks for joining us. ",
            from_email="no-reply@b-cafe.com",
            recipient_list=[instance.email],
            fail_silently=True,
        )