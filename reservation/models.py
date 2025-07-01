# -------------------   Django imports ------------------------
from django.db import models
# -------------------   Apps imports ------------------------
from utility.models import BaseModel

##################################################################################
#                             Reservation Model                                  #
##################################################################################

class Reservation(BaseModel):
    full_name = models.CharField(max_length=100, verbose_name="First and Last Name")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    date = models.DateField(verbose_name="Day")
    time = models.TimeField(verbose_name="Time")
    number_of_guests = models.PositiveIntegerField(verbose_name="Number of Guests")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
        
    class Meta:
        ordering = ["-created_date"]
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"{self.full_name} - {self.date} {self.time}"