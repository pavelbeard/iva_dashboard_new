import json

import requests
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control
from jsonview.views import JsonView

from . import models
from .handler import scraped_data_handler

# Create your views.py here.

app_version = settings.APP_VERSION
mail_to = settings.MAIL_TO_DEV
call_to = settings.CALL_TO_DEV


def index_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse_lazy("dashboard:dashboard"))
    else:

        storage = get_messages(request)

        if len(storage) == 0:
            messages.info(request, "Войдите в систему чтобы увидеть Инфопанель")

    return render(
        request=request,
        template_name="base/2_index.html",
        context={"app_version": app_version, "index": True, "mail_to": mail_to, "call_to": call_to}
    )


@login_required(login_url=reverse_lazy("dashboard_users:login"))
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_view(request):
    query = models.Target.objects.filter(is_being_scan=True)
    targets = [{
        "address": f"{target.address}:{target.port}",
        "id": f"{target.address.replace('.', '')}{target.port}",
    } for target in query]

    return render(
        request=request,
        template_name="base/4_dashboard.html",
        context={"targets": targets, "app_version": app_version, "mon_agent_available": True}
    )


class DataGetterFromAgent(JsonView):
    def get_context_data(self, **kwargs):
        settings_obj = models.DashboardSettings.objects.get(command_id=1)
        response = requests.get(settings_obj.scraper_url, headers={"Content-Type": "application/json"})
        json_data = scraped_data_handler(json.loads(response.content))
        return json_data

def get_interval(request):
    """Возвращает интервал снятия метрик в секундах"""
    try:
        dboard_settings = models.DashboardSettings.objects.get(command_id=1)
        interval = dboard_settings.scrape_interval
        return http.JsonResponse(json.dumps({"interval": interval}), safe=False)
    except models.DashboardSettings.DoesNotExist:
        http.JsonResponse(json.dumps({"SettingsObjectNotFound": "no data."}), safe=False)

