from allauth.account.models import EmailAddress
from django_filters.rest_framework import DjangoFilterBackend
from drf_psq import Rule, PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import Notary, UserProfile
from users.serializers import (
    NotarySerializer, UserProfileSerializer, UserSwitchNoticesSerializer, UserAgentContactsSerializer,
    UserManageNoticeSerializer, UserSubscriptionSerializer, UserSubscriptionRenewalSerializer, UserListSerializer
)
from users.services.subscription_renewal import renew_subscription


# region my Permissions
class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj
# endregion my Permissions


# region Notaries
class NotaryViewSet(PsqMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = NotarySerializer
    parser_classes = (MultiPartParser,)

    psq_rules = {
        ('create', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser]),
        ]
    }
# endregion Notaries


# region User Profile
class UserViewSet(GenericViewSet):
    queryset = UserProfile.objects.filter(is_staff=False, is_developer=False)
    serializer_class = UserProfileSerializer

    @extend_schema(description='Get personal data', methods=['get'])
    @action(detail=False)
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(description='Change personal contacts', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserProfileSerializer)
    def change_my_contacts(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Change contacts for personal agent', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserAgentContactsSerializer)
    def change_agent_contacts(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Subscription renewal', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserSubscriptionRenewalSerializer)
    def renew_subscription(self, request):
        renew_subscription(request.user)
        return Response({'status': 'Подписка успешно продлена!'})

    @extend_schema(description='Change status for subscription auto-renewal', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserSubscriptionSerializer)
    def change_auto_renewal_status(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Receiving notifications', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserManageNoticeSerializer)
    def change_recipient_for_notices(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Switch massages and calls to agent', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserSwitchNoticesSerializer)
    def switch_calls_to_agent(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
# endregion User Profile


# region Moderation
class UserListViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['in_blacklist']

    def get_queryset(self):
        queryset = UserProfile.objects.filter(is_staff=False, is_developer=False)
        return queryset
# endregion Moderation
