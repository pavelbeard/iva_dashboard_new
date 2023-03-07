from functools import partial

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

from core_logic.chart import Chart
from core_logic.filters import FilterByMinutes, filters_dict
from dashboard.models import Target
from monitor_serv import settings


class AppVersionMixin:
    def get_context_data(self, **kwargs):
        context = super(AppVersionMixin, self).get_context_data(**kwargs)
        context["app_version"] = settings.APP_VERSION
        return context


class DevCredentialsMixin:
    mail_to = None
    call_to = None

    def get_context_data(self, **kwargs):
        context = super(DevCredentialsMixin, self).get_context_data(**kwargs)
        context["mail_to"] = self.mail_to
        context["call_to"] = self.call_to
        return context


class ErrorMessageMixin:
    """
    Add an error message on successful form submission.
    """

    error_message = ""

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return self.render_to_response(self.get_context_data(form=form))

    def get_error_message(self, cleaned_data):
        return self.error_message % cleaned_data


class ContextDataFromImporterMixin:
    """
    Adding the mixin as handler of context data, which is an importer data from database.
    """
    model = None
    reverse_style_url = None
    chart_class = None
    keys = None
    filter = None
    time_value = None

    default_filter = filters_dict.get_filter("from1hour")

    def get_context_data(self, target_id, *args, **kwargs):
        context = super().get_context_data()
        chart = self.chart_class(self.model)

        data = []

        filter_ = self.default_filter if self.filter is None else self.filter

        for nested_keys in self.keys:
            data.append(chart.create_chart_data(
                nested_keys,
                target_id,
                filter_, *args, **kwargs
            ))

        context['chartData'] = data
        context['target_id'] = target_id

        urls = []

        for obj in Target.objects.filter(is_being_scan=True).order_by('address'):
            urls.append({
                'url': reverse(self.reverse_style_url, kwargs={'target_id': obj.id}),
                'address': obj.address
            })

        context['urls'] = urls
        context['address'] = Target.objects.filter(id=target_id).first().address

        return context

    def get(self, request, *args, **kwargs):
        target_id = int(kwargs.get('target_id'))
        context = self.get_context_data(target_id=target_id)

        if not request.headers.get('Content-Type') == "application/json":
            return self.render_to_response(context)
        else:
            for key in ['view', 'filters', 'urls']:
                context.pop(key)
            return JsonResponse(context, safe=False)


class DatetimeFiltersMixin:
    """
    Adding filters to the context data
    """
    # 1 hour, 3 hour, 6 hour, 12 hour, 1 days, 1 week, 6 months, 1 year, range
    filter_keys = (
        "hours", "hours", "days",
        "days", "months", "months",
        "range"
    )
    time_values = (1, 3, 1, 6, 1, 7, 1, 6, 1, 0)
    locale_keys = ("Данные за 1 час", "Данные за 3 часа", "Данные за 6 часов",
                   "Данные за 12 часов", "Данные за день", "Данные за неделю",
                   "Данные за месяц", "Вручную")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['filters'] = zip(self.filter_keys, self.time_values, self.locale_keys)
        return context
