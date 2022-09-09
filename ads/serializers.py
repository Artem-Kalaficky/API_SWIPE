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
            'is_incorrect_description', 'date_created'
        )
        read_only_fields = (
            'is_incorrect_price', 'is_incorrect_photo', 'is_incorrect_description', 'date_created'
        )

    def create(self, validated_data):
        instance = Ad.objects.create(
            **validated_data, user=self.context.get('request').user
        )
        validate_ad(validated_data)
        return instance

    def update(self, instance, validated_data):
        validate_ad(validated_data)
        return super().update(instance, validated_data)


class PromotionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'ad', 'is_gift', 'is_bargaining', 'is_by_the_sea', 'is_sleeping_area', 'is_nice_price', 'is_for_big_family',
            'is_family_home', 'is_private_parking', 'color', 'type_of_promotion', 'end_date'
        )
        read_only_fields = ('end_date',)


class UpdatePromotionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'is_gift', 'is_bargaining', 'is_by_the_sea', 'is_sleeping_area', 'is_nice_price', 'is_for_big_family',
            'is_family_home', 'is_private_parking', 'color', 'type_of_promotion'
        )
# endregion Ad
