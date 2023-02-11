from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.db.models import Model
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import SafeText


def admin_url_resolver(obj: Model, column: str, name: str = ""):
    col = obj.__getattribute__(column)
    url = resolve_url(admin_urlname(obj._meta, SafeText("change")), col)
    return format_html(f"<a href='{url}'>{name}{col}</a>")

