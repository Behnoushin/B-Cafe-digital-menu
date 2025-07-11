# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import Reservation, Table
from utility.serializers import BaseSerializer
# -------------------   Other imports ------------------------
from datetime import datetime, timedelta, time as djangotime

##################################################################################
#                             Table Serializer                                   #
##################################################################################

class TableSerializer(BaseSerializer):
    capacity_display = serializers.CharField(source='get_capacity_display', read_only=True)

    class Meta:
        model = Table
        fields = '__all__'

##################################################################################
#                          Reservation serializers                               #
##################################################################################

class ReservationSerializer(BaseSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['is_approved']

    def validate_number_of_guests(self, value):
        # Ensure number of guests is within allowed range
        if value < 1 or value > 80:
            raise serializers.ValidationError("The number of guests must be between 1 and 80.")
        return value

    def validate(self, attrs):
        # Extract relevant fields from input data
        res_date = attrs["date"]
        res_time = attrs["time"]
        duration_minutes = attrs.get("duration", 60)  # Default to 60 minutes if not provided
        number_of_guests = attrs["number_of_guests"]
        table = attrs.get("table")
        table_type = attrs.get("table_type")

        # Combine date and time to create datetime object for reservation start
        res_start = datetime.combine(res_date, res_time)
        # Calculate reservation end time based on duration
        res_end = res_start + timedelta(minutes=duration_minutes)

        # Validate reservation time is within allowed hours (10:00 - 22:00)
        if not djangotime(10, 0) <= res_time <= djangotime(22, 0):
            raise serializers.ValidationError("Reservation time must be between 10:00 and 22:00.")

        # Check if table is provided
        if not table:
            raise serializers.ValidationError("Table must be selected.")

        # Validate number of guests does not exceed table capacity
        try:
            capacity_int = int(table.capacity)
        except Exception:
            raise serializers.ValidationError("Invalid table capacity format.")

        if number_of_guests > capacity_int:
            raise serializers.ValidationError(
                f"The number of guests ({number_of_guests}) exceeds the table capacity ({capacity_int})."
            )

        # Check for overlapping approved reservations on the same table and date
        existing_reservations = Reservation.objects.filter(
            table=table,
            date=res_date,
            is_approved=True
        )

        for reservation in existing_reservations:
            existing_start = datetime.combine(reservation.date, reservation.time)
            existing_end = existing_start + timedelta(minutes=reservation.duration)

            # Check for time overlap (if new reservation start is before existing end AND
            # new reservation end is after existing start, then they overlap)
            if (res_start < existing_end) and (res_end > existing_start):
                raise serializers.ValidationError(
                    "This table is already reserved during the selected time."
                )

        # Validate reservation datetime is not in the past
        now = datetime.now()
        if res_start < now:
            raise serializers.ValidationError("Reservation cannot be in the past.")

        # For birthday reservations, require at least decoration or cake
        if attrs.get("reservation_type") == "birthday" and not (
            attrs.get("birthday_design") or attrs.get("birthday_cake")
        ):
            raise serializers.ValidationError("For birthday reservation, choose decoration or cake.")

        # Maximum allowed reservations per table_type at the same date and time
        max_capacity_per_type = {
            "2": 7,
            "4": 10,
            "8": 2,
            "10": 1,
        }

        if table_type not in max_capacity_per_type:
            raise serializers.ValidationError("Invalid table type selected.")

        approved_count = Reservation.objects.filter(
            table_type=table_type,
            date=res_date,
            time=res_time,
            is_approved=True
        ).count()

        if approved_count >= max_capacity_per_type[table_type]:
            raise serializers.ValidationError(
                f"All {table_type}-person tables are already reserved for the selected time."
            )

        return attrs
