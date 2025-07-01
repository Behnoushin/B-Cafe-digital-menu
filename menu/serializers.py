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
    
    final_price = serializers.SerializerMethodField(read_only=True)
    preparation_time = serializers.DurationField(required=False, allow_null=True)
    
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'discount_percent',
            'final_price',
            'stock',
            'status',
            'is_special',
            'preparation_time',
            'category',
            'category_id',
        ]
        read_only_fields = ['status', 'final_price']

    def get_final_price(self, obj):
        return obj.final_price