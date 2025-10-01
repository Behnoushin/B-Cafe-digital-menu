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

##################################################################################
#                        MyIngredientRequestsList View                            #
##################################################################################

class MyIngredientRequestsList(BaseAPIView, generics.ListAPIView):
    """
    View to list all ingredient requests of the logged-in chef.
    Chefs can only see their own requests.
    """
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'chef':
            return self.queryset.filter(chef=user)
        return self.queryset.none()  # only chef's own requests


##################################################################################
#                        CreateIngredientRequest View                             #
##################################################################################

class CreateIngredientRequest(BaseAPIView, generics.CreateAPIView):
    """
    View to create a new ingredient request with multiple items.
    Only chefs (and optionally admins) can create requests.
    """
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefOrAdmin]

    def perform_create(self, serializer):
        serializer.save(chef=self.request.user)


##################################################################################
#                        UpdateIngredientRequest View                             #
##################################################################################

class UpdateIngredientRequest(BaseAPIView, generics.UpdateAPIView):
    """
    View to update note and items of an ingredient request.
    Only allowed if the request is NOT reviewed by admin.
    """
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefAndNotApprovedOrAdmin]


##################################################################################
#                        DeleteIngredientRequest View                             #
##################################################################################

class DeleteIngredientRequest(BaseAPIView, generics.DestroyAPIView):
    """
    View to delete an ingredient request.
    Only allowed if the request is NOT reviewed by admin.
    """
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsChefAndNotApprovedOrAdmin]


##################################################################################
#                        AllIngredientRequestsList View                            #
##################################################################################

class AllIngredientRequestsList(BaseAPIView, generics.ListAPIView):
    """
    View to list all ingredient requests for admin.
    Admins can see requests from all chefs.
    """
    queryset = IngredientRequest.objects.all()
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsAdminOnly]


##################################################################################
#                        ApproveOrRejectIngredientItem View                       #
##################################################################################

class ApproveOrRejectIngredientItem(BaseAPIView, generics.UpdateAPIView):
    """
    View to approve, reject, or mark items as purchased.
    Only admins have access to this endpoint.
    """
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAdminOnly]


##################################################################################
#                        IngredientRequestByStatus View                           #
##################################################################################

class IngredientRequestByStatus(BaseAPIView, generics.ListAPIView):
    """
    View to filter ingredient requests based on is_reviewed status.
    Only admins can use this view.
    """
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        status = self.request.query_params.get('is_reviewed')
        if status is not None:
            return IngredientRequest.objects.filter(is_reviewed=status.lower() == 'true')
        return IngredientRequest.objects.all()


##################################################################################
#                        RecentIngredientRequests View                             #
##################################################################################

class RecentIngredientRequests(BaseAPIView, generics.ListAPIView):
    """
    View to list the most recent ingredient requests.
    Useful for admin dashboard.
    """
    serializer_class = IngredientRequestSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        return IngredientRequest.objects.all().order_by('-created_at')[:10]


##################################################################################
#                        IngredientItemByApprovalStatus View                      #
##################################################################################

class IngredientItemByApprovalStatus(BaseAPIView, generics.ListAPIView):
    """
    View to filter ingredient items by approval, rejection, or purchased status.
    Only accessible by admins.
    """
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
