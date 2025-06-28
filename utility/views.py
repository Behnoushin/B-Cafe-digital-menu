from rest_framework import generics
from .mixins import SoftDeleteMixin

class BaseAPIView(generics.GenericAPIView):
    pass

class SoftDeleteGenericView(SoftDeleteMixin, generics.DestroyAPIView):
    serializer_class = None 

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
