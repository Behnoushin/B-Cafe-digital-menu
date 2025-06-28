# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from utility.serializers import BaseSerializer
from .models import Category, MenuItem

##################################################################################
#                      CategorySerializer serializers                            #
##################################################################################

class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
##################################################################################
#                      MenuItemSerializer serializers                            #
##################################################################################        
        
class MenuItemSerializer(BaseSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id']