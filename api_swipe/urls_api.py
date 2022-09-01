from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView


urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),

    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
