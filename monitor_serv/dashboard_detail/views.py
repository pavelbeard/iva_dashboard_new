from django.shortcuts import render
from dashboard import models


# Create your views.py here.

# class CPUView()

def cpu_view(request):
    labels = [f.attname for f in models.CPU._meta.fields][2:-2]
    data = []

    queryset = models.CPU.objects.order_by("-record_date")[:50]

    for cpu_record in queryset:
        data.append(cpu_record.cpu_idle)

    return render(request, "dashboard_detail/index.html", {
        "labels": labels,
        "data": data
    })

# TODO: class LoadAverage
# TODO: class CPUUsageDetail
