from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class PageNumberPaginationExt(PageNumberPagination):

    max_page_size = 20
    max_page = 20
    page_size_query_param = 'ipp'

    def paginate_queryset(self, queryset, request, view=None):
        queryset = queryset[:self.max_page_size * self.max_page]
        return super().paginate_queryset(queryset, request, view=None)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('ipp', self.get_page_size(self.request)),
            ('page', self.page.number),
            ('total', self.page.paginator.count),
            ('objects', data)
        ]))


def get_data(request):
    if request.method == 'GET':
        data = request.GET
    else:
        try:
            data = request.data
        except AttributeError:
            data = {}
    try:
        return data.dict()
    except AttributeError:
        return data
