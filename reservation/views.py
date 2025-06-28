from rest_framework import generics
from .models import Reservation
from .serializers import ReservationSerializer
from .permissions import IsAdminOrCreateOnly
from utility.views import BaseAPIView 

##################################################################################
#                             Reservation Views                                  #
##################################################################################

class ReservationList(BaseAPIView, generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all reservations.
        Access allowed only for admin users.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new reservation.
        Open to all users (authentication not required).
        """
        return self.create(request, *args, **kwargs)


class ReservationDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get(self, request, *args, **kwargs):
        """
        Retrieve reservation details by ID.
        Admin access only.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Fully update a reservation.
        Admin access only.
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Partially update a reservation.
        Admin access only.
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete a reservation.
        Admin access only.
        """
        return self.destroy(request, *args, **kwargs)
