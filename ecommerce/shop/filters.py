import django_filters

from .models import Product


class ProductsFilter(django_filters.FilterSet):
    """ Django-filter for products """

    CHOICES_FIlTER = (
        ("", 'All'),
        ("in_stock", 'In Stock'),
        ("out_of_stock", 'Out of Stock'),
    )

    selling_price__gte = django_filters.NumberFilter(field_name='selling_price', lookup_expr='gte')
    selling_price__lte = django_filters.NumberFilter(field_name='selling_price', lookup_expr='lte')
    filter = django_filters.ChoiceFilter(
        label='Filter by',
        choices=CHOICES_FIlTER,
        method='filter_by_stock'
    )

    class Meta:
        model = Product
        fields = {
            'title': ['icontains', ],
            'description': ['icontains', ],
        }

    def filter_by_stock(self, queryset, name, value):
        print(name)
        if value == "in_stock":
            return queryset.filter(quantity__gt=0)
        elif value == "out_of_stock":
            return queryset.filter(quantity__lt=1)
        else:
            return queryset
