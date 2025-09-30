# -----------------  Django imports   ------------------------
from django.utils import timezone
# -------------------  DRF imports   ------------------------
from rest_framework import generics, filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# -------------------   Apps imports ------------------------
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .permissions import IsAdminOrReadOnly
from .filters import MenuItemFilter, MenuItemPrepTimeFilter
from .throttles import MenuItemListThrottle
from utility.views import BaseAPIView

##################################################################################
#                             Category Views                                     #
##################################################################################

class CategoryList(BaseAPIView, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        """
        Returns a list of all categories.
        """
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Only admins can create new categories.
        """
        return self.create(request, *args, **kwargs)


class CategoryDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        """
        Get a category with an ID.
        """
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
        Edit category (admin only).
        """
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """
        Partially edit a category (admin only).
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete category (admin only).
        """
        return self.destroy(request, *args, **kwargs)
    
    
##################################################################################
#                             MenuItem Views                                     #
##################################################################################

class MenuItemList(BaseAPIView, generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MenuItemFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'sold_count', 'created_at']
    ordering = ['-created_at']
    throttle_classes = [MenuItemListThrottle]
    
    def get(self, request, *args, **kwargs):
        """
        Returns a list of all menu items.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates a new menu item (admin only).
        """
        return self.create(request, *args, **kwargs)
    
    
class MenuItemDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        """
        Get a menu item by ID.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Edit menu item (admin only).
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Minor menu item editing (admin only).
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete menu item (admin only).
        """
        return self.destroy(request, *args, **kwargs)
    
##################################################################################
#                             SpecialOffer Views                                 #
##################################################################################

class SpecialOfferList(BaseAPIView, generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        now = timezone.now()
        return MenuItem.objects.filter(
            discount_percent__gt=0,
            discount_start__lte=now,
            discount_end__gte=now
        )

    def get(self, request, *args, **kwargs):
        """
        Return a list of all currently active special offer items.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new menu item with a special offer (admin only).
        """
        return self.create(request, *args, **kwargs)


class SpecialOfferDetail(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        now = timezone.now()
        return MenuItem.objects.filter(
            discount_percent__gt=0,
            discount_start__lte=now,
            discount_end__gte=now
        )

    def get(self, request, *args, **kwargs):
        """
        Retrieve details of a specific special offer item.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Fully update a special offer item (admin only).
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Partially update a special offer item (admin only).
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete a special offer item (admin only).
        """
        return self.destroy(request, *args, **kwargs)

##################################################################################
#                         TopSellingMenuItems Views                              #
##################################################################################

class TopSellingMenuItems(BaseAPIView, generics.ListAPIView):
    """
    API endpoint that returns the top 10 best-selling menu items.
    Accessible by all users (read-only), admins can modify items via other endpoints.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['sold_count']
    ordering = ['-sold_count']
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        # Order by sold_count descending and return top 10
        return MenuItem.objects.order_by('-sold_count')[:10]

##################################################################################
#                           RecentMenuItems Views                                #
##################################################################################

class RecentMenuItems(BaseAPIView, generics.ListAPIView):
    """
    API endpoint that returns the 10 most recently added menu items.
    Useful for showing new arrivals on the menu.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        # Order by creation date descending
        return MenuItem.objects.order_by('-created_at')[:10]
    
##################################################################################
#                         MenuItemsByPrepTime Views                              #
##################################################################################

class MenuItemsByPrepTime(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to filter menu items based on preparation time.
    Users can optionally provide a maximum preparation time to filter items.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = MenuItemPrepTimeFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        # Exclude items with null preparation time
        return MenuItem.objects.exclude(preparation_time__isnull=True)

##################################################################################
#                         ActiveMenuItems Views                                  #
##################################################################################

class ActiveMenuItems(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all menu items that are currently available (in stock).
    Useful for users to see items that can be ordered.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        return MenuItem.objects.filter(status='available')

##################################################################################
#                         OutOfStockMenuItems Views                              #
##################################################################################

class OutOfStockMenuItems(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to list all menu items that are out of stock.
    Mainly for admins to monitor inventory status.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [MenuItemListThrottle]

    def get_queryset(self):
        return MenuItem.objects.filter(status='out_of_stock')

##################################################################################
#                         MenuItemsByCategory Views                              #
##################################################################################

class MenuItemsByCategory(BaseAPIView, generics.ListAPIView):
    """
    API endpoint to retrieve menu items filtered by category ID.
    Allows users to view items belonging to a specific category.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return MenuItem.objects.filter(category_id=category_id)