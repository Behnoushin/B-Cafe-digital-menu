from django.urls import path
from .views import (
    AboutUsList, AboutUsDetail,
    ContactUsList, ContactUsDetail
)

urlpatterns = [
    # About Us
    path('about/', AboutUsList.as_view(), name='aboutus-list'),
    path('about/<int:pk>/', AboutUsDetail.as_view(), name='aboutus-detail'),

    # Contact Us
    path('contact/', ContactUsList.as_view(), name='contactus-list'),
    path('contact/<int:pk>/', ContactUsDetail.as_view(), name='contactus-detail'),
]