# -------------------  DRF imports   ------------------------
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# -------------------  Django imports   ------------------------
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
# -------------------  Apps imports   ------------------------
from .models import CustomUser, PurchaseHistory
from utility.serializers import BaseSerializer
# -------------------  Other imports   ------------------------
import random

##################################################################################
#                         User Serializer                                        #
##################################################################################

class UserSerializer(BaseSerializer):
    """
    Serializer for CustomUser model.
    Used to display user info (id, username, email, role).
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']


##################################################################################
#                         Register Serializer                                    #
##################################################################################

class RegisterSerializer(BaseSerializer):
    """
    Serializer to register new users.
    Validates password with Django validators.
    """
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data.get('email'),
            role=validated_data.get('role', 'customer')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


##################################################################################
#                    Change Password Serializer                                  #
##################################################################################

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    Requires old_password and new_password.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)


##################################################################################
#                    Purchase History Serializer                                #
##################################################################################

class PurchaseHistorySerializer(BaseSerializer):
    """
    Serializer for PurchaseHistory model.
    Handles product name, quantity, price, and formatted purchase date.
    Validates quantity to be at least 1.
    purchase_date is read-only and formatted as 'YYYY-MM-DD HH:mm:ss'.
    """

    purchase_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = PurchaseHistory
        fields = ['id', 'product_name', 'quantity', 'price', 'purchase_date']
        read_only_fields = ['id', 'purchase_date']


##################################################################################
#                    Purchase History Detail Serializer                         #
##################################################################################

class PurchaseHistoryDetailSerializer(PurchaseHistorySerializer):
    """
    Detail serializer for PurchaseHistory.
    (Extend this if you want to add extra fields later.)
    """
    class Meta(PurchaseHistorySerializer.Meta):
        fields = PurchaseHistorySerializer.Meta.fields


##################################################################################
#                          Custom Token Serializer                              #
##################################################################################

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customize JWT token to include username and role.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        return token


##################################################################################
#                          Send OTP Serializer                                  #
##################################################################################

class SendOTPSerializer(BaseSerializer):
    """
    Serializer to handle sending OTP to user's email.
    Validates that an email is provided and sends an OTP to that email.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is registered with this email.")
        return value

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp(self):
        otp_code = self.generate_otp()
        email = self.validated_data.get("email")

        send_mail(
            subject="Your OTP Code",
            message=f"Hi! Your OTP code is: {otp_code}",
            from_email="no-reply@b-cafe.com",
            recipient_list=[email],
            fail_silently=False,
        )
