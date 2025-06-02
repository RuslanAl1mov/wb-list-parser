from django_filters import rest_framework as filters
from .models import Product


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class ProductFilter(filters.FilterSet):
    category = NumberInFilter(field_name="category", lookup_expr="in")

    class Meta:
        model = Product
        fields = ["category"]