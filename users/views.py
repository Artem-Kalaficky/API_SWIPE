from rest_framework import viewsets, permissions

from users.models import Notary
from users.serializers import NotarySerializer


class NotaryViewSet(viewsets.ModelViewSet):
    """
    Notaries
    """
    queryset = Notary.objects.all()
    serializer_class = NotarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
