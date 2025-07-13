# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import Feedback
from utility.serializers import BaseSerializer

##################################################################################
#                            Feedback serializers                                #
##################################################################################

class FeedbackSerializer(BaseSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['user', 'status', 'admin_response', 'created_at', 'updated_at', 'user_ip', 'user_agent']
