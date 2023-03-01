from django.contrib import messages
from django.http import JsonResponse

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

    def get_context_data(self, target_id, **kwargs):
        context = super().get_context_data()
        context |= self.model.import_data_from_psql(target_id=target_id)
        return context

    def get(self, request, *args, **kwargs):
        target_id = int(kwargs.get('target_id'))
        context = self.get_context_data(target_id=target_id)
        del context['view']
        if not request.headers.get('Content-Type') == "application/json":
            return self.render_to_response(context)
        else:
            return JsonResponse(context, safe=False)
