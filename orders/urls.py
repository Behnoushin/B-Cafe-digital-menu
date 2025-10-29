# -------------------  Django imports   ------------------------
from django.urls import path
# -------------------   Apps imports ------------------------
from .views import (
    # Order Views
    OrderListCreateView, OrderRetrieveUpdateDestroyView, OrderByUserView,
    OrdersByStatusView, TopOrdersView, OrderHistoryView, ChangeOrderStatusView,
    
    # Payment Views
    PaymentListCreateView, PaymentRetrieveUpdateDestroyView, PaymentsByOrderView,
    PaymentsByStatusView, RecentPaymentsView, TotalCollectedView,
    MarkPaymentAsPaidView,
    
    # Invoice Views
    InvoiceListCreateView, InvoiceRetrieveUpdateDestroyView, InvoicesByUserView,
    UnpaidInvoicesView, InvoiceDetailView, GenerateInvoiceView,
    SendInvoiceEmailView,
    
    # Invoice Restore & History 
    InvoiceRestoreView, InvoiceHistoryView
)

urlpatterns = [
    
    # Order URLs
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('orders/user/', OrderByUserView.as_view(), name='orders-by-user'),
    path('orders/status/', OrdersByStatusView.as_view(), name='orders-by-status'),
    path('orders/top/', TopOrdersView.as_view(), name='top-orders'),
    path('orders/history/', OrderHistoryView.as_view(), name='order-history'),
    path('orders/<int:pk>/change-status/', ChangeOrderStatusView.as_view(), name='change-order-status'),

    # Payment URLs
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-detail'),
    path('payments/order/<int:order_id>/', PaymentsByOrderView.as_view(), name='payments-by-order'),
    path('payments/status/', PaymentsByStatusView.as_view(), name='payments-by-status'),
    path('payments/recent/', RecentPaymentsView.as_view(), name='recent-payments'),
    path('payments/total-collected/', TotalCollectedView.as_view(), name='total-collected'),
    path('payments/<int:pk>/mark-paid/', MarkPaymentAsPaidView.as_view(), name='mark-payment-paid'),

    # Invoice URLs
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-detail'),
    path('invoices/user/', InvoicesByUserView.as_view(), name='invoices-by-user'),
    path('invoices/unpaid/', UnpaidInvoicesView.as_view(), name='unpaid-invoices'),
    path('invoices/detail/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail-view'),
    path('invoices/generate/', GenerateInvoiceView.as_view(), name='generate-invoice'),
    path('invoices/<int:pk>/send-email/', SendInvoiceEmailView.as_view(), name='send-invoice-email'),
    
    # Invoice Restore & History URLs
    path('invoices/<int:pk>/restore/', InvoiceRestoreView.as_view(), name='invoice-restore'),
    path('invoices/history/', InvoiceHistoryView.as_view(), name='invoice-history'),
]