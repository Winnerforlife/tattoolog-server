from drf_spectacular.utils import extend_schema
from rest_framework import generics
from cities_light.models import City, Country
from rest_framework.permissions import AllowAny

from apps.accounts.models import Profile
from apps.tools.filters import CityLightFilter, CountryLightFilter
from apps.tools.serializers import CitySerializer, CountrySerializer, CRMIntegrationProfiles
from apps.tools.utils import CustomPagination


@extend_schema(
    summary='Retrieving all countries.',
    description=(
        'Using optional parameters: **country**. You can filter the final result.\n'
        '* country - filters by the country name.'
    )
)
class CountryFilterView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    filterset_class = CountryLightFilter
    pagination_class = CustomPagination


@extend_schema(
    summary='Retrieving all countries and cities.',
    description=(
        'Using optional parameters: **city**, **country**. You can filter the final result.\n'
        '* city - filters by the city name.\n'
        '* country - filters by the country name.'
    )
)
class CityFilterView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    filterset_class = CityLightFilter
    pagination_class = CustomPagination


@extend_schema(
    summary='Retrieving profiles for copy to CRM by date.',
    description=(
        'Using parameters: **date**. You can filter the final result\n'
        'and resieve objects from input date to actually date.'
    )
)
class CRMIntegrationProfilesAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = CRMIntegrationProfiles
    permission_classes = [AllowAny]
