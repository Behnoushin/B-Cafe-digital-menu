from django.contrib import admin
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
    list_display = ["id", "name", "category", "price", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    ordering = ["id"]
    list_filter = ["category", "created_at"]
    list_editable = ["name", "price"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)