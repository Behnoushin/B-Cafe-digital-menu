# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import CustomUser

#############################################
#              CustomUser Admin             #
#############################################

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'role']
    list_filter = ['role', 'is_staff', 'is_active']
    ordering = ['id']
    readonly_fields = ['id', 'last_login', 'date_joined']
    list_per_page = 20


admin.site.register(CustomUser, CustomUserAdmin)