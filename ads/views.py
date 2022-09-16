import base64

from django.core.files.base import ContentFile
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ads.filters import FeedFilter
from ads.models import Promotion
from ads.permissions import IsMyAd, IsMyPromotion
from ads.serializers import (
    AdSerializer, PromotionSerializers, UpdatePromotionSerializers, AdUpdateSerializers, FeedAdSerializer,
    FeedHouseSerializer, FeedAdComplaintSerializer, FavoritesAddSerializer, FavoritesRemoveSerializer
)
from houses.serializers import HouseSerializer
from users.models import Ad, House, Complaint, UserProfile


# region Ad and Promotion
class AdViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated & IsMyAd]
    parser_classes = [JSONParser]

    def get_queryset(self):
        queryset = Ad.objects.filter(user=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.favorites.all())
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.data.get('photos', False):
            for p_dict in request.data.get('photos'):
                p_dict['photo'] = ContentFile(base64.b64decode(p_dict['photo']), name='house.jpg')
        return super().create(request, *args, **kwargs)

    @extend_schema(description='Update Ad', methods=['put'])
    @action(detail=True, methods=['put'], serializer_class=AdUpdateSerializers)
    def update_ad(self, request, pk=None):
        if request.data.get('photos', False):
            for p_dict in request.data.get('photos'):
                p_dict['photo'] = ContentFile(base64.b64decode(p_dict['photo']), name='house.jpg')
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['promotions-for-ads'])
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
# endregion Ad and Promotion


# region Feed
class FeedListApiView(ListAPIView):
    queryset = Ad.objects.filter(is_disabled=False)
    serializer_class = FeedAdSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        house_serializer = FeedHouseSerializer(House.objects.all(), many=True)
        return Response(serializer.data + house_serializer.data)


class HouseCardRetrieveApiView(RetrieveAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class AdCardRetrieveApiView(RetrieveAPIView):
    queryset = Ad.objects.filter(is_disabled=False)
    serializer_class = FeedAdSerializer


class AdComplaintCreateApiView(CreateAPIView):
    queryset = Complaint.objects.all()
    serializer_class = FeedAdComplaintSerializer
# endregion Feed


# region Favorites
class FavoritesAdListAPIView(ListAPIView):
    serializer_class = FeedAdSerializer

    def get_queryset(self):
        queryset = self.request.user.ads.filter(is_disabled=False)
        return queryset


class FavoritesHouseListAPIView(ListAPIView):
    serializer_class = FeedHouseSerializer

    def get_queryset(self):
        queryset = self.request.user.houses.all()
        return queryset


class FavoritesAddApiView(GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = FavoritesAddSerializer

    @extend_schema(description='Add Ad or House to User Favorites', methods=['put'])
    @action(detail=False, methods=['put'])
    def add(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoritesDeleteApiView(GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = FavoritesRemoveSerializer

    @extend_schema(description='Remove Ad or House from User Favorites', methods=['put'])
    @action(detail=False, methods=['put'])
    def remove(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
# endregion Favorites
