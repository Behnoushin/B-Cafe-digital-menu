# -------------------   Django imports ------------------------
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F

# -------------------   Apps imports ------------------------
from utility.models import BaseModel
from .validators import validate_company_phone_number
from .choices import WeekDays
from simple_history.models import HistoricalRecords

##################################################################################
#                           AboutUs Model                                        #
##################################################################################

class AboutUs(BaseModel):
    """
    Stores company introduction and background details for the 'About Us' section.
    """
    title = models.CharField(max_length=150, verbose_name="Title")
    short_description = models.CharField(
        max_length=250,
        null=True, 
        blank=True, 
        verbose_name="Short Description"
        )
    content = models.TextField(verbose_name="Content")
    history = HistoricalRecords(inherit=True)
        
    def __str__(self):
        return f"About Us: {self.title}"
    
    def __repr__(self):
        return f"<AboutUs title='{self.title}'>"
       
    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us Sections"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["title"])]

##################################################################################
#                           ContactUs Model                                      #
##################################################################################
  
class ContactUs(BaseModel):
    """
    Holds the company's official contact number for public display.
    """
    phone_number = models.CharField(
        max_length=8,
        verbose_name="Contact number",
        validators=[validate_company_phone_number]
    )
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    social_links = models.JSONField(default=dict, blank=True, verbose_name="Social Links")
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return f"number: {self.phone_number}"
    
    def __repr__(self):
        return f"<ContactUs phone_number='{self.phone_number}'>"
    
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Information"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["phone_number"])]
        
##################################################################################
#                           WorkingHours Model                                   #
##################################################################################

class WorkingHours(BaseModel):
    """
    Represents the company's working hours for each day of the week.
    """
    day = models.CharField(
        max_length=3,
        choices=WeekDays.choices,
        verbose_name="Day",
        help_text="Select the weekday this schedule applies to."
    )
    open_time = models.TimeField(verbose_name="Opening Time")
    close_time = models.TimeField(verbose_name="Closing Time")
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return f"{self.get_day_display()}: {self.open_time.strftime('%H:%M')} - {self.close_time.strftime('%H:%M')}"

    def __repr__(self):
        return f"<WorkingHours day='{self.day}' open='{self.open_time}' close='{self.close_time}'>"
    
    class Meta:
        verbose_name = "Working Hour"
        verbose_name_plural = "Working Hours"
        ordering = ["day"]
        
        constraints = [
            models.CheckConstraint(
                check=Q(close_time__gt=F('open_time')),
                name='valid_working_hours'
            ),
            models.UniqueConstraint(
                fields=['day'],
                name='unique_working_day'
            )
        ]
        
        indexes = [
            models.Index(fields=["day"]),
            models.Index(fields=["day", "open_time"]),
        ]
        
    def clean(self):
        """Ensure valid open and close times."""
        if self.open_time >= self.close_time:
            raise ValidationError("Closing time must be after opening time.")
