# ------------------- Django imports ------------------------
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings

# ------------------- DRF imports ------------------------
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# ------------------- App imports ------------------------
from utility.views import BaseAPIView
from utility.mixins import RestoreMixin
from .models import IngredientRequest, IngredientItem
from .serializers import IngredientRequestSerializer, IngredientItemSerializer
from .permissions import IsChefOrAdmin, IsAdminOnly, IsChefAndNotApprovedOrAdmin

# ------------------- Constants ------------------------
CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 5)

##################################################################################
#                               Base View                                        #
##################################################################################

class IngredientBaseView(BaseAPIView):
    """
    Base view for IngredientRequest app.
    Handles:
    - Cache invalidation on update and delete
    - Provides common permission classes
    """
    permission_classes = [IsChefOrAdmin]

    def perform_update(self, serializer):
        instance = serializer.save()
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)
        return instance

    def perform_destroy(self, instance):
        instance.delete()
        cache_key = f'views.decorators.cache.cache_page.{self.request.get_full_path()}'
        cache.delete(cache_key)

##################################################################################
#                        IngredientRequest Views                                  #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class IngredientRequestListCreateView(IngredientBaseView, generics.ListCreateAPIView):
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'chef':
            return self.queryset.filter(chef=user)
        return self.queryset.all()

    def perform_create(self, serializer):
        serializer.save(chef=self.request.user)

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class IngredientRequestDetailView(IngredientBaseView, generics.RetrieveUpdateDestroyAPIView):
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefAndNotApprovedOrAdmin]

##################################################################################
#                        IngredientItem Update (Admin)                             #
##################################################################################

class IngredientItemUpdateView(IngredientBaseView, generics.UpdateAPIView):
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAdminOnly]

##################################################################################
#                        My Requests / Chef Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MyIngredientRequestsList(IngredientBaseView, generics.ListAPIView):
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'chef':
            return self.queryset.filter(chef=user)
        return self.queryset.none()

##################################################################################
#                        Create / Update / Delete Views                           #
##################################################################################

class CreateIngredientRequest(IngredientBaseView, generics.CreateAPIView):
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefOrAdmin]

    def perform_create(self, serializer):
        serializer.save(chef=self.request.user)

class UpdateIngredientRequest(IngredientBaseView, generics.UpdateAPIView):
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefAndNotApprovedOrAdmin]

class DeleteIngredientRequest(IngredientBaseView, generics.DestroyAPIView):
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefAndNotApprovedOrAdmin]

##################################################################################
#                        Admin Views                                              #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class AllIngredientRequestsList(IngredientBaseView, generics.ListAPIView):
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsAdminOnly]

class ApproveOrRejectIngredientItem(IngredientBaseView, generics.UpdateAPIView):
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAdminOnly]

class IngredientRequestByStatus(IngredientBaseView, generics.ListAPIView):
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        status_param = self.request.query_params.get('is_reviewed')
        if status_param is not None:
            return IngredientRequest.objects.filter(is_reviewed=status_param.lower() == 'true')
        return IngredientRequest.objects.all()

class RecentIngredientRequests(IngredientBaseView, generics.ListAPIView):
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return IngredientRequest.objects.all().order_by('-created_at')[:10]

class IngredientItemByApprovalStatus(IngredientBaseView, generics.ListAPIView):
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        approved = self.request.query_params.get('is_approved')
        rejected = self.request.query_params.get('is_rejected')
        purchased = self.request.query_params.get('is_purchased')

        queryset = IngredientItem.objects.all()
        if approved is not None:
            queryset = queryset.filter(is_approved=approved.lower() == 'true')
        if rejected is not None:
            queryset = queryset.filter(is_rejected=rejected.lower() == 'true')
        if purchased is not None:
            queryset = queryset.filter(is_purchased=purchased.lower() == 'true')
        return queryset

##################################################################################
#                        Restore & History Views                                 #
##################################################################################

class IngredientRequestRestoreView(RestoreMixin, APIView):
    permission_classes = [IsAdminOnly]

    def post(self, request, pk):
        instance = IngredientRequest.objects.get(pk=pk)
        instance.is_deleted = False
        instance.save()
        cache_key = f'views.decorators.cache.cache_page.{request.get_full_path()}'
        cache.delete(cache_key)
        return Response({"success": f"IngredientRequest '{instance.id}' restored"}, status=status.HTTP_200_OK)

class IngredientRequestHistoryList(IngredientBaseView, generics.ListAPIView):
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return IngredientRequest.history.all()
