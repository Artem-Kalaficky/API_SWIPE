from drf_psq import Rule, PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from houses.models import Document, News
from houses.serializers import DeveloperProfileSerializer, HouseInformationSerializer, HouseInfrastructureSerializer, \
    HouseAgreementSerializer, HouseSalesDepartmentSerializer, HouseDocumentSerializer, HouseNewsSerializer, \
    HouseAdvantageSerializer, HouseImageSerializers, HouseSerializer
from users.models import Notary, UserProfile, House


# region my Permissions
class IsDeveloperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_developer


class IsMyContent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.house == obj.house
# endregion my Permissions


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


class HouseDocumentViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    queryset = Document.objects.all()
    serializer_class = HouseDocumentSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsDeveloperUser & IsMyContent]


class HouseNewsViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = News.objects.all()
    serializer_class = HouseNewsSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsDeveloperUser & IsMyContent]
# endregion Developer Profile


# region House card
class HouseCardApiView(RetrieveAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
# endregion House card
