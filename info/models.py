# -------------------   Django imports ------------------------
from django.db import models
# -------------------   Apps imports ------------------------
from utility.models import BaseModel
from .validators import validate_company_phone_number
from .choices import WeekDays
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
    
##################################################################################
#                           WorkingHours Model                                   #
##################################################################################

class WorkingHours(BaseModel):
    day = models.CharField(max_length=3, choices=WeekDays.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.get_day_display()}: {self.open_time.strftime('%H:%M')} - {self.close_time.strftime('%H:%M')}"
