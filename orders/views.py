# -------------------  Django imports   ------------------------
from django.utils import timezone
# -------------------  DRF imports   ------------------------
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
# -------------------   Apps imports ------------------------
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsAdminUser, IsCashierUser, IsWaiterUser, IsCustomerUser
from utility.views import BaseAPIView
from .choices import OrderStatusChoices

##################################################################################
#                             Order Views                                        #
##################################################################################

class OrderListCreateView(BaseAPIView, generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Please log in to access this resource.")

        if user.role == 'admin':
            return Order.objects.all()
        elif user.role == 'cashier':
            return Order.objects.filter(status__in=[
                OrderStatusChoices.CONFIRMED, OrderStatusChoices.PAID
            ])
        elif user.role == 'waiter':
            return Order.objects.filter(status__in=[
                OrderStatusChoices.PENDING, OrderStatusChoices.CONFIRMED
            ])
        elif user.role == 'customer':
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            return [AllowAny()]  

        if user.role == 'admin':
            permission_classes = [IsAdminUser]
        elif user.role == 'cashier':
            permission_classes = [IsCashierUser]
        elif user.role == 'waiter':
            permission_classes = [IsWaiterUser]
        elif user.role == 'customer':
            permission_classes = [IsCustomerUser]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]


class OrderRetrieveUpdateDestroyView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            return [AllowAny()]

        if user.role == 'admin':
            permission_classes = [IsAdminUser]
        elif user.role == 'cashier':
            permission_classes = [IsCashierUser]
        elif user.role == 'waiter':
            permission_classes = [IsWaiterUser]
        elif user.role == 'customer':
            permission_classes = [IsCustomerUser]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        user = self.request.user
        new_status = serializer.validated_data.get('status', None)

        if user.role == 'cashier' and new_status != OrderStatusChoices.PAID:
            raise PermissionDenied("Cashiers are only allowed to change the order status to 'PAID'.")

        instance = serializer.save()
        if new_status == OrderStatusChoices.PAID and not instance.paid_at:
            instance.paid_at = timezone.now()
            instance.save(update_fields=["paid_at"])
