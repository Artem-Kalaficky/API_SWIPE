from django_filters import rest_framework as filters

from users.models import Apartment


class ApartmentFilter(filters.FilterSet):
    house = filters.NumberFilter(field_name="ad__house", required=True)
    min_price = filters.NumberFilter(field_name="ad__price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="ad__price", lookup_expr='lte')
    min_price_for_m2 = filters.NumberFilter(field_name="ad__price_for_m2", lookup_expr='gte')
    max_price_for_m2 = filters.NumberFilter(field_name="ad__price_for_m2", lookup_expr='lte')
    min_area = filters.NumberFilter(field_name="ad__total_area", lookup_expr='gte')
    max_area = filters.NumberFilter(field_name="ad__total_area", lookup_expr='lte')

    class Meta:
        model = Apartment
        fields = ['building', 'section', 'ad__condition']
        