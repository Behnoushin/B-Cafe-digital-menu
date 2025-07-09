from django.db import models

class OrderStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'
