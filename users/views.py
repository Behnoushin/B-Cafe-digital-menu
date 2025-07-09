# -------------------  DRF imports   ------------------------
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
# -------------------  Django imports   ------------------------
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# -------------------  Apps imports   ------------------------
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    PurchaseHistorySerializer,
    PurchaseHistoryDetailSerializer,
    SendOTPSerializer,
)
from utility.views import BaseAPIView

User = get_user_model()

##################################################################################
#                        User Registration Views                                 #
##################################################################################

class UserRegistrationView(BaseAPIView, generics.CreateAPIView):
    """
    API endpoint that allows new users to register.
    Accessible to anyone (AllowAny).
    Uses RegisterSerializer to validate and create users.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
##################################################################################
#                          UserLogin Views                                       #
##################################################################################

class UserLoginView(BaseAPIView, TokenObtainPairView):
    """
    API endpoint for user login.
    Returns JWT tokens on successful authentication.
    Uses CustomTokenObtainPairSerializer to include user role in token.
    Accessible to anyone (AllowAny).
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    
##################################################################################
#                             UserProfile Views                                  #
##################################################################################

class UserProfileView(BaseAPIView, generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    Only accessible to authenticated users.
    The user can GET their profile data or PUT/PATCH to update.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current logged-in user object
        return self.request.user
    


class UserProfileUpdateView(BaseAPIView, generics.UpdateAPIView):
    """
    API endpoint dedicated to updating user profile partially or fully.
    Accessible only to authenticated users.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current logged-in user object
        return self.request.user
    
##################################################################################
#                           ChangePassword Views                                 #
##################################################################################

class ChangePasswordView(BaseAPIView, generics.UpdateAPIView):
    """
    API endpoint for allowing users to change their password.
    Requires old_password and new_password in the request data.
    Validates old password, validates new password against Django's validators,
    and updates the password if valid.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current logged-in user object
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.data.get('old_password')
        new_password = serializer.data.get('new_password')

        # Check if old password is correct
        if not user.check_password(old_password):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Validate new password using Django's validators
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"new_password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password and save user
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

##################################################################################
#                        PurchaseHistory Views                                   #
##################################################################################

class PurchaseHistoryView(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list the purchase history of the authenticated user.
    Returns a list of purchase records.
    Accessible only to authenticated users.
    """
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return purchase history related to the current user
        return self.request.user.purchasehistory_set.all()

class PurchaseHistoryDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update or delete a specific purchase history record by id.
    Accessible only to authenticated users.
    """
    serializer_class = PurchaseHistoryDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return purchase history related to the current user
        return self.request.user.purchasehistory_set.all()

##################################################################################
#                             Send OTP Views                                     #
##################################################################################

class SendOTPView(BaseAPIView, generics.GenericAPIView):
    """
    API endpoint to send OTP (One-Time Password) to user email or phone.
    Typically used for verification or password reset.
    Accessible to anyone.
    """
    serializer_class = SendOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # The OTP sending logic should be implemented inside the serializer or here
        serializer.send_otp()
        return Response({"detail": "OTP sent successfully."}, status=status.HTTP_200_OK)
