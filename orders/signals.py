from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Order, OrderItem
from menu.models import MenuItem
from .choices import OrderStatusChoices


@receiver(post_save, sender=OrderItem)
def decrease_stock_on_orderitem_save(sender, instance, created, **kwargs):
    if created:
        menu_item = instance.menu_item
        menu_item.stock -= instance.quantity
        if menu_item.stock < 0:
            menu_item.stock = 0
        menu_item.save()

@receiver(post_delete, sender=OrderItem)
def increase_stock_on_orderitem_delete(sender, instance, **kwargs):
    menu_item = instance.menu_item
    menu_item.stock += instance.quantity
    menu_item.save()

@receiver(post_save, sender=Order)
def notify_when_order_paid(sender, instance, **kwargs):
    if instance.status == OrderStatusChoices.PAID:
        send_mail(
            subject="Your order has been paid for.",
            message=f"Your order number {instance.id} has been successfully paid. Thank you for your purchase!",
            from_email="no-reply@b-cafe.com",
            recipient_list=[instance.user.email],
            fail_silently=True,
        )
