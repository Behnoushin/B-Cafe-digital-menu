from django.db import models

class OrderStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'

class PaymentStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    FAILED = 'failed', 'Failed'

class PaymentMethodChoices(models.TextChoices):
    CASH = 'cash', 'Cash'
    ONLINE = 'online', 'Online'