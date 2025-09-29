from rest_framework import status
from rest_framework.response import Response

class SoftDeleteMixin:
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RestoreMixin:
    def perform_restore(self, instance):
        instance.restore()
        return Response(status=status.HTTP_200_OK)
