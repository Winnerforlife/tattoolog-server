from drf_spectacular.utils import extend_schema
from rest_framework import generics
from cities_light.models import City, Country
from rest_framework.permissions import AllowAny

from apps.tools.filters import CityLightFilter, CountryLightFilter
from apps.tools.serializers import CityCustomSerializer, CountryCustomSerializer
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
    serializer_class = CountryCustomSerializer
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
    serializer_class = CityCustomSerializer
    permission_classes = [AllowAny]
    filterset_class = CityLightFilter
    pagination_class = CustomPagination
