from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('', include('users.urls')),
    path('api/', include('api_swipe.urls_api')),

    # drf spectacular
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # django admin
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path('api/', include('api_swipe.urls_api')),
#     path('', include('users.urls')),
#
#     # drf spectacular
#     path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('docs/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#
#     # django admin
#     path('admin/', admin.site.urls),
# ]
