from drf_spectacular.utils import extend_schema
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ads.models import Promotion
from ads.serializers import AdSerializer, PromotionSerializers, UpdatePromotionSerializers
from users.models import Ad


# region my Permissions
class IsMyAd(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.ad.all()


class IsMyPromotion(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.ad in request.user.ad.all()
# endregion my Permissions


# region Ad
class AdViewSet(ModelViewSet):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated & IsMyAd]

    def get_queryset(self):
        queryset = Ad.objects.filter(user=self.request.user)
        return queryset


class PromotionViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializers
    permission_classes = [IsAuthenticated & IsMyPromotion]

    @extend_schema(description='Update promotion for Ad', methods=['put'])
    @action(detail=True, methods=['put'], serializer_class=UpdatePromotionSerializers)
    def update_promotion(self, request, pk=None):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
# endregion Ad
