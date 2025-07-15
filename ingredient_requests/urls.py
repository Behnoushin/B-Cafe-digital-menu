from django.urls import path
from .views import (
    IngredientRequestListCreateView,
    IngredientRequestDetailView,
    IngredientItemUpdateView,
)

urlpatterns = [
    path('requests/', IngredientRequestListCreateView.as_view(), name='ingredient-request-list'),
    path('requests/<int:pk>/', IngredientRequestDetailView.as_view(), name='ingredient-request-detail'),
    path('items/<int:pk>/update/', IngredientItemUpdateView.as_view(), name='ingredient-item-update'),
]
