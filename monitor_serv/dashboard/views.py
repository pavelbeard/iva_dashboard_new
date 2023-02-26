import json

import requests
from core_logic.views import AppVersionMixin, DevCredentialsMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, TemplateView
from jsonview.views import JsonView

from . import models
from .handler import scraped_data_handler

# Create your views.py here.

APP_VERSION = settings.APP_VERSION
MAIL_TO = settings.MAIL_TO_DEV
CALL_TO = settings.CALL_TO_DEV


class IndexView(AppVersionMixin, DevCredentialsMixin, RedirectView, TemplateView):
    template_name = "base/2_index.html"
    app_version = APP_VERSION
    mail_to = MAIL_TO
    call_to = CALL_TO
    url = reverse_lazy("dashboard:dashboard")

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


class DashboardView(AppVersionMixin, ListView):
    template_name = "base/1_dashboard.html"
    app_version = APP_VERSION

    def get_queryset(self):
        return models.Target.objects.filter(is_being_scan=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        targets = []
        for target in self.get_queryset():
            targets.append({
                "address": "{}:{}".format(target.address, target.port),
                "element_id": "{}{}".format(target.address.replace('.', ''), target.port),
                "data_target_id": target.id
            })

        context["targets"] = targets
        return context


class DataGetterFromAgent(JsonView):
    def get(self, request, *args, **kwargs):
        try:
            settings_obj = models.DashboardSettings.objects.get(command_id=1)
            response = requests.get(settings_obj.scraper_url, headers={"Content-Type": "application/json"})
            json_data = scraped_data_handler(json.loads(response.content))
            return json_data
        except requests.exceptions.ConnectionError:
            return json.dumps({"available": "false"})
        except models.DashboardSettings.DoesNotExist:
            return json.dumps({"DashboardSettingsNotFound": "no data."})


class CheckAgentHealth(JsonView):
    def get(self, request, *args, **kwargs):
        try:
            settings_obj = models.DashboardSettings.objects.get(command_id=1)
            response = requests.get(url=settings_obj.scraper_url_health_check)
            return json.dumps({"ping": "true"})
        except requests.exceptions.ConnectionError as e:
            return json.dumps({"ping": "false", "reason": "нет соединения с агентом."})
        except models.DashboardSettings.DoesNotExist:
            return json.dumps({"DashboardSettingsNotFound": "no data."})


class IntervalView(JsonView):
    """Возвращает интервал опроса в секундах"""
    def get(self, request, *args, **kwargs):
        try:
            dashboard_settings_obj = models.DashboardSettings.objects.get(command_id=1)
            interval = dashboard_settings_obj.scrape_interval
            return json.dumps({"interval": interval})

        except models.DashboardSettings.DoesNotExist:
            return json.dumps({"DashboardSettingsNotFound": "no data."})
