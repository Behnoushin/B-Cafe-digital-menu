from django.urls import path
from .views import (
    AboutUsList, AboutUsDetail, AboutUsHistoryList,
    ContactUsList, ContactUsDetail, ContactUsHistoryList,
    WorkingHoursList, WorkingHoursDetail, WorkingHoursHistoryList
)

urlpatterns = [
    # About Us
    path('about/', AboutUsList.as_view(), name='aboutus-list'),
    path('about/<int:pk>/', AboutUsDetail.as_view(), name='aboutus-detail'),
    path('about/history/', AboutUsHistoryList.as_view(), name='aboutus-history'),


    # Contact Us
    path('contact/', ContactUsList.as_view(), name='contactus-list'),
    path('contact/<int:pk>/', ContactUsDetail.as_view(), name='contactus-detail'),
    path('contact/history/', ContactUsHistoryList.as_view(), name='contactus-history'),

    
    # Working Hours
    path('working-hours/', WorkingHoursList.as_view(), name='working-hours-list'),
    path('working-hours/<int:pk>/', WorkingHoursDetail.as_view(), name='working-hours-detail'),
    path('working-hours/history/', WorkingHoursHistoryList.as_view(), name='working-hours-history'),

]