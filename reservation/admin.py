# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import Reservation, Table

#############################################
#                Table Admin                #
#############################################

class TableAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "capacity"]
    search_fields = ["number"]
    ordering = ["number"]
    list_editable = ["number", "capacity"]
    list_filter = ["capacity"]
    readonly_fields = ["id"]
    list_per_page = 20

#############################################
#              Reservation Admin            #
#############################################

class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "phone_number", "date", "time", "number_of_guests", "created_at", "updated_at"]
    search_fields = ["full_name", "phone_number"]
    ordering = ["-created_at"]
    list_filter = ["date", "created_at"]
    list_editable = ["full_name", "phone_number", "number_of_guests"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_per_page = 20

admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)