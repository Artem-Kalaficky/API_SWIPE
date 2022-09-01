from allauth.account.models import EmailAddress
from drf_psq import Rule, PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import Notary, UserProfile
from users.serializers import (
    NotarySerializer, UserProfileSerializer, UserSwitchNoticesSerializer, UserContactsSerializer,
    UserAgentContactsSerializer, UserManageNoticeSerializer
)


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
    queryset = Notary.objects.all()
    serializer_class = NotarySerializer
    parser_classes = (MultiPartParser,)

    psq_rules = {
        ('create', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser]),
        ]
    }
# endregion Notaries


# region User Profile
class UserViewSet(PsqMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = UserProfile.objects.filter(is_staff=False, is_developer=False)
    serializer_class = UserProfileSerializer
    permission_classes = [IsSelf]

    @action(detail=False, methods=['put'], serializer_class=UserContactsSerializer)
    def change_my_contacts(self, request, pk=None):
        user = self.request.user
        email = user.email
        serializer = UserContactsSerializer(data=request.data)
        if serializer.is_valid():
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.telephone = serializer.validated_data['telephone']
            user.email = serializer.validated_data['email']
            if email != user.email:
                EmailAddress.objects.get(user=user).delete()
                EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
            user.save()
            return Response({'status': 'contacts changed successfully'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(description='Change contacts for personal agent', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=UserAgentContactsSerializer)
    def change_agent_contacts(self, request):
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
