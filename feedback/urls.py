from django.urls import path
from .views import FeedbackListView, FeedbackCreateView

urlpatterns = [
    path('feedbacks/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedbacks/create/', FeedbackCreateView.as_view(), name='feedback-create'),
]
