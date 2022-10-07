from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_psq import Rule, PsqMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from users.models import Notary, UserProfile, Message, Filter, Ad
from users.permissions import IsMyFilter, IsMyProfile

from users.serializers import (
    NotarySerializer, UserProfileSerializer, UserSwitchNoticesSerializer, UserAgentContactsSerializer,
    UserManageNoticeSerializer, UserSubscriptionSerializer, UserSubscriptionRenewalSerializer,
    ModerationUserListSerializer, ModerationAdSerializer, MessageSerializer, MyFilterSerializer
)
from users.services.subscription_renewal import renew_subscription


# region Notaries
@extend_schema(description='Permissions: (IsAuthenticated for GET list of notaries) & IsAdminUser)')
class NotaryViewSet(PsqMixin, ModelViewSet):
    queryset = Notary.objects.all()
    http_method_names = ["put", "post", "get", "delete"]
    serializer_class = NotarySerializer
    parser_classes = (MultiPartParser,)

    psq_rules = {
        ('create', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser]),
        ]
    }
# endregion Notaries


# region User Profile
@extend_schema(description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer)')
class UserViewSet(GenericViewSet):
    queryset = UserProfile.objects.filter(is_staff=False, is_developer=False)
    serializer_class = UserProfileSerializer
    permission_classes = [IsMyProfile]
    parser_classes = (MultiPartParser,)

    @extend_schema(methods=['get'])
    @action(detail=False)
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserProfileSerializer)
    def change_my_contacts(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserAgentContactsSerializer)
    def change_agent_contacts(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserSubscriptionRenewalSerializer)
    def renew_subscription(self, request):
        renew_subscription(request.user)
        return Response({'status': 'Подписка успешно продлена!'})

    @extend_schema(methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserSubscriptionSerializer)
    def change_auto_renewal_status(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserManageNoticeSerializer)
    def change_recipient_for_notices(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserSwitchNoticesSerializer)
    def switch_calls_to_agent(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
# endregion User Profile


# region Chats
@extend_schema(description='Permissions: IsAuthenticated')
class MessageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericViewSet):
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        queryset = Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ) if self.request.user.is_authenticated else Message.objects.all()
        recipient = self.request.query_params.get('recipient')
        if recipient:
            queryset = queryset.filter(
                Q(sender=recipient) | Q(recipient=recipient)
            )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(name='recipient', description='Filter by chats', required=False, type=int)
        ]
    )
    def list(self, request):
        return super().list(request)
# endregion Chats


# region Filters
@extend_schema(description='Permissions: IsAuthenticated & IsMyFilter')
class FilterViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    http_method_names = ["put", "post", "get"]
    serializer_class = MyFilterSerializer
    permission_classes = [IsAuthenticated & IsMyFilter]
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Filter.objects.filter(user=self.request.user)
        return queryset
# endregion MyFilters


# region Moderation
@extend_schema(description='Permissions: IsAdminUser')
class ModerationUserListApiView(mixins.ListModelMixin,
                                mixins.UpdateModelMixin,
                                GenericViewSet):
    queryset = UserProfile.objects.filter(is_staff=False, is_developer=False)
    http_method_names = ["put", "get"]
    serializer_class = ModerationUserListSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['in_blacklist']
    search_fields = ['first_name', 'last_name']


@extend_schema(description='Permissions: IsAdminUser')
class ModerationAdViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    queryset = Ad.objects.filter(is_disabled=False)
    http_method_names = ["put", "get"]
    serializer_class = ModerationAdSerializer
    permission_classes = [IsAdminUser]
# endregion Moderation
