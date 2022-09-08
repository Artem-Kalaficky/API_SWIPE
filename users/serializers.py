from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from users.models import Notary, UserProfile, Message, Filter, Photo, Ad


# region User Login and Registration
class MyLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True, allow_blank=True)


class MyRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }
# endregion User Login and Registration


# region Notary
class NotarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notary
        fields = ['id', 'first_name', 'last_name', 'telephone', 'email', 'avatar']
# endregion Notary


# region User Profile
class UserProfileSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if validated_data.get('email') != instance.email:
            EmailAddress.objects.filter(user=instance).update(
                email=validated_data.get('email')
            )
        return super().update(instance, validated_data)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'first_name', 'last_name', 'telephone', 'email', 'agent_first_name', 'agent_last_name',
            'agent_telephone', 'agent_email', 'to_me', 'to_me_and_agent', 'to_agent', 'is_notices_disabled',
            'is_switch_to_agent', 'is_subscribed', 'is_auto_renewal', 'subscription_end_date'
        )
        read_only_fields = (
            'agent_first_name', 'agent_last_name', 'agent_telephone', 'agent_email', 'to_me', 'to_me_and_agent',
            'to_agent', 'is_notices_disabled', 'is_switch_to_agent', 'is_subscribed', 'is_auto_renewal',
            'subscription_end_date'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class UserAgentContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['agent_first_name', 'agent_last_name', 'agent_telephone', 'agent_email']


class UserSubscriptionRenewalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['subscription_end_date']
        read_only_fields = ('subscription_end_date',)


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['is_auto_renewal']


class UserManageNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['to_me', 'to_me_and_agent', 'to_agent', 'is_notices_disabled']


class UserSwitchNoticesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['is_switch_to_agent']
# endregion User Profile


# region Chats
class MessageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = Message.objects.create(
            **validated_data, sender=self.context.get('request').user
        )
        return instance

    class Meta:
        model = Message
        fields = ('sender', 'recipient', 'message', 'image', 'file', 'date')
        read_only_fields = ('sender', 'date')
# endregion Chats


# region Filters
class MyFilterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if len(Filter.objects.filter(user=self.context.get('request').user)) >= 4:
            raise serializers.ValidationError(
                'У пользователя не может быть более 4-х сохранённых фильтров.'
            )
        else:
            instance = Filter.objects.create(
                **validated_data, user=self.context.get('request').user
            )
        return instance

    class Meta:
        model = Filter
        fields = (
            'id', 'user', 'type', 'status_of_house', 'number_of_rooms', 'price_from', 'price_up_to', 'area_from',
            'area_up_to', 'purpose', 'purchase_term', 'condition', 'is_save'
        )
        read_only_fields = ('id', 'user')

# endregion MyFilters


# region Moderation
class ModerationUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'telephone', 'email', 'in_blacklist')


class ModerationAdSerializer(serializers.ModelSerializer):
    photos = serializers.PrimaryKeyRelatedField(many=True, queryset=Photo.objects.all())

    class Meta:
        model = Ad
        fields = ('price', 'address', 'date_created', 'number_of_rooms', 'total_area', 'photos')
# endregion Moderation
