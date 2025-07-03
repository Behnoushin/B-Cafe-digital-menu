import django_filters
from django.utils import timezone
from .models import MenuItem

class MenuItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    status = django_filters.CharFilter(field_name="status", lookup_expr='exact')
    is_discount_active = django_filters.BooleanFilter(method='filter_discount_active')

    def filter_discount_active(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(
                discount_percent__gt=0,
                discount_start__lte=now,
                discount_end__gte=now
            )
        return queryset.exclude(
            discount_percent__gt=0,
            discount_start__lte=now,
            discount_end__gte=now
        )

    class Meta:
        model = MenuItem
        fields = ['category', 'status', 'min_price', 'max_price']