import django_filters
from django.db.models import Q
from apps.accounts.models import Profile


class ProfileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['name', 'country', 'city']

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value))
