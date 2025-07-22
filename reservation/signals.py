from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Reservation
from users.models import CustomUser
from django.core.mail import send_mail
from .tasks import send_reservation_email

# ---------------------- Cache previous approval status before saving ----------------------
@receiver(pre_save, sender=Reservation)
def cache_approval_state(sender, instance, **kwargs):
    """
    Before saving the reservation, we store the previous approval status
    so we can check later in post_save if the status changed to approved.
    """
    if instance.pk:
        try:
            old_instance = Reservation.objects.get(pk=instance.pk)
            instance._was_approved = old_instance.is_approved
        except Reservation.DoesNotExist:
            instance._was_approved = False
    else:
        instance._was_approved = False

# ---------------------- Handle reservation events after saving ----------------------
def reservation_status_handler(sender, instance, created, **kwargs):
    # When a new reservation is created ---
    if created:
        user_msg = (
            f"Dear {instance.full_name}, your reservation for {instance.date} at {instance.time} is received. "
            f"Please wait for admin approval."
        )
        send_reservation_email.delay(
            "Reservation Received", user_msg, instance.email
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
        send_reservation_email.delay(
            "New Reservation", admin_msg, "admin@b-cafe.com"
        )

    # When a reservation is approved (updated, not created) ---
    if not created and not instance._was_approved and instance.is_approved:
        staff_msg = (
            f"Reservation approved:\n"
            f"Name: {instance.full_name}\n"
            f"Phone: {instance.phone_number}\n"
            f"Date: {instance.date}, Time: {instance.time}\n"
            f"Guests: {instance.number_of_guests}\n"
            f"Table: {instance.table}\n"
            f"Type: {instance.reservation_type}\n"
            f"Notes: {instance.extra_notes or 'No notes'}"
        )

        staff_members = CustomUser.objects.filter(role__in=['cashier', 'waiter'], is_active=True)

        for staff in staff_members:
            send_reservation_email.delay(
                "Reservation Approved", staff_msg, staff.email
            )
