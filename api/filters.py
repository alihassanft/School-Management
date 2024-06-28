from django.db.models import Q
from rest_framework.filters import BaseFilterBackend

class CustomSearchFilter(BaseFilterBackend):
    search_param = 'name'  
    def filter_queryset(self, request, queryset, view):
        search_value = request.query_params.get(self.search_param)
        if search_value:
            search_fields = getattr(view, 'search_fields', [])
            if search_fields:
                queries = [Q(**{f'{field}__icontains': search_value}) for field in search_fields]
                queryset = queryset.filter(*queries)
        return queryset
