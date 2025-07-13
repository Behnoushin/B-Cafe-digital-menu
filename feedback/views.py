# -------------------  DRF imports   ------------------------
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# -------------------   Apps imports ------------------------
from .models import Feedback
from .serializers import FeedbackSerializer
from menu.permissions import IsAdminOnly

##################################################################################
#                             Feedback Views                                     #
##################################################################################

class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOnly]

class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user_ip = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        serializer.save(user=user, user_ip=user_ip, user_agent=user_agent)
