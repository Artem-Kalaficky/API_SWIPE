from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers


urlpatterns = [
    path('', include('users.urls')),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('account/', include('allauth.urls')),

    # registration with verification email
    path('dj-rest-auth/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),

    # drf spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # django admin
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path("", include(router.urls)),
#     path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
#     path('account/', include('allauth.urls')),
#
#     # login
#     path('dj-rest-auth/', include('dj_rest_auth.urls')),
#
#     # registration with verification email
#     path('dj-rest-auth/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
#     path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
#     path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
#
#     # drf spectacular
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#
#     # django admin
#     path('admin/', admin.site.urls),
# ]