from django.utils import timezone

class SoftDeleteMixin:
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        return instance

class RestoreMixin:
    def perform_restore(self, instance):
        instance.is_deleted = False
        instance.deleted_at = None
        instance.save()
        return instance
