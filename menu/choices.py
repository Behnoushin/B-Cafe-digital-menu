from django.db.models import TextChoices

class ItemStatus(TextChoices):
    AVAILABLE = 'available', 'available'
    OUT_OF_STOCK = 'out_of_stock', 'out_of_stock'