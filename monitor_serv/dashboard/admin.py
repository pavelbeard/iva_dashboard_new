from django.conf import settings
from django.contrib import admin

from common.pass_handler import encrypt_pass
from dashboard.forms import TargetForm
from dashboard.models import Target, DashboardSettings, BackendVersion


# Register your models here.


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    form = TargetForm
    list_display = tuple('id address port'.split())

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data['password']
        if not password:
            instance_id = form.instance.id
            password = self.model.objects.get().password
            obj.password = password
        else:
            password = encrypt_pass(password=password, encryption_key=settings.ENCRYPTION_KEY)
            obj.password = password

        obj.save()


@admin.register(DashboardSettings)
class BackendSettingsAdmin(admin.ModelAdmin):
    list_display = tuple('id address_for_check_ssl port'.split())


@admin.register(BackendVersion)
class BackendVersionAdmin(admin.ModelAdmin):
    pass
