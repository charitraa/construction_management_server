from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data, message):
        return Response({
            "data": data,
            "pagination": {
                "total": self.page.paginator.count,       # total items
                "page": self.page.number,                 # current page
                "page_size": self.get_page_size(self.request),
                "total_pages": self.page.paginator.num_pages,
                "has_next": self.get_next_link() is not None,
                "has_previous": self.get_previous_link() is not None,
            },
            "message": message
        })