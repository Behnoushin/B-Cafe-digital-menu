from django.db.models import TextChoices

#############################################
#           Satisfaction Choices             #
#############################################

class SatisfactionChoices(TextChoices):
    YES = '1', 'Yes'
    SOMEWHAT = '2', 'Somewhat'
    NO = '3', 'No'

#############################################
#            Food Rating Choices            #
#############################################

class FoodRatingChoices(TextChoices):
    ONE = '1', '1 - Terrible'
    TWO = '2', '2 - Very Bad'
    THREE = '3', '3 - Bad'
    FOUR = '4', '4 - Not Good'
    FIVE = '5', '5 - Average'
    SIX = '6', '6 - Okay'
    SEVEN = '7', '7 - Good'
    EIGHT = '8', '8 - Very Good'
    NINE = '9', '9 - Excellent'
    TEN = '10', '10 - Perfect'

#############################################
#              Feedback Status              #
#############################################

class FeedbackStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    REVIEWED = 'reviewed', 'Reviewed'

#############################################
#              Feedback Type                #
#############################################

class FeedbackType(TextChoices):
    RESTAURANT_AND_CAFE = 'restaurant and cafe', 'Restaurant and cafe'
    SERVICE = 'service', 'Service'
    STAFF = 'staff', 'Staff'
    ENVIRONMENT = 'environment', 'Environment'
