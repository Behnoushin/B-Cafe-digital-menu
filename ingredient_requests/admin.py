# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import IngredientRequest, IngredientItem

#############################################
#               Base Admin                  #
#############################################

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20

#############################################
#           IngredientItemInline            #
#############################################

class IngredientItemInline(admin.TabularInline):
    model = IngredientItem
    extra = 0
    readonly_fields = ['is_approved', 'is_rejected', 'is_purchased']

#############################################
#         IngredientRequest Admin           #
#############################################

class IngredientRequestAdmin(BaseAdmin):
    list_display = ['id', 'chef', 'note', 'is_reviewed', 'created_at', 'updated_at']
    search_fields = ['chef__username', 'note']
    list_filter = ['is_reviewed', 'created_at']
    inlines = [IngredientItemInline]

#############################################
#          IngredientItem Admin             #
#############################################

class IngredientItemAdmin(BaseAdmin):
    list_display = ['id', 'request', 'name', 'quantity', 'is_approved', 'is_rejected', 'is_purchased']
    search_fields = ['name', 'request__chef__username']
    list_filter = ['is_approved', 'is_rejected', 'is_purchased']


admin.site.register(IngredientRequest, IngredientRequestAdmin)
admin.site.register(IngredientItem, IngredientItemAdmin)
