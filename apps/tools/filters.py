import django_filters
from cities_light.models import City, Country

from apps.tools.models import BlogPost


class CountryLightFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Country
        fields = ['country']


class CityLightFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['country', 'city']


class BlogPostsFilter(django_filters.FilterSet):
    language = django_filters.CharFilter(field_name='language', lookup_expr='iexact')
    country = django_filters.CharFilter(field_name='country', lookup_expr='iexact')

    class Meta:
        model = BlogPost
        fields = ['language', 'country']
