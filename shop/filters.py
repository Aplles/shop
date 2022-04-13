import django_filters

from .models import Product


class MyFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(MyFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = {'price': ['gt', 'lt']}
        order_by = ['-id']
