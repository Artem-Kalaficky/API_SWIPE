from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NotaryViewSet


router = DefaultRouter()
router.register(r'notaries', NotaryViewSet, basename="notary")

urlpatterns = [
    path('', include(router.urls)),
]
