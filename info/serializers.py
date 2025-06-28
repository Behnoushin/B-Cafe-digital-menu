from rest_framework import serializers
from .models import AboutUs, ContactUs

##################################################################################
#                      AboutUsSerializer serializers                             #
##################################################################################

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'
        
##################################################################################
#                      ContactUsSerializer serializers                           #
##################################################################################

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'