import django_filters
from django.utils import timezone
from .models import MenuItem
from django_filters.rest_framework import FilterSet, NumberFilter


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
        
        

class MenuItemPrepTimeFilter(FilterSet):
    max_minutes = NumberFilter(field_name='preparation_time', method='filter_max_time')

    def filter_max_time(self, queryset, name, value):
        from datetime import timedelta
        max_duration = timedelta(minutes=value)
        return queryset.filter(preparation_time__lte=max_duration)

    class Meta:
        model = MenuItem
        fields = ['max_minutes']
