from django.db.models import TextChoices

class OrderStatusChoices(TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'

class PaymentStatusChoices(TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    FAILED = 'failed', 'Failed'

class PaymentMethodChoices(TextChoices):
    CASH = 'cash', 'Cash'
    ONLINE = 'online', 'Online'