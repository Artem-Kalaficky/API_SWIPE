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
        ('create', 'update', 'destroy'): [
            Rule([IsAdminUser]),
        ]
    }

    @extend_schema(description='Permissions: IsAdminUser | IsAuthenticated.\nGet list of notaries.')
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(description='Permissions: IsAdminUser.\nGet notary by id.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)

    @extend_schema(description='Permissions: IsAdminUser.\nCreate new notary.')
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @extend_schema(description='Permissions: IsAdminUser.\nUpdate notary by id.')
    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    @extend_schema(description='Permissions: IsAdminUser.\nDelete notary by id.')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, args, kwargs)
# endregion Notaries


# region User Profile
class UserViewSet(GenericViewSet):
    queryset = UserProfile.objects.filter(is_staff=False, is_developer=False)
    serializer_class = UserProfileSerializer
    permission_classes = [IsMyProfile]
    parser_classes = (MultiPartParser,)

    @extend_schema(methods=['get'], description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer).\nGet all information for current user')
    @action(detail=False)
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(methods=['put'], description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer).\nUpdate personal information')
    @action(detail=False, methods=['put'], serializer_class=UserProfileSerializer)
    def change_my_contacts(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer).\nUpdate information for agent')
    @action(detail=False, methods=['put'], serializer_class=UserAgentContactsSerializer)
    def change_agent_contacts(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer).\nRenew subscription for current user')
    @action(detail=False, methods=['put'], serializer_class=UserSubscriptionRenewalSerializer)
    def renew_subscription(self, request):
        renew_subscription(request.user)
        return Response({'status': 'Подписка успешно продлена!'})

    @extend_schema(methods=['put'], description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer).\nOff or on autorenewal status for subscription')
    @action(detail=False, methods=['put'], serializer_class=UserSubscriptionSerializer)
    def change_auto_renewal_status(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer).\nChange recipient for getting notices')
    @action(detail=False, methods=['put'], serializer_class=UserManageNoticeSerializer)
    def change_recipient_for_notices(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsAuthenticated & IsMyProfile(only user, not admin or developer).\nSwitch getting calls and messages to agent')
    @action(detail=False, methods=['put'], serializer_class=UserSwitchNoticesSerializer)
    def switch_calls_to_agent(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
# endregion User Profile


# region Chats
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
        ], description='Permissions: IsAuthenticated.\nGet all messages. Get all messages of chat between current user and companion by id'
    )
    def list(self, request):
        return super().list(request)

    @extend_schema(description='Permissions: IsAuthenticated.\nSend message to user by id')
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)
# endregion Chats


# region Filters
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

    @extend_schema(description='Permissions: IsAuthenticated & IsMyFilter.\nGet all filter for user')
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(description='Permissions: IsAuthenticated & IsMyFilter.\nGet filter by id')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)

    @extend_schema(description='Permissions: IsAuthenticated & IsMyFilter.\nCreate new filter. Must be unique type for new filter. There are 4 filters in total')
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @extend_schema(description='Permissions: IsAuthenticated & IsMyFilter.\nUpdate filter by id')
    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)
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

    @extend_schema(description='Permissions: IsAdminUser.\nGet all users.')
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(description='Permissions: IsAdminUser.\nAdd or remove user from blacklist.')
    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)


@extend_schema(description='Permissions: IsAdminUser')
class ModerationAdViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    queryset = Ad.objects.filter(is_disabled=False)
    http_method_names = ["put", "get"]
    serializer_class = ModerationAdSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(description='Permissions: IsAdminUser.\nGet all ads for moderation.')
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(description='Permissions: IsAdminUser.\nGet ad by id for moderation.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)

    @extend_schema(description='Permissions: IsAdminUser.\nUpdate moderation action for ad by id.')
    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)
# endregion Moderation
