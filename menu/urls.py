from django.urls import path
from .views import (
    CategoryList,
    CategoryDetail,
    MenuItemList,
    MenuItemDetail,
    SpecialOfferList,
    SpecialOfferDetail,
    TopSellingMenuItems, 
    RecentMenuItems, 
    MenuItemsByPrepTime,
    ActiveMenuItems, 
    OutOfStockMenuItems,
    MenuItemsByCategory, 
    MenuItemRestoreView, MenuItemHistoryList
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
     
    # TopSellingMenuItems URL
    path("menu-items/top-selling/", TopSellingMenuItems.as_view(), name="menuitem-top-selling"),

    # RecentMenuItems URL
    path("menu-items/recent/", RecentMenuItems.as_view(), name="menuitem-recent"),
    
    # MenuItemsByPrepTime URL
    path("menu-items/by-preptime/", MenuItemsByPrepTime.as_view(), name="menuitem-by-preptime"),
    
    # ActiveMenuItems URL
    path("menu-items/active/", ActiveMenuItems.as_view(), name="menuitem-active"),
    
    # OutOfStockMenuItems URL
    path("menu-items/out-of-stock/", OutOfStockMenuItems.as_view(), name="menuitem-out-of-stock"),

    # MenuItemsByCategory URL
    path("categories/<int:category_id>/menu-items/", MenuItemsByCategory.as_view(), name="menuitems-by-category"),

    # Restore a soft-deleted menu item
    path("menu-items/<int:pk>/restore/", MenuItemRestoreView.as_view(), name="menuitem-restore"),

    # List historical changes of menu items
    path("menu-items/history/", MenuItemHistoryList.as_view(), name="menuitem-history"),
]
