import django_filters
from django.db.models import Q
from apps.accounts.models import Profile


class ProfileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains')
    open_to_work = django_filters.BooleanFilter(field_name='open_to_work')
    mentor = django_filters.BooleanFilter(field_name='mentor')
    relocate = django_filters.BooleanFilter(field_name='relocate')
    trusted_mentor = django_filters.BooleanFilter(field_name='trusted_mentor')
    posted_in_journal = django_filters.BooleanFilter(field_name='posted_in_journal')
    work_type = django_filters.CharFilter(method='filter_work_type')
    rating_order = django_filters.CharFilter(method='filter_rating_order', label='Rating Order')
    moderation_associate_type = django_filters.CharFilter(method='filter_moderation_associate_type')
    moderation_project_type = django_filters.CharFilter(method='filter_moderation_project_type')

    class Meta:
        model = Profile
        fields = [
            'name',
            'country',
            'city',
            'open_to_work',
            'mentor',
            'relocate',
            'work_type',
            'trusted_mentor',
            'posted_in_journal'
        ]

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value))

    def filter_work_type(self, queryset, name, value):
        return queryset.filter(post_profile__work_type__name=value).distinct()

    def filter_rating_order(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by('avg_rating', 'rating_count')
        elif value == 'desc':
            return queryset.order_by('-avg_rating', '-rating_count')
        return queryset

    def filter_moderation_associate_type(self, queryset, name, value):
        return queryset.filter(
            moderation_profile_associate__type__name=value
        ).distinct()

    def filter_moderation_project_type(self, queryset, name, value):
        return queryset.filter(
            moderation_profile_from_project__type__name=value
        ).distinct()
