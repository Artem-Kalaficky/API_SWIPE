from drf_psq import PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from houses.filters import ApartmentFilter
from houses.models import Document, News
from houses.permissions import IsDeveloperUser, IsMyContent, IsMyRequest
from houses.serializers import (
    DeveloperProfileSerializer, HouseInformationSerializer, HouseInfrastructureSerializer, HouseAgreementSerializer,
    HouseSalesDepartmentSerializer, HouseDocumentSerializer, HouseNewsSerializer, HouseAdvantageSerializer,
    HouseImageSerializers, HouseSerializer, ApartmentSerializer
)
from users.models import UserProfile, House, Apartment


# region Developer Profile
class DeveloperProfileViewSet(PsqMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = DeveloperProfileSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsDeveloperUser]

    @extend_schema(description='Get personal data', methods=['get'])
    @action(detail=False)
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(description='Update main information of House', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=HouseInformationSerializer)
    def update_house_information(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Update infrastructure information of House', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=HouseInfrastructureSerializer)
    def update_house_infrastructure(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Update the "registration and payment" section', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=HouseAgreementSerializer)
    def update_house_agreement(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Update information of sales department', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=HouseSalesDepartmentSerializer)
    def update_house_sales_department(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Update information of advantages', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=HouseAdvantageSerializer)
    def update_house_advantages(self, request):
        serializer = self.serializer_class(request.user.house.advantage, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Update images for house. Add Image id in "delete_list" for deleting', methods=['put'])
    @action(detail=False, methods=['put'], serializer_class=HouseImageSerializers)
    def update_house_images(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'Картинки дома успешно обновлены.'})


@extend_schema(tags=['house-documents'])
class HouseDocumentViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    queryset = Document.objects.all()
    http_method_names = ["put", "post", "delete"]
    serializer_class = HouseDocumentSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsDeveloperUser & IsMyContent]


@extend_schema(tags=['house-news'])
class HouseNewsViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = News.objects.all()
    http_method_names = ["put", "post", "delete"]
    serializer_class = HouseNewsSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsDeveloperUser & IsMyContent]


@extend_schema(tags=['house-add-requests'])
class HouseAddRequestsViewSet(mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              GenericViewSet):
    http_method_names = ["put", "get"]
    serializer_class = ApartmentSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsDeveloperUser & IsMyRequest]

    def get_queryset(self):
        queryset = Apartment.objects.filter(ad__house=self.request.user.house, is_reserved=False)
        return queryset
# endregion Developer Profile


# region House Checkerboard
@extend_schema(tags=['checkerboard'])
class HouseCheckerboardViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               GenericViewSet):
    queryset = Apartment.objects.filter(is_reserved=True)
    serializer_class = ApartmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApartmentFilter
# endregion House Checkerboard

