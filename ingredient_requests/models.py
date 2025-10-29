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
    
    class Meta:
        indexes = [
            models.Index(fields=['chef']),
            models.Index(fields=['is_reviewed', 'created_at']),
        ]
        
        constraints = [
            # Only one request with one note per chef
            models.UniqueConstraint(fields=['chef', 'note'], name='unique_request_per_chef')
        ]
        
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

    class Meta:
        indexes = [
            models.Index(fields=['request']),
            models.Index(fields=['name']),
            models.Index(fields=['request', 'name']), 
        ]

        constraints = [
            # Prevent items with the same name from appearing again in the same request
            models.UniqueConstraint(fields=['request', 'name'], name='unique_item_per_request'),
            
            # Making sure it doesn't get approved and rejected at the same time
            models.CheckConstraint(
                check=~(models.Q(is_approved=True) & models.Q(is_rejected=True)),
                name='approved_not_rejected'
            ),
        ]