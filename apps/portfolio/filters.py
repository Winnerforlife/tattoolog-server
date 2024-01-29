import django_filters
from apps.portfolio.models import WorkType


class WorkTypeFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='exact',
        help_text="Filter work types by category name. [tattoo, piercing]"
    )

    class Meta:
        model = WorkType
        fields = ['category',]
