from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation

@receiver(post_save, sender=Reservation)
def reservation_created_handler(sender, instance, created, **kwargs):
    if created:
        user_message = f"Dear {instance.full_name}, your table is successfully reserved for {instance.date} at {instance.time}."
        
        admin_message = (
            f"A new table reservation has been made:\n"
            f"Name: {instance.full_name}\n"
            f"Phone: {instance.phone_number}\n"
            f"Date: {instance.date}\n"
            f"Time: {instance.time}\n"
            f"Number of Guests: {instance.number_of_guests}"
        )
        
        print(user_message)
        print(admin_message)