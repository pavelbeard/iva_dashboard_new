from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, TemplateView

from common.mixins import AppVersionMixin, DevCredentialsMixin
from . import models

# Create your views here.

MAIL_TO = settings.MAIL_TO_DEV
CALL_TO = settings.CALL_TO_DEV


class IndexView(AppVersionMixin, DevCredentialsMixin, RedirectView, TemplateView):
    template_name = "base/2_index.html"
    mail_to = MAIL_TO
    call_to = CALL_TO
    url = reverse_lazy("dashboard:targets")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["index"] = True
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=self.url)
        else:
            storage = get_messages(request)

            if len(storage) == 0:
                messages.info(request, "Войдите в систему чтобы увидеть Инфопанель")

            return self.render_to_response(self.get_context_data())


class DashboardView(AppVersionMixin, TemplateView):
    template_name = "1_dashboard.html"


class TargetDetail(TemplateView):
    pass
