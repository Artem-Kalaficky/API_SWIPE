from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.core.exceptions import ValidationError
from rest_framework import serializers

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from users.models import Notary, UserProfile


class MyLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True, allow_blank=True)


class MyRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует.',
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except ValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


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


# region Moderation
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'telephone', 'email', 'in_blacklist')
# endregion Moderation
