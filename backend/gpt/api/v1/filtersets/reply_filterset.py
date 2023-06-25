from django_filters import rest_framework as filters

from gpt.models import Reply


class ReplyFilterSet(filters.FilterSet):
    created = filters.DateFromToRangeFilter()

    class Meta:
        model = Reply
        fields = [
            "created",
            "status",
        ]
