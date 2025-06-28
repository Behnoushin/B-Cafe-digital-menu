from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import MenuItem
from .choices import ItemStatus

@receiver(pre_save, sender=MenuItem)
def menu_item_change_handler(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    
    if instance.name != old_instance.name or instance.price != old_instance.price:
        print(f"Item '{old_instance.name}' changed!")
    
    if old_instance.stock > 0 and instance.stock == 0:
        print(f"The item '{instance.name}' does not exist!")
        
    if instance.stock == 0:
        instance.status = ItemStatus.OUT_OF_STOCK
    else:
        instance.status = ItemStatus.AVAILABLE