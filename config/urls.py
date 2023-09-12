from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView

from apps.accounts.views import activation_view


urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
    path("portfolio/", include("apps.portfolio.urls")),

    path("admin/", admin.site.urls),
    path("api/", include("config.spectacular.urls")),

    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path('auth/activation/<str:uid>/<str:token>/', activation_view, name='activation_view'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path('cities_light/api/', include('cities_light.contrib.restframework3')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
