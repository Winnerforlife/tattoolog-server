from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.accounts.views import (ProfileViewSet, ProfileApiView, CRMIntegrationProfilesAPIView,
                                 TransferActivationEmailView)

router = SimpleRouter()

router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path('profiles/<str:role>/', ProfileApiView.as_view(), name='role-profile-list'),
    path('integrationCRM/<str:date>/', CRMIntegrationProfilesAPIView.as_view(), name='integration-crm'),
    path('transfer-activation-email/', TransferActivationEmailView.as_view(), name='transfer-activation-email'),
] + router.urls
