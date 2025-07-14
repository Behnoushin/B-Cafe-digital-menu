# -------------------   Django imports ------------------------
from django.db import models
from django.conf import settings
# -------------------   Apps imports ------------------------
from menu.models import MenuItem
from orders.models import Order
from utility.models import BaseModel
from .choices import SatisfactionChoices, FoodRatingChoices, FeedbackStatus, FeedbackType

##################################################################################
#                           Feedback Model                                        #
##################################################################################

class Feedback(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='feedbacks')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(
        max_length=20,
        choices=FeedbackType.choices,
        default=FeedbackType.RESTAURANT_AND_CAFE
        )
    food_rating = models.CharField(max_length=2, choices=FoodRatingChoices.choices)
    service_satisfaction = models.CharField(max_length=2, choices=SatisfactionChoices.choices)
    staff_behavior = models.CharField(max_length=2, choices=SatisfactionChoices.choices)
    cleanliness = models.CharField(max_length=2, choices=SatisfactionChoices.choices)
    preparation_time = models.CharField(max_length=2, choices=SatisfactionChoices.choices)
    revisit_intent = models.CharField(max_length=2, choices=SatisfactionChoices.choices)
    comment = models.TextField(blank=True)
    admin_response = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=FeedbackStatus.choices, 
        default=FeedbackStatus.PENDING
        )
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"Feedback by {self.user} on {self.item} [{self.status}]"
