from drf_psq import Rule, PsqMixin
from rest_framework import viewsets, permissions, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from users.models import Notary
from users.serializers import NotarySerializer


# region Notaries
class NotaryViewSet(PsqMixin, mixins.CreateModelMixin,
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
