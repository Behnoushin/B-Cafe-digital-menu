# -------------------   Django imports ------------------------
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# -------------------   Apps imports ------------------------
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
    is_special = models.BooleanField(default=False)
    preparation_time = models.DurationField(null=True, blank=True)
    discount_percent = models.PositiveIntegerField(default=0)
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    sold_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=ItemStatus.choices,
        default=ItemStatus.AVAILABLE
        )

    @property
    def is_discount_active(self):
        now = timezone.now()
        return (
            self.discount_percent > 0
            and self.discount_start and self.discount_end
            and self.discount_start <= now <= self.discount_end
        )

    @property
    def final_price(self):
        if self.discount_percent:
            return self.price - (self.price * self.discount_percent / 100)
        return self.price
    
    
    def clean(self):
        """
        Perform model validation before saving.

        This method ensures:
        - Calls parent class's clean method to run any inherited validations.
        - The price cannot be negative.
        - The stock (inventory) cannot be negative.
        - The discount_percent must be between 0 and 100 inclusive.

        Raises:
            ValidationError: If any of the above validations fail.
        """
        super().clean()
        if self.price < 0:
            raise ValidationError("The price cannot be negative!")
        
        if self.stock < 0:
            raise ValidationError("Inventory cannot be negative!")

        if not 0 <= self.discount_percent <= 100:
            raise ValidationError("Discount percent must be between 0 and 100.")
    
    
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
        verbose_name_plural = "Menu items"
        constraints = [
            models.UniqueConstraint(fields=['name', 'category'], name='unique_item_per_category')
        ]
        

        
