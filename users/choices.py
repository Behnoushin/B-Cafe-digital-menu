from django.db.models import TextChoices

class Roles(TextChoices):
    ADMIN = "admin", "Admin"
    CASHIER = "cashier", "Cashier"
    WAITER = "waiter", "Waiter"
    CUSTOMER = "customer", "Customer"