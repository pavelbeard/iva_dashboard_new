import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class PaginationResponseMixin(PageNumberPagination):
    def get_paginated_response(self, data):
        url = self.request.build_absolute_uri()
        page_size = self.get_page_size(self.request)
        page_number = self.page.number
        pages_count = self.page.paginator.count
        # first_page = replace_query_param(url, self.page_query_param, 1)
        first_page = 1
        left_visible_pages_range = [page for page in range(page_number, page_number - 4, -1) if page >= 1]

        # last_page_num = math.ceil(pages_count / page_size)
        last_page = math.ceil(pages_count / page_size)
        # last_page = replace_query_param(url, self.page_query_param, last_page_num)

        # right_visible_pages_range = [page for page in range(page_number, page_number + 3) if page < last_page_num - 1]
        right_visible_pages_range = [page for page in range(page_number, page_number + 3) if page < last_page - 1]

        if max(right_visible_pages_range) < 7:
            for i in range(min(right_visible_pages_range), 7):
                right_visible_pages_range.append(i)

        pages_range = []
        pages = list(set(left_visible_pages_range + right_visible_pages_range))
        pages.sort()
        for page in pages:
            # pages_range.append(replace_query_param(url, self.page_query_param, page))
            pages_range.append(page)

        return Response({
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link(),
            # },
            # 'references': {
            #     'next': self.page.number + 1,
            #     'previous': self.page.number - 1 if self.page.number - 1 < 0 else None,
            # },
            'pageSize': page_size,
            # 'firstPage': first_page,
            'lastPage': last_page,
            'pagesRange': pages_range,
            'count': pages_count,
            'results': data
        })


class LargeResultsSetPagination(PaginationResponseMixin):
    page_size = 100
    page_query_param = 'page'
    page_size_query_description = 'page_size'
    max_page_size = 200


class StandardResultsSetPagination(PaginationResponseMixin):
    page_size = 25
    page_query_param = 'page'
    page_size_query_description = 'page_size'
    max_page_size = 100

    #
    # def get_paginated_response(self, data, **kwargs):
    #     super().get_paginated_response(data, page_size=self.page_size)
