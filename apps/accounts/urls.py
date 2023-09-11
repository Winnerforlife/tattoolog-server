from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.accounts.views import ProfileViewSet, ProfileApiView

router = SimpleRouter()

router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
    path('profiles/<str:role>/', ProfileApiView.as_view(), name='role-profile-list'),
] + router.urls
