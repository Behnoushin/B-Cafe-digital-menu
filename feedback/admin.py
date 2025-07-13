# -------------------   Django imports ------------------------
from django.contrib import admin
# -------------------   Apps imports ------------------------
from .models import Feedback

#############################################
#              Feedback Admin               #
#############################################

class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "item",
        "food_rating",
        "revisit_intent",
        "status",
        "feedback_type",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "user__username",
        "item__name",
        "comment",
        "admin_response",
    ]
    ordering = ["-created_at"]
    readonly_fields = [
        "id",
        "user",
        "order",
        "item",
        "food_rating",
        "service_satisfaction",
        "staff_behavior",
        "cleanliness",
        "preparation_time",
        "revisit_intent",
        "comment",
        "user_ip",
        "user_agent",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "status",
        "feedback_type",
        "food_rating",
        "revisit_intent",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "created_at"
    list_per_page = 20

    def has_add_permission(self, request):
        # Prevent manual addition of feedback via admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent feedback from being deleted
        return False

    def has_change_permission(self, request, obj=None):
        # Only admins can edit
        return request.user.is_staff


admin.site.register(Feedback, FeedbackAdmin)
