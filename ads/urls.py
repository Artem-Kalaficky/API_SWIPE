from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AdViewSet, PromotionViewSet

router = DefaultRouter()
router.register(r'my-ads', AdViewSet, basename='my-ad')
router.register(r'promotions', PromotionViewSet)


urlpatterns = [
    path('ads/', include(router.urls)),
]

