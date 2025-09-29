# -------------------  DRF imports   ------------------------
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# -------------------  DRF imports   ------------------------
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
# -------------------   Apps imports ------------------------
from .models import AboutUs, ContactUs, WorkingHours
from .serializers import AboutUsSerializer, ContactUsSerializer, WorkingHoursSerializer
from .permissions import IsAdminOrReadOnly
from utility.views import BaseAPIView  


CACHE_TTL = getattr(settings, 'CACHE_TTL', 60*5)

##################################################################################
#                             AboutUs Views                                      #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class AboutUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [IsAdminOrReadOnly]

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class AboutUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)
        return instance

    def perform_destroy(self, instance):
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)
        instance.delete()
        
class AboutUsHistoryList(generics.ListAPIView):
    permission_classes = [IsAdminUser] 
    def get_queryset(self):
        return AboutUs.history.all() 
        
##################################################################################
#                             ContactUs Views                                    #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ContactUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrReadOnly]

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ContactUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)
        return instance

    def perform_destroy(self, instance):
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)
        instance.delete()

class ContactUsHistoryList(generics.ListAPIView):
    permission_classes = [IsAdminUser] 
    def get_queryset(self):
        return ContactUs.history.all() 

##################################################################################
#                             WorkingHours Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class WorkingHoursList(generics.ListCreateAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer
    permission_classes = [IsAdminOrReadOnly]

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class WorkingHoursDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def perform_update(self, serializer):
        instance = serializer.save()
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)
        return instance

    def perform_destroy(self, instance):
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)
        instance.delete()

class WorkingHoursHistoryList(generics.ListAPIView):
    permission_classes = [IsAdminUser] 
    def get_queryset(self):
        return WorkingHours.history.all()