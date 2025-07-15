# -------------------  DRF imports   ------------------------
from rest_framework import generics
# -------------------   Apps imports ------------------------
from .models import IngredientRequest, IngredientItem
from .serializers import IngredientRequestSerializer, IngredientItemSerializer
from .permissions import IsChefOrAdmin, IsAdminOnly, IsChefAndNotApprovedOrAdmin
from utility.views import BaseAPIView

##################################################################################
#                        IngredientRequest Views                                  #
##################################################################################

class IngredientRequestListCreateView(BaseAPIView, generics.ListCreateAPIView):
    """
    View to:
    - List ingredient requests:
      * Chefs see only their own requests
      * Admins see all requests
    - Create new ingredient requests by chefs (and admins if needed)
    """
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


class IngredientRequestDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    View to:
    - Retrieve details of a specific ingredient request
    - Allow chefs to update or delete their requests only if NOT approved by admin
    - Allow admins to view, update, or delete any request at any time
    - Prevent chefs from editing or deleting after admin approval
    """
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefAndNotApprovedOrAdmin]

##################################################################################
#                        IngredientItemUpdate Views                              #
##################################################################################

class IngredientItemUpdateView(BaseAPIView, generics.UpdateAPIView):
    """
    View to:
    - Update status of each ingredient item (approved, rejected, purchased)
      Only admins have permission
    - Chefs do NOT have access to this endpoint
    """
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAdminOnly]
