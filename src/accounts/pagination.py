from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            '다음': self.get_next_link(),
            '이전': self.get_previous_link(),
            '총 개수': self.page.paginator.count,
            '결과': data
        })