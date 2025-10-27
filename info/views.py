# -------------------  Django & DRF imports   ------------------------
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# -------------------  DRF imports   ------------------------
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
# -------------------   Apps imports ------------------------
from .models import AboutUs, ContactUs, WorkingHours
from .serializers import AboutUsSerializer, ContactUsSerializer, WorkingHoursSerializer
from .permissions import IsAdminOrReadOnly
from utility.views import BaseAPIView
from utility.mixins import SoftDeleteMixin, RestoreMixin


CACHE_TTL = getattr(settings, 'CACHE_TTL', 60*5)


##################################################################################
#                             InfoBase Views                                      #
##################################################################################

class InfoBaseView(BaseAPIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False)

    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete(f'views.decorators.cache.cache_page.{self.request.get_full_path()}')
        return instance

    def perform_destroy(self, instance):
        SoftDeleteMixin.perform_destroy(self, instance)
        cache.delete(f'views.decorators.cache.cache_page.{self.request.get_full_path()}')

# ----------------- Restore & History -----------------
class InfoRestoreView(RestoreMixin, APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        self.perform_restore(instance)
        return Response({"success": f"{self.model.__name__} restored"}, status=status.HTTP_200_OK)

class InfoHistoryList(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return self.model.history.all()
    
##################################################################################
#                             AboutUs Views                                      #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class AboutUsList(InfoBaseView, generics.ListCreateAPIView):
    model = AboutUs
    serializer_class = AboutUsSerializer

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class AboutUsDetail(InfoBaseView, generics.RetrieveUpdateDestroyAPIView):
    model = AboutUs
    serializer_class = AboutUsSerializer

class AboutUsRestore(InfoRestoreView):
    model = AboutUs

class AboutUsHistory(InfoHistoryList):
    model = AboutUs

##################################################################################
#                             ContactUs Views                                    #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ContactUsList(InfoBaseView, generics.ListCreateAPIView):
    model = ContactUs
    serializer_class = ContactUsSerializer

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ContactUsDetail(InfoBaseView, generics.RetrieveUpdateDestroyAPIView):
    model = ContactUs
    serializer_class = ContactUsSerializer

class ContactUsRestore(InfoRestoreView):
    model = ContactUs

class ContactUsHistory(InfoHistoryList):
    model = ContactUs


##################################################################################
#                             WorkingHours Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class WorkingHoursList(InfoBaseView, generics.ListCreateAPIView):
    model = WorkingHours
    serializer_class = WorkingHoursSerializer

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class WorkingHoursDetail(InfoBaseView, generics.RetrieveUpdateDestroyAPIView):
    model = WorkingHours
    serializer_class = WorkingHoursSerializer

class WorkingHoursRestore(InfoRestoreView):
    model = WorkingHours

class WorkingHoursHistory(InfoHistoryList):
    model = WorkingHours
