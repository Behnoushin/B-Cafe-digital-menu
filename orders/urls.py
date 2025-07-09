from django.urls import path
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='list_create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='detail'),
]
