from django.urls import path
from .views import (
    AboutUsList, AboutUsDetail, AboutUsRestore, AboutUsHistory,
    ContactUsList, ContactUsDetail, ContactUsRestore, ContactUsHistory,
    WorkingHoursList, WorkingHoursDetail, WorkingHoursRestore, WorkingHoursHistory
)

urlpatterns = [
    # About Us
    path('about/', AboutUsList.as_view(), name='aboutus-list'),
    path('about/<int:pk>/', AboutUsDetail.as_view(), name='aboutus-detail'),
    path('about/restore/<int:pk>/', AboutUsRestore.as_view(), name='aboutus-restore'),
    path('about/history/', AboutUsHistory.as_view(), name='aboutus-history'),

    # Contact Us
    path('contact/', ContactUsList.as_view(), name='contactus-list'),
    path('contact/<int:pk>/', ContactUsDetail.as_view(), name='contactus-detail'),
    path('contact/restore/<int:pk>/', ContactUsRestore.as_view(), name='contactus-restore'),
    path('contact/history/', ContactUsHistory.as_view(), name='contactus-history'),

    # Working Hours
    path('working-hours/', WorkingHoursList.as_view(), name='working-hours-list'),
    path('working-hours/<int:pk>/', WorkingHoursDetail.as_view(), name='working-hours-detail'),
    path('working-hours/restore/<int:pk>/', WorkingHoursRestore.as_view(), name='working-hours-restore'),
    path('working-hours/history/', WorkingHoursHistory.as_view(), name='working-hours-history'),
]
