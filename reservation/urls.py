from django.urls import path
from .views import (
    ReservationList,
    ReservationDetail,
    ReservationsByDate,
    ReservationsByTable,
    UpcomingReservations,
    ApprovedReservations,
    PendingReservations,
    AvailableTables,
)

urlpatterns = [
    # Reservation URLs
    path("reservations/", ReservationList.as_view(), name="reservation-list"),
    path("reservations/<int:pk>/", ReservationDetail.as_view(), name="reservation-detail"),

    # ReservationsByDate URLs
    path("reservations/date/<str:date>/", ReservationsByDate.as_view(), name="reservations-by-date"),
    
    # ReservationsByTable URLs
    path("reservations/table/<int:table_id>/", ReservationsByTable.as_view(), name="reservations-by-table"),
    
    # UpcomingReservations URLs
    path("reservations/upcoming/", UpcomingReservations.as_view(), name="upcoming-reservations"),
    
    # ApprovedReservations URLs
    path("reservations/approved/", ApprovedReservations.as_view(), name="approved-reservations"),
    
    # PendingReservations URLs
    path("reservations/pending/", PendingReservations.as_view(), name="pending-reservations"),

    # AvailableTables URLs
    path("tables/available/", AvailableTables.as_view(), name="available-tables"),
]
