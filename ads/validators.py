from rest_framework import serializers


def validate_ad(validated_data):
    if validated_data.get('purpose') != 'cottage' and not validated_data.get('house', False):
        raise serializers.ValidationError(
            {'house_error': 'Поле ЖК для квартиры или новостроя обязательно к заполнению.'},
        )
    if validated_data.get('house', False) and validated_data.get('purpose') == 'cottage':
        raise serializers.ValidationError(
            {'purpose_error': 'Объявление с назначением "Частный сектор" не может сождержать поле с выбранным ЖК.'}
        )
    if validated_data.get('total_area', False) and validated_data.get('kitchen_area', False) \
            and validated_data.get('total_area', False) < validated_data.get('kitchen_area', False):
        raise serializers.ValidationError(
            {'area_error': 'Площадь кухни не может быть больше общей площади.'}
        )
    
    