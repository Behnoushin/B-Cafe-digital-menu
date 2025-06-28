# -------------------  DRF imports   ------------------------
from rest_framework import generics
# -------------------   Apps imports ------------------------
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .permissions import IsAdminOnly, IsAdminOrReadOnly
from utility.views import BaseAPIView


##################################################################################
#                             Category Views                                     #
##################################################################################

class CategoryList(BaseAPIView, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        "Returns a list of all categories."
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        "Only admins can create new categories."
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