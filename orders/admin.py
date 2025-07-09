# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import Order, OrderItem

#############################################
#              OrderItemInline              #
#############################################

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 
    readonly_fields = ['final_price', 'total_item_price']

#############################################
#               Order Admin                 #
#############################################

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'table', 'status', 'created_at', 'total_price']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'note']
    readonly_fields = ['id', 'created_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
    list_per_page = 20
    date_hierarchy = 'created_at'

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

#############################################
#            OrderItem Admin                #
#############################################

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'menu_item', 'quantity', 'total_item_price']
    search_fields = ['order__id', 'menu_item__name']
    readonly_fields = ['total_item_price']
    ordering = ['id']
    list_per_page = 20


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)



