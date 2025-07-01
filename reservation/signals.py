from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation

@receiver(post_save, sender=Reservation)
def reservation_created_handler(sender, instance, created, **kwargs):
    if created:
        user_msg = (
            f"Dear {instance.full_name}, your reservation for {instance.date} at {instance.time} is received. "
            f"Please wait for admin approval."
        )

        admin_msg = (
            f"New reservation request:\n"
            f"Name: {instance.full_name}\n"
            f"Phone: {instance.phone_number}\n"
            f"Date: {instance.date}, Time: {instance.time}\n"
            f"Guests: {instance.number_of_guests}\n"
            f"Table: {instance.table}\n"
            f"Type: {instance.reservation_type}\n"
            f"Notes: {instance.extra_notes or 'No notes'}"
        )

        print(user_msg)
        print("ADMIN ALERT:", admin_msg)
