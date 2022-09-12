from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DeveloperProfileViewSet, HouseDocumentViewSet, HouseNewsViewSet, HouseCardApiView, HouseAddRequestsViewSet,
    HouseCheckerboardViewSet
)

router = DefaultRouter()
router.register(r'developer-profile', DeveloperProfileViewSet, basename="developer-profile")
router.register(r'house/documents', HouseDocumentViewSet, basename="document")
router.register(r'house/news', HouseNewsViewSet, basename="news")
router.register(r'house/requests-to-add', HouseAddRequestsViewSet, basename="request")
router.register(r'house/checkerboard', HouseCheckerboardViewSet, basename="checkerboard")

urlpatterns = [
    path('', include(router.urls)),

    path('house-card/<int:pk>', HouseCardApiView.as_view())
]
