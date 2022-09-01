from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NotaryViewSet, UserViewSet


router = DefaultRouter()
router.register(r'notaries', NotaryViewSet, basename="notary")
router.register(r'profile', UserViewSet, basename="profile")

urlpatterns = [
    path('', include(router.urls)),

    # User Auth
    path('account/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('account/register/', RegisterView.as_view()),
    path('account/login/', LoginView.as_view()),
    path('account/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('account/', include('allauth.urls')),
]
