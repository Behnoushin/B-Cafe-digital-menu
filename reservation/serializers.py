# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import Reservation, Table
from utility.serializers import BaseSerializer
# -------------------   Other imports ------------------------
from datetime import datetime, time as djangotime

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

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("The mobile number must be 11 digits and only numbers.")
        return value

    def validate_number_of_guests(self, value):
        if value < 1 or value > 80:
            raise serializers.ValidationError("The number of guests must be between 1 and 80.")
        return value

    def validate(self, attrs):
        res_date = attrs["date"]
        res_time = attrs["time"]
        table_type = attrs.get("table_type")

        # --- Validation of booking time ---
        now = datetime.now()
        res_datetime = datetime.combine(res_date, res_time)
        if res_datetime < now:
            raise serializers.ValidationError("Reservation cannot be in the past.")
        
        if not djangotime(10, 0) <= res_time <= djangotime(22, 0):
            raise serializers.ValidationError("Time must be between 10:00 and 22:00.")

        #--- Birthday reservation review ---
        if attrs.get("reservation_type") == "birthday" and not (
            attrs.get("birthday_design") or attrs.get("birthday_cake")
        ):
            raise serializers.ValidationError("For birthday reservation, choose decoration or cake.")

        #--- Checking the table capacity at that date and time ---
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
