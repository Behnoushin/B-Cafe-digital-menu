from django.urls import path
from .views import (
    AdminFeedbackList,
    FeedbackByStatus,
    FeedbackByType,
    RespondToFeedback,
    RecentFeedbacks,
    FeedbackAnalytics,
    ExportFeedbacks,
    FeedbackCreate,
    MyFeedbackList,
    FeedbackDetail,
    UpdateFeedback,
    DeleteFeedback,
    FeedbackSummaryForOrder,
    PublicFeedbackList,
    ItemFeedbackList,
    TopRatedItems,
    FeedbackHistoryView
)

urlpatterns = [
    # ----------------- Admin URLs -----------------
    path('admin/list/', AdminFeedbackList.as_view(), name='admin-feedback-list'),
    path('admin/status/', FeedbackByStatus.as_view(), name='admin-feedback-by-status'),
    path('admin/type/', FeedbackByType.as_view(), name='admin-feedback-by-type'),
    path('admin/respond/<int:pk>/', RespondToFeedback.as_view(), name='admin-respond-feedback'),
    path('admin/recent/', RecentFeedbacks.as_view(), name='admin-recent-feedbacks'),
    path('admin/analytics/', FeedbackAnalytics.as_view(), name='admin-feedback-analytics'),
    path('admin/export/', ExportFeedbacks.as_view(), name='admin-feedback-export'),
    path('admin/history/', FeedbackHistoryView.as_view(), name='admin-feedback-history'),

    # ----------------- User URLs -----------------
    path('create/', FeedbackCreate.as_view(), name='feedback-create'),
    path('my/', MyFeedbackList.as_view(), name='my-feedback-list'),
    path('detail/<int:pk>/', FeedbackDetail.as_view(), name='feedback-detail'),
    path('update/<int:pk>/', UpdateFeedback.as_view(), name='feedback-update'),
    path('delete/<int:pk>/', DeleteFeedback.as_view(), name='feedback-delete'),
    path('summary/order/', FeedbackSummaryForOrder.as_view(), name='feedback-summary-order'),

    # ----------------- Public URLs -----------------
    path('public/', PublicFeedbackList.as_view(), name='public-feedback-list'),
    path('item/', ItemFeedbackList.as_view(), name='item-feedback-list'),
    path('top-rated/', TopRatedItems.as_view(), name='top-rated-items'),
]