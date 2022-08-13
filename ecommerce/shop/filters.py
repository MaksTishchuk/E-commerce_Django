import django_filters

from .models import Product


class ProductsFilter(django_filters.FilterSet):
    """ Django-filter for products """

    selling_price__gte = django_filters.NumberFilter(field_name='selling_price', lookup_expr='gte')
    selling_price__lte = django_filters.NumberFilter(field_name='selling_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = {
            'title': ['icontains', ],
            'description': ['icontains', ],
        }
