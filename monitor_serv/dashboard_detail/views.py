import json

from django import http
from django.shortcuts import render
from dashboard import models
from monitor_serv import settings

# Create your views.py here.

app_version = settings.APP_VERSION


def cpu_view(request, target_id):
    labels = [f.attname for f in models.CPU._meta.fields][2:-2]
    cpu_idle_data = []
    cpu_iowait_data = []
    cpu_irq_data = []
    cpu_nice_data = []
    cpu_softirq_data = []
    cpu_steal_data = []
    cpu_sys_data = []
    cpu_user_data = []
    record_dates = []

    queryset = models.CPU.objects.filter(target_id=target_id).order_by("-record_date")[:50]

    for cpu_record in queryset:
        cpu_idle_data.append(cpu_record.cpu_idle)
        cpu_iowait_data.append(cpu_record.cpu_iowait)
        cpu_irq_data.append(cpu_record.cpu_irq)
        cpu_nice_data.append(cpu_record.cpu_nice)
        cpu_softirq_data.append(cpu_record.cpu_softirq)
        cpu_steal_data.append(cpu_record.cpu_steal)
        cpu_sys_data.append(cpu_record.cpu_sys)
        cpu_user_data.append(cpu_record.cpu_user)
        record_dates.append(cpu_record.record_date.__format__("%d/%m/%y %H:%M:%S"))

    context = {
        "labels": labels,
        "cpu_idle_data": cpu_idle_data,
        "cpu_iowait_data": cpu_iowait_data,
        "cpu_irq_data": cpu_irq_data,
        "cpu_nice_data": cpu_nice_data,
        "cpu_softirq_data": cpu_softirq_data,
        "cpu_steal_data": cpu_steal_data,
        "cpu_sys_data": cpu_sys_data,
        "cpu_user_data": cpu_user_data,
        "record_dates": record_dates,
        "target_id": target_id
    }

    if not request.headers.get('Content-Type') == "application/json":
        context |= {"app_version": app_version}
        return render(request, "dashboard_detail/1_cpu.html", context)
    else:
        return http.JsonResponse(context, safe=False)

# TODO: class LoadAverage
# TODO: class CPUUsageDetail
