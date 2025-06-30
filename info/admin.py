from django.contrib import admin
from .models import AboutUs, ContactUs

#############################################
#              AboutUs Admin                #
#############################################

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "updated_at"]
    search_fields = ["title", "content"]
    ordering = ["id"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20
    
#############################################
#              ContactUs Admin              #
#############################################

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "created_at", "updated_at"]
    search_fields = ["phone_number"]
    ordering = ["id"]
    readonly_fields = ["id", "created_at", "updated_at"]
    date_hierarchy = 'created_at'
    list_per_page = 20
    
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
