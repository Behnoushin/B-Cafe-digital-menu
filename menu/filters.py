import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import MenuItem


class MenuItemFilter(django_filters.FilterSet):
    """
    Filters menu items based on price, category, status, and discount activity.
    """
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Minimum Price"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Maximum Price"
    )
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains", label="Category (contains)"
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=[("available", "Available"), ("out_of_stock", "Out of Stock")],
        label="Item Status"
    )
    is_discount_active = django_filters.BooleanFilter(
        method="filter_discount_active",
        label="Active Discount"
    )

    def filter_discount_active(self, queryset, name, value):
        """
        Filters items based on whether they currently have an active discount.
        """
        now = timezone.now()
        condition = {
            "discount_percent__gt": 0,
            "discount_start__lte": now,
            "discount_end__gte": now
        }
        return queryset.filter(**condition) if value else queryset.exclude(**condition)

    class Meta:
        model = MenuItem
        fields = ["category", "status", "min_price", "max_price", "is_discount_active"]


class MenuItemPrepTimeFilter(django_filters.FilterSet):
    """
    Filters menu items by maximum preparation time in minutes.
    """
    max_minutes = django_filters.NumberFilter(
        method="filter_max_time",
        label="Max Preparation Time (minutes)"
    )

    def filter_max_time(self, queryset, name, value):
        """
        Returns items that can be prepared within the given time limit.
        """
        if value is not None:
            max_duration = timedelta(minutes=value)
            return queryset.filter(preparation_time__lte=max_duration)
        return queryset

    class Meta:
        model = MenuItem
        fields = ["max_minutes"]
