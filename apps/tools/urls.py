from django.urls import path
from apps.tools.views import CountryFilterView, CityFilterView, CRMIntegrationProfilesAPIView

urlpatterns = [
    path('cities/', CityFilterView.as_view(), name='city-list'),
    path('countries/', CountryFilterView.as_view(), name='country-list'),
    path('integrationCRM/profiles/', CRMIntegrationProfilesAPIView.as_view(), name='integration-crm-profiles'),
]
