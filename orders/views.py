# -------------------  Django imports   ------------------------
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db import models
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# -------------------  DRF imports   ------------------------
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

# -------------------   Apps imports ------------------------
from .models import Order, Payment, Invoice
from .serializers import OrderSerializer, PaymentSerializer, InvoiceSerializer
from .permissions import IsAdminUser, IsCashierUser, IsWaiterUser, IsCustomerUser
from utility.views import BaseAPIView
from .choices import OrderStatusChoices
from utility.mixins import RestoreMixin

# ------------------- Constants ------------------------
CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 5)

##################################################################################
#                             Order Views                                        #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
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
#                             OrderByUser Views                                  #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class OrderByUserView(BaseAPIView, generics.ListAPIView):
    """
    Returns orders for the current authenticated user.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

##################################################################################
#                           OrdersByStatus Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class OrdersByStatusView(BaseAPIView, generics.ListAPIView):
    """
    Returns orders filtered by a given status query parameter.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return Order.objects.filter(status=status)
        return Order.objects.all()

##################################################################################
#                             TopOrders Views                                    #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class TopOrdersView(BaseAPIView, generics.ListAPIView):
    """
    Returns top 10 orders by total price.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.all().order_by('-total_price')[:10]

##################################################################################
#                           OrderHistory Views                                   #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class OrderHistoryView(BaseAPIView, generics.ListAPIView):
    """
    Returns all orders of the current user sorted by creation time.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

##################################################################################
#                       ChangeOrderStatus Views                                  #
##################################################################################

class ChangeOrderStatusView(BaseAPIView, generics.UpdateAPIView):
    """
    Allows Admin or Cashier to change the status of an order.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser | IsCashierUser]

    def perform_update(self, serializer):
        new_status = serializer.validated_data.get('status')
        order = serializer.save()
        if new_status == OrderStatusChoices.PAID and not order.paid_at:
            order.paid_at = timezone.now()
            order.save(update_fields=['paid_at'])


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
#                         PaymentsByOrder Views                                  #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class PaymentsByOrderView(BaseAPIView, generics.ListAPIView):
    """
    Returns all payments associated with a specific order.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return Payment.objects.filter(order__id=order_id)

##################################################################################
#                         PaymentsByStatus Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class PaymentsByStatusView(BaseAPIView, generics.ListAPIView):
    """
    Returns payments filtered by their status (Paid/Pending).
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return Payment.objects.filter(status=status)
        return Payment.objects.all()

##################################################################################
#                           RecentPayments Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class RecentPaymentsView(BaseAPIView, generics.ListAPIView):
    """
    Returns the last 10 payments by creation date.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.all().order_by('-created_at')[:10]

##################################################################################
#                           TotalCollected Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class TotalCollectedView(BaseAPIView, generics.GenericAPIView):
    """
    Returns the total amount of all successful payments.
    Read-only endpoint.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total = Payment.objects.filter(status='paid').aggregate(total=models.Sum('amount'))['total'] or 0
        return Response({'total_collected': total})

##################################################################################
#                           MarkPaymentAsPaid Views                              #
##################################################################################

class MarkPaymentAsPaidView(BaseAPIView, generics.UpdateAPIView):
    """
    Allows Admin or Cashier to mark a payment as 'Paid'.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAdminUser | IsCashierUser]

    def perform_update(self, serializer):
        payment = serializer.save(status='paid')
        payment.mark_as_paid()
        invoice = getattr(payment.order, 'invoice', None)
        if invoice:
            invoice.is_paid = True
            invoice.save(update_fields=['is_paid'])


##################################################################################
#                             Invoice Views                                        #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
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
    
##################################################################################
#                           InvoicesByUser Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class InvoicesByUserView(BaseAPIView, generics.ListAPIView):
    """
    Returns all invoices for the current user.
    """
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(order__user=self.request.user)

##################################################################################
#                           UnpaidInvoices Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class UnpaidInvoicesView(BaseAPIView, generics.ListAPIView):
    """
    Returns all unpaid invoices.
    """
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(is_paid=False)

##################################################################################
#                            InvoiceDetail Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class InvoiceDetailView(BaseAPIView, generics.RetrieveAPIView):
    """
    Returns detailed information of a specific invoice.
    """
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]

##################################################################################
#                            GenerateInvoic Views                                #
##################################################################################

class GenerateInvoiceView(BaseAPIView, generics.CreateAPIView):
    """
    Creates a new invoice with a unique invoice number.
    """
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminUser | IsCashierUser]

    def perform_create(self, serializer):
        invoice_number = get_random_string(length=10).upper()
        serializer.save(invoice_number=invoice_number)

##################################################################################
#                            SendInvoiceEmail Views                              #
##################################################################################

class SendInvoiceEmailView(BaseAPIView, generics.GenericAPIView):
    """
    Sends invoice email to the user for a given invoice.
    """
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminUser | IsCashierUser]

    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        send_mail(
            subject=f"Invoice #{invoice.invoice_number}",
            message=f"Your invoice total is {invoice.total_amount}.",
            from_email="no-reply@b-cafe.com",
            recipient_list=[invoice.order.user.email],
            fail_silently=True
        )
        return Response({'status': 'email sent'})
    
##################################################################################
#                         Restore & History Views                                 #
##################################################################################

class InvoiceRestoreView(RestoreMixin, APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        instance = Invoice.objects.get(pk=pk)
        self.perform_restore(instance)
        return Response({"success": f"Invoice '{instance.id}' restored"}, status=200)

class InvoiceHistoryView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Invoice.history.all()