# -------------------   Django imports ------------------------
from django.db import models
# -------------------   Apps imports ------------------------
from .choices import TableTypeChoices, ReservationTypeChoices, DurationChoices
from utility.models import BaseModel

##################################################################################
#                                 Table Model                                    #
##################################################################################

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Table Number")
    capacity = models.CharField(max_length=2, choices=TableTypeChoices.choices, verbose_name="Capacity")

    def __str__(self):
        return f"Table {self.number} - {self.get_capacity_display()}"
    
##################################################################################
#                             Reservation Model                                  #
##################################################################################

class Reservation(BaseModel):
    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    date = models.DateField(verbose_name="Day")
    time = models.TimeField(verbose_name="Time")
    number_of_guests = models.PositiveIntegerField(verbose_name="Number of Guests")
    table_type = models.CharField(max_length=2, choices=TableTypeChoices.choices)
    extra_notes = models.TextField(blank=True, null=True, verbose_name="Extra Notes")
    reservation_type = models.CharField(
        max_length=20,
        choices=ReservationTypeChoices.choices,
        default=ReservationTypeChoices.NORMAL,
        verbose_name="Reservation Type"
    )
    birthday_design = models.BooleanField(default=False, verbose_name="Birthday Decoration")
    birthday_cake = models.BooleanField(default=False, verbose_name="Birthday Cake")
    duration = models.PositiveIntegerField(
        choices=DurationChoices.choices,
        default=DurationChoices.MIN_60,
        verbose_name="Duration (minutes)"
    )
    table = models.ForeignKey("Table", on_delete=models.CASCADE, verbose_name="Selected Table")
    is_approved = models.BooleanField(default=False, verbose_name="Approved by Admin")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"{self.full_name} - {self.date} {self.time}"
    
