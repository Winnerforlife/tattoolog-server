import django_filters
from django.utils.translation import gettext_lazy as _
from cities_light.models import City, Country
from apps.tools.models import BlogPost, BlogCategory, Festival


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
    language = django_filters.CharFilter(
        field_name='language',
        lookup_expr='iexact',
        help_text="Filter posts by language."
    )
    country = django_filters.CharFilter(
        field_name='country',
        lookup_expr='iexact',
        help_text="Filter posts by country."
    )
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__name',
        to_field_name='name',
        queryset=BlogCategory.objects.all(),
        help_text="Filter posts by blog category name."
    )

    class Meta:
        model = BlogPost
        fields = ['language', 'country', 'category']


class FestivalFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='iexact',
        help_text="Filter festival objects by festival category name."
    )
    country = django_filters.CharFilter(
        field_name='country',
        lookup_expr='iexact',
        help_text="Filter festival objects by country."
    )

    class Meta:
        model = Festival
        fields = ['category', 'country']
