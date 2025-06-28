from django.db import models
from utility.models import BaseModel
from .validators import validate_company_phone_number
##################################################################################
#                           AboutUs Model                                        #
##################################################################################

class AboutUs(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()

    def __str__(self):
        return "About Us"

##################################################################################
#                           ContactUs Model                                      #
##################################################################################
  
class ContactUs(BaseModel):
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Contact number",
        validators=[validate_company_phone_number]
    )

    def __str__(self):
        return f"number: {self.phone_number}"