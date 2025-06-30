import django_filters
from .models import MenuItem

class MenuItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    status = django_filters.CharFilter(field_name="status", lookup_expr='exact')

    class Meta:
        model = MenuItem
        fields = ['category', 'status', 'min_price', 'max_price']