from allauth.account.models import EmailAddress
from rest_framework import serializers

from users.models import UserProfile, House


# region Developer Profile
class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('name', 'address')


class DeveloperProfileSerializer(serializers.ModelSerializer):
    my_house = HouseSerializer(read_only=True)

    def update(self, instance, validated_data):
        if validated_data.get('email') != instance.email:
            EmailAddress.objects.filter(user=instance).update(
                email=validated_data.get('email')
            )
        return super().update(instance, validated_data)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'telephone', 'email', 'avatar', 'my_house')
# endregion Developer Profile
