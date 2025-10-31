# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import AboutUs, ContactUs, WorkingHours
from utility.serializers import BaseSerializer

##################################################################################
#                      AboutUsSerializer serializers                             #
##################################################################################

class AboutUsSerializer(BaseSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'history',)

##################################################################################
#                      ContactUsSerializer serializers                           #
##################################################################################

class ContactUsSerializer(BaseSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'history',)

##################################################################################
#                      WorkingHoursSerializer serializers                        #
##################################################################################   

class WorkingHoursSerializer(BaseSerializer):
    class Meta:
        model = WorkingHours
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'history',)
        
    def validate(self, attrs):
        """Ensure opening time is before closing time"""
        open_time = attrs.get('open_time')
        close_time = attrs.get('close_time')
        if open_time and close_time and open_time >= close_time:
            raise serializers.ValidationError("Closing time must be after opening time.")
        return attrs