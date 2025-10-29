# -------------------   Django imports ------------------------
from django.contrib import admin
from django.utils.html import format_html
# -------------------   Apps imports ------------------------
from .models import Category, MenuItem

#############################################
#                Base Admin                 #
#############################################

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_per_page = 20

#############################################
#              Category Admin               #
#############################################

class CategoryAdmin(BaseAdmin):
    list_display = ["id", "name", "is_cofe", "created_at", "updated_at"]
    search_fields = ["name"]
    ordering = ["id"]
    list_filter = ["is_cofe", "created_at"]
    list_editable = ["name", "is_cofe"]

#############################################
#              MenuItem Admin               #
#############################################

class MenuItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "category",
        "price",
        "discount_percent",
        "discount_start",
        "discount_end",
        "final_price_display",
        "discount_active",
        "colored_status",
        "stock",
        "is_special",
        "preparation_time",
        "created_at",
        "updated_at"
    ]

    list_editable = ["price", "discount_percent", "stock", "is_special", "discount_start", "discount_end"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]
    list_filter = ["category", "is_special", "status", "created_at", "discount_start", "discount_end"]


    @admin.display(description="Final Price")
    def final_price_display(self, obj):
        """
        Returns the final price of the menu item after applying any active discount.
        If no discount is active, returns the original price.
        """
        if obj.final_price is not None:
            return "{:.2f} $".format(obj.final_price)
        return "-"


    @admin.display(boolean=True, description="Discount Active")
    def discount_active(self, obj):
        """
        Indicates whether the menu item currently has an active discount.
        """
        return obj.is_discount_active


    @admin.display(description="Status")
    def colored_status(self, obj):
        """
        Displays the availability status of the menu item in colored text:
        green for available, red for out of stock.
        """
        color = "green" if obj.status == "available" else "red"
        return format_html('<span style="color: {};">{}</span>', color, obj.status)


admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
