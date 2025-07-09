# -------------------   Django imports ------------------------
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
# -------------------   Apps imports ------------------------
from .choices import Roles
from utility.models import BaseModel
##################################################################################
#                           CustomUser Model                                     #
##################################################################################

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def clean(self):
        valid_roles = [role[0] for role in Roles.choices]
        if self.role not in valid_roles:
            raise ValidationError("The selected role is not valid.")
        if self.email and CustomUser.objects.exclude(pk=self.pk).filter(email=self.email).exists():
            raise ValidationError("This email has already been registered.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
 
##################################################################################
#                           PurchaseHistory Model                                #
##################################################################################       
        
class PurchaseHistory(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchasehistory_set')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.user.username}"