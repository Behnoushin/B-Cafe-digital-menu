from django.urls import path
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView, PaymentListCreateView, InvoiceListCreateView

urlpatterns = [
    # Order URLs
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),

    # Payment URLs
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),

    # Invoice URLs
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
]