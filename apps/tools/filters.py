import django_filters
from cities_light.models import City


class CityLightFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['country', 'city']
