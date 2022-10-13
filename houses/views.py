from drf_psq import PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
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
    HouseImageSerializers, HouseSerializer, ApartmentSerializer, DeveloperAvatarSerializer
)
from users.models import UserProfile, House, Apartment


# region Developer Profile
class DeveloperProfileViewSet(PsqMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = DeveloperProfileSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsDeveloperUser]

    @extend_schema(methods=['get'], description='Permissions: IsDeveloperUser.\nGet information of developer and his house')
    @action(detail=False)
    def my_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(methods=['put'], description='Permissions: IsDeveloperUser.\nUpdate avatar for developer')
    @action(detail=False, methods=['put'], serializer_class=DeveloperAvatarSerializer)
    def update_avatar(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsDeveloperUser.\nUpdate main information for house')
    @action(detail=False, methods=['put'], serializer_class=HouseInformationSerializer)
    def update_house_information(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsDeveloperUser.\nUpdate infrastructure for house')
    @action(detail=False, methods=['put'], serializer_class=HouseInfrastructureSerializer)
    def update_house_infrastructure(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsDeveloperUser.\nUpdate agreement for house')
    @action(detail=False, methods=['put'], serializer_class=HouseAgreementSerializer)
    def update_house_agreement(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsDeveloperUser.\nUpdate sales department for house')
    @action(detail=False, methods=['put'], serializer_class=HouseSalesDepartmentSerializer)
    def update_house_sales_department(self, request):
        serializer = self.serializer_class(request.user.house, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=['put'], description='Permissions: IsDeveloperUser.\nUpdate advantages for house')
    @action(detail=False, methods=['put'], serializer_class=HouseAdvantageSerializer)
    def update_house_advantages(self, request):
        serializer = self.serializer_class(request.user.house.advantage, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(description='Permissions: IsDeveloperUser.\nUpdate images for house. Add Image id in "delete_list" for deleting', methods=['put'])
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

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyContent.\nCreate new document for house')
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyContent.\nUpdate document by id for house')
    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyContent.\nDelete document by id for house')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, args, kwargs)


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

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyContent.\nCreate new news for house')
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyContent.\nUpdate news by id for house')
    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyContent.\nDelete news by id for house')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, args, kwargs)


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

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyRequest.\nGet all requests(apartment) for adding to checkerboard of current deleloper')
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(description='Permissions: IsDeveloperUser & IsMyRequest.\nAdd apartment by id to checkerboard of current deleloper')
    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)
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

    @extend_schema(description='Permissions: IsAuthenticated.\nGet all apartments in checkerboard of house')
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(description='Permissions: IsAuthenticated.\nGet apartment by id in checkerboard of house')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)
# endregion House Checkerboard

