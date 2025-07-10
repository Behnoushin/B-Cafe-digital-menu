from django.urls import path
from .views import (
    CategoryList, CategoryDetail, MenuItemList,
    MenuItemDetail, SpecialOfferList, SpecialOfferDetail
    )

urlpatterns = [
    
    # Category URLs
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetail.as_view(), name="category-detail"),
    
    # MenuItem URLs
    path("menu-items/", MenuItemList.as_view(), name='menuitem-list'),
    path("menu-items/<int:pk>/", MenuItemDetail.as_view(), name='menuitem-detail'),
    
    # SpecialOffer URLs
    path("special-offers/", SpecialOfferList.as_view(), name='special-offer-list'),
    path("special-offers/<int:pk>/", SpecialOfferDetail.as_view(), name='special-offer-detail'),
]
