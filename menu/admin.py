# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import Category, MenuItem

#############################################
#              Category Admin               #
#############################################

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_cofe", "created_at", "updated_at"]
    search_fields = ["name"]
    ordering = ["id"]
    list_filter = ["is_cofe", "created_at"]
    list_editable = ["name", "is_cofe"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20
    
#############################################
#              MenuItem Admin               #
#############################################

class MenuItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "category",
        "price",
        "final_price_display",
        "discount_percent",
        "discount_start",
        "discount_end",
        "stock",
        "status",
        "is_special",
        "preparation_time",
        "created_at",
        "updated_at"
    ]
    
    search_fields = ["name", "description"]
    ordering = ["-created_at"]
    list_filter = ["category", "is_special", "status", "created_at", "discount_start", "discount_end"]
    list_editable = ["price", "discount_percent", "stock", "is_special", "discount_start", "discount_end"]
    readonly_fields = ["id", "status", "final_price_display", "created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_per_page = 20

    @admin.display(description="Final Price")
    def final_price_display(self, obj):
        if obj.final_price is not None:
            return "{:.2f} $".format(obj.final_price)
        return "-"

admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)