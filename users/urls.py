from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserProfileUpdateView,
    ChangePasswordView,
    PurchaseHistoryView,
    PurchaseHistoryDetailView,
    SendOTPView,
)

urlpatterns = [
    # User Registration and Login
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),

    # User Profile Views
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # Get or update own profile
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),

    # Password Change
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Purchase History
    path('purchase-history/', PurchaseHistoryView.as_view(), name='purchase-history'),  # List all purchases of current user
    path('purchase-history/<int:pk>/', PurchaseHistoryDetailView.as_view(), name='purchase-history-detail'),  # Retrieve, update or delete a specific record

    # Send OTP
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),  # Send OTP code to user's email
]
