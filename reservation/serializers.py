# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import Reservation
from utility.serializers import BaseSerializer

##################################################################################
#                          Reservation serializers                               #
##################################################################################

class ReservationSerializer(BaseSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['created_date']

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("The mobile number must be 11 digits and only numbers.")
        return value

    def validate_number_of_guests(self, value):
        if value < 1 or value > 30:
            raise serializers.ValidationError("The number of guests must be between 1 and 30.")
        return value