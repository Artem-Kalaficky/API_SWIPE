from django_filters import rest_framework as filters

from users.models import Ad


class FeedFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_area = filters.NumberFilter(field_name="total_area", lookup_expr='gte')
    max_area = filters.NumberFilter(field_name="total_area", lookup_expr='lte')

    class Meta:
        model = Ad
        fields = ['purpose', 'number_of_rooms', 'condition', 'payment_option']