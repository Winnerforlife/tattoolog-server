from django.db.models import Avg
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from cities_light.models import City, Country
from rest_framework.permissions import AllowAny

from apps.tools.filters import CityLightFilter, CountryLightFilter
from apps.tools.models import Partners, Blog, Rating
from apps.tools.serializers import CityCustomSerializer, CountryCustomSerializer, PartnersSerializer, BlogSerializer, \
    RatingSerializer, AverageRatingSerializer
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
    queryset = Blog.objects.all()
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


@extend_schema(
    summary='Obtaining the average rating for a specific user.',
)
class AverageRatingView(generics.RetrieveAPIView):
    serializer_class = AverageRatingSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        profile_id = self.kwargs.get('id')
        average_rating = self.get_average_rating(profile_id)
        return {'average_rating': average_rating}

    def get_average_rating(self, profile_id):
        average_rating = Rating.objects.filter(profile=profile_id).aggregate(Avg('mark'))['mark__avg']
        return round(average_rating, 1) if average_rating is not None else 0.0
