from django import http
from django.core import paginator
from django.views import generic
from . import models


# Create your views here.


class IvcsGetAccessLogRecords(generic.ListView):
    paginate_by = 500
    paginator_class = paginator.Paginator
    model = models.AccessLogRecord

    def get(self, request, *args, **kwargs):
        query = self.model.objects.all()
        pages = self.paginator_class(query, self.paginate_by)

        page_num = request.GET.get('page', 1)

        page = [obj.request_path for obj in pages.get_page(page_num)]

        return http.JsonResponse(data={"status": "ok", "page": page}, safe=False)
