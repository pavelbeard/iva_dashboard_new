from functools import partial

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

from core_logic.filters import BaseDatetimeFilter
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

    def get_context_data(self, target_id, **kwargs):
        context = super().get_context_data()
        context |= self.model.import_data_from_psql(target_id=target_id)
        context |= {"urls": [{"url": partial(reverse, self.reverse_style_url, kwargs={"target_id": i.id}),
                              "address": i.address}
                             for i in Target.objects.filter(is_being_scan=True).order_by('address')]}
        context |= {"address": Target.objects.filter(id=target_id).first().address}
        return context

    def get(self, request, *args, **kwargs):
        target_id = int(kwargs.get('target_id'))
        context = self.get_context_data(target_id=target_id)
        if not request.headers.get('Content-Type') == "application/json":
            return self.render_to_response(context)
        else:
            del context['view']
            del context['filters']
            del context['urls']
            return JsonResponse(context, safe=False)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class DatetimeFiltersMixin:
    """
    Adding filters to the context data
    """
    # 1 min, 15 min, 30 min, 1 hour, 6 hour, 1 day, 7 days, 1 month, 6 months, 1 year, range
    filter_keys = (
        "minutes", "minutes", "minutes",
        "hours", "hours", "days",
        "days", "months", "months",
        "years", "range"
    )
    time_values = (1, 15, 30, 1, 6, 1, 7, 1, 6, 1, 0)
    locale_keys = ("Данные за 1 минуту", "Данные за 15 минут", "Данные за 30 минут",
                   "Данные за 1 час", "Данные за 6 часов", "Данные за день",
                   "Данные за неделю", "Данные за месяц", "Данные за полгода",
                   "Данные за год", "Вручную")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context |= {"filters": zip(self.filter_keys, self.time_values, self.locale_keys)}
        return context
