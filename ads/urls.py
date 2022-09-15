from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AdViewSet, PromotionViewSet, FeedListApiView, HouseCardRetrieveApiView, AdCardRetrieveApiView,
    AdComplaintCreateApiView, FavoritesAdListAPIView, FavoritesHouseListAPIView, FavoritesAddApiView,
    FavoritesDeleteApiView
)

router = DefaultRouter()
router.register(r'my-ads', AdViewSet, basename='my-ad')
router.register(r'promotions', PromotionViewSet)


urlpatterns = [
    path('ads/', include(router.urls)),

    # Feed
    path('feed/house-card/<int:pk>/', HouseCardRetrieveApiView.as_view()),
    path('feed/ad-card/complaint/', AdComplaintCreateApiView.as_view()),
    path('feed/ad-card/<int:pk>/', AdCardRetrieveApiView.as_view()),
    path('feed/', FeedListApiView.as_view()),

    # Favorites
    path('favorites/delete/', FavoritesDeleteApiView.as_view({'put': 'remove'})),
    path('favorites/add/', FavoritesAddApiView.as_view({'put': 'add'})),
    path('favorites/houses/', FavoritesHouseListAPIView.as_view()),
    path('favorites/ads/', FavoritesAdListAPIView.as_view()),
]

