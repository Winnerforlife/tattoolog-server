from drf_spectacular.utils import extend_schema
from rest_framework import generics
from cities_light.models import City, Country
from rest_framework.permissions import AllowAny

from apps.tools.filters import CityLightFilter, CountryLightFilter
from apps.tools.models import Partners, Blog, Rating, AssociationType
from apps.tools.serializers import CityCustomSerializer, CountryCustomSerializer, PartnersSerializer, BlogSerializer, \
    RatingSerializer, AssociationTypeSerializer
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


@extend_schema(
    summary='Retrieving all partners info.',
)
class PartnersView(generics.ListAPIView):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary='Retrieving all blog objects. (Default pagination size 10 objects)',
)
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination


@extend_schema(
    summary='Retrieving detail blog object.',
)
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary='Setting a user profile rating.',
)
class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]


@extend_schema(summary='Retrieving work types.')
class AssociationTypeApiView(generics.ListAPIView):
    serializer_class = AssociationTypeSerializer
    queryset = AssociationType.objects.all()
    permission_classes = [AllowAny]
