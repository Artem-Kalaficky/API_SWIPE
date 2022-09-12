from rest_framework import serializers


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
