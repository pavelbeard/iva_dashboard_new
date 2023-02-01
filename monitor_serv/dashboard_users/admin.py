from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import forms
from . import models

# Register your models here.


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password')
        }),
        ('Разрешения и группы', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')
        })

    )

    add_fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        }),
        ('Разрешения и группы', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')
        })
    )

    filter_horizontal = ('groups', 'user_permissions')

    list_display = tuple('username display_groups email last_login is_superuser is_staff is_active'.split())
    list_filter = tuple('username email last_login is_superuser is_staff is_active '.split())
    actions = ['make_is_active']

    ordering = ('username', )
    save_on_top = True

    @admin.action(description="Пометить пользователя(-ей) как активированных.", permissions=['change'])
    def make_is_active(self, modeladmin, request, queryset):
        queryset.update(is_active=True)

    @admin.display(description="Группы")
    def display_groups(self, queryset):
        try:
            groups = [group.name for group in models.Group.objects.filter(customuser=queryset)]
            return groups
        except queryset.ObjectDoesNotExists:
            return "N/A"


admin.site.site_header = "Панель администратора платформы IVA MCU Dashboard"
admin.site.index_title = "Администрирование сайта"
admin.site.site_title = "Панель администратора"
