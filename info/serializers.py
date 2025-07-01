# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import AboutUs, ContactUs
from utility.serializers import BaseSerializer

##################################################################################
#                      AboutUsSerializer serializers                             #
##################################################################################

class AboutUsSerializer(BaseSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'
        
##################################################################################
#                      ContactUsSerializer serializers                           #
##################################################################################

class ContactUsSerializer(BaseSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'