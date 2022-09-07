from allauth.account.models import EmailAddress
from rest_framework import serializers

from houses.models import Advantage, News, Document, Image
from users.models import UserProfile, House


# region Developer Profile
class AdvantagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantage
        fields = ('advantage1', 'advantage2')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('name', 'description')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('document',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('photo',)


class HouseSerializer(serializers.ModelSerializer):
    advantage = AdvantagesSerializer(read_only=True)
    news = NewsSerializer(many=True, read_only=True, allow_null=True)
    documents = DocumentSerializer(many=True, read_only=True, allow_null=True)
    images = ImageSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = House
        fields = (
            'name', 'address', 'min_price', 'price_for_m2', 'area_from', 'area_up_to', 'description', 'house_status',
            'house_type', 'house_class', 'building_technique', 'territory', 'distance_to_the_sea', 'communal_payments',
            'ceiling_height', 'gas', 'heating', 'type_of_sewerage', 'water_supply', 'agreements', 'payment_option',
            'house_purpose', 'amount_in_contract', 'department_first_name', 'department_last_name',
            'department_telephone', 'department_email', 'advantage', 'news', 'documents', 'images'
        )


class DeveloperProfileSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)

    def update(self, instance, validated_data):
        if validated_data.get('email') != instance.email:
            EmailAddress.objects.filter(user=instance).update(
                email=validated_data.get('email')
            )
        return super().update(instance, validated_data)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'telephone', 'email', 'avatar', 'house')
# endregion Developer Profile


# region update House
class HouseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('name', 'address', 'min_price', 'price_for_m2', 'area_from', 'area_up_to', 'description')


class HouseInfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = (
            'house_status', 'house_type', 'house_class', 'building_technique', 'territory', 'distance_to_the_sea',
            'communal_payments', 'ceiling_height', 'gas', 'heating', 'type_of_sewerage', 'water_supply'
        )


class HouseAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('agreements', 'payment_option', 'house_purpose', 'amount_in_contract')


class HouseSalesDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('department_first_name', 'department_last_name', 'department_telephone', 'department_email')


class HouseAdvantageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantage
        fields = ('advantage1', 'advantage2')
# endregion update House


# region Documents and News
class HouseDocumentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = Document.objects.create(
            **validated_data, house=self.context.get('request').user.house
        )
        return instance

    class Meta:
        model = Document
        fields = ('id', 'document')


class HouseNewsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = News.objects.create(
            **validated_data, house=self.context.get('request').user.house
        )
        return instance

    class Meta:
        model = News
        fields = ('id', 'name', 'description')
# endregion Documents and News
