from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ads.models import Promotion
from ads.validators import validate_ad
from users.models import Ad


# region Ad
class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = (
            'id', 'address', 'house', 'foundation_document', 'purpose', 'number_of_rooms', 'apartment_layout',
            'condition', 'total_area', 'kitchen_area', 'balcony', 'heating_type', 'payment_option', 'agent_commission',
            'communication_method', 'description', 'price', 'is_incorrect_price', 'is_incorrect_photo',
            'is_incorrect_description', 'date_created', 'promotion'
        )
        read_only_fields = (
            'is_incorrect_price', 'is_incorrect_photo', 'is_incorrect_description', 'date_created', 'promotion'
        )
        extra_kwargs = {
            'purpose': {'required': True}
        }

    def validate(self, attrs):
        validate_ad(attrs)
        return attrs

    def create(self, validated_data):
        price_for_m2 = validated_data.get('price') / validated_data.get('total_area')
        instance = Ad.objects.create(
            **validated_data, user=self.context.get('request').user, price_for_m2=price_for_m2
        )
        return instance


class AdUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = (
            'id', 'address', 'foundation_document', 'number_of_rooms', 'apartment_layout', 'condition', 'total_area',
            'kitchen_area', 'balcony', 'heating_type', 'payment_option', 'agent_commission', 'communication_method',
            'description', 'price'
        )

    def validate(self, attrs):
        if attrs.get('total_area', False) and attrs.get('kitchen_area', False) \
                and attrs.get('total_area', False) < attrs.get('kitchen_area', False):
            raise serializers.ValidationError(
                {'area_error': 'Площадь кухни не может быть больше общей площади.'}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.price_for_m2 = validated_data.get('price') / validated_data.get('total_area')
        instance.save()
        return super().update(instance, validated_data)

# endregion Ad


# region Promotion
class PromotionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'ad', 'is_gift', 'is_bargaining', 'is_by_the_sea', 'is_sleeping_area', 'is_nice_price', 'is_for_big_family',
            'is_family_home', 'is_private_parking', 'color', 'type_of_promotion', 'end_date'
        )
        read_only_fields = ('end_date',)

    def validate(self, attrs):
        if attrs.get('ad') not in self.context.get('request').user.ad.all():
            raise serializers.ValidationError(
                {'ad': f"Недопустимый первичный ключ '{attrs.get('ad').id}' - объект не существует."},
            )
        return attrs


class UpdatePromotionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'is_gift', 'is_bargaining', 'is_by_the_sea', 'is_sleeping_area', 'is_nice_price', 'is_for_big_family',
            'is_family_home', 'is_private_parking', 'color', 'type_of_promotion'
        )
# endregion Promotion
