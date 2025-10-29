# -----------------  Django imports   ------------------------
from django.utils import timezone
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# -------------------  DRF imports   ------------------------
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

# -------------------   Apps imports ------------------------
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .permissions import IsAdminOrReadOnly
from .filters import MenuItemFilter, MenuItemPrepTimeFilter
from .throttles import MenuItemListThrottle
from utility.views import BaseAPIView
from utility.mixins import RestoreMixin

# ----------------- Cache TTL -----------------
CACHE_TTL = 60 * 5  # 5 minutes


##################################################################################
#                            Base Generic Views                                  #
##################################################################################

class BaseListCreateView(BaseAPIView, generics.ListCreateAPIView):
    """
    Base class for list and create endpoints.
    Provides default permission and behavior.
    """
    permission_classes = [IsAdminOrReadOnly]


class BaseRetrieveUpdateDestroyView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    Base class for retrieve, update, and destroy endpoints.
    Provides default permission and behavior.
    """
    permission_classes = [IsAdminOrReadOnly]

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
#                             Category Views                                     #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CategoryList(BaseListCreateView):
    """
    List all categories or create a new one (admin only).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CategoryDetail(BaseRetrieveUpdateDestroyView):
    """
    Retrieve, update or delete a category (admin only for write ops).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


##################################################################################
#                             MenuItem Views                                     #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MenuItemList(BaseListCreateView):
    """
    List all menu items or create a new one (admin only).
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MenuItemFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "sold_count", "created_at"]
    ordering = ["-created_at"]
    throttle_classes = [MenuItemListThrottle]


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MenuItemDetail(BaseRetrieveUpdateDestroyView):
    """
    Retrieve, update or delete a menu item (admin only for write ops).
    """
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer


##################################################################################
#                             SpecialOffer Views                                 #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SpecialOfferBaseView(BaseAPIView):
    """
    Base queryset logic for active special offers.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        now = timezone.now()
        return MenuItem.objects.filter(
            discount_percent__gt=0,
            discount_start__lte=now,
            discount_end__gte=now
        )


class SpecialOfferList(SpecialOfferBaseView, generics.ListCreateAPIView):
    """
    List or create special offers (admin only for create).
    """


class SpecialOfferDetail(SpecialOfferBaseView, generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a special offer item (admin only for write ops).
    """


##################################################################################
#                         TopSellingMenuItems Views                              #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class TopSellingMenuItems(BaseAPIView, generics.ListAPIView):
    """
    Returns the top 10 best-selling menu items.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        return MenuItem.objects.order_by("-sold_count")[:10]


##################################################################################
#                           RecentMenuItems Views                                #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class RecentMenuItems(BaseAPIView, generics.ListAPIView):
    """
    Returns the 10 most recently added menu items.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        return MenuItem.objects.order_by("-created_at")[:10]


##################################################################################
#                         MenuItemsByPrepTime Views                              #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MenuItemsByPrepTime(BaseAPIView, generics.ListAPIView):
    """
    Filters menu items based on preparation time (max_minutes).
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuItemPrepTimeFilter

    def get_queryset(self):
        return MenuItem.objects.exclude(preparation_time__isnull=True)


##################################################################################
#                         ActiveMenuItems Views                                  #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ActiveMenuItems(BaseAPIView, generics.ListAPIView):
    """
    Lists all available (in-stock) menu items.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        return MenuItem.objects.filter(status="available")


##################################################################################
#                         OutOfStockMenuItems Views                              #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class OutOfStockMenuItems(BaseAPIView, generics.ListAPIView):
    """
    Lists all out-of-stock menu items.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        return MenuItem.objects.filter(status="out_of_stock")


##################################################################################
#                         MenuItemsByCategory Views                              #
##################################################################################

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MenuItemsByCategory(BaseAPIView, generics.ListAPIView):
    """
    Returns menu items filtered by category ID.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return MenuItem.objects.filter(category_id=category_id)


##################################################################################
#                         Restore & History Views                                 #
##################################################################################

class MenuItemRestoreView(RestoreMixin, APIView):
    """
    Restore a soft-deleted menu item (admin only).
    """
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        instance = MenuItem.objects.get(pk=pk)
        instance.is_deleted = False
        instance.save()
        return Response({"success": f"MenuItem '{instance.name}' restored"}, status=status.HTTP_200_OK)


class MenuItemHistoryList(generics.ListAPIView):
    """
    List all historical changes for menu items (admin only).
    """
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return MenuItem.history.all()  
