from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_reservation_email(subject, message, to_email):
    # Test print for debugging and verification
    if to_email == "test@test.com":
        print(f"[TEST MODE] Sending email to {to_email} with subject '{subject}'")
    send_mail(
        subject=subject,
        message=message,
        from_email="no-reply@b-cafe.com",
        recipient_list=[to_email],
        fail_silently=True,
    )
    if to_email == "test@test.com":
        print(f"[TEST MODE] Email sent to {to_email}")