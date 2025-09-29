# ------------------- Django imports ------------------------
from django.db import models
from django.conf import settings
from django.db.models import Q, CheckConstraint
# ------------------- Apps imports ------------------------
from menu.models import MenuItem
from reservation.models import Table
from .choices import OrderStatusChoices, PaymentMethodChoices, PaymentStatusChoices
from utility.models import BaseModel

##################################################################################
#                             Order Model                                        #
##################################################################################

class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    table = models.ForeignKey(
        Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING
    )
    note = models.TextField(blank=True, null=True)
    payment_status = models.DateTimeField(null=True, blank=True)


    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(status__in=[choice.value for choice in OrderStatusChoices]),
                name='valid_order_status'
            )
        ]

    def total_price(self):
        return sum(item.total_item_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} - {self.status.title()} by {self.user.username}"
    

##################################################################################
#                             OrderItem Model                                    #
##################################################################################

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    @property
    def final_price(self):
        return self.menu_item.final_price

    @property
    def total_item_price(self):
        return self.final_price * self.quantity

##################################################################################
#                           Payment Model                                        #
##################################################################################

class Payment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING
    )
    method = models.CharField(
        max_length=50,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CASH
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


##################################################################################
#                           Invoice Model                                        #
##################################################################################

class Invoice(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for Order #{self.order.id}"
