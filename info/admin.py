# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import AboutUs, ContactUs, WorkingHours

#############################################
#                ‌Base Admin                 #
#############################################

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "updated_at"]
    list_per_page = 20
    list_filter = ["is_deleted", "created_at"]
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_deleted=False)
    
#############################################
#              AboutUs Admin                #
#############################################

class AboutUsAdmin(BaseAdmin):
    list_display = ["id", "title", "created_at", "updated_at"]
    search_fields = ["title", "content"]
    ordering = ["id"]
    date_hierarchy = 'created_at'
    
#############################################
#              ContactUs Admin              #
#############################################

class ContactUsAdmin(BaseAdmin):
    list_display = ["id", "phone_number", "created_at", "updated_at"]
    search_fields = ["phone_number"]
    ordering = ["id"]
    date_hierarchy = 'created_at'
 
#############################################
#              WorkingHours Admin           #
#############################################
   
class WorkingHoursAdmin(BaseAdmin):
    list_display = ['day', 'open_time', 'close_time']
    ordering = ['day']
    
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(WorkingHours, WorkingHoursAdmin)

