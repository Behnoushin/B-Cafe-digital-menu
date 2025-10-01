# -------------------  DRF imports   ------------------------
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# -------------------   Apps imports ------------------------
from .models import Feedback
from .serializers import FeedbackSerializer
from menu.permissions import IsAdminOnly

##################################################################################
#                       Feedback List-Create Views                               #
##################################################################################

class FeedbackListView(generics.ListAPIView):
    """
    List all feedbacks in the system (Admin only).
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOnly]


class FeedbackCreateView(generics.CreateAPIView):
    """
    Allow authenticated users to create a new feedback.
    Captures user IP and user agent automatically.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user_ip = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        serializer.save(user=user, user_ip=user_ip, user_agent=user_agent)


##################################################################################
#                             MyFeedbackList                                     #
##################################################################################

class MyFeedbackList(generics.ListAPIView):
    """
    Returns all feedbacks created by the logged-in user.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)


##################################################################################
#                             FeedbackDetailView                                  #
##################################################################################

class FeedbackDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific feedback for the logged-in user.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)


##################################################################################
#                             UpdateFeedback                                      #
##################################################################################

class UpdateFeedback(generics.UpdateAPIView):
    """
    Allow user to update their feedback only if status is PENDING.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user, status='pending')


##################################################################################
#                             DeleteFeedback                                      #
##################################################################################

class DeleteFeedback(generics.DestroyAPIView):
    """
    Allow user to delete their feedback before it is reviewed by admin.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user, status='pending')


##################################################################################
#                             FeedbackByStatus                                    #
##################################################################################

class FeedbackByStatus(generics.ListAPIView):
    """
    Filter feedbacks based on status (PENDING, REVIEWED) for admin.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return Feedback.objects.filter(status=status)
        return Feedback.objects.all()


##################################################################################
#                             RespondToFeedback                                  #
##################################################################################

class RespondToFeedback(generics.UpdateAPIView):
    """
    Admin can respond to feedback and mark status as REVIEWED.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return Feedback.objects.all()

    def perform_update(self, serializer):
        serializer.save(status='reviewed')


##################################################################################
#                             FeedbackByType                                     #
##################################################################################

class FeedbackByType(generics.ListAPIView):
    """
    Filter feedbacks by type (Service, Staff, Environment) for admin.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        feedback_type = self.request.query_params.get('type')
        if feedback_type:
            return Feedback.objects.filter(feedback_type=feedback_type)
        return Feedback.objects.all()


##################################################################################
#                             RecentFeedbacks                                    #
##################################################################################

class RecentFeedbacks(generics.ListAPIView):
    """
    Return the last 10 feedbacks for admin dashboard.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return Feedback.objects.all().order_by('-created_at')[:10]


##################################################################################
#                             FeedbackAnalytics                                   #
##################################################################################

class FeedbackAnalytics(generics.RetrieveAPIView):
    """
    Read-only aggregated statistics for dashboard (avg food_rating, service satisfaction, etc.).
    """
    serializer_class = FeedbackSerializer  # Can create a custom analytics serializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return Feedback.objects.all()


##################################################################################
#                             PublicFeedbackList                                 #
##################################################################################

class PublicFeedbackList(generics.ListAPIView):
    """
    Display feedbacks that are reviewed (status=REVIEWED) for menu items publicly.
    """
    serializer_class = FeedbackSerializer
    permission_classes = []

    def get_queryset(self):
        return Feedback.objects.filter(status='reviewed')


##################################################################################
#                             ItemFeedbackList                                   #
##################################################################################

class ItemFeedbackList(generics.ListAPIView):
    """
    List all feedbacks for a specific menu item.
    """
    serializer_class = FeedbackSerializer
    permission_classes = []

    def get_queryset(self):
        item_id = self.request.query_params.get('item_id')
        return Feedback.objects.filter(item__id=item_id, status='reviewed')


##################################################################################
#                             TopRatedItems                                      #
##################################################################################

class TopRatedItems(generics.ListAPIView):
    """
    Return menu items with highest average food_rating.
    """
    serializer_class = FeedbackSerializer  # Or a custom serializer for item ratings
    permission_classes = []

    def get_queryset(self):
        from django.db.models import Avg
        return Feedback.objects.filter(status='reviewed').values('item__id', 'item__name')\
            .annotate(avg_rating=Avg('food_rating')).order_by('-avg_rating')[:10]


##################################################################################
#                             FeedbackSummaryForOrder                             #
##################################################################################

class FeedbackSummaryForOrder(generics.ListAPIView):
    """
    Show feedback related to a specific order for the customer.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.request.query_params.get('order_id')
        return Feedback.objects.filter(order__id=order_id, user=self.request.user)


##################################################################################
#                             RevisitIntentStats                                  #
##################################################################################

class RevisitIntentStats(generics.RetrieveAPIView):
    """
    Return percentage of users who intend to revisit (revisit_intent=YES).
    """
    serializer_class = FeedbackSerializer  # Can use a custom serializer for stats
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return Feedback.objects.all()


##################################################################################
#                             ExportFeedbacks                                     #
##################################################################################

class ExportFeedbacks(generics.ListAPIView):
    """
    Admin can export all feedbacks to CSV/Excel.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return Feedback.objects.all()
