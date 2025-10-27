# -------------------  DRF imports   ------------------------
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# -------------------  DRF imports   ------------------------
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Avg
# -------------------   Apps imports ------------------------
from .models import Feedback
from .serializers import FeedbackSerializer
from menu.permissions import IsAdminOnly
from utility.mixins import SoftDeleteMixin, RestoreMixin


CACHE_TTL = getattr(settings, 'CACHE_TTL', 60*5)

##################################################################################
#                              Base Feedback View                                #
##################################################################################

class BaseFeedbackView(generics.GenericAPIView):
    """
    Base view for all Feedback-related views.
    Includes soft delete, restore, and caching.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False)

    def perform_destroy(self, instance):
        """
        Soft delete an instance.
        """
        SoftDeleteMixin.perform_destroy(self, instance)

    def perform_restore(self, instance):
        """
        Restore a soft-deleted instance.
        """
        RestoreMixin.perform_restore(self, instance)


##################################################################################
#                              Admin Views                                       #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class AdminFeedbackList(BaseFeedbackView, generics.ListAPIView):
    """List all feedbacks (Admin only)."""
    permission_classes = [IsAdminOnly]


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class FeedbackByStatus(BaseFeedbackView, generics.ListAPIView):
    """Filter feedbacks by status (PENDING, REVIEWED) for admin."""
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return super().get_queryset().filter(status=status)
        return super().get_queryset()


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class FeedbackByType(BaseFeedbackView, generics.ListAPIView):
    """Filter feedbacks by type (Service, Staff, Environment) for admin."""
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        f_type = self.request.query_params.get('type')
        if f_type:
            return super().get_queryset().filter(feedback_type=f_type)
        return super().get_queryset()


class RespondToFeedback(BaseFeedbackView, generics.UpdateAPIView):
    """Admin can respond to feedback and mark as REVIEWED."""
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return super().get_queryset()

    def perform_update(self, serializer):
        serializer.save(status='reviewed')


class RecentFeedbacks(BaseFeedbackView, generics.ListAPIView):
    """Return the last 10 feedbacks for the admin dashboard."""
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')[:10]


class FeedbackAnalytics(BaseFeedbackView, generics.RetrieveAPIView):
    """Provide aggregated statistics for feedbacks."""
    permission_classes = [IsAdminOnly]


class ExportFeedbacks(BaseFeedbackView, generics.ListAPIView):
    """Export all feedbacks to CSV/Excel (Admin only)."""
    permission_classes = [IsAdminOnly]


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class FeedbackHistoryView(BaseFeedbackView, generics.ListAPIView):
    """
    List all historical records of feedbacks (Admin only).
    Uses django-simple-history.
    """
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        # Access history from simple_history
        return Feedback.history.all()
    
##################################################################################
#                              User Views                                        #
##################################################################################

class FeedbackCreate(BaseFeedbackView, generics.CreateAPIView):
    """Authenticated users can create feedback."""
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user_ip = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        serializer.save(user=user, user_ip=user_ip, user_agent=user_agent)


class MyFeedbackList(BaseFeedbackView, generics.ListAPIView):
    """List all feedbacks created by the logged-in user."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FeedbackDetail(BaseFeedbackView, generics.RetrieveAPIView):
    """Retrieve details of a specific feedback for the logged-in user."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UpdateFeedback(BaseFeedbackView, generics.UpdateAPIView):
    """Allow users to update their feedback if status is PENDING."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, status='pending')


class DeleteFeedback(BaseFeedbackView, generics.DestroyAPIView):
    """Allow users to delete their feedback before it is reviewed by admin."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, status='pending')


class FeedbackSummaryForOrder(BaseFeedbackView, generics.ListAPIView):
    """Show feedbacks related to a specific order for the customer."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.request.query_params.get('order_id')
        return super().get_queryset().filter(order__id=order_id, user=self.request.user)


##################################################################################
#                              Public Views                                      #
##################################################################################

class PublicFeedbackList(BaseFeedbackView, generics.ListAPIView):
    """Display all reviewed feedbacks publicly."""
    permission_classes = []

    def get_queryset(self):
        return super().get_queryset().filter(status='reviewed')


class ItemFeedbackList(BaseFeedbackView, generics.ListAPIView):
    """List all feedbacks for a specific menu item."""
    permission_classes = []

    def get_queryset(self):
        item_id = self.request.query_params.get('item_id')
        return super().get_queryset().filter(item__id=item_id, status='reviewed')


class TopRatedItems(BaseFeedbackView, generics.ListAPIView):
    """Return menu items with highest average food rating."""
    permission_classes = []

    def get_queryset(self):
        return super().get_queryset().filter(status='reviewed')\
            .values('item__id', 'item__name')\
            .annotate(avg_rating=Avg('food_rating'))\
            .order_by('-avg_rating')