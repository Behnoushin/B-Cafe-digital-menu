# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import IngredientRequest, IngredientItem

#############################################
#           IngredientItemInline             #
#############################################

class IngredientItemInline(admin.TabularInline):
    model = IngredientItem
    extra = 0
    readonly_fields = ['is_approved', 'is_rejected', 'is_purchased']

#############################################
#         IngredientRequest Admin            #
#############################################

class IngredientRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'chef', 'note', 'is_reviewed', 'created_at', 'updated_at']
    search_fields = ['chef__username', 'note']
    list_filter = ['is_reviewed', 'created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [IngredientItemInline]
    list_per_page = 20

#############################################
#          IngredientItem Admin             #
#############################################

class IngredientItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'request', 'name', 'quantity', 'is_approved', 'is_rejected', 'is_purchased']
    list_filter = ['is_approved', 'is_rejected', 'is_purchased']
    search_fields = ['name', 'request__chef__username']
    readonly_fields = ['id']
    list_per_page = 25

admin.site.register(IngredientRequest, IngredientRequestAdmin)
admin.site.register(IngredientItem, IngredientItemAdmin)