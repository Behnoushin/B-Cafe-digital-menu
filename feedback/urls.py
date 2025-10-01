from django.urls import path
from .views import (
    MyFeedbackList,
    FeedbackDetailView,
    UpdateFeedback,
    DeleteFeedback,
    FeedbackByStatus,
    RespondToFeedback,
    FeedbackByType,
    RecentFeedbacks,
    FeedbackAnalytics,
    PublicFeedbackList,
    ItemFeedbackList,
    TopRatedItems,
    FeedbackSummaryForOrder,
    RevisitIntentStats,
    ExportFeedbacks
)

urlpatterns = [
    
    # User Feedback URLs
    path("my-feedbacks/", MyFeedbackList.as_view(), name="my-feedbacks"),
    path("feedbacks/<int:pk>/", FeedbackDetailView.as_view(), name="feedback-detail"),
    path("feedbacks/<int:pk>/update/", UpdateFeedback.as_view(), name="feedback-update"),
    path("feedbacks/<int:pk>/delete/", DeleteFeedback.as_view(), name="feedback-delete"),

    # Admin Feedback URLs
    path("feedbacks/by-status/", FeedbackByStatus.as_view(), name="feedback-by-status"),
    path("feedbacks/respond/<int:pk>/", RespondToFeedback.as_view(), name="respond-feedback"),
    path("feedbacks/by-type/", FeedbackByType.as_view(), name="feedback-by-type"),
    path("feedbacks/recent/", RecentFeedbacks.as_view(), name="recent-feedbacks"),
    path("feedbacks/analytics/", FeedbackAnalytics.as_view(), name="feedback-analytics"),
    path("feedbacks/export/", ExportFeedbacks.as_view(), name="export-feedbacks"),

    # Public Feedback URLs 
    path("feedbacks/public/", PublicFeedbackList.as_view(), name="public-feedbacks"),
    path("feedbacks/item/<int:item_id>/", ItemFeedbackList.as_view(), name="item-feedbacks"),
    path("feedbacks/top-rated-items/", TopRatedItems.as_view(), name="top-rated-items"),

    # Special / Stats Feedback URLs 
    path("feedbacks/order/<int:order_id>/summary/", FeedbackSummaryForOrder.as_view(), name="feedback-summary-order"),
    path("feedbacks/revisit-intent/", RevisitIntentStats.as_view(), name="revisit-intent-stats"),
    
]
