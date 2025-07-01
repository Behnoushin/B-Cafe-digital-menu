# -------------------  DRF imports   ------------------------
from rest_framework import generics
# -------------------   Apps imports ------------------------
from .models import AboutUs, ContactUs
from .serializers import AboutUsSerializer, ContactUsSerializer
from .permissions import IsAdminOrReadOnly
from utility.views import BaseAPIView  

##################################################################################
#                             AboutUs Views                                      #
##################################################################################

class AboutUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [IsAdminOrReadOnly]


class AboutUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [IsAdminOrReadOnly]

##################################################################################
#                             ContactUs Views                                    #
##################################################################################

class ContactUsList(BaseAPIView, generics.ListCreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrReadOnly]


class ContactUsDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrReadOnly]
