from django.urls import path
from .views import (
    IngredientRequestListCreateView,
    IngredientRequestDetailView,
    IngredientItemUpdateView,
    MyIngredientRequestsList,
    CreateIngredientRequest,
    UpdateIngredientRequest,
    DeleteIngredientRequest,
    AllIngredientRequestsList,
    ApproveOrRejectIngredientItem,
    IngredientRequestByStatus,
    RecentIngredientRequests,
    IngredientItemByApprovalStatus,
)

urlpatterns = [
    # IngredientRequest URLs
    path('requests/', IngredientRequestListCreateView.as_view(), name='ingredient-request-list'),
    path('requests/<int:pk>/', IngredientRequestDetailView.as_view(), name='ingredient-request-detail'),

    # IngredientItem URLs (Admin only)
    path('items/<int:pk>/update/', IngredientItemUpdateView.as_view(), name='ingredient-item-update'),
    
    # Chef URLs
    path('requests/my/', MyIngredientRequestsList.as_view(), name='my-ingredient-requests'),
    path('requests/create/', CreateIngredientRequest.as_view(), name='create-ingredient-request'),
    path('requests/<int:pk>/update/', UpdateIngredientRequest.as_view(), name='update-ingredient-request'),
    path('requests/<int:pk>/delete/', DeleteIngredientRequest.as_view(), name='delete-ingredient-request'),

    # Admin URLs
    path('requests/all/', AllIngredientRequestsList.as_view(), name='all-ingredient-requests'),
    path('requests/status/', IngredientRequestByStatus.as_view(), name='ingredient-requests-by-status'),
    path('requests/recent/', RecentIngredientRequests.as_view(), name='recent-ingredient-requests'),

    # Ingredient Item URLs (Admin only)
    path('items/<int:pk>/update/', ApproveOrRejectIngredientItem.as_view(), name='update-ingredient-item'),
    path('items/filter/', IngredientItemByApprovalStatus.as_view(), name='ingredient-items-by-status'),
]
