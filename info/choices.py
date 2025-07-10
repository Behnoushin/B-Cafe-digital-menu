from django.db.models import TextChoices

class WeekDays(TextChoices):
    SATURDAY = 'sat', 'Saturday'
    SUNDAY = 'sun', 'Sunday'
    MONDAY = 'mon', 'Monday'
    TUESDAY = 'tue', 'Tuesday'
    WEDNESDAY = 'wed', 'Wednesday'
    THURSDAY = 'thu', 'Thursday'
    FRIDAY = 'fri', 'Friday'
