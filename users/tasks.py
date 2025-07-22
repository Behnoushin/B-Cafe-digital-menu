from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email_task(email, username):
    
    print(f"[TEST] Starting to send welcome email to {email} for user {username}")

    send_mail(
        subject="Welcome to B-Cafe.",
        message=f"Hi {username}! Thanks for joining us.",
        from_email="no-reply@b-cafe.com",
        recipient_list=[email],
        fail_silently=True,
    )

    print(f"[TEST] Finished sending welcome email to {email}")
