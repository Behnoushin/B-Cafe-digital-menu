from django.db import models

class TableTypeChoices(models.TextChoices):
    TWO = "2", "2 solo"
    FOUR = "4", "4 solo"
    EIGHT = "8", "8 solo"
    TEN = "10", "10 solo"

class ReservationTypeChoices(models.TextChoices):
    NORMAL = 'normal', 'Normal'
    BIRTHDAY = 'birthday', 'Birthday'

class DurationChoices(models.IntegerChoices):
    MIN_60 = 60, "60 Minutes"
    MIN_90 = 90, "90 Minutes"
    MIN_120 = 120, "120 Minutes"
    MIN_150 = 150, "150 Minutes"
