# -------------------  Django imports   ------------------------
from django.utils import timezone
from django.utils.crypto import get_random_string
# -------------------  DRF imports   ------------------------
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
# -------------------   Apps imports ------------------------
from .models import Order, Payment, Invoice
from .serializers import OrderSerializer, PaymentSerializer, InvoiceSerializer
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


##################################################################################
#                             Payment Views                                        #
##################################################################################

class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'cashier']:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=user)

    def perform_create(self, serializer):
        payment = serializer.save()
        if payment.status == 'paid':
            payment.mark_as_paid()
            invoice = getattr(payment.order, 'invoice', None)
            if invoice:
                invoice.is_paid = True
                invoice.save(update_fields=['is_paid'])


class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'paid' and not instance.paid_at:
            instance.mark_as_paid()
            invoice = getattr(instance.order, 'invoice', None)
            if invoice:
                invoice.is_paid = True
                invoice.save(update_fields=['is_paid'])


##################################################################################
#                             Invoice Views                                        #
##################################################################################

class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'cashier']:
            return Invoice.objects.all()
        return Invoice.objects.filter(order__user=user)

    def perform_create(self, serializer):
        invoice_number = get_random_string(length=10).upper()
        serializer.save(invoice_number=invoice_number)


class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]