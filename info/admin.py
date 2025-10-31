# -------------------   Django imports ------------------------
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
# -------------------   Apps imports ------------------------
from .models import AboutUs, ContactUs, WorkingHours

#############################################
#                ‌Base Admin                 #
#############################################

class BaseAdmin(admin.ModelAdmin):
    """
    Base admin for all models: provides readonly fields, 
    soft-delete filtering, history integration, and pagination.
    """
    readonly_fields = ["id", "created_at", "updated_at"]
    list_per_page = 20
    list_filter = ["is_deleted", "created_at"]
    
    def get_queryset(self, request):
        """Return only non-deleted objects."""
        return super().get_queryset(request).filter(is_deleted=False)
    
#############################################
#              AboutUs Admin                #
#############################################

class AboutUsAdmin(SimpleHistoryAdmin, BaseAdmin):
    list_display = ["id", "title", "short_description", "created_at", "updated_at"]
    search_fields = ["title", "short_description", "content"]
    ordering = ["-created_at"]
    date_hierarchy = 'created_at'
    readonly_fields = BaseAdmin.readonly_fields + ["history"]
    
#############################################
#              ContactUs Admin              #
#############################################

class ContactUsAdmin(SimpleHistoryAdmin, BaseAdmin):
    list_display = ["id", "phone_number", "email", "created_at", "updated_at"]
    search_fields = ["phone_number", "email", "address"]
    ordering = ["-created_at"]
    list_filter = BaseAdmin.list_filter + ["email"]
    readonly_fields = BaseAdmin.readonly_fields + ["history"]
 
#############################################
#              WorkingHours Admin           #
#############################################
   
class WorkingHoursAdmin(SimpleHistoryAdmin, BaseAdmin):
    list_display = ['day', 'open_time', 'close_time']
    search_fields = ['day']
    ordering = ['day']
    list_filter = ['day']
    readonly_fields = BaseAdmin.readonly_fields + ["history"]
    
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(WorkingHours, WorkingHoursAdmin)