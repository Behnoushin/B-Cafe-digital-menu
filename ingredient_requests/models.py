# -------------------   Django imports ------------------------
from django.db import models
from django.conf import settings
# -------------------   Apps imports ------------------------
from utility.models import BaseModel

##################################################################################
#                       IngredientRequest Model                                  #
##################################################################################

class IngredientRequest(BaseModel):
    chef = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ingredient_requests")
    note = models.TextField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)  # Manager approval or rejection

    def __str__(self):
        return f"Request by {self.chef}"

##################################################################################
#                         IngredientItem Model                                   #
##################################################################################

class IngredientItem(BaseModel):
    request = models.ForeignKey(IngredientRequest, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
