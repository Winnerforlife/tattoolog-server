import django_filters
from django.db.models import Q
from apps.accounts.models import Profile


class ProfileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Profile
        fields = ['name']

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value))
