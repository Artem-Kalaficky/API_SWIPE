from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DeveloperProfileViewSet


router = DefaultRouter()
router.register(r'developer-profile', DeveloperProfileViewSet, basename="developer-profile")


urlpatterns = [
    path('', include(router.urls)),
]
