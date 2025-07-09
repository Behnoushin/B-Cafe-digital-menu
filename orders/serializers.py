# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import Order, OrderItem
from menu.serializers import MenuItemSerializer
from menu.models import MenuItem
from utility.serializers import BaseSerializer
##################################################################################
#                          OrderItem serializers                                 #
##################################################################################

class OrderItemSerializer(BaseSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source='menu_item',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'final_price']

##################################################################################
#                            Order serializers                                   #
##################################################################################

class OrderSerializer(BaseSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    table_number = serializers.IntegerField(source='table.number', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'table', 'table_number', 'status', 'items', 'total_price', 'created_at', 'note']

    def get_total_price(self, obj):
        return obj.total_price()

    def validate(self, data):
        items_data = data.get('items', [])
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            if menu_item.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for {menu_item.name}.")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            # Decrease menu item stock
            menu_item = item_data['menu_item']
            menu_item.stock -= item_data['quantity']
            menu_item.save()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance.status = validated_data.get('status', instance.status)
        instance.table = validated_data.get('table', instance.table)
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        if items_data:
            # Restore stock for previous items
            for old_item in instance.items.all():
                menu_item = old_item.menu_item
                menu_item.stock += old_item.quantity
                menu_item.save()
            # Delete old items
            instance.items.all().delete()
            # Add new items
            for item_data in items_data:
                if item_data['menu_item'].stock < item_data['quantity']:
                    raise serializers.ValidationError(f"Not enough stock for {item_data['menu_item'].name}.")
                OrderItem.objects.create(order=instance, **item_data)
                menu_item = item_data['menu_item']
                menu_item.stock -= item_data['quantity']
                menu_item.save()
        return instance
