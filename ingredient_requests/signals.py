from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IngredientRequest

@receiver(post_save, sender=IngredientRequest)
def notify_admin_on_request(sender, instance, created, **kwargs):
    if created:
        print(f"New request registered on behalf of {instance.chef.username}.")