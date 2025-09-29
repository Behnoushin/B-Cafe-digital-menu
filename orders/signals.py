# -------------------  Django imports   ------------------------
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone

# -------------------   Apps imports ------------------------
from .models import Order, OrderItem, Payment
from .choices import OrderStatusChoices

# ----------------------- OrderItem Signals -----------------------

@receiver(post_save, sender=OrderItem)
def decrease_stock_on_orderitem_save(sender, instance, created, **kwargs):
    """
    Decrease the stock of a menu item when a new OrderItem is created.
    Prevent stock from going below zero.
    """
    if created:
        menu_item = instance.menu_item
        menu_item.stock -= instance.quantity
        if menu_item.stock < 0:
            menu_item.stock = 0
        menu_item.save()


@receiver(post_delete, sender=OrderItem)
def increase_stock_on_orderitem_delete(sender, instance, **kwargs):
    """
    Increase the stock of a menu item when an OrderItem is deleted.
    """
    menu_item = instance.menu_item
    menu_item.stock += instance.quantity
    menu_item.save()


# ----------------------- Order Signals ---------------------------

@receiver(post_save, sender=Order)
def notify_when_order_paid(sender, instance, **kwargs):
    """
    Send an email notification to the user when the order is marked as paid.
    """
    if instance.status == OrderStatusChoices.PAID:
        send_mail(
            subject="Your order has been paid for.",
            message=f"Your order number {instance.id} has been successfully paid. Thank you for your purchase!",
            from_email="no-reply@b-cafe.com",
            recipient_list=[instance.user.email],
            fail_silently=True,
        )


# ----------------------- Payment Signals -------------------------

@receiver(post_save, sender=Payment)
def update_invoice_on_payment(sender, instance, created, **kwargs):
    """
    Automatically mark the related invoice as paid when the payment status is 'paid'.
    """
    if instance.status == 'paid' and hasattr(instance.order, 'invoice'):
        invoice = instance.order.invoice
        if not invoice.is_paid:
            invoice.is_paid = True
            invoice.paid_at = timezone.now()
            invoice.save(update_fields=['is_paid', 'paid_at'])
