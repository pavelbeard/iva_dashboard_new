from functools import partial

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from rest_framework.response import Response

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


class EmptyQueryCheckMixin:
    model = None

    def get_queryset(self):
        query = self.model.objects.all()
        if len(query) == 0:
            return []

        return query
