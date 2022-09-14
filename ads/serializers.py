from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from ads.models import Promotion
from ads.services.encode_files import generate_base64
from ads.validators import validate_ad
from users.models import Ad, House, Complaint, UserProfile, Photo


# region Ad
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'photo', 'order')


class OrderPhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example 1',
            value={
                'address': 'Some Address 1',
                'house': 9,
                'foundation_document': 'property',
                'purpose': 'apartment',
                'number_of_rooms': 'one-room',
                'apartment_layout': 'studio',
                'condition': 'rough',
                'total_area': '80',
                'kitchen_area': '20',
                'balcony': 'yes',
                'heating_type': 'gas',
                'payment_option': 'mortgage',
                'agent_commission': '1000',
                'communication_method': 'email',
                'description': 'Some description for this interesting ad',
                'price': 4500000,
                "photos": [
                    {
                      "order": 1,
                      "photo": generate_base64()
                    },
                    {
                      "order": 2,
                      "photo": generate_base64()
                    },
                    {
                      "order": 3,
                      "photo": generate_base64()
                    },
                ],
            },
            request_only=True,
            response_only=False,
        ),
    ],
)
class AdSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)

    class Meta:
        model = Ad
        fields = (
            'id', 'address', 'house', 'foundation_document', 'purpose', 'number_of_rooms', 'apartment_layout',
            'condition', 'total_area', 'kitchen_area', 'balcony', 'heating_type', 'payment_option', 'agent_commission',
            'communication_method', 'description', 'price', 'photos', 'is_incorrect_price', 'is_incorrect_photo',
            'is_incorrect_description', 'date_created', 'promotion', 'is_disabled'
        )
        read_only_fields = (
            'is_incorrect_price', 'is_incorrect_photo', 'is_incorrect_description', 'date_created', 'promotion',
            'is_disabled'
        )
        extra_kwargs = {
            'purpose': {'required': True}
        }

    def validate(self, attrs):
        validate_ad(attrs)
        return attrs

    def create(self, validated_data):
        photos_data = validated_data.pop('photos')
        price_for_m2 = validated_data.get('price') / validated_data.get('total_area')
        instance = Ad.objects.create(
            **validated_data, user=self.context.get('request').user, price_for_m2=price_for_m2
        )
        if photos_data:
            for photo_data in photos_data:
                Photo.objects.create(ad=instance, photo=photo_data.get('photo'), order=photo_data.get('order'))
        return instance


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example 1',
            value={
                'address': 'Some Address 1',
                'foundation_document': 'property',
                'number_of_rooms': 'one-room',
                'apartment_layout': 'studio',
                'condition': 'rough',
                'total_area': '80',
                'kitchen_area': '20',
                'balcony': 'yes',
                'heating_type': 'gas',
                'payment_option': 'mortgage',
                'agent_commission': '1000',
                'communication_method': 'email',
                'description': 'Some description for this interesting ad',
                'price': 4500000,
                'photos_order': [
                    {
                        'id': 0,
                        'order': 0
                    }
                ],
                "photos": [
                    # {
                    #   "order": 1,
                    #   "photo": generate_base64()
                    # },
                    # {
                    #   "order": 2,
                    #   "photo": generate_base64()
                    # },
                    # {
                    #   "order": 3,
                    #   "photo": generate_base64()
                    # },
                ],
            },
            request_only=True,
            response_only=False,
        ),
    ],
)
class AdUpdateSerializers(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    order_photos = OrderPhotoSerializer(many=True)

    class Meta:
        model = Ad
        fields = (
            'id', 'address', 'foundation_document', 'number_of_rooms', 'apartment_layout', 'condition', 'total_area',
            'kitchen_area', 'balcony', 'heating_type', 'payment_option', 'agent_commission', 'communication_method',
            'description', 'price', 'order_photos', 'photos'
        )
        extra_kwargs = {
            'order_photos': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs.get('total_area', False) and attrs.get('kitchen_area', False) \
                and attrs.get('total_area', False) < attrs.get('kitchen_area', False):
            raise serializers.ValidationError(
                {'area_error': 'Площадь кухни не может быть больше общей площади.'}
            )
        return attrs

    def update(self, instance, validated_data):
        print(validated_data)
        instance.price_for_m2 = validated_data.get('price') / validated_data.get('total_area')
        instance.save()
        return instance
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


# region Feed
class FeedAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = (
            'id', 'address', 'house', 'foundation_document', 'purpose', 'number_of_rooms', 'apartment_layout',
            'condition', 'total_area', 'kitchen_area', 'balcony', 'heating_type', 'payment_option', 'price',
            'date_created'
        )


class FeedHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name', 'address', 'min_price', 'area_from')


class FeedAdComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('ad', 'text')

    def create(self, validated_data):
        if validated_data.get('ad') in self.context.get('request').user.ad.all():
            raise serializers.ValidationError({'ad_error': 'Вы не можете пожаловаться на своё объявление!'})
        instance = Complaint.objects.create(
            **validated_data, user=self.context.get('request').user
        )
        return instance
# endregion Feed


# region Favorites
class FavoritesAddSerializer(serializers.ModelSerializer):
    id_ad = serializers.IntegerField(required=False)
    id_house = serializers.IntegerField(required=False)

    class Meta:
        model = UserProfile
        fields = ('ads', 'houses', 'id_ad', 'id_house')
        read_only_fields = ('ads', 'houses')
        extra_kwargs = {
            'id_ad': {'write_only': True},
            'id_house': {'write_only': True}
        }

    def update(self, instance, validated_data):
        if validated_data.get('id_ad', False):
            try:
                ad = get_object_or_404(Ad, pk=validated_data.get('id_ad'))
                instance.ads.add(ad)
            except:
                raise serializers.ValidationError({'ad_error': 'Такого объявления не существует.'})
        if validated_data.get('id_house', False):
            try:
                house = get_object_or_404(House, pk=validated_data.get('id_house'))
                instance.houses.add(house)
            except:
                raise serializers.ValidationError({'house_error': 'Такого ЖК не существует.'})
        return super().update(instance, validated_data)


class FavoritesRemoveSerializer(FavoritesAddSerializer):
    def update(self, instance, validated_data):
        if validated_data.get('id_ad', False):
            try:
                ad = get_object_or_404(Ad, pk=validated_data.get('id_ad'))
                instance.ads.remove(ad)
            except:
                raise serializers.ValidationError({'ad_error': 'Такого объявления нет в избранном.'})
        if validated_data.get('id_house', False):
            try:
                house = get_object_or_404(House, pk=validated_data.get('id_house'))
                instance.houses.remove(house)
            except:
                raise serializers.ValidationError({'house_error': 'Такого ЖК нет в избранном.'})
        instance.save()
        return instance
# endregion Favorites
