from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Reservation
from users.models import CustomUser
from django.core.mail import send_mail

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
@receiver(post_save, sender=Reservation)
def reservation_status_handler(sender, instance, created, **kwargs):
    """
    Handles notifications when a reservation is created or approved:
    - Sends a message to the customer when the reservation is created.
    - Sends a message to the admin when a new reservation is submitted.
    - Notifies cashier and waiter when a reservation is approved by admin.
    """
    # Notify user upon reservation creation
    if created:
        user_msg = (
            f"Dear {instance.full_name}, your reservation for {instance.date} at {instance.time} is received. "
            f"Please wait for admin approval."
        )
        print("USER:", user_msg)
        # Uncomment to send actual email:
        # send_mail("Reservation Received", user_msg, "no-reply@b-cafe.com", [instance.email])

        # Notify admin about new reservation
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
        print("ADMIN:", admin_msg)
        # Uncomment to send email to admin
        # send_mail("New Reservation", admin_msg, "no-reply@b-cafe.com", ["admin@b-cafe.com"])

    # Notify cashier and waiter when admin approves the reservation
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
        for staff in CustomUser.objects.filter(role__in=['cashier', 'waiter'], is_active=True):
            print(f"Notify {staff.username} ({staff.role}): {staff_msg}")
            # Uncomment to send email to staff
            # send_mail("Reservation Approved", staff_msg, "no-reply@b-cafe.com", [staff.email])
