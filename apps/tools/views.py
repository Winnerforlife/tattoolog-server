from drf_spectacular.utils import extend_schema
from rest_framework import generics
from cities_light.models import City
from rest_framework.permissions import AllowAny

from apps.tools.filters import CityLightFilter
from apps.tools.serializers import CitySerializer


@extend_schema(
    summary='Retrieving all countries and cities.',
    description=(
        'Using optional parameters: **city**, **country**. You can filter the final result.\n'
        '* city - filters by the city name.\n'
        '* country - filters by the country name.'
    )
)
class CountryFilterView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    filterset_class = CityLightFilter
