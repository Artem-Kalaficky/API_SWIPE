from rest_framework import serializers


def validate_filter(attrs):
    price_from = attrs.get('price_from', False)
    price_up_to = attrs.get('price_up_to', False)
    area_from = attrs.get('area_from', False)
    area_up_to = attrs.get('area_up_to', False)
    if price_from and price_up_to:
        if price_from > price_up_to:
            raise serializers.ValidationError({'price_error': '"Цена от" не может превышать "Цена до"'})
    if area_from and area_up_to:
        if area_from > area_up_to:
            raise serializers.ValidationError({'area_error': '"Площадь от" не может превышать "Площадь до"'})

