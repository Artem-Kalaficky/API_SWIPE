from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NotaryViewSet, UserViewSet, ModerationUserListApiView, MessageViewSet, FilterViewSet

router = DefaultRouter()
router.register(r'notaries', NotaryViewSet, basename="notary")
router.register(r'profile', UserViewSet, basename="profile")
router.register(r'messages', MessageViewSet, basename="message")
router.register(r'my-filters', FilterViewSet, basename="my-filter")


urlpatterns = [
    path('', include(router.urls)),

    # moderation
    path('moderation/list-of-users/', ModerationUserListApiView.as_view()),

    # User Auth
    path('account/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('account/register/', RegisterView.as_view()),
    path('account/login/', LoginView.as_view()),
    path('account/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('account/', include('allauth.urls')),
]
