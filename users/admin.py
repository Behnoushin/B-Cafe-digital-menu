# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import CustomUser, PurchaseHistory

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

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

#############################################
#         PurchaseHistory Admin             #
#############################################

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_name', 'quantity', 'price', 'purchase_date']
    search_fields = ['product_name', 'user__username']
    list_filter = ['purchase_date']
    readonly_fields = ['id', 'purchase_date', 'created_at', 'updated_at']
    ordering = ['-purchase_date']
    list_per_page = 25

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)