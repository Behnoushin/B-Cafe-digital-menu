# -------------------  DRF imports   ------------------------
from rest_framework import serializers
# -------------------   Apps imports ------------------------
from .models import IngredientRequest, IngredientItem
from utility.serializers import BaseSerializer

##################################################################################
#                      IngredientItem serializers                                #
##################################################################################

class IngredientItemSerializer(BaseSerializer):
    class Meta:
        model = IngredientItem
        fields = '__all__'
        read_only_fields = ['is_approved', 'is_rejected', 'is_purchased', 'request']

##################################################################################
#                      IngredientRequest serializers                             #
##################################################################################

class IngredientRequestSerializer(BaseSerializer):
    items = IngredientItemSerializer(many=True, write_only=True)
    chef = serializers.StringRelatedField(read_only=True)
    items_detail = IngredientItemSerializer(source='items', many=True, read_only=True)

    class Meta:
        model = IngredientRequest
        fields = ['id', 'chef', 'note', 'items', 'items_detail', 'is_reviewed', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = IngredientRequest.objects.create(chef=self.context['request'].user, **validated_data)
        for item_data in items_data:
            IngredientItem.objects.create(request=request, **item_data)
        return request

    def update(self, instance, validated_data):
        # Only allows notes and items to be changed before admin approval
        if instance.is_reviewed:
            raise serializers.ValidationError("Cannot modify a reviewed request.")

        items_data = validated_data.pop('items', None)
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        if items_data is not None:
            # Delete previous items and create new items
            instance.items.all().delete()
            for item_data in items_data:
                IngredientItem.objects.create(request=instance, **item_data)

        return instance
