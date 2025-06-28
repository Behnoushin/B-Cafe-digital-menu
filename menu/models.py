from django.db import models
from django.core.exceptions import ValidationError
from utility.models import BaseModel
from .choices import ItemStatus

##################################################################################
#                             Category Model                                     #
##################################################################################

class Category(BaseModel):
    name = models.CharField(max_length=100)
    is_cofe = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

##################################################################################
#                             MenuItem Model                                     #
##################################################################################

class MenuItem(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=ItemStatus.choices,
        default=ItemStatus.AVAILABLE
        )
    
    def clean(self):
        if self.price < 0:
            raise ValidationError("The price cannot be negative!")
        if self.stock < 0:
            raise ValidationError("Inventory can be negative!")
    
    def save(self, *args, **kwargs):
        self.status = (
            ItemStatus.OUT_OF_STOCK if self.stock == 0 else ItemStatus.AVAILABLE
        )
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} - ({self.price} Toman.)"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Menu item"
        verbose_name_plural = "Menu item"
        constraints = [
            models.UniqueConstraint(fields=['name', 'category'], name='unique_item_per_category')
        ]
        