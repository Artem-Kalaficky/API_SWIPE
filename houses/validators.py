from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from users.models import Apartment


def validate_apartment(house, apartment):
    if apartment.get('building') > house.building:
        raise serializers.ValidationError(
            {'building_error': f'Корпуса {apartment.get("building")} не существует. Корпусов в ЖК {house.building}'}
        )
    if apartment.get('section') > house.section:
        raise serializers.ValidationError(
            {'section_error': f'Секции {apartment.get("section")} не существует. Секций в ЖК {house.section}'}
        )
    if apartment.get('floor') > house.floor:
        raise serializers.ValidationError(
            {'floor_error': f'Этажа {apartment.get("floor")} не существует. Этажей в ЖК {house.floor}'}
        )
    if apartment.get('riser') > house.riser:
        raise serializers.ValidationError(
            {'riser_error': f'Стояка {apartment.get("riser")} не существует. Стояков в ЖК {house.riser}'}
        )

    try:
        Apartment.objects.get(
            building=apartment.get('building'),
            section=apartment.get('section'),
            floor=apartment.get('floor'),
            riser=apartment.get('riser'),
            number=apartment.get('number'),
            ad__house=house,
            is_reserved=True
        )
        raise serializers.ValidationError({'apartment_arror': 'Квартира с такими данными уже существует в этом доме.'})
    except ObjectDoesNotExist:
        pass

    try:
        Apartment.objects.get(
            number=apartment.get('number'),
            building=apartment.get('building'),
            ad__house=house,
            is_reserved=True
        )
        raise serializers.ValidationError({'number_error': 'Квартира с таким номером уже существует в этом корпусе.'})
    except ObjectDoesNotExist:
        pass

