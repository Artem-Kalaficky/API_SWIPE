from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DeveloperProfileViewSet, HouseDocumentViewSet, HouseNewsViewSet


router = DefaultRouter()
router.register(r'developer-profile', DeveloperProfileViewSet, basename="developer-profile")
router.register(r'house/documents', HouseDocumentViewSet, basename="document")
router.register(r'house/news', HouseNewsViewSet, basename="news")


urlpatterns = [
    path('', include(router.urls)),
]
