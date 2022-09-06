from drf_psq import Rule, PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from houses.serializers import DeveloperProfileSerializer
from users.models import Notary, UserProfile


# region my Permissions

# endregion my Permissions


# region Developer Profile
class DeveloperProfileViewSet(mixins.UpdateModelMixin,
                              GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = DeveloperProfileSerializer
    parser_classes = (MultiPartParser,)

    @extend_schema(description='Get personal data', methods=['get'])
    @action(detail=False)
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
# endregion Developer Profile
