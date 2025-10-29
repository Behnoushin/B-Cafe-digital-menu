# -------------------  Django imports   ------------------------
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings

# -------------------  DRF imports   ------------------------
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

# -------------------   Apps imports ------------------------
from .models import Reservation , Table
from .serializers import ReservationSerializer, TableSerializer
from .permissions import IsAdminOrCreateOnly
from utility.views import BaseAPIView 
from utility.mixins import RestoreMixin
from menu.models import MenuItem


# ------------------- Constants ------------------------
CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 5)


##################################################################################
#                             Reservation Views                                  #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='get')
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

##################################################################################
#                         ReservationsByDate Views                                #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='get')
class ReservationsByDate(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all reservations for a specific date.
    Useful for admins to manage daily bookings.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get_queryset(self):
        date = self.kwargs['date']
        return Reservation.objects.filter(date=date)

##################################################################################
#                         ReservationsByTable Views                               #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='get')
class ReservationsByTable(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all reservations for a specific table.
    Helps admins check table occupancy.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get_queryset(self):
        table_id = self.kwargs['table_id']
        return Reservation.objects.filter(table_id=table_id)

##################################################################################
#                         UpcomingReservations Views                              #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='get')
class UpcomingReservations(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all upcoming reservations.
    Shows reservations with date/time after current time.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get_queryset(self):
        now = timezone.now()
        return Reservation.objects.filter(
            date__gt=now.date()
        ) | Reservation.objects.filter(
            date=now.date(),
            time__gte=now.time()
        )

##################################################################################
#                         ApprovedReservations Views                              #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='get')
class ApprovedReservations(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all approved reservations.
    Only reservations confirmed by admin are returned.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get_queryset(self):
        return Reservation.objects.filter(is_approved=True)

##################################################################################
#                         PendingReservations Views                               #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='get')
class PendingReservations(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all pending reservations.
    Only reservations awaiting admin approval are returned.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get_queryset(self):
        return Reservation.objects.filter(is_approved=False)

##################################################################################
#                         AvailableTables Views                                   #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='get')
class AvailableTables(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all available tables for a given date and time.
    Helps users choose a free table when making a reservation.
    """
    serializer_class = TableSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get_queryset(self):
        date = self.request.query_params.get("date")
        time = self.request.query_params.get("time")
        reserved_tables = Reservation.objects.filter(
            date=date,
            time=time,
            is_approved=True
        ).values_list('table_id', flat=True)
        return Table.objects.exclude(id__in=reserved_tables)


##################################################################################
#                        MenuItem Restore & History Views                         #
##################################################################################

class MenuItemRestoreView(RestoreMixin, APIView):
    """
    Restore a soft-deleted menu item (admin only).
    """
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        instance = MenuItem.objects.get(pk=pk)
        instance.is_deleted = False
        instance.save()
        return Response({"success": f"MenuItem '{instance.name}' restored"}, status=status.HTTP_200_OK)


class MenuItemHistoryList(BaseAPIView, generics.ListAPIView):
    """
    List all historical changes for menu items (admin only).
    """
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return MenuItem.history.all()